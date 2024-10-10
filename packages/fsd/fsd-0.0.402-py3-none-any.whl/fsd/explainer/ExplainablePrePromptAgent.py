import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)
class ExplainablePrePromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_prePrompt_plan(self, user_prompt, file_attachments, focused_files):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.
            file_attachments (list): List of file paths attached by the user.
            focused_files (list): List of files the user is currently focused on.

        Returns:
            dict: Development plan or error reason.
        """

        tree = self.repo.print_tree()
    
        messages = [
            {
                "role": "system",
                "content": (
                    "Look at the user's question, project files, and any attached files carefully. Give an answer in this exact JSON format:\n\n"
                    "1. original_prompt_language: \n"
                    "   - Use the language the user asked for, if they said one.\n"
                    "   - If not, figure out what language the user's question is in.\n\n"
                    "2. processed_prompt: \n"
                    "   - If it's not in English, translate it to English.\n"
                    "   - Make sure it's clear and short, but keeps the main idea.\n"
                    "   - If the question isn't clear, ask for more details.\n\n"
                    "3. pipeline: \n"
                    "   - Pick '1' if:\n"
                    "     * The question is about this project files\n"
                    "     * It's about the current project\n"
                    "     * We need to look at the project structure or code\n"
                    "   - Pick '2' if:\n"
                    "     * It's a general question not about the project\n"
                    "     * It's about files already attached and we don't need to look at the project\n"
                    "     * It's a theory question not directly about the project\n"
                    "     * It's a general question about life, greetings, or casual conversation\n"
                    "     * It's any kind of generated question or nice chat\n\n"
                    "4. role: \n"
                    "   - Choose the best expert to answer the question.\n"
                    "   - For example: 'Senior C++ Engineer', 'iOS Development Expert', 'AI Ethics Specialist', etc.\n"
                    "   - Be specific and pick a role that fits the question.\n"
                    "   - If we need more than one expert, list the main one first.\n"
                    "   - For general questions or chat, use 'Conversational AI' or a relevant general expert.\n\n"
                    "5. confidence: \n"
                    "   - How sure are we that we understand and can answer the question?\n"
                    "   - Use a scale from 1 to 5, where 1 means not sure and 5 means very sure.\n\n"
                    "Use this exact JSON format:\n"
                    "{\n"
                    '    "role": "Specific Expert Title",\n'
                    '    "processed_prompt": "Clear, short English version of the question",\n'
                    '    "original_prompt_language": "Language we found or user asked for",\n'
                    '    "pipeline": "1 or 2",\n'
                    '    "confidence": 1-5\n'
                    "}\n\n"
                    "Make sure the JSON is correct. Don't add any extra words outside the JSON."
                )
            },
            {
                "role": "user",
                "content": f"User prompt:\n{user_prompt}\n\nDetailed project structure:\n{tree}"
            }
        ]

        if file_attachments:
            messages[-1]["content"] += f"\n\nAttached files:\n{file_attachments}"

        if focused_files:
            messages[-1]["content"] += f"\n\nFocused files:\n{focused_files}"

        try:
            logger.debug("\n #### The `ExplainablePrePromptAgent` is initiating:\n A request to the AI for pre-prompt planning")
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            logger.debug("\n #### The `ExplainablePrePromptAgent` has successfully:\n Received the AI response for pre-prompt planning")
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.debug("\n #### The `ExplainablePrePromptAgent` is attempting:\n To repair a JSON decoding error in the AI response")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f" #### The `ExplainablePrePromptAgent` encountered an error:\n While getting the pre-prompt plan\n Error: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt, file_attachments, focused_files):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `ExplainablePrePromptAgent` is beginning:\n The pre-prompt planning process")
        plan = await self.get_prePrompt_plan(user_prompt, file_attachments, focused_files)
        logger.debug("\n #### The `ExplainablePrePromptAgent` has finished:\n The pre-prompt planning process")
        return plan
