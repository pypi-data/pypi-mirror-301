import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ImageAnalysAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.project_path = self.repo.get_repo_path()
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, style_files):
        """
        Initialize the conversation with a system prompt and user context.
        """

        all_file_contents = ""
        tree_contents = self.repo.print_tree()

        style_files_path = style_files

        if style_files:
            for file_path in style_files_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"UI/UX designer for image analysis. Analyze files, describe images. FOLLOW:\n\n"
            "2. Analyze style files\n"
            "3. Extract theme elements and color scheme\n"
            "4. Determine image sizes\n"
            "5. Identify backgrounds and textures\n"
            "6. Analyze existing images\n"
            "7. Describe images matching style, including detailed descriptions of most fitting elements\n"
            "8. Adapt to theme, color scheme, and sizes (1024x1024, 1792x1024, 1024x1792)\n"
            f"9. MUST ALWAYS provide FULL PATH within `{self.repo.get_repo_path()}` to save each image\n"
            "10. Support PNG, JPG, JPEG only\n"
            "11. Specify style that fits the overall design theme\n\n"
            "Focus on detailed analysis and description. No code changes.\n\n"
            "Use exact paths. Follow requirements strictly.\n\n"
            "Provide comprehensive color scheme analysis.\n\n"
            "Offer detailed descriptions of elements that best fit the design.\n\n"
            "Clearly articulate the overall style that aligns with the design theme.\n\n"
            "Organize with clear headings (max ####) and spacing."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject structure: {tree_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})


    async def get_idea_plan(self, user_prompt, original_prompt_language):
        prompt = (
            f"User image generation request:\n{user_prompt}\n\n"
            f"Use the provided data to help generate a fitting image for the current project\n"
            f"Image Analysis Guidelines\n\n"
            f"- Only mention images that need to be generated\n"
            f"- Do not include any existing images or additional information\n"
            f"- Use the following format for each image table:\n\n"
            f"| Aspect | Description |\n"
            f"|--------|-------------|\n"
            f"| Image Name | [Name] |\n"
            f"| Description | [Detailed description] |\n"
            f"| Size | [Width x Height] |\n"
            f"| Style | [Style description] |\n"
            f"| Colors | [Color scheme] |\n"
            f"| File Path | [Exact full path as mentioned in the user request] |\n\n"
            f"- Separate each image table with a line of dashes (---------------------)\n"
            f"- Only describe images explicitly mentioned in the user prompt\n"
            f"- Do not add or invent additional images\n"
            f"- Use ONLY the exact full paths for images as specified in the user's request\n"
            f"- Do not modify, guess, or create new paths for images\n\n"
            f"Provide the response in the following language: {original_prompt_language}"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            logger.debug("\n #### The `ImageAnalysAgent` is initiating the AI prompt for idea generation")
            response = await self.ai.stream_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            logger.debug("\n #### The `ImageAnalysAgent` has successfully received the AI response")
            return response
        except Exception as e:
            logger.error(f" #### The `ImageAnalysAgent` encountered an error during idea generation\n Error: {e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("\n #### The `ImageAnalysAgent` is beginning the process of generating idea plans")
        plan = await self.get_idea_plan(user_prompt, original_prompt_language)
        logger.debug("\n #### The `ImageAnalysAgent` has completed generating idea plans")
        return plan
