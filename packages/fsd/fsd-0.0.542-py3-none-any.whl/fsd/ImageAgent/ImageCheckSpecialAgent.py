import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ImageCheckSpecialAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_image_check_plan(self, user_prompt, original_prompt_language):
        """
        Get an image check plan from Azure OpenAI based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.
            original_prompt_language (str): The language to use for the response.

        Returns:
            dict: Image check plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    f"STRICTLY analyze the user's request for ONLY PNG, png, JPG, jpg, JPEG, jpeg, or .ico images. EXCLUDE ALL OTHER IMAGE FORMATS, INCLUDING SVG. For each valid image mentioned, extract and return the following details in a markdown table format:\n\n"
                    "| Image Path | Format |\n"
                    "|------------|--------|\n"
                    "| [full path including root and correct relative path to image file] | [image format] |\n\n"
                    "DO NOT process or include any other types of assets or image formats. Respond ONLY with the extracted details for PNG, JPG, JPEG, and .ico images.\n"
                    f"- Separate each image table clearly using a line of dashes (---------------------)\n"
                    "Use appropriate spacing to ensure the text is clear and easy to read.\n"
                    "Use clear headings (maximum size #### for h4) to organize your response.\n"
                    "MUST use a nice table markdown to display\n"
                    f"Provide the response in the following language: {original_prompt_language}\n"
                    "IMPORTANT: If the user request contains any image formats other than PNG, JPG, JPEG, or .ico, completely ignore and do not mention them in the response.\n"
                    "CRITICAL: Use ONLY the exact full image paths mentioned in the development plan. DO NOT modify, guess, or create new paths. The full path MUST include the provided root and correct relative path to the image file."
                )
            },
            {
                "role": "user",
                "content": f"Finding images in this development plan: {user_prompt}"
            }
        ]

        response = await self.ai.stream_prompt(messages, self.max_tokens, 0, 0)
        return response

    async def get_image_check_plans(self, user_prompt, original_prompt_language):
        """
        Get image check plans based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image check plan or error reason.
        """
        logger.debug(f" #### The `ImageCheckSpecialAgent` is initiating the image check plan generation\n User prompt: {user_prompt}")
        plan = await self.get_image_check_plan(user_prompt, original_prompt_language)
        logger.debug(f" #### The `ImageCheckSpecialAgent` has completed generating the image check plan")
        return plan
