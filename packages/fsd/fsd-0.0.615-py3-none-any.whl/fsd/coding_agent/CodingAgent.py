import os
import sys
import asyncio
from datetime import datetime
import aiohttp
import json
import re
from json_repair import repair_json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class CodingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def initial_setup(self, context_files, instructions, context, crawl_logs):
        """Initialize the setup with the provided instructions and context."""

        logger.debug("\n #### The `CodingAgent` is initializing setup with provided instructions and context")

        prompt = f"""You are an expert software engineer. Follow these guidelines strictly when responding to instructions:

                **Response Guidelines:**
                1. Use ONLY the following SEARCH/REPLACE block format for ALL code changes, additions, or deletions:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. Ensure the SEARCH section exactly matches existing code, including whitespace and comments.

                4. For large files, focus on relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. MUST break complex changes or large files into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of SEARCH/REPLACE blocks. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                Remember: Your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.

        """

        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Development plan: {instructions}"},
            {"role": "assistant", "content": "Understood!"},
            {"role": "user", "content": f"Current working file: {context}"},
            {"role": "assistant", "content": "Understood!"},
        ]

        if context_files:
            all_file_contents = ""

            for file_path in context_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are all the supported files to provide context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll use this context when implementing changes."})

        if crawl_logs:
            self.conversation_history.append({"role": "user", "content": f"This is supported data for this entire process, use it if appropriate: {crawl_logs}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood. I'll consider this data when making changes."})


    async def get_coding_request(self, file, techStack, prompt):
        """
        Get coding response for the given instruction and context from Azure OpenAI.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            prompt (str): The specific task or instruction for coding.

        Returns:
            str: The code response.
        """
        file_name = os.path.basename(file)
        is_svg = file_name.lower().endswith('.svg')

        lazy_prompt = "You are diligent and tireless. You NEVER leave comments describing code without implementing it. You always COMPLETELY IMPLEMENT the needed code."

        user_prompt = f"As a world-class, highly experienced {'SVG designer' if is_svg else f'{techStack} developer'}, implement the following task with utmost efficiency and precision:\n"
        user_prompt += f"For: {file_name}:\n"
        
        if is_svg:
            #user_prompt += f"Image implementation: {prompt}\n"
            user_prompt += (
                "Create a visually appealing design with elegant UI.\n"
                "Balance aesthetics and functionality, ensuring each element enhances the user experience.\n"
                "Prioritize smooth performance and sophistication in all visual aspects.\n"
            )
        else:
            #user_prompt += f"Main Task: {prompt}\n"
            user_prompt += (
                "For UI-related tasks:\n"
                "- Ensure perfect alignment and consistent padding for a clean, modern look.\n"
                "- Implement a visually striking design with NICE UI and interactions.\n"
                "- Apply responsive design principles and prioritize whitespace usage.\n"
                "- Enhance user experience while maintaining optimal performance.\n"
                "- Respect the current code structure and conventions.\n"
                "For ALL CODE TYPES:"
                "- Use only existing imports; do not add new ones unless explicitly instructed.\n"
                "- Maintain the exact coding style, indentation, and naming conventions of the original code.\n"
                "- Modify only the specific parts mentioned in the instructions; leave all other code unchanged.\n"
                "- Implement only the changes explicitly requested in the given instructions.\n"
                "- Ensure all variable names, function names, and class names remain consistent with the original code.\n"
                "- Do not alter the overall structure or logic flow of the existing code if not explicitly requested .\n"
                "- Strictly adhere to the development plan; do not implement anything not explicitly mentioned.\n"
                "- Do not create or modify any UI elements unless specifically instructed to do so.\n"
            )
            user_prompt += "Always refer back to the High level development instruction to ensure alignment and completeness.\n"

        user_prompt += f"{lazy_prompt}\n" if not is_svg else ""
        user_prompt += "NOTICE: Your response should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed."

        if self.conversation_history and self.conversation_history[-1]["role"] == "user":
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        self.conversation_history.append({"role": "user", "content": user_prompt})

        try:
            response = await self.ai.coding_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            content = response.choices[0].message.content

            if content.endswith(">>>>>>> REPLACE"):
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
            else:
                self.conversation_history.append({"role": "assistant", "content": content})
                # The response was cut off, prompt AI to continue
                continuation_prompt = "The previous response was cut off before completing the SEARCH/REPLACE block. Please continue from where you left off without overlapping any content. Ensure the continuation ends with '>>>>>>> REPLACE'."
                self.conversation_history.append({"role": "user", "content": continuation_prompt})
                
                continuation_response = await self.ai.coding_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
                continuation_content = continuation_response.choices[0].message.content

                if continuation_content.endswith(">>>>>>> REPLACE"):
                    # Combine the incomplete and continuation responses
                    complete_content = content + continuation_content
                    self.conversation_history = self.conversation_history[:-2]
                    self.conversation_history.append({"role": "assistant", "content": complete_content})
                    return complete_content
                else:
                    logger.error("Response was cut off and could not be completed.")
                    return "The response was cut off and could not be completed. Please try again."

        except Exception as e:
            logger.error(f" #### The `CodingAgent` encountered an error while getting coding request: {e}")
            raise


    async def get_coding_requests(self, file, techStack, prompt):
        """
        Get coding responses for a file from Azure OpenAI based on user instruction.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.
            prompt (str): The coding task prompt.

        Returns:
            str: The code response or error reason.
        """
        return await self.get_coding_request(file, techStack, prompt)

    def clear_conversation_history(self):
        """Clear the conversation history."""
        logger.debug("\n #### The `CodingAgent` is clearing conversation history")
        self.conversation_history = []

    def destroy(self):
        """De-initialize and destroy this instance."""
        logger.debug("\n #### The `CodingAgent` is being destroyed")
        self.repo = None
        self.conversation_history = None
        self.ai = None