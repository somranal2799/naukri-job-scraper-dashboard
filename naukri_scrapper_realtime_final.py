from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

def scrape_naukri_jobs(role, location, pages=5, save_with_timestamp=True):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")  # run in background
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    service = Service(r"C:\Users\somra\Downloads\Naukri Scrapper\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_jobs = []

    for page in range(pages):
        start = page * 20
        url = f"https://www.naukri.com/{role.replace(' ', '-')}-jobs-in-{location.lower()}-{start}"
        print(f"\n🔎 Scraping Page {page + 1}: {url}")
        driver.get(url)
        time.sleep(2)

        try:
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.jobTuple, div.srp-jobtuple-wrapper")))

            jobs = driver.find_elements(By.CSS_SELECTOR, "article.jobTuple, div.srp-jobtuple-wrapper")
            print(f"✅ Found {len(jobs)} jobs")

            for job in jobs:
                try:
                    title = job.find_element(By.CSS_SELECTOR, "a.title").text.strip()
                    link = job.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
                    company = job.find_element(By.CSS_SELECTOR, "a.comp-name").text.strip()

                    location = job.find_element(By.CSS_SELECTOR, "span.locWdth").text.strip() if job.find_elements(By.CSS_SELECTOR, "span.locWdth") else "Not mentioned"
                    experience = job.find_element(By.CSS_SELECTOR, "span.expwdth").text.strip() if job.find_elements(By.CSS_SELECTOR, "span.expwdth") else "Not mentioned"
                    desc = job.find_element(By.CSS_SELECTOR, "span.job-desc").text.strip() if job.find_elements(By.CSS_SELECTOR, "span.job-desc") else "No description"
                    posted = job.find_element(By.CSS_SELECTOR, "span.job-post-day").text.strip() if job.find_elements(By.CSS_SELECTOR, "span.job-post-day") else "N/A"

                    tags_elements = job.find_elements(By.CSS_SELECTOR, "ul.tags-gt li")
                    tags = ', '.join([tag.text for tag in tags_elements]) if tags_elements else "N/A"

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
            break  # stop scraping further if page failed

    driver.quit()

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        if save_with_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"naukri_jobs_{timestamp}.csv"
        else:
            filename = "naukri_data_analyst_jobs.csv"

        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✅ Saved {len(all_jobs)} job listings to '{filename}'")
    else:
        print("❌ No jobs extracted.")

# Run once now
scrape_naukri_jobs("data analyst", "india", pages=10, save_with_timestamp=True)
