import os
import sys
import json
import asyncio

from .CodingAgent import CodingAgent
from .FormattingAgent import FormattingAgent
from .FileManagerAgent import FileManagerAgent
from .FileFinderAgent import FileFinderAgent
from .IdeaDevelopment import IdeaDevelopment
from .ShortIdeaDevelopment import ShortIdeaDevelopment
from .PrePromptAgent import PrePromptAgent
from .LanguageAgent import LanguageAgent
from .TaskPlanner import TaskPlanner
from .TaskPlannerPro import TaskPlannerPro
from .PlanCheckAgent import PlanCheckAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.ImageAgent.ImageControllerAgent import ImageControllerAgent
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.MainOperation.ProjectsRunner import ProjectsRunner
from fsd.system.FileContentManager import FileContentManager
from fsd.Crawler.CrawlerAgent import CrawlerAgent
from fsd.Crawler.CrawlerTaskPlanner import CrawlerTaskPlanner
from fsd.dependency.DependencyControllerAgent import DependencyControllerAgent
from fsd.compile.CompileControllerAgent import CompileControllerAgent
from fsd.Deployment.DeploymentControllerAgent import DeploymentControllerAgent 
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        directory_path = self.repo.get_repo_path()
        self.directory_path = directory_path
        self.idea = IdeaDevelopment(repo)
        self.short_idea = ShortIdeaDevelopment(repo)
        self.planCheckAgent = PlanCheckAgent(repo)
        self.preprompt = PrePromptAgent(repo)
        self.taskPlanner = TaskPlanner(repo)
        self.taskPlannerPro = TaskPlannerPro(repo)
        self.coder = CodingAgent(repo)
        self.project = ProjectManager(repo)
        self.image = ImageControllerAgent(repo)
        self.compile = CompileControllerAgent(repo)
        self.runner = ProjectsRunner(repo)
        self.format = FormattingAgent(repo)
        self.fileManager = FileManagerAgent(repo)
        self.fileFinder = FileFinderAgent(repo)
        self.lang = LanguageAgent(repo)
        self.deploy = DeploymentControllerAgent(repo)
        self.code_manager = FileContentManager()  # Initialize CodeManager in the constructor
        self.crawler = CrawlerAgent("fc-ce5f3e7178184ee387e17e9de608781f")
        self.crawlerPlaner = CrawlerTaskPlanner(repo)
        self.dependency = DependencyControllerAgent(repo)

    def filter_non_asset_files(self, file_set):
        # Define a set of common code file extensions
        code_extensions = {
            # Programming languages
            '.py', '.pyw',  # Python
            '.js', '.jsx', '.ts', '.tsx',  # JavaScript/TypeScript
            '.java',  # Java
            '.c', '.h', '.cpp', '.hpp', '.cc', '.cxx', '.hh', '.hxx', '.ino',  # C/C++
            '.cs',  # C#
            '.go',  # Go
            '.rb', '.rbw', '.rake', '.gemspec', '.rhtml',  # Ruby
            '.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps', '.phpt',  # PHP
            '.kt', '.kts',  # Kotlin
            '.swift',  # Swift
            '.m', '.mm',  # Objective-C
            '.r', '.rdata', '.rds', '.rda', '.rproj',  # R
            '.pl', '.pm', '.t',  # Perl
            '.sh', '.bash', '.bats', '.zsh', '.ksh', '.csh',  # Shell scripts
            '.lua',  # Lua
            '.erl', '.hrl',  # Erlang
            '.ex', '.exs',  # Elixir
            '.ml', '.mli', '.fs', '.fsi', '.fsx', '.fsscript',  # OCaml/F#
            '.scala', '.sbt', '.sc',  # Scala
            '.jl',  # Julia
            '.hs', '.lhs',  # Haskell
            '.clj', '.cljs', '.cljc', '.edn',  # Clojure
            '.groovy', '.gvy', '.gy', '.gsh',  # Groovy
            '.v', '.vh', '.sv', '.svh',  # Verilog/SystemVerilog
            '.vhd', '.vhdl',  # VHDL
            '.adb', '.ads', '.ada',  # Ada
            '.d', '.di',  # D
            '.nim', '.nims',  # Nim
            '.rs',  # Rust
            '.cr',  # Crystal
            # Markup and stylesheets
            '.html', '.htm', '.xhtml', '.jhtml',  # HTML
            '.css', '.scss', '.sass', '.less',  # CSS and preprocessors
            '.xml', '.xsl', '.xslt', '.xsd', '.dtd', '.wsdl',  # XML
            '.md', '.markdown', '.mdown', '.mkdn', '.mkd', '.rst', '.adoc', '.asciidoc',  # Markdown/AsciiDoc/ReStructuredText
            # Configuration files often edited directly
            '.json', '.yml', '.yaml', '.ini', '.cfg', '.conf', '.toml', '.plist', '.env', '.editorconfig',
            # iOS-specific
            '.nib', '.xib', '.storyboard',  # iOS
            # Android-specific
            '.gradle', '.pro', '.aidl', '.rs', '.rsh', '.xml',  # Android (note: '.rs' is Rust, so might need context-specific filtering)
            # Desktop app specific
            '.manifest', '.rc', '.resx', '.xaml', '.appxmanifest',  # App manifests and resource files
            # Web app specific
            '.asp', '.aspx', '.ejs', '.hbs', '.jsp', '.jspx', '.php', '.cfm',  # Server-side scripts
            # Database related
            '.sql',  # SQL scripts
            # Others
            '.tex', '.bib', '.txt',  # Text and documentation
            '.svg',  # Scalable Vector Graphics
        }

        # Use a set comprehension to filter files with code extensions
        code_files = {file for file in file_set if any(file.endswith(ext) for ext in code_extensions)}

        return code_files

    def is_coding_file(self, filename):
        # Define a set of common code file extensions
        code_extensions = {
            # Programming languages
            '.py', '.pyw',  # Python
            '.js', '.jsx', '.ts', '.tsx',  # JavaScript/TypeScript
            '.java',  # Java
            '.c', '.h', '.cpp', '.hpp', '.cc', '.cxx', '.hh', '.hxx', '.ino',  # C/C++
            '.cs',  # C#
            '.go',  # Go
            '.rb', '.rbw', '.rake', '.gemspec', '.rhtml',  # Ruby
            '.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps', '.phpt',  # PHP
            '.kt', '.kts',  # Kotlin
            '.swift',  # Swift
            '.m', '.mm',  # Objective-C
            '.r', '.rdata', '.rds', '.rda', '.rproj',  # R
            '.pl', '.pm', '.t',  # Perl
            '.sh', '.bash', '.bats', '.zsh', '.ksh', '.csh',  # Shell scripts
            '.lua',  # Lua
            '.erl', '.hrl',  # Erlang
            '.ex', '.exs',  # Elixir
            '.ml', '.mli', '.fs', '.fsi', '.fsx', '.fsscript',  # OCaml/F#
            '.scala', '.sbt', '.sc',  # Scala
            '.jl',  # Julia
            '.hs', '.lhs',  # Haskell
            '.clj', '.cljs', '.cljc', '.edn',  # Clojure
            '.groovy', '.gvy', '.gy', '.gsh',  # Groovy
            '.v', '.vh', '.sv', '.svh',  # Verilog/SystemVerilog
            '.vhd', '.vhdl',  # VHDL
            '.adb', '.ads', '.ada',  # Ada
            '.d', '.di',  # D
            '.nim', '.nims',  # Nim
            '.rs',  # Rust
            '.cr',  # Crystal
            # Markup and stylesheets
            '.html', '.htm', '.xhtml', '.jhtml',  # HTML
            '.css', '.scss', '.sass', '.less',  # CSS and preprocessors
            '.xml', '.xsl', '.xslt', '.xsd', '.dtd', '.wsdl',  # XML
            '.md', '.markdown', '.mdown', '.mkdn', '.mkd', '.rst', '.adoc', '.asciidoc',  # Markdown/AsciiDoc/ReStructuredText
            # Configuration files often edited directly
            '.json', '.yml', '.yaml', '.ini', '.cfg', '.conf', '.toml', '.plist', '.env', '.editorconfig',
            # iOS-specific
            '.nib', '.xib', '.storyboard',  # iOS
            # Android-specific
            '.gradle', '.pro', '.aidl', '.rs', '.rsh', '.xml',  # Android (note: '.rs' is Rust, so might need context-specific filtering)
            # Desktop app specific
            '.manifest', '.rc', '.resx', '.xaml', '.appxmanifest',  # App manifests and resource files
            # Web app specific
            '.asp', '.aspx', '.ejs', '.hbs', '.jsp', '.jspx', '.php', '.cfm',  # Server-side scripts
            # Database related
            '.sql',  # SQL scripts
            # Others
            '.tex', '.bib', '.txt',  # Text and documentation
            '.svg',  # Scalable Vector Graphics
        }

        # Check if the file has a code extension
        return any(filename.endswith(ext) for ext in code_extensions)

    async def get_prompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.prompt.get_prompt_plans(user_prompt)

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)

    async def get_taskPlanner(self, instruction, file_lists, original_prompt_language):
        """Generate idea plans based on user prompt and available files."""
        return await self.taskPlanner.get_task_plans(instruction, file_lists, original_prompt_language)
    
    async def get_taskPlanner_pro(self, instruction, file_lists, original_prompt_language):
        """Generate idea plans based on user prompt and available files."""
        return await self.taskPlannerPro.get_task_plans(instruction, file_lists, original_prompt_language)

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        """Generate idea plans based on user prompt and available files."""
        return await self.idea.get_idea_plans(user_prompt, original_prompt_language)

    async def get_lightIdea_plans(self, user_prompt, original_prompt_language):
        """Generate idea plans based on user prompt and available files."""
        return await self.short_idea.get_idea_plans(user_prompt, original_prompt_language)

    async def get_bugs_plans(self, files, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.bug_scanner.get_idea_plans(files, user_prompt)

    async def get_long_idea_plans(self, files, user_prompt, is_first):
        """Generate idea plans based on user prompt and available files."""
        return await self.long.get_idea_plans(files, user_prompt, is_first)

    async def get_file_planning(self, idea_plan):
        """Generate file planning based on idea plan and directory tree."""
        return await self.fileManager.get_file_plannings(idea_plan)

    async def get_adding_file_planning(self, idea_plan, tree):
        """Generate file planning for adding new files based on idea plan and directory tree."""
        return await self.fileManager.get_adding_file_plannings(idea_plan, tree)

    async def get_moving_file_planning(self, idea_plan, tree):
        """Generate file planning for adding new files based on idea plan and directory tree."""
        return await self.fileManager.get_moving_file_plannings(idea_plan, tree)

    async def get_formatting_files(self, prompt):
        """Generate formatting plans based on user prompt and directory tree."""
        return await self.fileFinder.get_file_plannings(prompt)

    async def run_requests(self, request_list, role, original_prompt_language):
        """Run project requests."""
        return await self.runner.run_project(request_list, role, original_prompt_language)

    async def process_creation(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_creating'):
            processes = data.get('Adding_new_files', [])
            await self.project.execute_files_creation(processes)

    async def process_moving(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_moving'):
            processes = data.get('Moving_new_files', [])
            await self.project.execute_files_creation(processes)

    async def build_existing_context(self, existing_files):
        """Build and return the context of existing files."""
        all_context = ""
        for path in existing_files:
            file_context = read_file_content(path)
            if file_context:
                all_context += f"\n\nFile: {path}:\n{file_context}"

        return all_context

    async def get_coding_requests(self, instructions, context, file_lists, context_files, role, crawl_logs, original_prompt_language):
        """Generate coding requests based on instructions and context."""
        self.coder.initial_setup(context_files, instructions, context, crawl_logs)

        logger.info("#### The `Task Planner` is preparing the task.")
        plan = await self.get_taskPlanner(instructions, file_lists, original_prompt_language)
        logger.info("-------------------------------------------------")
        logger.info("#### The `Coding Agent` is starting the coding phase.")
        is_first = True
        for step in plan.get('steps', []):
            file_name = step.get('file_name')
            if self.is_coding_file(file_name):
                main_path = file_name
                if main_path:
                    techStack = step.get('techStack')
                    prompt = ""

                    logger.info("-------------------------------------------------")
                    logger.info(f"#### The `{techStack.upper()} Agent` is processing file: `{os.path.basename(file_name)}`.")

                    try:
                        result = await self.coder.get_coding_requests(file_name, techStack, prompt)

                        await self.code_manager.handle_coding_agent_response(main_path, result)

                        logger.info(f"\n #### `{techStack.upper()} Agent` finished successfully: `{os.path.basename(file_name)}`.")
                        is_first = False
                    except Exception as e:
                        logger.error(f" #### Error processing file `{file_name}`: {str(e)}")
                else:
                    logger.debug(f" #### File not found: `{file_name}`")


    async def get_pro_coding_requests(self, instructions, context, file_lists, context_files, role, crawl_logs, original_prompt_language):
        """Generate coding requests based on instructions and context."""
        self.coder.initial_setup(context_files, instructions, context, crawl_logs)

        logger.info("#### The `Task Planner Pro` is preparing the task.")
        plan = await self.get_taskPlanner_pro(instructions, file_lists, original_prompt_language)
        logger.info("-------------------------------------------------")
        logger.info("#### The `Coding Agent Pro` is starting the coding phase in supercharged mode.")

        for group in plan.get('groups', []):
            group_name = group.get('group_name')
            tasks = group.get('tasks', [])
            logger.info(f"#### Processing group: {group_name}")

            async def process_task(task):
                file_name = task.get('file_name')
                if self.is_coding_file(file_name):
                    main_path = file_name
                    if main_path:
                        techStack = task.get('techStack')
                        prompt = ""

                        logger.info(f"#### The `{techStack.upper()} Agent` is processing file: `{os.path.basename(file_name)}`.")

                        try:
                            result = await self.coder.get_coding_requests(file_name, techStack, prompt)
                            await self.code_manager.handle_coding_agent_response(main_path, result)
                            logger.info(f"\n #### `{techStack.upper()} Agent` finished successfully: `{os.path.basename(file_name)}`.")
                        except Exception as e:
                            logger.error(f" #### Error processing file `{file_name}`: {str(e)}")
                    else:
                        logger.debug(f" #### File not found: `{file_name}`")

            # Execute tasks in the group concurrently
            await asyncio.gather(*[process_task(task) for task in tasks])
            logger.info(f"#### Completed group: {group_name}")
            logger.info("-------------------------------------------------")

    async def replace_all_code_in_file(self, file_path, new_code_snippet):
        """Replace the entire content of a file with the new code snippet."""
        try:
            with open(file_path, 'w') as file:
                file.write(new_code_snippet)
            logger.debug(f" #### The codes have been successfully written in... `{file_path}`.")
        except Exception as e:
            logger.error(f" #### Error writing code. Error: {e}")

    async def replace_all_code_in_file(self, file_path, new_code_snippet):
        """Replace the entire content of a file with the new code snippet."""
        try:
            with open(file_path, 'w') as file:
                file.write(new_code_snippet)
            logger.debug(f" #### The codes have been successfully written in... `{file_path}`.")
        except Exception as e:
            logger.error(f" #### Error writing code. Error: {e}")


    async def build_and_fix_compile_error(self, file_list, role, original_prompt_language):
        """Build project and fix compile errors."""
        await self.run_requests(file_list, role, original_prompt_language)


    async def fix_compile_error_pipeline(self,file_list, role, original_prompt_language):
        """Pipeline for fixing compile errors."""
        logger.info("-------------------------------------------------")
        await self.build_and_fix_compile_error(file_list, role, original_prompt_language)
        logger.info("-------------------------------------------------")


    async def add_files_folders_pipeline(self, finalPrompt, role):
        """Pipeline for adding files and folders."""
        logger.info("-------------------------------------------------")
        logger.debug(" #### Initiating add_files_folders_pipeline")
        logger.info(" #### The `File Manager Agent` is processing files.")
        file_result = await self.get_adding_file_planning(finalPrompt, self.repo.print_tree())
        await self.process_creation(file_result)
        files = []
        if file_result.get('Is_creating'):
            processes = file_result.get('Adding_new_files', [])
            for process in processes:
                file_name = process['Parameters']['file_name']
                files.append(file_name)
        files = [file for file in files if file]
        logger.info("-------------------------------------------------")

    async def move_files_folders_pipeline(self, finalPrompt, role):
        """Pipeline for adding files and folders."""
        logger.info("-------------------------------------------------")
        logger.debug("\n #### Initiating move_files_folders_pipeline")
        logger.info(" #### The `file manager agent` is processing files.")
        file_result = await self.get_moving_file_planning(finalPrompt, self.repo.print_tree())
        logger.debug(file_result)
        await self.process_moving(file_result)
        logger.info("-------------------------------------------------")


    async def regular_code_task_pipeline(self, tier, finalPrompt, role, original_prompt_language):
        """Pipeline for regular coding tasks."""
        logger.info("-------------------------------------------------")
        logger.debug("\n #### Initiating regular_code_task_pipeline")

        result_check = await self.planCheckAgent.get_idea_check_plans(finalPrompt)

        isLight = True

        if result_check.get('result') == '1':
            isLight = False
        elif result_check.get('result') == '2':
            isLight = True
        else:
            isLight = True

        crawl_plan = await self.crawlerPlaner.get_crawl_plans(finalPrompt)
        crawl_logs = []
        if crawl_plan:
            for step in crawl_plan.get('crawl_tasks', []):
                crawl_url = step.get('crawl_url')
                crawl_format = step.get('crawl_format')
                if crawl_url:
                    logger.info(f" #### The `Crawler Agent` is reading: `{crawl_url}`")
                    result = self.crawler.process(crawl_url, crawl_format)
                    logger.info(f" #### The `Crawler Agent` has finished reading: `{crawl_url}`")
                    crawl_logs.append({
                        'url': crawl_url,
                        'result': result
                    })

        if isLight:
            self.short_idea.initial_setup(role, crawl_logs)
        else:
            self.idea.initial_setup(role, crawl_logs)

        if isLight:
            logger.info(" #### The `Planner Agent` is creating an initial development plan.")
        else:
            logger.info(" #### The `Planner Agent Pro` is creating an initial development plan.")

        if crawl_logs:
            if isLight:
                idea_plan = await self.get_lightIdea_plans(finalPrompt + f"crawled data: {crawl_logs}", original_prompt_language)
            else:
                idea_plan = await self.get_idea_plans(finalPrompt + f"crawled data: {crawl_logs}", original_prompt_language)
        else:
            if isLight:
                idea_plan = await self.get_lightIdea_plans(finalPrompt, original_prompt_language)
            else:
                idea_plan = await self.get_idea_plans(finalPrompt, original_prompt_language)

        while True:
            if isLight:
                logger.info(" #### The `Planner Agent` is requesting feedback. Click `Approve` if you feel satisfied, click `Skip` to end this process, or type your feedback below.")
            else:
                logger.info(" #### The `Planner Agent Pro` is requesting feedback. Click `Approve` if you feel satisfied, click `Skip` to end this process, or type your feedback below.")

            logger.info(" ### Press a or Approve to execute this step, or Enter to skip: ")

            user_prompt_json = input()
            user_prompt, _ = parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == 's':
                if isLight:
                    logger.info(" #### The `Planner Agent` has detected that the run/compile process has been skipped.")
                else:
                    logger.info(" #### The `Planner Agent Pro` has detected that the run/compile process has been skipped.")
                logger.info("-------------------------------------------------")
                return

            if user_prompt == "a":
                break
            else:
                logger.info(" #### The `Planner Agent` is updating the development plan.")
                eng_prompt = await self.lang.get_language_plans(user_prompt, role)
                finalPrompt = finalPrompt + " " + eng_prompt
                self.idea.remove_latest_conversation()
                if crawl_logs:
                    if isLight:
                        idea_plan = await self.get_lightIdea_plans(finalPrompt + f"crawled data: {crawl_logs}", original_prompt_language)
                    else:
                        idea_plan = await self.get_idea_plans(finalPrompt + f"crawled data: {crawl_logs}", original_prompt_language)
                else:
                    if isLight:
                        idea_plan = await self.get_lightIdea_plans(finalPrompt, original_prompt_language)
                    else:
                        idea_plan = await self.get_idea_plans(finalPrompt, original_prompt_language)

        self.idea.clear_conversation_history()
        logger.info(" #### The `File Manager Agent` is processing files.")
        file_result = await self.get_file_planning(idea_plan)
        await self.process_creation(file_result)
        logger.debug("\n #### The `File Manager Agent` has completed processing files.")
        logger.info("-------------------------------------------------")
        logger.info(" #### The `Dependency Agent` is performing dependency checks.")
        await self.dependency.get_started_coding_pipeline(idea_plan, original_prompt_language)
        logger.info(" #### The `Dependency Agent` has finished with dependency checks.")
        logger.info("-------------------------------------------------")
        existing_files = file_result.get('Existing_files', [])
        new_adding_files = []
        context_files = file_result.get('Context_files', [])
        adding_new_files = file_result.get('Adding_new_files', [])
        if adding_new_files:
            for item in adding_new_files:
                file_info = item['Parameters']
                full_path = file_info['full_path']
                new_adding_files.append(full_path)

        final_working_files = set()
        final_working_files.update(existing_files)
        final_working_files.update(new_adding_files)
        final_working_files = self.filter_non_asset_files(final_working_files)
        all_context = await self.build_existing_context(list(final_working_files))

        if tier == "Pro":
            await self.get_pro_coding_requests(idea_plan, all_context, list(final_working_files), context_files, role, crawl_logs, original_prompt_language)
        else:
            await self.get_coding_requests(idea_plan, all_context, list(final_working_files), context_files, role, crawl_logs, original_prompt_language)

        await self.image.get_started_image_generation(tier, idea_plan, original_prompt_language)
        """
        current_commit = self.repo.get_commit() + " - coding process done"
        self.repo.add_all_files(current_commit)
        """

        await self.build_and_fix_compile_error(final_working_files, role, original_prompt_language)

        logger.info(" #### The `Coding Agent` has completed the coding phase.")
        logger.info("-------------------------------------------------")


    async def get_started(self, user_prompt, tier):
        """Process the user prompt."""
        logger.info("-------------------------------------------------")
        logger.info(" #### The `Director Action Agent` will now begin processing your request.")

        prePrompt = await self.get_prePrompt(user_prompt)
        role = prePrompt['role']
        finalPrompt = prePrompt['processed_prompt']
        pipeline = prePrompt['pipeline']
        original_prompt_language = prePrompt['original_prompt_language']

        if pipeline in ["1", 1]:
            await self.fix_compile_error_pipeline([], role, original_prompt_language)
        elif pipeline in ["2", 2]:
            await self.add_files_folders_pipeline(finalPrompt, role)
        elif pipeline in ["3", 3]:
            await self.move_files_folders_pipeline(finalPrompt, role)
        elif pipeline in ["4", 4]:
            await self.regular_code_task_pipeline(tier, finalPrompt, role, original_prompt_language)
        elif pipeline in ["7", 7]:
            await self.deploy.get_started_deploy_pipeline()
        elif pipeline in ["5", 5, "6", 6, "8", 8]:
            if tier == "Pro":
                if pipeline in ["5", 5]:
                    await self.dependency.get_started(finalPrompt, original_prompt_language)
                elif pipeline in ["6", 6]:
                    await self.compile.get_started(finalPrompt, [], original_prompt_language)
                elif pipeline in ["8", 8]:
                    await self.image.get_started(tier, user_prompt, original_prompt_language)
            else:
                logger.info(f"#### Pro Tier required. Upgrade [HERE](https://dashboard.zinley.com/)!")
        else:
            logger.info(prePrompt)

        logger.info("#### `Director Action Agent` completed all tasks.")
        logger.info("-------------------------------------------------")
