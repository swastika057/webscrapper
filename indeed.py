from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Set your local chromedriver path
DRIVER_PATH = r'c:\Users\S chhetri\Downloads\chromedriver\chromedriver.exe'


def init_driver(driver_path=DRIVER_PATH, headless=True):
    options = Options()
    options.headless = headless
    options.add_argument("--window-size=1920,1200")

    service = Service(driver_path)

    try:
        return webdriver.Chrome(service=service, options=options)
    except WebDriverException as e:
        print("Error initializing WebDriver:", e)
        return None


def fetch_job_elements(driver):
    print("Fetching job listings from Indeed UK...")
    driver.get("https://uk.indeed.com/jobs?q=python%20developer&l=london%22")

    # Use WebDriverWait instead of time.sleep for reliability
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'jobTitle'))
    )

    return {
        'titles': driver.find_elements(By.CLASS_NAME, 'jobTitle'),
        # The following classes might change; use more stable locators if possible
        'companies': driver.find_elements(By.CSS_SELECTOR, 'span.company_name'),
        'locations': driver.find_elements(By.CSS_SELECTOR, 'div.text_location'),
        'urls': driver.find_elements(By.XPATH, '//h2[contains(@class,"jobTitle")]/a')
    }


def extract_job_info(jobs):
    job_list = []

    for title_el, company_el, location_el, url_el in zip(
        jobs['titles'], jobs['companies'], jobs['locations'], jobs['urls']
    ):
        try:
            job = {
                'title': title_el.text.strip(),
                'company': company_el.text.strip(),
                'location': location_el.text.strip(),
                'url': url_el.get_attribute('href')
            }
            job_list.append(job)
        except Exception as e:
            print("Error extracting job data:", e)
    return job_list


def display_jobs(job_list):
    for job in job_list:
        print("--------------------")
        print(f"Job name : {job['title']}")
        print(f"Company  : {job['company']}")
        print(f"Location : {job['location']}")
        print(f"URL      : {job['url']}")


def main():
    # Set headless=False to see the browser
    driver = init_driver(headless=False)
    if not driver:
        return

    try:
        jobs = fetch_job_elements(driver)
        job_list = extract_job_info(jobs)
        display_jobs(job_list)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
