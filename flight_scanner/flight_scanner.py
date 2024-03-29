import time

from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException, InvalidSelectorException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Flight import Travel
from interpreters import driver_setup, find_my_element_by_xpath, sort_flights_by_price, get_list_flights_xpaths


def scanning(input_data):
    list_flights = []
    for set_num in range(0, len(input_data['dates_list'])):
        driver = driver_setup()
        try:
            button_accept_all = find_my_element_by_xpath(driver, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
            button_accept_all.click()
            time.sleep(3)
        finally:
            adding_week_flights(input_data, set_num, list_flights, driver)
            driver.quit()
    sorted_list_flights = sorted(list_flights, key=lambda flight: flight.price)
    return sorted_list_flights


def add_flights(flight, list_flights, input_data, driver):
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
        list_flights.append(Travel(flight_info, input_data))
       # list_flights.append(  {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text, 'link': driver.current_url})
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
        list_flights.append(Travel(flight_info, input_data))
        list_flights.append(
            {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text,
             'link': driver.current_url})
        print('Flight: ', {'price': price.text, 'departure_flight': departure_flight.text, 'arrival_flight': arrival_flight.text, 'link': driver.current_url})

    finally:
        time.sleep(3)
        driver.back()
        find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul')
        driver.back()


def search_flight(input_data, set_num, driver):
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
        return 1
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
        return 1
    search = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button')
    search.click()
    time.sleep(3)
    return 0


def adding_week_flights(input_data, set_num, list_flights, driver):
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
    sort_flights_by_price(driver)
    time.sleep(3)
    list_flights_xpaths = get_list_flights_xpaths(driver)
    for flight_xpath in list_flights_xpaths:
        add_flights(find_my_element_by_xpath(driver, flight_xpath), list_flights, input_data, driver)
        time.sleep(3)


"""  search_result = search_flight('Varna', 'Sofia', 'Fri, Mar 1', 'Sun, Mar 3', driver)
 
     list_sorted_flights = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul')
        items = list_sorted_flights.find_elements(By.TAG_NAME, 'li')
        if len(items)>2:
            for count in range(1,3):
                add_flights(find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[1]/div/div[' + str(count) + ']'), flights, driver)
                time.sleep(2)
        print(flights)
        
        
        {
            'departure_weekday': 'Friday', 
            'arrival_weekday': 'Sunday', 
            'flight_from': 'Sofia', 
            'flight_to': 'Varna', 
            'dates_list': [{'End': '14-12-2023', 'Start': '08-12-2023'}, 
                            {'End': '21-12-2023', 'Start': '15-12-2023'}, 
                            {'End': '28-12-2023', 'Start': '22-12-2023'}, 
                            {'End': '04-01-2024', 'Start': '29-12-2023'}, 
                            {'End': '11-01-2024', 'Start': '05-01-2024'}, 
                            {'End': '18-01-2024', 'Start': '12-01-2024'}, 
                            {'End': '25-01-2024', 'Start': '19-01-2024'}, 
                            {'End': '01-02-2024', 'Start': '26-01-2024'}]}"""