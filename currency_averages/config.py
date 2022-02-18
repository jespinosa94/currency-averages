from datetime import datetime
import logging
import yaml
import orchestrator


class Config:
    def __init__(self):
        config = self.read_config("config/config.yaml")
        self.downloads_folder = config['downloads_folder']
        self.backup_folder = config['backup_folder']
        self.test_logging = config['test_logging']
        self.enable_downloader = config['enable_downloader']
        self.enable_remove_files = config['enable_remove_files']
        self.output_folder = config['output_folder']
        self.configure_logging()

    @staticmethod
    def read_config(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def configure_logging(self):
        """
            1. Debug - detailed information when diagnosing problems
            2. Info - confirmation that things are working as expected
            3. Warning - something unexpected happened
            4. Error - software has not been able to perform some function
            5. Critical - program is unable to continue running
            """
        # create logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # create file handler and set level to debug
        log_file = "test" if self.test_logging else datetime.now().strftime("%Y-%m-%d %H%M%S")
        orchestrator.Orchestrator.check_folder_exists("logs")
        file_handler = logging.FileHandler('logs/' + log_file + '.log', 'w', encoding='utf-8', )
        file_handler.setLevel(logging.DEBUG)

        # create formatter
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        logger.addHandler(file_handler)

        logging.info("Starting project CURRENCY AVERAGES")
