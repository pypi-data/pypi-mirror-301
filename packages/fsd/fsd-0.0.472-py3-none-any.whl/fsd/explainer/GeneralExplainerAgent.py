import os
import aiohttp
import asyncio
import json
import sys
import base64
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class GeneralExplainerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def initial_setup(self):
        """Initialize the setup with the provided instructions and context."""

        logger.debug("\n #### The `GeneralExplainerAgent` is initializing setup with provided instructions and context")

        prompt = f"""Your name is Zinley.

        You need to reply to the user prompt and respond in the provided request language.

        Do not hallucinate what you don't know, your response must be based on truth, comprehensive and detailed, in the easiest way to help people understand.

        Only if asked about the AI model you are using, mention that you are using a model configured by the Zinley team. If they don't ask, don't say anything.

        #### Response Guidelines:
        1. Formatting:
           - Return a nicely formatted response
           - Use clear headings (no larger than h4)
           - For bash commands, use markdown code blocks with 'bash' syntax highlighting

        2. Readability:
           - Space wisely
           - Ensure the text is clear and easy to read
           - Avoid crowding content together

        3. Clarity:
           - No weird symbols or unnecessary text
           - Avoid distractions or patterns

        4. AI Model Information:
           - If asked, state that you use a model configured by the Zinley team

        5. Bash Commands:
           - Format all bash commands using the following structure:
             ```bash
             command here
             ```

        6. Project Tree Structure:
           - When displaying a project tree structure, use this markdown format:
             ```plaintext
             project/
             ├── src/
             │   ├── main.py
             │   └── utils.py
             ├── tests/
             │   └── test_main.py
             └── README.md
             ```

        Respond directly to support the user's request. Do not provide irrelevant information or hallucinate. Only provide the project tree structure if explicitly asked or if it's directly relevant to the user's question.
        Only answer what the user is asking for. Do not engage in unnecessary talk or provide any additional information.
        """

        self.conversation_history = [
            {"role": "system", "content": prompt}
        ]

    async def get_normal_answer_plan(self, user_prompt, language, role, file_attachments, focused_files, crawl_logs):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.
            language (str): The language in which the response should be given.
            role (str): The role of the AI assistant.
            file_attachments (list): List of attached file paths.
            focused_files (list): List of focused file paths.
            crawl_logs (list): List of crawl logs.

        Returns:
            dict: The development plan or error reason.
        """
        logger.debug("\n #### The `GeneralExplainerAgent` is preparing to generate a response plan")

        prompt = ""
        all_attachment_file_contents = ""
        all_focused_files_contents = ""

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if focused_files:
            for file_path in focused_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if crawl_logs:
            prompt += f"\nThis is supported data for this entire process, use it if appropriate: {crawl_logs}"

        if all_attachment_file_contents:
            prompt += f"\nUser has attached these files for you, use them appropriately: {all_attachment_file_contents}"

        for file_name, base64_image in image_files.items():
            prompt += f"\n\nAttached image: {file_name}\n{base64_image}"

        if all_focused_files_contents:
            prompt += f"\nUser has focused on these files in the current project, pay special attention to them according to user prompt: {all_focused_files_contents}"

        prompt += (
            f"User prompt:\n{user_prompt}\n"
            f"Respond in this language:\n{language}"
        )


        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            logger.info(f"\n #### The `{role}` is in charge.\n")
            res = await self.ai.explainer_stream_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            self.conversation_history.append({"role": "assistant", "content": res})
            
            # Keep conversation history no longer than 30 pairs, excluding the system prompt
            if len(self.conversation_history) > 61:  # 1 system + 30 user/assistant pairs
                self.conversation_history = self.conversation_history[:1] + self.conversation_history[-60:]
            
            return res
        except Exception as e:
            logger.error(f" #### The `{role}` encountered some errors\n")
            # Remove the last user prompt from history in case of error
            if len(self.conversation_history) > 1 and self.conversation_history[-1]["role"] == "user":
                self.conversation_history.pop()
            return {
                "reason": str(e)
            }

    async def get_normal_answer_plans(self, user_prompt, language, role, file_attachments, focused_files, crawl_logs):
        logger.debug("\n #### The `GeneralExplainerAgent` is commencing the process of obtaining normal answer plans")
        plan = await self.get_normal_answer_plan(user_prompt, language, role, file_attachments, focused_files, crawl_logs)
        logger.debug("\n #### The `GeneralExplainerAgent` has successfully retrieved the normal answer plan")
        return plan
