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


def enter_dates(start_date, end_date, type):
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[1]/td[2]/input[1]')))
    if type == "thuisbezorgd":

    elif type == "POS":

    else:
        return ValueError("Unknown type")

    start_date_field = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[1]/td[2]/input[1]')
    end_date_field = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/form/table/tbody/tr[1]/td[2]/input[3]')

    current_date = start_date
    while current_date <= end_date:
        start_date_field.send_keys(current_date.strftime("%d-%m-%Y"))
        current_date += timedelta(days=7)
        end_date_field.send_keys(current_date.strftime("%d-%m-%Y"))
        start_date_field.clear()
        end_date_field.clear()


if __name__ == "__main__":
    driver.get(website_url)
    login()
    navigate_to_dishes()
    enter_dates(start_date=date(2021, 7, 1), end_date=date(2024, 4, 30))

