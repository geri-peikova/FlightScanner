import time

from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def driver_setup(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #chrome_options.add_argument('--headless')  # to not see what is happening in chrome
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get(url)
    return driver


def find_my_element_by_xpath(driver, xpath):
    try:
        my_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except:
        driver.refresh()
        find_my_element_by_xpath(driver, xpath)
    return my_element


def get_list_flights_xpaths(driver):
    list_flights = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul')
    count_flights = len(list_flights.find_elements(By.TAG_NAME, 'li'))
    list_flights = []
    if count_flights == 0:
        driver.quit()
        return 1
    for i in range(1, count_flights):
        list_flights.append('/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[' + str(i) + ']')
        print(list_flights[i-1])
        if i == 2:  # get 2 flights per date
            break
    return list_flights


def sort_flights_by_price(driver):
    sort_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div/button')))
    sort_button.click()
    time.sleep(2)
    sort_by_price_button = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[2]/div/ul/li[2]')
    sort_by_price_button.click()
    time.sleep(2)
