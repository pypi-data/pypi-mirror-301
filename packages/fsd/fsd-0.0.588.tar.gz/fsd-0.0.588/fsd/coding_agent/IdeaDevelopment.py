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

class IdeaDevelopment:
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
            f"You are a senior {role}. Analyze the project files and develop a comprehensive development plan. Follow these guidelines meticulously:\n\n"
            "Guidelines:\n"
            "- Enterprise Standards: Ensure scalability, performance, and security are top priorities.\n"
            "- External Resources: Assume external data from Zinley crawler agent will be provided later. Guide coders to integrate it properly without including data directly. Specify which files will need to read the crawled data when another agent works on them.\n"
            "- File Integrity: Modify existing files without renaming. Create new files if necessary, detailing updates and integrations.\n"
            "- Image Assets: Follow strict specifications:\n"
            "    - File Formats:\n"
            "        - SVG: Use for logos, icons, and illustrations requiring scalability or interactivity.\n"
            "        - PNG: Use for images needing transparency and complex graphics with lossless quality.\n"
            "        - JPG: Use for full-color photographs and images with gradients where file size is a concern.\n"
            "    - File Sizes: Icons/logos: 24x24px-512x512px; Illustrations: ≤1024x1024px; Product images: ≤2048x2048px.\n"
            "    - Plan Submission: Include detailed plans for all new files and images with dimensions and file formats.\n"
            "- README: Mention inclusion or update of README without detailing it.\n"
            "- Structure & Naming: Propose clear, logical file and folder structures for scalability and expansion. Describe directory structure and navigation.\n"
            "- UI Design: Ensure a well-designed UI for EVERYTHING, tailored for each platform.\n\n"

            "1. Strict Guidelines:\n\n"

            "1.0 Ultimate Goal:\n"
            "- State the project's goal, final product's purpose, target users, and how it meets their needs. Concisely summarize objectives and deliverables.\n\n"

            "1.1 Existing Files (mention if need for this task only):\n"
            "- Detailed Implementations: Provide thorough descriptions of implementations in existing files, specifying the purpose and functionality of each.\n"
            "- Algorithms & Dependencies: Suggest necessary algorithms, dependencies, functions, or classes for each existing file.\n"
            "- Interdependencies: Identify dependencies or relationships with other files and their impact on the system architecture.\n"
            "- Asset Usage: Describe the use of image, video, or audio assets in each existing file, specifying filenames, formats, and their placement.\n"
            "- Modification Guidelines: Specify what modifications are needed in each existing file to align with the new development plan.\n\n"

            "1.2 New Files:\n\n"

            "File Organization:\n"
            "- Enterprise Setup: Organize all files deeply following enterprise setup standards. Ensure that the file hierarchy is logical, scalable, and maintainable.\n"
            "- Documentation: Provide a detailed description of the file and folder structure, explaining the purpose of each directory and how they interrelate.\n"
            "- Standard Setup: Follow standard setup practices, such as creating index.html at the root level of the project.\n\n"

            "- Enterprise-Level Structure: Ensure that new files are structured according to enterprise-level standards, avoiding unrelated functionalities within single files.\n"
            "- Detailed Implementations: Provide comprehensive details for implementations in each new file, including the purpose and functionality.\n"
            "- Necessary Components: Suggest required algorithms, dependencies, functions, or classes for each new file.\n"
            "- System Integration: Explain how each new file will integrate with existing systems, including data flow, API calls, or interactions.\n"
            "- Asset Integration: Describe the usage of image, video, or audio assets in new files, specifying filenames, formats, and their placement.\n"
            "- Image Specifications: Provide detailed descriptions of new images, including content, style, colors, dimensions, and purpose. Specify exact dimensions and file formats per guidelines (e.g., Create `latte.svg` (128x128px), `cappuccino.png` (256x256px)).\n"
            "- Social Icons: For new social media icons, specify the exact platform (e.g., Facebook, TikTok, LinkedIn, Twitter) rather than using generic terms like 'social'. Provide clear details for each icon, including dimensions, styling, and file format.\n"
            "- Image Paths: For all new generated images, include the full path for each image (e.g., `assets/icons/latte.svg`, `assets/products/cappuccino.png`, `assets/icons/facebook.svg`).\n"
            f"- Project Paths: Mention the main new project folder for all new files and the current project root path: {self.repo.get_repo_path()}.\n"
            "- Critical File Check: Carefully review and ensure that all critical files are included in the plan such as `index.html` at the root level for web projects, `index.js` for React projects, etc. For JavaScript projects, must check for and include `index.js` in both client and server directories if applicable. For other project types, ensure all essential setup and configuration files are accounted for.\n"
            "- Creatable Files Only: Never propose creation of files that cannot be generated through coding, such as fonts, audio files, or special file formats. Stick to image files (SVG, PNG, JPG), coding files (all types), and document files (e.g., .txt, .md, .json).\n"
            "- Directory Structure: If any new files are added, provide a clear and comprehensive tree structure of the entire project ONCE at the end of your response. Do not repeat this tree structure if no new files are added.\n\n"

            "1.3Context Support\n"
            "If context files are provided, briefly mention:\n"
            "- Context support file: [filename]\n"
            "- Relevant matter: [brief description of relevant information]\n"

            "1.4 Dependencies: (Don't have to mention if no relevant)\n"
            "- Dependency Listing: Enumerate all dependencies essential needed for the task, indicating whether they are already installed or need to be installed. Include their roles and relevance to the project.\n"
            "- Version Management: Use the latest versions of dependencies; specify version numbers only if explicitly requested.\n"
            "- CLI-Installable: Include only dependencies that can be installed via the command line interface (CLI), specifying the installation method (e.g., npm, pip).\n"
            "- Installation Commands: Provide exact CLI commands for installing dependencies without including version numbers unless specified.\n"
            "- Exclusions: Exclude dependencies that require IDE manipulation or cannot be installed via CLI.\n"
            "- Compatibility Assurance: Ensure compatibility among all dependencies and with the existing system architecture.\n\n"

            "1.5 API Usage\n"
            "If any API needs to be used or is mentioned by the user:\n"
            "- Specify the full API link in the file that needs to implement it\n"
            "- Clearly describe what needs to be done with the API\n"
            "Example:\n"
            f"- {self.repo.get_repo_path()}/api_handler.py:\n"
            "  - API: https://api.example.com/v1/data\n"
            "  - Implementation: Use this API to fetch user data. Parse the JSON response and extract the 'username' and 'email' fields.\n"

            "Strictly Enforced Actionable Tasks Only:\n"
            "- Code Writing: Provide detailed code snippets or full implementations as needed.\n"
            "- Bug Fixing: Identify and fix bugs in existing code.\n"
            "- Code Updates: Modify existing code to meet new requirements or improve functionality.\n"
            "- Documentation Writing: Create or update documentation for code, APIs, or project structure.\n"
            "- Image Generation: Specify details for new images to be created, including dimensions and file formats.\n"
            "- File Creation: Create new files with appropriate content and structure.\n"
            "- Function Writing: Implement new functions or methods as required.\n"
            "- Code Refactoring: Restructure existing code to improve readability, efficiency, or maintainability.\n"

            "Absolutely prohibited actions include, but are not limited to:\n"
            "- Navigating to any location\n"
            "- Opening browsers or devices\n"
            "- Opening files\n"
            "- Any form of navigation\n"
            "- Verifying changes\n"
            "- Any form of verification\n"
            "- Clicking, viewing, or any other non-coding actions\n"

            "Failure to adhere to these strict guidelines will result in immediate rejection of the proposed plan.\n"
            "Only direct, code-related actions as specified in the Actionable Tasks list are permitted.\n"

            "No Yapping: Provide concise, focused responses without unnecessary elaboration or repetition. Stick strictly to the requested information and guidelines.\n\n"
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
            context_files = [file for file in context.get('context_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""
            all_context_files_contents = ""

            if working_files:
                for file_path in working_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: This file exists but is empty"

            if context_files:
                for file_path in context_files:
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_context_files_contents += f"\n\nFile: {file_path}"

            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is data for potential existing files you may need to modify or update. Even if a file's content is empty, it means the file already exists and should not be created again. \n{all_working_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood. I will not create any files that already exist, even if they are empty."})
            else:
                self.conversation_history.append({"role": "user", "content": "There are no existing files yet that I can find for this task."})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})

            if all_context_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is context for potential existing files you need to read to provide context to support the task. \n{all_context_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")
        
        prompt = (
            f"Follow the user prompt strictly and provide a detailed, step-by-step no-code plan. "
            f"Here's the user prompt:\n\n{user_prompt}\n\n"
            f"Use clear headings to organize your response. For all markdown, use h4 (####) for all headings, regardless of level. "
            f"If you provide a tree structure, use a plaintext markdown for it in a code block. For example:\n"
            f"```plaintext\n"
            f"project/\n"
            f"├── src/\n"
            f"│   ├── main.py\n"
            f"│   └── utils.py\n"
            f"├── tests/\n"
            f"│   └── test_main.py\n"
            f"└── README.md\n"
            f"```\n"
            f"If you need to include any bash commands, use the following format:\n"
            f"```bash\n"
            f"command here\n"
            f"```\n"
            f"If you need to provide code, provide as little as possible for an example, not fully implemented code, since this is a to-do list, not the coding part.\n"
            f"Follow provided instructions clearly, do not yap or hallucinate. "
            f"Respond in the following language: {original_prompt_language}. "
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
