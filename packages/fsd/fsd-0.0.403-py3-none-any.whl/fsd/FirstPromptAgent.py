import os
import sys
import json
from json_repair import repair_json
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = get_logger(__name__)

class FirstPromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.ai = AIGateway()

    async def get_prePrompt_plans(self, user_prompt):
        """
        Get development plans based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        try:
            logger.info("#### Hi there! The `Receptionist Agent` is processing your request.")
            messages = self._create_messages(user_prompt)
            response = await self.ai.prompt(messages, 4096, 0, 0)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"#### The `FirstPromptAgent` encountered an error during pre-prompt planning:\n{str(e)}")
            return {"reason": str(e)}

    def _create_messages(self, user_prompt):
        logger.debug("#### The `FirstPromptAgent` is constructing messages for the AI gateway")
        system_content = (
            "You are a senior developer and prompt engineering specialist. "
            "Analyze the user's prompt and respond in JSON format. Follow these guidelines strictly:\n\n"
            "pipeline: Pick one best pipeline that fits the user's prompt. "
            "Respond with a number (1, 2, 3) for the specific pipeline:\n"
            "1. Talkable: Use for general conversation, non-code related requests, or when the user wants to talk about something. "
            "This includes explanations, Q&A, any general interaction where AI can converse with people, "
            "and requests to write sample code or discuss coding topics without actually modifying a project.\n"
            "2. Actionable: Use ONLY for requests to create new code, files, or modify existing code in a real project. "
            "This includes requests to run, compile, build, fix, or write serious code for an actual project. "
            "Do NOT use this for non-code-related tasks or sample code requests.\n"
            '{"pipeline": "1 or 2"}\n'
            "Return only a valid JSON response without additional text or symbols or MARKDOWN."
        )
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"User original prompt:\n{user_prompt}"}
        ]

    def _parse_response(self, response):
        logger.debug("#### The `FirstPromptAgent` is parsing the AI gateway response")
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.error("#### The `Receptionist Agent` encountered an error and is attempting to repair.")
            logger.debug(f"DAMAGE RESPOND: {response.choices[0].message.content}")
            repaired_json = repair_json(response.choices[0].message.content)
            return json.loads(repaired_json)
