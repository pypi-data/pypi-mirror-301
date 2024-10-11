import os
import json
import asyncio
from .ExplainablePrePromptAgent import ExplainablePrePromptAgent
from .GeneralExplainerAgent import GeneralExplainerAgent
from .ExplainableFileFinderAgent import ExplainableFileFinderAgent
from .MainExplainerAgent import MainExplainerAgent
from fsd.util import utils
import sys
import subprocess
import re
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ExplainerController:

    def __init__(self, repo):
        self.repo = repo
        self.preprompt = ExplainablePrePromptAgent(repo)
        self.normalExplainer = GeneralExplainerAgent(repo)
        self.mainExplainer = MainExplainerAgent(repo)
        self.fileFinder = ExplainableFileFinderAgent(repo)

    async def get_prePrompt(self, user_prompt, file_attachments, focused_files):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt, file_attachments, focused_files)

    async def get_normal_answer(self, user_prompt, language, role,file_attachments, focused_files):
        """Generate idea plans based on user prompt and available files."""
        return await self.normalExplainer.get_normal_answer_plans(user_prompt, language, role, file_attachments, focused_files)

    async def get_file_answer(self, user_prompt, language, files, role, file_attachments, focused_files):
        """Generate idea plans based on user prompt and available files."""
        return await self.mainExplainer.get_answer_plans(user_prompt, language, files, role, file_attachments, focused_files)

    async def get_explaining_files(self, prompt, file_attachments, focused_files):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileFinder.get_file_plannings(prompt, file_attachments, focused_files)

    async def get_started(self, user_prompt, file_attachments, focused_files):
        logger.info(" #### The `Director Support Agent` will now begin processing your request.")
        logger.info("-------------------------------------------------")

        prePrompt = await self.get_prePrompt(user_prompt, file_attachments, focused_files)
        finalPrompt = prePrompt['processed_prompt']
        pipeline = prePrompt['pipeline']
        language = prePrompt['original_prompt_language']
        role = prePrompt['role']

        if pipeline == "1" or pipeline == 1:
            logger.debug("\n #### The `File Finder Agent` is currently embarking on a quest to locate relevant files.")
            file_result = await self.get_explaining_files(finalPrompt, file_attachments, focused_files)
            working_files = file_result.get('working_files', [])
            await self.get_file_answer(finalPrompt, language, working_files, role, file_attachments, focused_files)
        elif pipeline == "2" or pipeline == 2:
            logger.debug("\n #### The `General Explainer Agent` is presently engaged in processing your query and formulating a comprehensive response.")
            await self.get_normal_answer(finalPrompt, language, role, file_attachments, focused_files)

        logger.info("\n-------------------------------------------------")
