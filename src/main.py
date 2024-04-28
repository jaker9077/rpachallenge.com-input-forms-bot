from robocorp.tasks import task
import time

# Custom packages
from modules.functions import establish_driver, get_url, download_excel_file, submit_form

@task
def main():
    # Establish driver
    driver = establish_driver()
    # Get URL
    get_url(driver)
    excel_file = download_excel_file(driver)
    submit_form(driver, excel_file)
    #time.sleep(5) # Sleep for 5 seconds to see the results

if __name__ == "__main__":
    main()
