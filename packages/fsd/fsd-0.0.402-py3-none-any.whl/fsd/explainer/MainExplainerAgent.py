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
        self.ai = AIGateway()

    def read_all_file_content(self, all_path):
        all_context = ""

        for path in all_path:
            file_context = read_file_content(path)
            all_context += f"\n\nFile: {path}\n{file_context}"

        return all_context

    async def get_answer_plan(self, user_prompt, language, all_file_content, role, file_attachments, focused_files):
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

        messages = [
            {
                "role": "system",
                "content": (
                    "Your name is Zinley.\n\n"
                     f"Project tree, only use if need: {self.repo.print_tree()}\n"
                    "Instructions:\n"
                    "1. Respond directly to support the user's request based on the given context.\n"
                    "2. If no context is provided, inform the user that no relevant files were found.\n"
                    "3. Provide a brief, concise guide on how to proceed or find relevant information.\n"
                    "4. Keep the response comprehensive and detailed, while being easy to understand.\n"
                    "5. Format your response for clarity and readability:\n"
                    "   - Use appropriate spacing\n"
                    "   - Ensure text is not crowded\n"
                    "   - Avoid weird symbols, unnecessary text, or distracting patterns\n"
                    "   - Use clear headings (no larger than h4) to organize information\n"
                    "6. Keep the response focused and to the point, avoiding unnecessary elaboration.\n"
                    "7. Respond in the language specified in the request.\n"
                    "8. Only mention using a model configured by the Zinley team if explicitly asked about the AI model.\n"
                    "9. For any bash commands, use the following format:\n"
                    "   ```bash\n"
                    "   command here\n"
                    "   ```\n"
                    "10. When displaying a project tree structure, only if explicitly asked or directly relevant, use this markdown format:\n"
                    "```plaintext\n"
                    "project/\n"
                    "├── src/\n"
                    "│   ├── main.py\n"
                    "│   └── utils.py\n"
                    "├── tests/\n"
                    "│   └── test_main.py\n"
                    "└── README.md\n"
                    "```\n"
                    "11. Do not provide irrelevant information or hallucinate.\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{all_file_content}\n"
                    f"User prompt:\n{user_prompt}\n"
                )
            }
        ]

        if all_attachment_file_contents:
            messages[1]["content"] += f"\nUser has attached these files for you, use them appropriately: {all_attachment_file_contents}\n"

        if all_focused_files_contents:
            messages[1]["content"] += f"\nUser has focused on these files in the current project, pay special attention to them according to user prompt: {all_focused_files_contents}\n"

        messages[1]["content"] += f"\nRespond in this language:\n{language}\n"

        try:
            logger.info(f"\n #### The `{role}` is in charge.\n")
            await self.ai.stream_prompt(messages, self.max_tokens, 0.2, 0.1)
            return ""
        except Exception as e:
            logger.error(f" #### The `{role}` encountered some errors\n")
            return {
                "reason": str(e)
            }

    async def get_answer_plans(self, user_prompt, language, files, role, file_attachments, focused_files):
        files = [file for file in files if file]

        all_path = files
        logger.debug("\n #### `File Aggregator Agent`: Commencing file content aggregation for analysis")
        all_file_content = self.read_all_file_content(all_path)

        logger.debug("\n #### `Answer Plan Generator`: Initiating answer plan generation based on user input")
        plan = await self.get_answer_plan(user_prompt, language, all_file_content, role, file_attachments, focused_files)
        return plan
