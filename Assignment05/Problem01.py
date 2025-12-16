from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome Options
chrome_options = Options()
chrome_options.add_argument("--headless=new") 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    url = "https://www.sunbeaminfo.in/internship"
    driver.get(url)
    time.sleep(3) 

    rows = driver.find_elements(By.XPATH, "//table//tr[td]")
    
    print(f"{'Batch Name':<45} | {'Start Date'}")
    print("-" * 60)
    
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 3:
            batch_name = cols[1].text.strip()
            start_date = cols[2].text.strip()
            
            # --- PASTE THE CHECK HERE ---
            # This 'if' condition prevents printing empty rows
            if batch_name or start_date:
                print(f"{batch_name:<45} | {start_date}")

finally:
    driver.quit()