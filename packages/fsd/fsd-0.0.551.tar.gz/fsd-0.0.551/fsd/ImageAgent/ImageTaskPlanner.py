import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class ImageTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_task_plan(self, instruction):
        """
        Get a dependency installation plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for image planning.

        Returns:
            dict: Dependency installation plan or error reason.
        """

        logger.debug("\n #### Initiating `ImageTaskPlanner` to generate AI-powered task plan")

        messages = [
            {
                "role": "system",
                "content": (
                    "You're an EXPERT UI/UX designer for professional image generation. Create a step-by-step plan based on project style and user instructions. Follow these rules:\n\n"
                    f"1. Use the exact file paths provided in the instruction for image saving. If only a relative path is given, prepend it with the root path: {self.repo.get_repo_path()}\n"
                    "2. Organize steps logically, matching project style.\n"
                    "3. Provide professional, elegant, and clean prompts aligned with project style.\n"
                    "4. Use only the file paths specified in the instruction. Do not modify or create new paths.\n"
                    "5. Include dimensions and format. Use only '1024x1024', '1792x1024', '1024x1792' for DALL-E 3.\n\n"
                    "For each task, provide:\n"
                    "- file_path: Exact file path as specified in the instruction, or full path including root if only relative path was given\n"
                    "- prompt: Detailed description for professional, elegant, and clean image\n"
                    "- dalle_dimension: DALL-E 3 size\n"
                    "- actual_dimension: Use case adaptive size\n"
                    "- format: Image format (lowercase)\n\n"
                    "Respond with this JSON format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    f'            "file_path": "{self.repo.get_repo_path()}/exact/path/from/instruction/example.png",\n'
                    '            "prompt": "Create a professional, elegant image of..., must use English",\n'
                    '            "dalle_dimension": "1024x1024",\n'
                    '            "actual_dimension": "800x600",\n'
                    '            "format": "png"\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "Provide only JSON. No additional text. Ensure lowercase image formats."
                )
            },
            {
                "role": "user",
                "content": f"Create a professional, elegant, and clean image generation plan based on these instructions. Align with project style. Use the exact file paths provided in the instruction, or if only relative paths are given, prepend them with the root path: {self.repo.get_repo_path()}. Use DALL-E 3 dimensions ('1024x1024', '1792x1024', '1024x1792') and adaptive actual dimensions. Use lowercase formats. Ensure all content is appropriate and maintains a professional aesthetic:\n{instruction}\n"
            }
        ]

        try:
            logger.debug("\n #### Sending request to AI gateway for task plan generation")
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### Successfully received and parsed AI-generated task plan")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### Encountered JSON decoding error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### Successfully repaired and parsed JSON task plan")
            return plan_json
        except Exception as e:
            logger.error(f" #### `ImageTaskPlanner` encountered an error while generating task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug(f" #### Beginning task plan retrieval process in {instruction}")
        plan = await self.get_task_plan(instruction)
        logger.debug("\n #### Successfully retrieved task plan from `ImageTaskPlanner`")
        return plan
