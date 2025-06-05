from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_naukri_jobs(role, location, pages=3):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    service = Service(r"C:\Users\somra\Downloads\Naukri Scrapper\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_jobs = []

    for page in range(pages):
        start = page * 20
        url = f"https://www.naukri.com/{role.replace(' ', '-')}-jobs-in-{location.lower()}-{start}"
        print(f"\n🔎 Scraping Page {page + 1}: {url}")
        driver.get(url)
        time.sleep(3)  # Let the page load

        try:
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.srp-jobtuple-wrapper")))

            jobs = driver.find_elements(By.CSS_SELECTOR, "div.srp-jobtuple-wrapper")
            print(f"✅ Found {len(jobs)} jobs")

            for job in jobs:
                try:
                    title = job.find_element(By.CSS_SELECTOR, "a.title").text.strip()
                    link = job.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
                    company = job.find_element(By.CSS_SELECTOR, "a.comp-name").text.strip()

                    # Location
                    try:
                        location = job.find_element(By.CSS_SELECTOR, "span.locWdth").text.strip()
                    except:
                        location = "Not mentioned"

                    # Experience
                    try:
                        experience = job.find_element(By.CSS_SELECTOR, "span.expwdth").text.strip()
                    except:
                        experience = "Not mentioned"

                    # Description
                    try:
                        desc = job.find_element(By.CSS_SELECTOR, "span.job-desc").text.strip()
                    except:
                        desc = "No description"

                    # Tags
                    try:
                        tags_elements = job.find_elements(By.CSS_SELECTOR, "ul.tags-gt li")
                        tags = ', '.join([tag.text for tag in tags_elements])
                    except:
                        tags = "N/A"

                    # Posted
                    try:
                        posted = job.find_element(By.CSS_SELECTOR, "span.job-post-day").text.strip()
                    except:
                        posted = "N/A"

                    all_jobs.append({
                        "Title": title,
                        "Company": company,
                        "Location": location,
                        "Experience": experience,
                        "Description": desc,
                        "Skills": tags,
                        "Posted": posted,
                        "Job URL": link
                    })

                except Exception as e:
                    print("⚠️ Skipping job due to error:", e)

        except Exception as e:
            print(f"❌ Error loading job cards: {e}")

    driver.quit()

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        df.to_csv("naukri_data_analyst_jobs.csv", index=False, encoding='utf-8-sig')
        print(f"\n✅ Saved {len(all_jobs)} job listings to 'naukri_data_analyst_jobs.csv'")
    else:
        print("❌ No jobs extracted.")

scrape_naukri_jobs("data analyst", "india", pages=20)
