import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BRAVE_PATH = "/home/josecaban/.local/share/flatpak/app/com.brave.Browser/x86_64/stable/a0f739dbb810d7fbd3f77cea498fa7111cb6a2c1422544c6aad77c5d9e8ea4c3/files/brave/brave"
DRIVER_PATH = "/usr/local/bin/chromedriver"


def load_config():
    with open("config.json") as f:
        return json.load(f)


def get_driver():
    options = Options()
    options.binary_location = BRAVE_PATH
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(service=Service(DRIVER_PATH), options=options)


def login(driver, email, password):
    driver.get("https://www.upwork.com/login")
    wait = WebDriverWait(driver, 15)

    email_field = wait.until(EC.presence_of_element_located((By.ID, "login_username")))
    email_field.send_keys(email)
    driver.find_element(By.ID, "login_password_continue").click()

    time.sleep(4)

    password_field = wait.until(EC.element_to_be_clickable((By.ID, "login_password")))
    password_field.send_keys(password)
    driver.find_element(By.ID, "login_control_continue").click()

    time.sleep(3)
    print(f"Logged in. Current URL: {driver.current_url}")


def collect_jobs(driver, keywords):
    query = "+".join(keywords[:3])
    url = f"https://www.upwork.com/nx/search/jobs/?q={query}&sort=recency"
    driver.get(url)
    time.sleep(3)

    job_links = []
    cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/jobs/']")
    for card in cards[:10]:
        href = card.get_attribute("href")
        if href and "/jobs/" in href and href not in job_links:
            job_links.append(href)

    print(f"Found {len(job_links)} job links")
    return job_links


def scrape_job(driver, url):
    driver.get(url)
    time.sleep(2)

    try:
        title = driver.find_element(By.CSS_SELECTOR, "h1").text
    except:
        title = "Unknown"

    try:
        description = driver.find_element(By.CSS_SELECTOR, "[data-test='description']").text
    except:
        description = ""

    return {
        "title": title,
        "company": "Upwork",
        "location": "Remote",
        "description": description[:500],
        "url": url,
        "date_posted": time.strftime("%Y-%m-%d")
    }


def save_jobs(jobs):
    import os
    os.makedirs("data", exist_ok=True)
    path = f"data/jobs_{time.strftime('%Y-%m-%d')}.json"
    with open(path, "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"Saved {len(jobs)} jobs to {path}")
    return path


def main():
    print("Starting collector...")
    config = load_config()
    email = config["upwork"]["email"]
    password = config["upwork"]["password"]
    keywords = config["keywords"]

    driver = get_driver()

    try:
        login(driver, email, password)
        links = collect_jobs(driver, keywords)

        jobs = []
        for link in links:
            job = scrape_job(driver, link)
            print(f"Scraped: {job['title']}")
            jobs.append(job)
            time.sleep(2)

        save_jobs(jobs)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()