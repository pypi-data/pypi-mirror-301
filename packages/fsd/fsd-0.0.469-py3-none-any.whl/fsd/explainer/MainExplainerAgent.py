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

class MainExplainerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def initial_setup(self):
        """Initialize the setup with the provided instructions and context."""

        logger.debug("\n #### The `MainExplainerAgent` is initializing setup with provided instructions and context")

        prompt = f"""Your name is Zinley.

        Instructions:
        1. Respond directly to support the user's request based on the given context.
        2. If no context is provided, inform the user that no relevant files were found.
        3. Provide a brief, concise guide on how to proceed or find relevant information.
        4. Keep the response comprehensive and detailed, while being easy to understand.
        5. Format your response for clarity and readability:
           - Use appropriate spacing
           - Ensure text is not crowded
           - Avoid weird symbols, unnecessary text, or distracting patterns
           - Use clear headings (no larger than h4) to organize information
        6. Keep the response focused and to the point, avoiding unnecessary elaboration.
        7. Respond in the language specified in the request.
        8. Only mention using a model configured by the Zinley team if explicitly asked about the AI model.
        9. For any bash commands, use the following format:
           ```bash
           command here
           ```
        10. When displaying a project tree structure, only if explicitly asked or directly relevant, use this markdown format:
        ```plaintext
        project/
        ├── src/
        │   ├── main.py
        │   └── utils.py
        ├── tests/
        │   └── test_main.py
        └── README.md
        ```
        11. Do not provide irrelevant information or hallucinate.
        12. For every answer related to this project, provide citations and detailed references.
        13. If relevant, offer in-depth explanations to help the user understand complex concepts.
        14. When referencing specific parts of the code or documentation, use the following format:
            [File: path/to/file.py, Line: X]
        15. If explaining a concept, provide examples from the project files when possible.
        16. When suggesting solutions or improvements, always relate them back to the project structure and existing code.
        """

        self.conversation_history = [
            {"role": "system", "content": prompt}
        ]

    def read_all_file_content(self, all_path):
        all_context = ""

        for path in all_path:
            file_context = read_file_content(path)
            all_context += f"\n\nFile: {path}\n{file_context}"

        return all_context

    async def get_answer_plan(self, user_prompt, language, all_file_content, role, file_attachments, focused_files, crawl_logs):
        prompt = ""
        all_attachment_file_contents = ""
        all_focused_files_contents = ""

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

        if all_focused_files_contents:
            prompt += f"\nUser has focused on these files in the current project, pay special attention to them according to user prompt: {all_focused_files_contents}"

        prompt += (
            f"Context:\n{all_file_content}\n"
            f"User prompt:\n{user_prompt}\n"
            f"Project tree, only use if need: {self.repo.print_tree()}\n"
            f"Respond in this language:\n{language}"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            logger.info(f"\n #### The `{role}` is in charge.\n")
            res = await self.ai.explainer_stream_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            self.conversation_history.append({"role": "assistant", "content": res})
            return res
        except Exception as e:
            logger.error(f" #### The `{role}` encountered some errors\n")
            return {
                "reason": str(e)
            }

    async def get_answer_plans(self, user_prompt, language, files, role, file_attachments, focused_files, crawl_logs):
        files = [file for file in files if file]

        all_path = files
        logger.debug("\n #### `File Aggregator Agent`: Commencing file content aggregation for analysis")
        all_file_content = self.read_all_file_content(all_path)

        logger.debug("\n #### `Answer Plan Generator`: Initiating answer plan generation based on user input")
        plan = await self.get_answer_plan(user_prompt, language, all_file_content, role, file_attachments, focused_files, crawl_logs)
        return plan
