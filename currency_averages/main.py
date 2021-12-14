import web_extractor as we
import toolkit


config = toolkit.Config()

# web_extractor = we.WebExtractor()
# web_extractor.extract_historical_data("USD")
toolkit.load_historical_data(config.downloads_folder)