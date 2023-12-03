import time

from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def scanning():
    driver = driver_setup()
    try:
        button_accept_all = find_my_element_by_xpath(driver, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
        button_accept_all.click()
    finally:
        search_result = search_flight('Varna', 'Sofia', 'Fri, Mar 1', 'Sun, Mar 3', driver)
        if search_result == 1:
            return 1
        try:
            popup_close_button = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/span/span/span[2]/div/div/div/div[3]')
            popup_close_button.click()
        except:
            print('Popup have not shown!')

        sort_by_price(driver)

        flights = []
        time.sleep(1)

        add_flights(find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[1]'), flights, driver)
        time.sleep(2)
        add_flights(find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[2]'), flights, driver)
        time.sleep(2)
        add_flights(find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[3]'), flights, driver)
        print(flights)
        return 0


def driver_setup():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_argument('--headless')  # to not see what is happening in chrome
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get('https://www.google.com/travel/flights')
    return driver


def add_flights(flight, flights, driver):
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    flight.click()
    time.sleep(1)
    flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul/li/div/div[2]')
    flight.click()
    try:
        departure_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div/div[2]')
        arrival_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div/div[2]')
        price = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/span')
        time.sleep(1)
        flights.append(
            {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text,
             'link': driver.current_url})
        time.sleep(1)
        print('Flight: ',
              {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text,
               'link': driver.current_url})

    except NoSuchElementException or StaleElementReferenceException:
        driver.refresh()
        departure_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div/div[2]')
        arrival_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div/div[2]')
        price = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/span')
        time.sleep(1)
        flights.append(
            {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text,
             'link': driver.current_url})
        print('Flight: ', {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text, 'link': driver.current_url})

    finally:
        time.sleep(1)
        driver.back()
        find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul')
        driver.back()


def find_my_element_by_xpath(driver, xpath):
    try:
        my_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except:
        driver.refresh()
        find_my_element_by_xpath(driver, xpath)
    return my_element


def sort_by_price(driver):
    sort_button = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div/button')
    sort_button.click()
    sort_by_price_button = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[2]/div/ul/li[2]')
    sort_by_price_button.click()


def search_flight(flight_from, flight_to, depart_date, return_date, driver):
    depart_date_input = find_my_element_by_xpath(driver,
                                                 '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input')
    depart_date_input.send_keys(depart_date)
    depart_date_input.send_keys(Keys.ENTER)

    return_date_input = find_my_element_by_xpath(driver,
                                                 '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input')
    return_date_input.send_keys(return_date)
    return_date_input.send_keys(Keys.ENTER)

    flight_to_input = find_my_element_by_xpath(driver,
                                               '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input')
    flight_to_input.send_keys(flight_to)
    try:
        flight_to_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                            '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]')))
        flight_to_input.click()
    except:
        driver.quit()
        return 1
    flight_from_input = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input')
    flight_from_input.clear()
    flight_from_input.send_keys(flight_from)
    try:
        flight_to_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                            '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]')))
        flight_to_input.click()
    except:
        driver.quit()
        return 1
    search = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button')
    search.click()
    return 0


"""        list_sorted_flights = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul')
        items = list_sorted_flights.find_elements(By.TAG_NAME, 'li')
        if len(items)>2:
            for count in range(1,3):
                add_flights(find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[1]/div/div[' + str(count) + ']'), flights, driver)
                time.sleep(2)
        print(flights)"""