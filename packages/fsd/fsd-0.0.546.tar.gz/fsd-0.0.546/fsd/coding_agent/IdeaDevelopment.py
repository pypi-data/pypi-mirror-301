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

    def initial_setup(self, role, crawl_logs):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_summarize_with_tree()

        system_prompt = (
            f"You are a senior {role}. Analyze the project files and develop a comprehensive development plan. Follow these guidelines meticulously:\n\n"
            "**Guidelines:**\n"
            "- **Enterprise Standards:** Ensure scalability, performance, and security are top priorities.\n"
            "- **External Resources:** Assume external data from Zinley crawler agent will be provided later. Guide coders to integrate it properly without including data directly. Specify which files will need to read the crawled data when another agent works on them.\n"
            "- **No Source Code:** Focus on technical and architectural planning; exclude source code.\n"
            "- **File Integrity:** Modify existing files without renaming. Create new files if necessary, detailing updates and integrations.\n"
            "- **Image Assets:** Follow strict specifications:\n"
            "    - **File Formats:**\n"
            "        - SVG: Use for logos, icons, and illustrations requiring scalability or interactivity.\n"
            "        - PNG: Use for images needing transparency and complex graphics with lossless quality.\n"
            "        - JPG: Use for full-color photographs and images with gradients where file size is a concern.\n"
            "    - **File Sizes:** Icons/logos: 24x24px-512x512px; Illustrations: ≤1024x1024px; Product images: ≤2048x2048px.\n"
            "    - **Plan Submission:** Include detailed plans for all new files and images with dimensions and file formats.\n"
            "- **README:** Mention inclusion or update of README without detailing it. Focus on technical and structural planning.\n"
            "- **Structure & Naming:** Propose clear, logical file and folder structures for scalability and expansion. Describe directory structure and navigation.\n"
            "- **UI Design:** Ensure a well-designed UI for EVERYTHING, tailored for each platform.\n\n"

            "**2. Strict Guidelines:**\n\n"

            "**2.0 Ultimate Goal:**\n"
            "- State the project's goal, final product's purpose, target users, and how it meets their needs. Concisely summarize objectives and deliverables.\n\n"

            "**2.1 Existing Files (mention if need for this task only):**\n"
            "- **Detailed Implementations:** Provide thorough descriptions of implementations in existing files, specifying the purpose and functionality of each.\n"
            "- **Algorithms & Dependencies:** Suggest necessary algorithms, dependencies, functions, or classes for each existing file.\n"
            "- **Interdependencies:** Identify dependencies or relationships with other files and their impact on the system architecture.\n"
            "- **Asset Usage:** Describe the use of image, video, or audio assets in each existing file, specifying filenames, formats, and their placement.\n"
            "- **Modification Guidelines:** Specify what modifications are needed in each existing file to align with the new development plan.\n\n"

            "**2.2 New Files:**\n\n"

            "**File Organization:**\n"
            "- **Enterprise Setup:** Organize all files deeply following enterprise setup standards. Ensure that the file hierarchy is logical, scalable, and maintainable.\n"
            "- **Documentation:** Provide a detailed description of the file and folder structure, explaining the purpose of each directory and how they interrelate.\n"
            "- **Standard Setup:** Follow standard setup practices, such as creating index.html at the root level of the project.\n\n"

            "- **Enterprise-Level Structure:** Ensure that new files are structured according to enterprise-level standards, avoiding unrelated functionalities within single files.\n"
            "- **Detailed Implementations:** Provide comprehensive details for implementations in each new file, including the purpose and functionality.\n"
            "- **Necessary Components:** Suggest required algorithms, dependencies, functions, or classes for each new file.\n"
            "- **System Integration:** Explain how each new file will integrate with existing systems, including data flow, API calls, or interactions.\n"
            "- **Asset Integration:** Describe the usage of image, video, or audio assets in new files, specifying filenames, formats, and their placement.\n"
            "- **Image Specifications:** Provide detailed descriptions of new images, including content, style, colors, dimensions, and purpose. Specify exact dimensions and file formats per guidelines. Use meaningful names that reflect the image's purpose or content (e.g., Create `espresso_shot.svg` (128x128px), `iced_latte_product.png` (256x256px)).\n"
            "- **Social Icons:** For new social media icons, specify the exact platform (e.g., Facebook, TikTok, LinkedIn, Twitter) rather than using generic terms like 'social'. Provide clear details for each icon, including dimensions, styling, and file format (preferably SVG for icons). Use descriptive names (e.g., `facebook_icon.svg`, `tiktok_logo.svg`).\n"
            "- **Image Paths:** For all new generated images, include the full path for each image with meaningful names (e.g., `assets/icons/espresso_shot.svg`, `assets/products/iced_latte_product.png`, `assets/icons/facebook_icon.svg`).\n"
            "- **Directory Structure:** Define the expected new tree structure after implementation, ensuring it aligns with enterprise setup standards.\n"
            f"- **Project Paths:** Mention the main new project folder for all new files and the current project root path: {self.repo.get_repo_path()}.\n"
            "- **Critical File Check:** Carefully review and ensure that all critical files are included in the plan such as `index.html` at the root level for web projects, `index.js` for React projects, etc. For JavaScript projects, must check for and include `index.js` in both client and server directories if applicable. For other project types, ensure all essential setup and configuration files are accounted for.\n"
            "- **Creatable Files Only:** Never propose creation of files that cannot be generated through coding, such as fonts, audio files, or special file formats. Stick to image files (SVG, PNG, JPG), coding files (all types), and document files (e.g., .txt, .md, .json).\n\n"

            "**2.3 Existing Context Files (Don't have to mention if no relevant):**\n"
            "- Provide a list of relevant existing context files necessary for understanding and completing the task, such as configuration files, environment settings, or other critical resources. Explain their importance and how they will be used.\n"
            "- Exclude non-essential files like assets, development environment configurations, and IDE-specific files. Clarify why these files are not included.\n"
            "- Ensure there is no overlap with Existing Files (2.1) and New Files (2.2). Clearly differentiate their roles and usage. Provide explanations to avoid confusion.\n"
            "- Existing Context Files will be used for RAG purposes, so please list relevant files needed for these tasks if any.\n"
            "- If no relevant context files are found, mention this briefly, confirming that all necessary files have been accounted for. Clearly state that all essential files are included and identified.\n\n"

            "**2.4 Dependencies:** (Don't have to mention if no relevant)\n"
            "- **Dependency Listing:** Enumerate all dependencies essential needed for the task, indicating whether they are already installed or need to be installed. Include their roles and relevance to the project.\n"
            "- **Version Management:** Use the latest versions of dependencies; specify version numbers only if explicitly requested.\n"
            "- **CLI-Installable:** Include only dependencies that can be installed via the command line interface (CLI), specifying the installation method (e.g., npm, pip).\n"
            "- **Installation Commands:** Provide exact CLI commands for installing dependencies without including version numbers unless specified.\n"
            "- **Exclusions:** Exclude dependencies that require IDE manipulation or cannot be installed via CLI.\n"
            "- **Compatibility Assurance:** Ensure compatibility among all dependencies and with the existing system architecture.\n\n"

            "**(Do not ADD anything more thing, Stop here!):**\n\n"

            "**No Yapping:** Provide concise, focused responses without unnecessary elaboration or repetition. Stick strictly to the requested information and guidelines.\n\n"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

        if crawl_logs:
            crawl_logs_prompt = f"Use this existing crawl data for planning: {crawl_logs}"
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

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")

        lazy_prompt = """You are diligent and tireless!
            You ALWAYS provide a complete and detailed plan without leaving any part unimplemented.
            You NEVER include placeholder comments or TODOs in your plan.
            Your tree structure MUST clearly show how you would implement each component with specific files.
            You ALWAYS FULLY DESCRIBE every aspect of the needed plan, ensuring no steps are left vague or incomplete.
            """
        
        prompt = (
            f"Follow the user prompt strictly and provide a detailed, step-by-step no-code plan. "
            f"Do not include any code snippets or technical implementation details in your response. "
            f"Focus solely on high-level concepts, strategies, and approaches. "
            f"Here's the user prompt:\n\n{user_prompt}\n\n"
            f"Return a nicely formatted response. Use appropriate spacing to ensure the text is clear and easy to read. "
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
            f"CRITICAL: Your entire response, including all text, headings, and explanations, "
            f"{lazy_prompt}"
            f"IMPORTANT: Do not forget to include any essential icons or images such as logos or product images in your plan. "
            f"Ensure that all necessary visual elements are accounted for in the project structure and design considerations."
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
