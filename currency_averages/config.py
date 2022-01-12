from datetime import datetime
import logging
import toolkit


class Config:
    def __init__(self):
        config = toolkit.read_config("config/config.yaml")
        self.downloads_folder = config['downloads_folder']
        self.configure_logging()
        
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
        logger.setLevel(logging.DEBUG)
        
        # create file handler and set level to debug
        now = datetime.now().strftime("%Y-%m-%d %H%M%S")
        toolkit.check_folder_exists("logs")
        file_handler = logging.FileHandler('logs/'+now+'.log', 'w', encoding='utf-8', )
        file_handler.setLevel(logging.DEBUG)
        
        # create formatter
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        
        logger.addHandler(file_handler)
        
        logging.info("Starting project CURRENCY AVERAGES")