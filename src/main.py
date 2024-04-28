from robocorp.tasks import task

# Custom packages
from modules.functions import establish_driver, get_url, download_excel_file, submit_form

@task
def main():
    driver = establish_driver()
    get_url(driver)
    download_excel_file(driver)
    submit_form(driver)


if __name__ == "__main__":
    main()
