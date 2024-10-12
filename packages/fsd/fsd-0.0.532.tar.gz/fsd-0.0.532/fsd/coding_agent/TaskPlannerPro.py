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
                    "You are a principal engineer specializing in Pyramid architecture. Generate an ordered list of task groups for implementing a system based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. Only include files from the provided `file_list`.\n"
                    "2. Group tasks that are completely independent and can be worked on concurrently without any context from each other.\n"
                    "3. Strictly enforce separation of concerns. Files that need context from others (e.g., main files, style files, script files) must never be in the same group.\n"
                    "4. Order groups following Pyramid architecture principles, ensuring each group provides necessary context for subsequent groups.\n"
                    "5. Within each group, order tasks based on their internal dependencies, if any.\n"
                    "6. Provide `file_name` (full path) and `techStack` for each task.\n"
                    "7. Omit configuration, dependencies, and non-essential files.\n"
                    "8. If the original instruction requires SVG files, group all SVG files together as the first group.\n"
                    "9. Exclude all image files except `.svg` and all audio asset files.\n"
                    "10. For web development tasks, always order groups as HTML first, then CSS, then JavaScript. This is because HTML provides the structure, CSS styles that structure, and JavaScript adds interactivity.\n"
                    "11. For other tech stacks, apply similar principles. For example, in a backend system, group database schema files before API route files.\n"
                    "12. Never group files of different tech stacks together. For instance, Python files should be in a separate group from JavaScript files.\n"
                    "13. For each tech stack, create a separate group for the main or index file (e.g., index.html, main.css, app.js) before grouping other files of the same type. This allows subsequent files to follow the established pattern.\n"
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
                "content": f"Create a grouped task list and an ordered list of groups following Pyramid architecture. Only select files from this list:\n{file_list}\n\nIf the original instruction requires SVG files, group all SVG files together as the first group. Then, strictly group only tasks that are completely independent and can be executed without any knowledge of other files' configurations or contents. Enforce a strong separation between files that need context from others (e.g., main files, style files, script files) - these must always be in separate groups. Order the groups to ensure each group, when completed, provides necessary context for the next group's execution, adhering strictly to Pyramid architecture principles. For website-related tasks, always order groups as HTML first, then CSS, then JavaScript, because HTML provides structure, CSS styles that structure, and JavaScript adds interactivity. For other tech stacks, apply similar principles (e.g., database schema files before API route files in a backend system). Never group files of different tech stacks together. Within each group, order tasks based on their internal dependencies, if any. For each tech stack, create a separate group for the main or index file (e.g., index.html, main.css, app.js) before grouping other files of the same type. This allows subsequent files to follow the established pattern. Include `file_name` (full path) and `techStack` for each task in JSON format. Ensure correct paths. Original instruction: {instruction}\n\n"
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