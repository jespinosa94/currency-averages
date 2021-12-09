from datetime import date, timedelta
import calendar
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

    
    
def click_cookies_button():
    """Click cookies banner.
    This banner prevents the download element to be clickable.
    """
    cookies_button_xpath = '/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]'
    
    try:
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, cookies_button_xpath))
        )
    except:
        print("The object can't be found, probably the dialog changed.")
    cookies_button.click()
    


def extract_historical_data(currency):
    """Extracts the historical data of a currency in files of 12 months.

    Args:
        currency (string): a currency to extract data.
    """
    # Select month average.
    driver.find_element_by_name('MA').click()

    # Select excel output.
    excel_xpath = '/html/body/form/table/tbody/tr[13]/td[2]/input[2]'
    driver.find_element_by_xpath(excel_xpath).click()

    # Set download button
    button_download_xpath = '/html/body/form/table/tbody/tr[14]/td[2]/input'
    button_download = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_download_xpath))
    )

    # Source currency.
    select_source_currency = Select(driver.find_element_by_name('C1'))
    select_source_currency.select_by_value('EUR')

    # Target currency.
    select_target_currency = Select(driver.find_element_by_name('C2'))
    select_target_currency.select_by_value(currency)

    # Declare date form elements.
    form_start_day = driver.find_element_by_id('DD1')
    form_start_month = driver.find_element_by_id('MM1')
    form_start_year = driver.find_element_by_id('YYYY1')
    form_end_day = driver.find_element_by_id('DD2')
    form_end_month = driver.find_element_by_id('MM2')
    form_end_year = driver.find_element_by_id('YYYY2')

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
        

    WebDriverWait(driver, 5)
    driver.close()
    
    
    
driver = webdriver.Chrome('/Users/jorge/Documents/chromedriver')
driver.get("https://fxtop.com/dev/submithisto.php")

click_cookies_button()


extract_historical_data("USD")
    
