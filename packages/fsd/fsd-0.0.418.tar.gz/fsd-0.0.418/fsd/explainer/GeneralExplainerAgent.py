import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class GeneralExplainerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_normal_answer_plan(self, user_prompt, language, role, file_attachments, focused_files):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.
            language (str): The language in which the response should be given.

        Returns:
            dict: The development plan or error reason.
        """
        logger.debug("\n #### The `GeneralExplainerAgent` is preparing to generate a response plan")

        all_attachment_file_contents = ""

        file_attachments_path = file_attachments

        if file_attachments_path:
            for file_path in file_attachments_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        all_focused_files_contents = ""

        all_focused_path = focused_files

        if all_focused_path:
            for file_path in all_focused_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        messages = [
            {
                "role": "system",
                "content": (
                    "Your name is Zinley.\n\n"
                    "You need to reply to the user prompt and respond in the provided request language.\n\n"
                    "Do not hallucinate what you don't know, your response must be based on truth, comprehensive and detailed, in the easiest way to help people understand.\n\n"
                    "Only if asked about the AI model you are using, mention that you are using a model configured by the Zinley team. If they don't ask, don't say anything.\n\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"#### User prompt:\n"
                    f"User prompt: {user_prompt}\n\n"
                )
            }
        ]

        if all_attachment_file_contents:
            messages[1]["content"] += (
                f"#### Attached Files:\n"
                f"The user has provided the following file attachments. Please use this information to inform your response:\n"
                f"{all_attachment_file_contents}\n\n"
            )

        if all_focused_files_contents:
            messages[1]["content"] += (
                f"#### Focused Files:\n"
                f"The user is currently focusing on the following files from the project. Pay special attention to them according to user prompt:\n"
                f"{all_focused_files_contents}\n\n"
            )

        messages[1]["content"] += (
            f"#### Response Guidelines:\n"
            f"1. Formatting:\n"
            f"   - Return a nicely formatted response\n"
            f"   - Use clear headings (no larger than h4)\n"
            f"   - For bash commands, use markdown code blocks with 'bash' syntax highlighting\n\n"
            f"2. Readability:\n"
            f"   - Space wisely\n"
            f"   - Ensure the text is clear and easy to read\n"
            f"   - Avoid crowding content together\n\n"
            f"3. Clarity:\n"
            f"   - No weird symbols or unnecessary text\n"
            f"   - Avoid distractions or patterns\n\n"
            f"4. AI Model Information:\n"
            f"   - If asked, state that you use a model configured by the Zinley team\n\n"
            f"5. Bash Commands:\n"
            f"   - Format all bash commands using the following structure:\n"
            f"     ```bash\n"
            f"     command here\n"
            f"     ```\n\n"
            f"6. Project Tree Structure:\n"
            f"   - When displaying a project tree structure, use this markdown format:\n"
            f"     ```plaintext\n"
            f"     project/\n"
            f"     ├── src/\n"
            f"     │   ├── main.py\n"
            f"     │   └── utils.py\n"
            f"     ├── tests/\n"
            f"     │   └── test_main.py\n"
            f"     └── README.md\n"
            f"     ```\n\n"
            f"Respond directly to support the user's request. Do not provide irrelevant information or hallucinate. Only provide the project tree structure if explicitly asked or if it's directly relevant to the user's question.\n"
            f"Only answer what the user is asking for. Do not engage in unnecessary talk or provide any additional information.\n\n"
            f"#### Response Language:\n"
            f"{language}\n\n"
        )

        try:
            logger.info(f"\n #### The `{role}` is in charge.\n")
            await self.ai.stream_prompt(messages, self.max_tokens, 0.2, 0.1)
            logger.debug("\n #### The `GeneralExplainerAgent` has successfully received AI response")
            return ""
        except Exception as e:
            logger.error(f" #### The `GeneralExplainerAgent` encountered an error during response generation: `{str(e)}`")
            return {
                "reason": str(e)
            }


    async def get_normal_answer_plans(self, user_prompt, language, role, file_attachments, focused_files):
        logger.debug("\n #### The `GeneralExplainerAgent` is commencing the process of obtaining normal answer plans")
        plan = await self.get_normal_answer_plan(user_prompt, language, role, file_attachments, focused_files)
        logger.debug("\n #### The `GeneralExplainerAgent` has successfully retrieved the normal answer plan")
        return plan
