from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Open a Chrome browser window controlled by Selenium
driver = webdriver.Chrome()

# Go to the Indeed UK jobs page for London
driver.get("https://uk.indeed.com/jobs?l=london")

# Wait for 15 seconds to make sure the page loads completely
time.sleep(15)

# Find all job titles on the page by looking for elements with class 'jobTitle'
job_titles = driver.find_elements(By.CLASS_NAME, 'jobTitle')

# Find all company names by class 'css-1hlukg'
company_name = driver.find_elements(By.CLASS_NAME, 'css-1hlukg')

# Find all company locations by class 'css-1restlb'
company_locations = driver.find_elements(By.CLASS_NAME, 'css-1restlb')

# Find all job URLs by locating <a> tags inside <h2> with class starting with 'jobTitle'
urls = driver.find_elements(By.XPATH, '//h2[starts-with(@class,"jobTitle")]/a')

# Loop through all jobs by pairing together job titles, companies, locations, and URLs
for job_data in zip(job_titles, company_name, company_locations, urls):
    print("--------------------")
    try:
        # Extract text from job title element
        job_name = job_data[0].text

        # Extract text from company name element
        company_name = job_data[1].text

        # Extract text from company location element
        company_location = job_data[2].text

        # Get the URL from the 'href' attribute of the <a> tag
        url = job_data[3].get_attribute('href')

        # Print the job information
        print(f"Job name: {job_name}")
        print(f"Company: {company_name}")
        print(f"Location: {company_location}")
        print(f"URL: {url}")

    except Exception as e:
        # If something goes wrong, print the error message
        print("Error extracting job data:", e)
