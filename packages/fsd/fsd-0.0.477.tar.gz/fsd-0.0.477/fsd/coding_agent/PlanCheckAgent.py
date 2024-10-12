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

class PlanCheckAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_idea_check_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = self.repo.print_summarize_with_tree()
        messages = [
            {
                "role": "system",
                "content": (
                    f"As an expert analyst, carefully examine the user request and provided context to determine the appropriate plan. Consider the following detailed criteria:\n\n"
                    f"Plan 1 is for comprehensive work that requires a clear, step-by-step approach. Examples include:\n"
                    f"- Building a new feature (e.g., implementing a user authentication system)\n"
                    f"- Creating a new module (e.g., developing a data processing pipeline)\n"
                    f"- Large-scale setup (e.g., initializing a new microservices architecture)\n"
                    f"- Refactoring a significant portion of the codebase\n"
                    f"- Implementing a new database schema and related ORM models\n"
                    f"- Setting up a CI/CD pipeline from scratch\n\n"
                    f"Plan 2 is for specific, well-defined tasks that don't require extensive planning. Examples include:\n"
                    f"- Changing a UI element's color\n"
                    f"- Updating a configuration file with new parameters\n"
                    f"- Fixing a known bug with a clear solution\n"
                    f"- Adding a new field to an existing database table\n"
                    f"- Updating dependencies in a project file\n"
                    f"- Modifying a specific function to handle an edge case\n\n"
                    f"Analyze the project structure, file summaries, and user prompt to make your decision. Consider factors such as the scope of changes, number of files affected, and complexity of the task.\n\n"
                    f"Based on your expert analysis, respond with either '1' or '2' in this exact JSON format:\n"
                    f"{{\n"
                    f'    "result": "1" or "2"\n'
                    f"}}\n\n"
                    f"Project structure and file summaries:\n{all_file_contents}"
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        try:
            logger.debug("\n #### The `DependencyCheckAgent` is initiating a request to the AI Gateway")
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `DependencyCheckAgent` has successfully parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### The `DependencyCheckAgent` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `DependencyCheckAgent` has successfully repaired and parsed the JSON")
            return plan_json
        except Exception as e:
            logger.error(f" #### The `DependencyCheckAgent` encountered an error during the process: `{e}`")
            return {
                "reason": str(e)
            }

    async def get_idea_check_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `DependencyCheckAgent` is beginning to retrieve dependency check plans")
        plan = await self.get_idea_check_plan(user_prompt)
        logger.debug("\n #### The `DependencyCheckAgent` has successfully retrieved dependency check plans")
        return plan
