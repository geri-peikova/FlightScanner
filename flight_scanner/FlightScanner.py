from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def scanning():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get('https://www.google.com/travel/flights')

    
