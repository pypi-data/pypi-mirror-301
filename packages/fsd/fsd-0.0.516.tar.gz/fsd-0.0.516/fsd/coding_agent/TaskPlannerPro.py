import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskPlannerPro:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, file_list, original_prompt_language):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.
            file_list (list): List of available files.
            original_prompt_language (str): The language of the original prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is initiating the process to generate a task plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal engineer specializing in Pyramid architecture. Generate a strictly ordered list of task groups for implementing a system based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. Only include files from the provided `file_list`.\n"
                    "2. Group tasks that can be worked on completely independently without any context from other files.\n"
                    "3. Order groups strictly following Pyramid architecture principles, ensuring each group builds upon and benefits from the work done in previous groups.\n"
                    "4. Within each group, order tasks based on their dependencies and logical flow. Ensure prerequisite files are placed before dependent files. For example:\n"
                    "   - In web development: HTML files before CSS, then JavaScript.\n"
                    "   - In backend development: Database schemas before models, then controllers.\n"
                    "   - In system architecture: Core components before modules that depend on them.\n"
                    "   Adapt this ordering principle to the specific technologies and architecture of the project.\n"
                    "5. Provide `file_name` (full path) and `techStack` for each task.\n"
                    "6. Omit configuration, dependencies, and non-essential files.\n"
                    "7. Exclude all image files except `.svg` and all audio asset files.\n"
                    "8. Files that need ANY context from other files MUST be placed in separate, later groups. This rule is to be strictly enforced.\n"
                    "Response Format:\n"
                    "{\n"
                    '    "groups": [\n'
                    '        {\n'
                    '            "group_name": "",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/file.py",\n'
                    '                    "techStack": "python"\n'
                    '                }\n'
                    '            ]\n'
                    '        },\n'
                    '        {\n'
                    '            "group_name": "",\n'
                    '            "tasks": [\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/file.html",\n'
                    '                    "techStack": "html"\n'
                    '                },\n'
                    '                {\n'
                    '                    "file_name": "/full/path/to/file.css",\n'
                    '                    "techStack": "css"\n'
                    '                }\n'
                    '            ]\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    f"Current working project is {self.repo.get_repo_path()}\n\n"
                    "Return only valid JSON without additional text or formatting."
                )
            },
            {
                "role": "user",
                "content": f"Create a strictly grouped task list and an ordered list of groups following Pyramid architecture. Only select files from this list:\n{file_list}\n\nGroup tasks that can be worked on completely independently without ANY context from other files. Ensure each group, when completed, provides necessary context and benefits for the next group's execution, strictly adhering to Pyramid architecture principles. Within each group, carefully order tasks based on their dependencies and logical flow, ensuring prerequisite files are always placed before dependent files. Files that need ANY context from other files MUST be placed in separate, later groups. This rule is to be strictly enforced. Include `file_name` (full path) and `techStack` for each task in JSON format. Ensure correct paths. Original instruction: {instruction}\n\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `TaskPlanner` has successfully generated the task plan")
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `TaskPlanner` has repaired and processed the JSON response")
            return plan_json
        except Exception as e:
            logger.error(f" #### The `TaskPlanner` encountered an error while generating the task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists, original_prompt_language):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is generating task plans")
        plan = await self.get_task_plan(instruction, file_lists, original_prompt_language)
        logger.debug("\n #### The `TaskPlanner` has completed generating the task plans")
        return plan