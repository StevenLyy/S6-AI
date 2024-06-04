import os
import time

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
chrome_options.add_argument("--start-maximized")

download_dir = os.path.join(os.getcwd(), "data")
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

website_url = "https://mijn.sitedish.nl/"

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 7)


def login(key_file, encrypted_file):
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')

    username.send_keys(decrypt(key_file, encrypted_file)[0])
    password.send_keys(decrypt(key_file, encrypted_file)[1])

    login_button = driver.find_element(By.XPATH, '/html/body/form/div/button')
    login_button.click()


def navigate_to_dishes():
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/a'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[6]/a'))).click()


def enter_dates_and_export(start_date, end_date, system):
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[1]/td[2]/input[1]')))
    if system == "POS":
        driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[2]/td[2]/input[2]').click()
    elif system == "Thuisbezorgd":
        driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[2]/td[2]/input[3]').click()
    else:
        return ValueError("Unknown type")

    start_date_field = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[1]/td[2]/input[1]')
    end_date_field = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[1]/td[2]/input[3]')

    current_date = start_date
    while current_date <= end_date:
        print(current_date, current_date + timedelta(days=7))
        new_file_name = f"{system}__{current_date}__{current_date + timedelta(days=7)}.csv"
        start_date_field.send_keys(current_date.strftime("%d-%m-%Y"))
        current_date += timedelta(days=7)
        end_date_field.send_keys(current_date.strftime("%d-%m-%Y"))
        driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/a[1]').click()
        time.sleep(4)

        downloaded_file = max([download_dir + "/" + f for f in os.listdir(download_dir)], key=os.path.getctime)
        new_file_path = os.path.join(download_dir, new_file_name)

        os.rename(downloaded_file, new_file_path)
        start_date_field.clear()
        end_date_field.clear()


if __name__ == "__main__":
    driver.get(website_url)
    login("security/key.key", "security/vxvxvxv.txt")
    navigate_to_dishes()
    enter_dates_and_export(start_date=date(2021, 7, 1), end_date=date(2024, 4, 30), system="Thuisbezorgd")
