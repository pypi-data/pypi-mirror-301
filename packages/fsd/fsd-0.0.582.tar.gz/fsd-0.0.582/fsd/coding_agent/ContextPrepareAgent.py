import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ContextPrepareAgent:
    def __init__(self, repo):
        """
        Initialize the ContextPrepareAgent with the repository.

        Args:
            repo: The repository object containing project information.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_file_planning(self, idea):
        """
        Request file planning from AI for a given idea and project structure.

        Args:
            idea (str): The user's task or development plan.

        Returns:
            dict: JSON response with the plan including working files and context files.
        """
        logger.debug("\n #### Context prepare agent is initiating file planning process")
        prompt = (
            "Based on the provided development plan and project structure, create a JSON response with two lists: 'working_files' and 'context_files'. "
            "Provide only a JSON response without any additional text or Markdown formatting. "
            "'working_files' must include the full path for only existing files that needs to work on to complete the user's task. "
            "'context_files' must include the full path for existing files that provide most relevant supporting information for the task, but won't be modified. "
            "Carefully examine the provided project structure. Only include files that actually exist in the given project structure. "
            "Do not ignore any project folder names, as this may lead to incomplete paths. "
            "Do not include any files if you're unsure of their relevance. "
            "Exclude all third-party libraries, generated folders, and dependency files like package-lock.json, yarn.lock, etc. "
            "Also exclude all asset files such as .png, .mp4, .jpg, .jpeg, .gif, .bmp, .tiff, .wav, .mp3, .ogg that require a vision model to read. "
            "Do not invent or hallucinate files that are not present in the given structure. "
            "The 'working_files' and 'context_files' lists must not overlap - a file can only be in one list, not both. "
            "If no files are found for either category, return an empty list for that category. "
            "Use this JSON format:"
            "{\n"
            "    \"working_files\": [\"/full/path/to/file1.extension\", \"/full/path/to/file2.extension\"],\n"
            "    \"context_files\": [\"/full/path/to/context1.extension\", \"/full/path/to/context2.extension\"]\n"
            "}\n\n"
            "If both lists are empty, return:"
            "{\n"
            "    \"working_files\": [],\n"
            "    \"context_files\": []\n"
            "}\n\n"
            "If only working_files is empty:"
            "{\n"
            "    \"working_files\": [],\n"
            "    \"context_files\": [\"/full/path/to/context1.extension\", \"/full/path/to/context2.extension\"]\n"
            "}\n\n"
            "If only context_files is empty:"
            "{\n"
            "    \"working_files\": [\"/full/path/to/file1.extension\", \"/full/path/to/file2.extension\"],\n"
            "    \"context_files\": []\n"
            "}\n\n"
            f"current project path is \"{self.repo.get_repo_path()}\"\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is the user's request to do:\n{idea}\nThis is the current project structure:\n{self.repo.print_tree()}\n"
            }
        ]

        try:
            logger.debug("\n #### Context prepare agent is sending request to AI for file planning")
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            logger.debug("\n #### Context prepare agent has received response from AI")
            plan_json = json.loads(response.choices[0].message.content)
            
            # Ensure both lists exist and contain only unique elements
            plan_json["working_files"] = list(set(plan_json.get("working_files", [])))
            plan_json["context_files"] = list(set(plan_json.get("context_files", [])))
            
            # Remove any overlapping files from context_files
            plan_json["context_files"] = [f for f in plan_json["context_files"] if f not in plan_json["working_files"]]
            
            return plan_json
        except json.JSONDecodeError:
            logger.debug("\n #### Context prepare agent encountered JSON decode error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f" #### Context prepare agent encountered an error: `{e}`")
            return {
                "working_files": [],
                "context_files": [],
                "reason": str(e)
            }

    async def get_file_plannings(self, idea):
        logger.debug("\n #### Context prepare agent is starting file planning process")
        return await self.get_file_planning(idea)
