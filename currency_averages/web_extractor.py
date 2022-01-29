from datetime import date, timedelta
import calendar
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging


class WebExtractor:
    def __init__(self, config):
        if config.enable_downloader:
            self.driver = webdriver.Chrome('/Users/jorge/Documents/chromedriver')
        else:
            logging.info("web explorer extraction disabled")

        self.config = config

    def open_explorer(self):
        self.driver.get("https://fxtop.com/dev/submithisto.php")
    
    def close_explorer(self):
        time.sleep(5)
        self.driver.close()  
    
    def click_cookies_button(self):
        """Click cookies banner.
        This banner prevents the download element to be clickable.
        """
        cookies_button_xpath = '/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]'
        
        try:
            cookies_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, cookies_button_xpath))
            )
        except:
            print("The object can't be found, probably the dialog changed.")
        cookies_button.click()

    def extract_currency(self, currency):
        """Extracts the historical data of a currency in files of 12 months.

        Args:
            currency (string): a currency to extract data.
        """
        if not self.config.enable_downloader:
            return

        self.open_explorer()
        self.click_cookies_button()
        
        # Select month average.
        self.driver.find_element_by_name('MA').click()

        # Select excel output.
        excel_xpath = '/html/body/form/table/tbody/tr[13]/td[2]/input[2]'
        self.driver.find_element_by_xpath(excel_xpath).click()

        # Set download button
        button_download_xpath = '/html/body/form/table/tbody/tr[14]/td[2]/input'
        button_download = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_download_xpath))
        )

        # Source currency.
        select_source_currency = Select(self.driver.find_element_by_name('C1'))
        select_source_currency.select_by_value('EUR')

        # Target currency.
        select_target_currency = Select(self.driver.find_element_by_name('C2'))
        select_target_currency.select_by_value(currency)

        # Declare date form elements.
        form_start_day = self.driver.find_element_by_id('DD1')
        form_start_month = self.driver.find_element_by_id('MM1')
        form_start_year = self.driver.find_element_by_id('YYYY1')
        form_end_day = self.driver.find_element_by_id('DD2')
        form_end_month = self.driver.find_element_by_id('MM2')
        form_end_year = self.driver.find_element_by_id('YYYY2')

        # Dates declaration.
        today = date(date.today().year, 
                    date.today().month, 
                    calendar.monthrange(date.today().year, 
                                        date.today().month)
                    [-1])
        start_date = date(2000, 1, 1)
        end_date = date(start_date.year, 12, 31)

        # Download each year data until it reaches today.
        while start_date < today:
            form_start_day.clear()
            form_start_day.send_keys('{:02d}'.format(start_date.day))
            form_start_month.clear()
            form_start_month.send_keys('{:02d}'.format(start_date.month))
            form_start_year.clear()
            form_start_year.send_keys(start_date.year)
            
            form_end_day.clear()
            form_end_day.send_keys('{:02d}'.format(end_date.day))
            form_end_month.clear()
            form_end_month.send_keys('{:02d}'.format(end_date.month))
            form_end_year.clear()
            form_end_year.send_keys(end_date.year)
            
            start_date = end_date + timedelta(days=1)
            end_date = date(start_date.year, 12, 31)
            
            button_download.click()
            
        self.close_explorer()
        
        
    def extract_last_months(self, currencies):
        """Extracts the last 12 months of each currency.

        Args:
            currencies (list): each currency.
        """
        if not self.config.enable_downloader: return

        self.open_explorer()
        self.click_cookies_button()
        
        # Select month average.
        self.driver.find_element_by_name('MA').click()

        # Select excel output.
        excel_xpath = '/html/body/form/table/tbody/tr[13]/td[2]/input[2]'
        self.driver.find_element_by_xpath(excel_xpath).click()

        # Set download button
        button_download_xpath = '/html/body/form/table/tbody/tr[14]/td[2]/input'
        button_download = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_download_xpath))
        )

        # Source currency.
        select_source_currency = Select(self.driver.find_element_by_name('C1'))
        select_source_currency.select_by_value('EUR')
        

        # Declare date form elements.
        form_start_day = self.driver.find_element_by_id('DD1')
        form_start_month = self.driver.find_element_by_id('MM1')
        form_start_year = self.driver.find_element_by_id('YYYY1')
        form_end_day = self.driver.find_element_by_id('DD2')
        form_end_month = self.driver.find_element_by_id('MM2')
        form_end_year = self.driver.find_element_by_id('YYYY2')

        # Dates declaration.
        today = date(date.today().year, 
                    date.today().month, 
                    calendar.monthrange(date.today().year, 
                                        date.today().month)
                    [-1])
        start_date = date(today.year - 1, today.month, 1)
        end_date = today

        form_start_day.clear()
        form_start_day.send_keys('{:02d}'.format(start_date.day))
        form_start_month.clear()
        form_start_month.send_keys('{:02d}'.format(start_date.month))
        form_start_year.clear()
        form_start_year.send_keys(start_date.year)
        
        form_end_day.clear()
        form_end_day.send_keys('{:02d}'.format(end_date.day))
        form_end_month.clear()
        form_end_month.send_keys('{:02d}'.format(end_date.month))
        form_end_year.clear()
        form_end_year.send_keys(end_date.year)
        
        # Target currency and download each one
        for currency in currencies:
            select_target_currency = Select(self.driver.find_element_by_name('C2'))
            select_target_currency.select_by_value(currency)
            button_download.click()
            
        logging.info("downloaded last months of each currency")
            
        self.close_explorer()

