"""Module providing instructions for webdriver to follow"""

# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=broad-exception-raised
# pylint: disable=raise-missing-from
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def driver_setup_headless(url):
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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get(url)
    return driver


def find_my_element_by_xpath(driver, xpath, retries=2):
    """
    Finds an element on a web page by its XPath.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance to use for finding the element.
    xpath : str
        The XPath of the element to find.
    retries : int, optional
        The number of retries to attempt if the element is not found. Defaults to 2.

    Returns
    -------
    WebElement
        The found web element.

    Raises
    ------
    Exception
        If the element is not found after the specified number of retries.
    """
    try:
        my_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except Exception:
        if retries > 0:
            driver.refresh()
            return find_my_element_by_xpath(driver, xpath, retries=retries - 1)
        raise Exception("Element not found after retries")
    return my_element


def sort_flights_by_price_driver(driver):
    """
    Sorts the flights by price on the web page using the WebDriver.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance to use for interacting with the elements.
    """
    try:
        sort_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div/button')
            )
        )
        sort_by_price_xpath = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[2]/div/ul/li[2]'
    except Exception:
        sort_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div[1]/div/button')
            )
        )
        sort_by_price_xpath = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/div/div/div[2]/div/ul/li[2]'
    finally:
        sort_button.click()
        time.sleep(2)
        sort_by_price_button = find_my_element_by_xpath(driver, sort_by_price_xpath)
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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    print(f"Opening link: {url}")
    driver.maximize_window()
    driver.get(url)
    return driver


def get_xpath_for_li(set_num, driver):
    """
    Retrieves the XPath for a specific flight element on a web page.

    Parameters
    ----------
    set_num : int
        The set number to determine the XPath.
    driver : WebDriver
        The Selenium WebDriver instance to use for finding the elements.

    Returns
    -------
    str
        The XPath expression for the flight element.

    Raises
    ------
    Exception
        If no flights are found.
    """
    exit_code = 1
    list_flights = find_my_element_by_xpath(driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul')
    count_flights = len(list_flights.find_elements(By.TAG_NAME, 'li'))
    if count_flights == 0:
        driver.quit()
        return exit_code
    list_index = set_num % 2 + 1
    xpath = f'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[{list_index}]'
    return xpath


def get_sorted_list_flights(list_flights):
    """
    Sorts the list of flights by price and returns the top 8 flights.

    Parameters
    ----------
    list_flights : list
        The list of flights to sort.

    Returns
    -------
    list
        A sorted list of the top 8 flights by price.
    """
    sorted_flights = sorted(list_flights, key=lambda flight: flight.price)[:8]
    return sorted_flights
