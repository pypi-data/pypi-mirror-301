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

class ShortIdeaDevelopment:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()


    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, role, crawl_logs, context):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_tree()
        system_prompt = (
            f"As a senior {role}, provide a concise, specific plan:\n\n"
            "File Updates\n"
            f"- {self.repo.get_repo_path()}/path/to/file1.ext:\n"
            "  - Change: [specific code change]\n"
            "  - Reason: [brief justification]\n"
            f"- {{self.repo.get_repo_path()}}/path/to/file2.ext:\n"
            "  - Change: [specific code change]\n"
            "  - Reason: [brief justification]\n\n"
            "New Files (if needed)\n"
            f"- {self.repo.get_repo_path()}/path/to/new_file1.ext:\n"
            "  - Implementation: [detailed description of what to implement]\n"
            "  - Purpose: [brief explanation of the file's purpose]\n"
            f"- {self.repo.get_repo_path()}/path/to/new_file2.ext:\n"
            "  - Implementation: [detailed description of what to implement]\n"
            "  - Purpose: [brief explanation of the file's purpose]\n\n"
            "Code Flow (if applicable)\n"
            "1. [First specific modification]\n"
            "2. [Next specific modification]\n\n"
            "Focus on code changes only. Be specific, not general. Avoid non-code details.\n\n"
            "Context Support\n"
            "If context files are provided, briefly mention:\n"
            f"- Context support file: {self.repo.get_repo_path()}/path/to/context_file.ext\n"
            "- Relevant matter: [brief description of relevant information]\n"
            "Use this context to inform your plan, but do not modify context files.\n"
            "Note: If no new files need to be created, omit the 'New Files' section.\n"
            "API Usage\n"
            "If any API needs to be used or is mentioned by the user:\n"
            "- Specify the full API link in the file that needs to implement it\n"
            "- Clearly describe what needs to be done with the API\n"
            "Example:\n"
            f"- {self.repo.get_repo_path()}/api_handler.py:\n"
            "  - API: https://api.example.com/v1/data\n"
            "  - Implementation: Use this API to fetch user data. Parse the JSON response and extract the 'username' and 'email' fields.\n"
            "Asset Integration\n"
            "- Describe usage of image/video/audio assets in new files (filename, format, placement)\n"
            "- For new images: Provide content, style, colors, dimensions, purpose\n"
            "- For social icons: Specify platform (e.g., Facebook, TikTok), details, dimensions, format\n"
            "- Only propose creatable files (images, code, documents). No fonts or audio or video files.\n"

            "Strictly Enforced Actionable Tasks Only:\n"
            "- Code Writing: Provide detailed code snippets or full implementations as needed.\n"
            "- Bug Fixing: Identify and fix bugs in existing code.\n"
            "- Code Updates: Modify existing code to meet new requirements or improve functionality.\n"
            "- Documentation Writing: Create or update documentation for code, APIs, or project structure.\n"
            "- Image Generation: Specify details for new images to be created, including dimensions and file formats.\n"
            "- File Creation: Create new files with appropriate content and structure.\n"
            "- Function Writing: Implement new functions or methods as required.\n"
            "- Code Refactoring: Restructure existing code to improve readability, efficiency, or maintainability.\n"

            "Stricly do not include these task, since it'a already automatically:\n"
            "- Navigating to any location\n"
            "- Opening browsers or devices\n"
            "- Opening any files\n"
            "- Any form of navigation\n"
            "- Verifying changes\n"
            "- Any form of verification\n"
            "- Clicking, viewing, or any other non-coding actions\n"

            "Important: When you encounter a file that already exists but is empty, do not propose to create a new one. Instead, treat it as an existing file and suggest modifications or updates to it.\n"
            "No Yapping: Provide concise, focused responses without unnecessary elaboration or repetition\n"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

        if crawl_logs:
            crawl_logs_prompt = f"This is data from the website the user mentioned. You don't need to crawl again: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})

            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original development plan guidelines strictly. No additional crawling or API calls needed."})
        
        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            logger.info(working_files)

            all_working_files_contents = ""
          

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE - NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"

            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is data for potential existing files you may need to modify or update or provide context. \n{all_working_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})
            else:
                self.conversation_history.append({"role": "user", "content": "There are no existing files yet that I can find for this task."})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})



    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")

        prompt = (
            f"Provide a clear to-do list for:\n\n{user_prompt}\n\n"
            f"Use clear headings (max h4). "
            f"Format for readability. "
            f"If you provide a tree structure, use a plaintext markdown for it. "
            f"If you provide any bash commands, use the following format:\n"
            f"```bash\n"
            f"command here\n"
            f"```\n"
            f"If you need to provide code, provide as little as possible for an example, not fully implemented code, since this is a to-do list, not the coding part.\n"
            f"Strictly do not include these tasks, since they're already automatically handled:\n"
            f"- Navigating to any location\n"
            f"- Opening browsers or devices\n"
            f"- Opening any files\n"
            f"- Any form of navigation\n"
            f"- Verifying changes\n"
            f"- Any form of verification\n"
            f"- Clicking, viewing, or any other non-coding/non-image-generation actions\n"
            f"Respond in: {original_prompt_language}"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.stream_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt, original_prompt_language)
