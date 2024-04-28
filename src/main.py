from robocorp.tasks import task

# Custom packages
#from modules.functions import establish_driver, get_url, download_file, submit_form
import modules.functions as f
@task
def main():
    driver = f.establish_driver()
    f.get_url(driver)
    df = f.download_file(driver)
    f.submit_form(driver, df)


if __name__ == "__main__":
    main()
