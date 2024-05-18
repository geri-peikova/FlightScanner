import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def driver_setup(url):
    """
    Sets up and initializes a Selenium WebDriver for Chrome with specific options.

    Parameters
    ----------
    url : str
        The URL to open with the WebDriver.

    Returns
    -------
    WebDriver
        A configured instance of Selenium WebDriver for Chrome.

    """
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
    """
   Finds an element on a web page by its XPath.

   Parameters
   ----------
   driver : WebDriver
       The Selenium WebDriver instance to use for finding the element.
   xpath : str
       The XPath of the element to find.

   Returns
   -------
   WebElement
       The found web element.
   """
    try:
        my_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except:
        driver.refresh()
        find_my_element_by_xpath(driver, xpath)
    return my_element


def get_list_flights_xpaths(driver):
    """
    Retrieves a list of XPath expressions for flight elements on a web page.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance to use for finding the elements.

    Returns
    -------
    list_flights: list
        A list of XPath expressions for the flight elements.
    exit_code: int
        Returns 1 if no flights are found.
    """
    exit_code = 1
    list_flights = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul')
    count_flights = len(list_flights.find_elements(By.TAG_NAME, 'li'))
    list_flights = []
    if count_flights == 0:
        driver.quit()
        return exit_code
    for i in range(1, count_flights):
        list_flights.append('/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[' + str(i) + ']')
        print(list_flights[i-1])
        if i == 2:  # get 2 flights per date
            break
    return list_flights


def sort_flights_by_price(driver):
    """
    Sorts the flights by price.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance to use for interacting with the elements.
    """
    sort_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div/button')))
    sort_button.click()
    time.sleep(2)
    sort_by_price_button = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[2]/div/ul/li[2]')
    sort_by_price_button.click()
    time.sleep(2)


def open_link(url):
    """
    Opens a given URL using the Selenium WebDriver setup.

    Parameters
    ----------
    url : str
        The URL to open.
    """
    driver_setup(url)
    print(f"Opening link: {url}")


def get_sorted_list_flights(list_flights):
    """
    Sorts the list of flights by price and returns the top 8 flights.

    Parameters
    ----------
    list_flights : list
        The list of flights to sort.

    Returns
    -------
    sorted_flights : list
        A sorted list of the top 8 flights by price.
    """
    sorted_flights = sorted(list_flights, key=lambda flight: flight.price)[:8]
    return sorted_flights
