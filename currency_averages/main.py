import web_extractor as we
import toolkit


config = toolkit.read_config("config/config.yaml")
toolkit.remove_files_from(config['downloads_folder'])

# web_extractor = we.WebExtractor()

# web_extractor.open_explorer()
# web_extractor.click_cookies_button()
# web_extractor.extract_historical_data("USD")