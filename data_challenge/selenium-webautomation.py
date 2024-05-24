from security.decrypter import decrypt
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

website_url = "https://mijn.sitedish.nl/"

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 7)

def login():
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')

    username.send_keys(decrypt("key.key", "vxvxvxv.txt")[0])
    password.send_keys(decrypt("key.key", "vxvxvxv.txt")[1])

    login_button = driver.find_element(By.XPATH, '/html/body/form/div/button')
    login_button.click()

def navigate_to_dishes():
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/a'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[6]/a'))).click()

def enter_dates():
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[1]/td[2]/input[1]'))).send_keys("01-2-2024")
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[1]/td[2]/input[3]'))).send_keys("29-2-2024")

if __name__ == "__main__":
    driver.get(website_url)
    login()
    navigate_to_dishes()
    enter_dates()











# def enter_and_export_dates(date_from, date_to):
# # Starting and end dates
# start_date = date(2021, 7, 1)
# end_date = date(2024, 4, 30)
#   # Find the date input fields (replace with actual locators)
#   date_from_field = driver.find_element(By.ID, "date_from")
#   date_to_field = driver.find_element(By.ID, "date_to")
#
#   # Clear any existing values
#   date_from_field.clear()
#   date_to_field.clear()
#
#   # Enter the dates as YYYY-MM-DD format
#   date_from_field.send_keys(date_from.strftime('%Y-%m-%d'))
#   date_to_field.send_keys(date_to.strftime('%Y-%m-%d'))
#
#   # Find the export button and click it
#   export_button = driver.find_element(By.ID, export_button_locator)
#   export_button.click()
#
# current_date = start_date
# while current_date <= end_date:
#   enter_and_export_dates(current_date, current_date)
#   current_date += timedelta(days=1)







