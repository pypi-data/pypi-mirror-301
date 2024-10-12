import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class CrawlerTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_crawl_plan(self, prompt):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `CrawlerTaskPlanner` agent is initiating the crawl plan generation process")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a visionary principal-level engineer tasked with creating an innovative, focused, and highly detailed step-by-step development plan. Your goal is to analyze the user's instruction and determine if any web crawling is required. If crawling is needed, provide a JSON response with the necessary details for each crawling task. If no crawling is required, return an empty JSON.\n\n"
                    "For each crawling task, provide:\n"
                    "- crawl_url: The URL to crawl.\n"
                    "- crawl_format: 'HTML' or 'Markdown'.\n"
                    "  - Request HTML format if we need to understand the webpage code structure (e.g., for building a scraper tool or performing structural analysis) - less common.\n"
                    "  - Request Markdown format if we only need the content for context, documentation, or general reading purposes - most common.\n\n"
                    "Respond with a valid JSON in this format without additional text or symbols or MARKDOWN:\n"
                    "{\n"
                    '    "crawl_tasks": [\n'
                    '        {\n'
                    '            "crawl_url": "",\n'
                    '            "crawl_format": ""\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "If no crawling is needed, return an empty JSON: {}\n"
                    "Provide only the JSON response without additional text or Markdown symbols. Each website that needs to be crawled should be a separate entry in the 'crawl_tasks' array."
                )
            },
            {
                "role": "user",
                "content": f"Analyze this prompt and determine if any web crawling is required. If yes, provide the crawling details in JSON format. If no crawling is needed, return an empty JSON:\n{prompt}\n"
            }
        ]

        try:
            logger.debug("\n #### The `CrawlerTaskPlanner` agent is sending a request to the AI Gateway")
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `CrawlerTaskPlanner` agent has successfully parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### The `CrawlerTaskPlanner` agent encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `CrawlerTaskPlanner` agent has successfully repaired and parsed the JSON")
            return plan_json
        except Exception as e:
            logger.error(f" #### The `CrawlerTaskPlanner` agent failed to get task plan: {e}")
            return {"reason": str(e)}

    async def get_crawl_plans(self, prompt):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `CrawlerTaskPlanner` agent is beginning to retrieve crawl plans")
        plan = await self.get_crawl_plan(prompt)
        logger.debug("\n #### The `CrawlerTaskPlanner` agent has successfully retrieved crawl plans")
        return plan
