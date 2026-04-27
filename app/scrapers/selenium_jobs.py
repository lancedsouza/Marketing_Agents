import pandas as pd
import time
import random
import os
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_linkedin_v16_hybrid():
    # --- 📂 DYNAMIC FILE SETUP ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    excel_file = os.path.join(current_dir, f"linkedin_fintech_full_{timestamp}.xlsx")
    csv_file = os.path.join(current_dir, f"linkedin_fintech_full_{timestamp}.csv")
    
    opts = Options()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # Update this if you have version mismatch (e.g., driver = webdriver.Chrome(options=opts))
    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 15)
    all_leads = []

    try:
        # STEP 1: LOGIN
        driver.get('https://www.linkedin.com/login')
        print("\n--- 🛑 ACTION REQUIRED ---")
        print("1. Log in manually.")
        input("👉 Once you see your Home Feed, press ENTER here...")

        # STEP 2: SEARCH
        search_url = "https://www.linkedin.com/jobs/search/?keywords=startups%2Bfintech&location=Mumbai"
        driver.get(search_url)
        time.sleep(5)

        for page in range(1, 11): # Adjust page count as needed
            print(f"📄 Processing Page {page}...")
            
            # --- SIDEBAR SCROLL (Your V4 Logic) ---
            try:
                sidebar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list, .scaffold-layout__list")))
                for i in range(1, 10):
                    driver.execute_script(f"arguments[0].scrollTop = {i * 600};", sidebar)
                    time.sleep(0.4)
                driver.execute_script("arguments[0].scrollTop = 0;", sidebar)
            except:
                print("⚠️ Sidebar scroll failed, trying visible area...")

            # --- CARD DETECTION (Your V4 Selectors) ---
            job_cards = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item, .job-card-container")
            
            for card in job_cards:
                try:
                    # 1. POSITION & URL (Grabbed directly from the card using your V4 logic)
                    position = card.find_element(By.CSS_SELECTOR, "strong, h3, .job-card-list__title").text.strip()
                    job_url = card.find_element(By.TAG_NAME, "a").get_attribute("href").split('?')[0]
                    
                    # 2. CLICK TO LOAD RIGHT PANE
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                    time.sleep(0.5)
                    card.click()
                    time.sleep(random.uniform(2, 3.5))

                    # 3. EXTRACTION FROM RIGHT PANE (New Fields)
                    detail_pane = driver.find_element(By.CLASS_NAME, "jobs-search__job-details--container")
                    
                    # Company Name
                    company = detail_pane.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__company-name").text.strip()
                    
                    # Salary (Looking for INR or $)
                    try:
                        salary = detail_pane.find_element(By.XPATH, ".//span[contains(text(), 'INR') or contains(text(), '$') or contains(text(), '/yr')]").text.strip()
                    except: salary = "Not Disclosed"

                    # Work Type (On-site / Remote / Hybrid)
                    try:
                        work_type = detail_pane.find_element(By.XPATH, ".//span[contains(text(), 'On-site') or contains(text(), 'Remote') or contains(text(), 'Hybrid')]").text.strip()
                    except: work_type = "Not Listed"

                    # Employees
                    try:
                        emp_text = detail_pane.find_element(By.XPATH, ".//*[contains(text(), 'employees')]").text.strip()
                        employees = emp_text.split('·')[-1].strip() if '·' in emp_text else emp_text
                    except: employees = "Not Listed"

                    # Posted Date
                    try:
                        posted = detail_pane.find_element(By.XPATH, ".//span[contains(text(), 'ago') or contains(text(), 'Posted')]").text.strip()
                    except: posted = "Unknown"

                    # Location
                    try:
                        location = detail_pane.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__bullet, .app-indicator__caption--secondary").text.strip()
                    except: location = "Mumbai"

                    all_leads.append({
                        "Company": company.split('\n')[0],
                        "Position": position,
                        "Salary": salary,
                        "Work Type": work_type,
                        "Employees": employees,
                        "Location": location,
                        "Posted": posted,
                        "URL": job_url
                    })
                    print(f"✅ [{len(all_leads)}] {company} | {position}")

                except Exception as e:
                    continue
            
            # --- LIVE SAVE (Prevents data loss) ---
            if all_leads:
                pd.DataFrame(all_leads).to_excel(excel_file, index=False)

            # --- PAGINATION ---
            try:
                next_btn = driver.find_element(By.XPATH, f"//button[@aria-label='Page {page + 1}']")
                driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(random.uniform(5, 7))
            except:
                break

    except Exception as e:
        print(f"🚨 Error: {e}")
    finally:
        if all_leads:
            df = pd.DataFrame(all_leads)
            df.to_excel(excel_file, index=False)
            df.to_csv(csv_file, index=False)
            print(f"\n🎯 SUCCESS! Total Leads: {len(all_leads)}")
            print(f"📂 Saved to: {excel_file}")
        driver.quit()

if __name__ == "__main__":
    scrape_linkedin_v16_hybrid()