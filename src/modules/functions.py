# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Webdriver Manager
from webdriver_manager.chrome import ChromeDriverManager
# Other
import os
import pandas as pd


# Establish chrome driver
def establish_driver():

    # Set the WDM_LOCAL environment variable to '1' - This allows the driver to be installed locally inside the src -> .wdm folder instead of users .wdm folder on OS
    os.environ['WDM_LOCAL'] = '1'

    # Check if chromedriver is already installed and is the proper version to match current browser version, if not install it
    chrome_driver_path = ChromeDriverManager().install()

    # Specify the download directory
    download_dir = os.path.join(os.getcwd(), 'output')

    # Add chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=3")  # Suppress all log messages except fatal ones
    chrome_options.add_argument("--headless") # Run the browser in headless mode
    
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": download_dir, # Change default directory for downloads
        "download.prompt_for_download": False, # To auto download the file
        "download.directory_upgrade": True, # Chrome will use the new download directory system
        "plugins.always_open_pdf_externally": True # It will not show PDF directly in chrome
    })
    
    # Create driver object
    driver = webdriver.Chrome(service=ChromeService(chrome_driver_path), options=chrome_options)
    return driver, download_dir


# Get the URL
def get_url(driver):
    url = "https://www.rpachallenge.com" # The URL of the website to be automated
    driver.get(url) # Send GET request to the URL


# Download excel file
def download_excel_file(driver, download_dir):

    # Specify the path to the excel file
    excel_file = os.path.join(download_dir, 'challenge.xlsx')
    
    # *** REDUNDANT CODE - This code shows both ways | This would depend on client needs*** #
    #   Example: If the file only changes every 6 months, then I would not remove it every time
    
    # Delete the file if it already exists
    if os.path.exists(excel_file):
        os.remove(excel_file)

    # Only download the file if it doesn't exist
    if not os.path.exists(excel_file):
        download_url = "https://rpachallenge.com/assets/downloadFiles/challenge.xlsx"
        driver.get(download_url)
    
    return excel_file


# Submit the form
def submit_form(driver, excel_file):

    # Click the start button
    wait = WebDriverWait(driver, 10)
    start_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button")))
    start_button.click()

    # Read the excel file
    df = pd.read_excel(excel_file)
    # Remove leading and trailing whitespaces from column names
    df.columns = df.columns.str.strip()

    submission_number = 1

    for row, column in df.iterrows():
        # Reselect the form every time after submitting the form
        wait = WebDriverWait(driver, 10)
        form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'form'))) # Locate the form element on the web page
        submit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn.uiColorButton'))) # Locate the submit button on the form
        
        # Locate the input fields on the form
        first_name = form.find_element(By.XPATH, "//label[text()='First Name']/following-sibling::input")
        last_name = form.find_element(By.XPATH, "//label[text()='Last Name']/following-sibling::input")
        email = form.find_element(By.XPATH, "//label[text()='Email']/following-sibling::input")
        phone_number = form.find_element(By.XPATH, "//label[text()='Phone Number']/following-sibling::input")
        company_name = form.find_element(By.XPATH, "//label[text()='Company Name']/following-sibling::input")
        role_in_company = form.find_element(By.XPATH, "//label[text()='Role in Company']/following-sibling::input")
        address = form.find_element(By.XPATH, "//label[text()='Address']/following-sibling::input")

        # Fill in the input fields with the data from the current row
        first_name.send_keys(column['First Name'])
        last_name.send_keys(column['Last Name'])
        email.send_keys(column['Email'])
        phone_number.send_keys(column['Phone Number'])
        company_name.send_keys(column['Company Name'])
        role_in_company.send_keys(column['Role in Company'])
        address.send_keys(column['Address'])

        # Submit the form
        submit_button.click()
        #print(f"Form #{submission_number} submitted")
        submission_number += 1
    
    