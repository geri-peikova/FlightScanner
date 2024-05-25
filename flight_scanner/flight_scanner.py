import time

from selenium.common import NoSuchElementException, StaleElementReferenceException, InvalidSelectorException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Flight import Travel
from interpreters import find_my_element_by_xpath, sort_flights_by_price_driver, get_xpath_for_li


def add_flights(flight, list_flights, input_data, driver, lock):
    """
    Adds flight information to the list of flights.

    Parameters
    ----------
    flight : WebElement
        The web element representing the flight.
    list_flights : list
        The list to append the flight information to.
    input_data : dict
        A dictionary containing additional flight search parameters.
    driver : WebDriver
        The Selenium WebDriver instance to use for finding elements.
    """
    flight.click()
    time.sleep(3)
    flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul/li/div/div[2]')
    flight.click()
    time.sleep(3)
    try:
        try:    # if 'Unfortunately, the price you saw on the previous page has changed' occurs
            tip_changed_price = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[1]'))).text
            if tip_changed_price == 'Unfortunately, the price you saw on the previous page has changed':
                departure_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div[1]')
                arrival_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[3]/div[1]/div/div/div/div[2]/div[2]/div')
            else:
                raise InvalidSelectorException

        except InvalidSelectorException:    # If normal
            departure_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div/div[2]')
            arrival_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div/div[2]')

        price = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/span')
        time.sleep(3)
        flight_info = {'price': price.text, 'departure_flight': departure_flight.text,
                       'arrival_flight': arrival_flight.text,
                       'link': driver.current_url}
        with lock:
            list_flights.append(Travel(flight_info, input_data))
            time.sleep(3)
            print('Flight: ',
                  {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text,
                   'link': driver.current_url})

    except NoSuchElementException or StaleElementReferenceException:
        driver.refresh()
        departure_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div/div[2]')
        arrival_flight = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div/div[2]')
        price = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/span')
        time.sleep(3)

        flight_info = {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text,
             'link': driver.current_url}
        with lock:
            list_flights.append(Travel(flight_info, input_data))
            print('Flight: ', {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text, 'link': driver.current_url})


def search_flight(input_data, set_num, driver):
    """
    Searches for flights based on the provided input data.

    Parameters
    ----------
    input_data : dict
        A dictionary containing dates and other flight search parameters.
    set_num : int
        The index of the current set of dates to search for.
    driver : WebDriver
        The Selenium WebDriver instance to use for finding elements.

    Returns
    -------
    exit_code : int
        0 if the search is successful, 1 if it fails.
    """
    depart_date_input = find_my_element_by_xpath(driver,
                                                 '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input')
    depart_date_input.send_keys(input_data['dates_list'][set_num]['Start'])
    depart_date_input.send_keys(Keys.ENTER)
    time.sleep(3)
    return_date_input = find_my_element_by_xpath(driver,
                                                 '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input')
    return_date_input.send_keys(input_data['dates_list'][set_num]['End'])
    return_date_input.send_keys(Keys.ENTER)
    time.sleep(3)
    flight_to_input = find_my_element_by_xpath(driver,
                                               '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input')
    flight_to_input.send_keys(input_data['flight_to'])
    try:
        flight_to_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                            '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]')))
        flight_to_input.click()
        time.sleep(3)
    except:
        driver.quit()
        exit_code = 1
        return exit_code
    flight_from_input = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input')
    flight_from_input.clear()
    flight_from_input.send_keys(input_data['flight_from'])
    try:
        flight_to_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                            '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]')))
        flight_to_input.click()
        time.sleep(3)
    except:
        driver.quit()
        exit_code = 1
        return exit_code
    search = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button')
    search.click()
    time.sleep(3)
    exit_code = 0
    return exit_code


def adding_set_of_flights(input_data, set_num, list_flights, driver, lock):
    """
   Adds a set of flights to the list of flights.

   Parameters
   ----------
   input_data : dict
       A dictionary containing dates and other flight search parameters.
   set_num : int
       The index of the current set of dates to search for.
   list_flights : list
       The list to append the flight information to.
   driver : WebDriver
       The Selenium WebDriver instance to use for finding elements.
   """
    search_result = search_flight(input_data, set_num, driver)
    if search_result == 1:
        pass
    try:
        popup_close_button = driver.find_element(By.XPATH,
                                                 '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/span/span/span[2]/div/div/div/div[3]')
        popup_close_button.click()
        time.sleep(3)
    except:
        print('Popup have not shown!')
    sort_flights_by_price_driver(driver)
    time.sleep(3)
    flight_xpath = get_xpath_for_li(set_num, driver)
    add_flights(find_my_element_by_xpath(driver, flight_xpath), list_flights, input_data, driver, lock)
    time.sleep(3)
