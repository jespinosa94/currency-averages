import web_extractor as we

web_extractor = we.WebExtractor()

web_extractor.open_explorer()
web_extractor.click_cookies_button()
web_extractor.extract_historical_data("USD")