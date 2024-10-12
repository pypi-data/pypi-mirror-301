import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)
class ExplainableFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_file_planning(self, idea, file_attachments, focused_files):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.

        Returns:
            dict: JSON response with the plan or an empty array if no files are found.
        """

        all_attachment_file_contents = ""

        file_attachments_path = file_attachments

        if file_attachments_path:
            for file_path in file_attachments_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {file_path}:\n{file_content}"

        all_focused_files_contents = ""

        all_focused_path = focused_files

        if all_focused_path:
            for file_path in all_focused_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {file_path}:\n{file_content}"

        all_file_contents = self.repo.print_tree()
        directory_path = self.repo.get_repo_path()
        prompt = (
            f"Analyze the user prompt and project structure to identify the most relevant files for providing context to answer the user's request. "
            f"Build a JSON response listing these files. Include only files that are directly related to the user's query or essential for understanding the context. "
            f"Provide only a JSON response without any additional text or Markdown formatting. "
            f"Current working project is {directory_path}. "
            f"Use this JSON format:"
            "{\n"
            f"    \"working_files\": [\"{directory_path}/path/to/most_relevant_file1.ext\", \"{directory_path}/path/to/most_relevant_file2.ext\"]\n"
            "}\n\n"
            "Ensure the 'working_files' list contains only the most pertinent files, prioritizing those that directly address the user's request. "
            "It is crucial that each file path in the 'working_files' list is an absolute path, starting from the root directory. "
            f"Always prepend '{directory_path}' to each file path to ensure it's a full, absolute path. "
            "If no relevant files are found, return an empty array for 'working_files' like this: "
            "{\n"
            f"    \"working_files\": []\n"
            "}\n"
            "Return only valid JSON without Markdown symbols or invalid escapes. "
            "Exclude third-party libraries and generated folders. "
            "Carefully examine the provided project structure. Only include files that actually exist in the tree. "
            "Do not hallucinate or assume the existence of files not present in the given structure. "
            "IMPORTANT: Never include long, unnecessary files such as package-lock.json, yarn.lock, Podfile.lock, Gemfile.lock, poetry.lock, composer.lock, cargo.lock, or any other third-party dependency files. "
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is user request to do:\n{idea}\nThis is the current project context:\n{all_file_contents}"
            }
        ]

        if all_attachment_file_contents:
            messages[-1]["content"] += f"\nUser has attached these files for you, from user request and this file, find something the most relevant files from provided tree to answer their question: {all_attachment_file_contents}"

        if all_focused_files_contents:
            messages[-1]["content"] += f"\nUser has focused on these files inside the current project. No need to re-mention these files since we already have them: {all_focused_files_contents}"

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            return {
                "reason": str(e)
            }

    async def get_file_plannings(self, idea, file_attachments, focused_files):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            files (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the plan.
        """
        logger.info(f"\n #### The `File Manager Agent` is looking for any relevant context.")
        logger.info("-------------------------------------------------")
        plan = await self.get_file_planning(idea,file_attachments, focused_files)
        logger.debug(f" #### `File Manager Agent`: Successfully completed the search for relevant files")
        return plan
