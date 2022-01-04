import web_extractor as we
import currencies as cur
import toolkit


config = toolkit.Config()
currencies = cur.Currencies()

# web_extractor = we.WebExtractor()
# web_extractor.extract_historical_data("USD")
df_new_currency = toolkit.load_historical_data(config.downloads_folder)
currencies.append_currency(df_new_currency)
currencies.save_backup()

print("Finished")