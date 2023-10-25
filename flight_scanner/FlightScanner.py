import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
#AIzaSyDwluc0SlxuEyjmn173yjSwlYe8Lcfe26o

def scanning():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

    chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #chrome_options.add_argument('--headless')  # to not see what is happening in chrome
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get('https://www.google.com/travel/flights')
    try:
        button_accept_all = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
        wait = WebDriverWait(driver, timeout=2)
        wait.until(lambda d: button_accept_all.is_displayed())
        button_accept_all.click()
    finally:

        depart_input = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input')
        wait.until(lambda d: depart_input.is_displayed())
        depart_input.send_keys("10 November")
        depart_input.send_keys(Keys.ENTER)

        return_input = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input')
        wait.until(lambda d: return_input.is_displayed())
        return_input.send_keys("12 November")
        return_input.send_keys(Keys.ENTER)

        destination = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input')
        destination.click()
        time.sleep(2)
        destination = driver.find_element((By.CLASS_NAME, 'II2One j0Ppje zmMKJ LbIaRd'))
        print(destination.text)
        wait.until(lambda d: destination.is_displayed())
        destination.send_keys("Rome")


        button_search = driver.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button')
        print(button_search.text)

        # <input type="text" value="" class="II2One j0Ppje zmMKJ LbIaRd" aria-label="Where else?"
        # <input type="text" value="" jsname="yrriRe" jsaction="focus:h06R8; blur:zjh6rb" class="II2One j0Ppje zmMKJ LbIaRd" autocomplete="off" role="combobox" aria-autocomplete="both" aria-haspopup="true" aria-expanded="true" aria-label="Where else?" aria-describedby="i29" autofocus="" aria-owns="h0T7hb-158" tabindex="0">