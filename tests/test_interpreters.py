"""Tests for interpreters"""

# pylint: disable=line-too-long
# pylint: disable=redefined-outer-name
# pylint: disable=no-member
# pylint: disable=unused-argument


from unittest.mock import Mock, patch, MagicMock

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from flight_scanner.interpreters import driver_setup_headless, find_my_element_by_xpath, open_link, \
    get_xpath_for_li, get_sorted_list_flights
from tests.setup import LIST_FLIGHTS_UNSORTED


@pytest.fixture
def mock_webdriver(mocker):
    """
    Fixture to mock the WebDriver for testing.
    """
    mock_driver = mocker.MagicMock(spec=webdriver.Chrome)
    mocker.patch('selenium.webdriver.Chrome', return_value=mock_driver)
    return mock_driver


@pytest.fixture
def mock_webelement(mocker):
    """
    Fixture to mock the WebElement for testing.
    """
    return mocker.MagicMock(spec=WebElement)


@pytest.fixture
def mock_webdriver_wait(mocker):
    """
    Fixture to mock WebDriverWait for testing.
    """
    return mocker.patch('selenium.webdriver.support.ui.WebDriverWait', autospec=True)


def test_driver_setup_returns_webdriver_instance(mock_webdriver):
    """
    Test case to verify that driver_setup returns a WebDriver instance.
    """
    url = "https://www.google.com"
    driver = driver_setup_headless(url)
    assert driver is mock_webdriver


def test_driver_setup_opens_correct_url(mock_webdriver):
    """
    Test case to verify that driver_setup opens the correct URL.
    """
    url = "https://www.google.com"
    driver = driver_setup_headless(url)
    driver.get.assert_called_once_with(url)


def test_driver_setup_maximizes_window(mock_webdriver):
    """
    Test case to verify that driver_setup maximizes the window.
    """
    url = "https://www.google.com"
    driver = driver_setup_headless(url)
    driver.maximize_window.assert_called_once()


def test_find_my_element_by_xpath_retry_success(mock_webdriver):
    """
    Test case to verify that find_my_element_by_xpath retries finding the element and succeeds after a page refresh.
    """
    xpath = "//div[@id='test']"
    mock_element = Mock()

    with patch('selenium.webdriver.support.ui.WebDriverWait.until', side_effect=[Exception, mock_element]) as mock_wait:
        with patch.object(mock_webdriver, 'refresh', return_value=None) as mock_refresh:
            element = find_my_element_by_xpath(mock_webdriver, xpath, retries=1)
            assert element == mock_element
            assert mock_wait.call_count == 2
            mock_refresh.assert_called_once()


def test_find_my_element_by_xpath_fail(mock_webdriver):
    """
    Test case to verify that find_my_element_by_xpath raises an exception if the element cannot be found after retries.
    """
    xpath = "//div[@id='test']"

    with patch('selenium.webdriver.support.ui.WebDriverWait.until', side_effect=Exception) as mock_wait:
        with patch.object(mock_webdriver, 'refresh', return_value=None) as mock_refresh:
            with pytest.raises(Exception, match="Element not found after retries"):
                find_my_element_by_xpath(mock_webdriver, xpath, retries=1)
            assert mock_wait.call_count == 2
            mock_refresh.assert_called_once()


def test_open_link(mock_webdriver):
    """
    Test the open_link function.
    """
    url = "https://www.google.com"
    driver = open_link(url)
    assert driver is mock_webdriver


@patch('flight_scanner.interpreters.find_my_element_by_xpath')
def test_get_xpath_for_li_found(mock_find_my_element_by_xpath):
    """
    Test get_xpath_for_li when flights are found.
    """
    set_num = 1
    driver = MagicMock()
    mock_list_flights = MagicMock()
    mock_list_flights.find_elements.return_value = ['flight1', 'flight2']
    mock_find_my_element_by_xpath.return_value = mock_list_flights

    xpath = get_xpath_for_li(set_num, driver)

    expected_xpath = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul/li[2]'
    assert xpath == expected_xpath
    mock_find_my_element_by_xpath.assert_called_once_with(
        driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul'
    )


@patch('flight_scanner.interpreters.find_my_element_by_xpath')
def test_get_xpath_for_li_not_found(mock_find_my_element_by_xpath):
    """
    Test get_xpath_for_li when no flights are found.
    """
    set_num = 1
    driver = MagicMock()
    mock_list_flights = MagicMock()
    mock_list_flights.find_elements.return_value = []
    mock_find_my_element_by_xpath.return_value = mock_list_flights

    result = get_xpath_for_li(set_num, driver)

    assert result == 1
    driver.quit.assert_called_once()
    mock_find_my_element_by_xpath.assert_called_once_with(
        driver, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[4]/ul'
    )


def test_get_sorted_list_flights():
    """
    Test get_sorted_list_flights function.
    """
    result = get_sorted_list_flights(LIST_FLIGHTS_UNSORTED)
    for i in range(1, len(result)):
        assert int(result[i].price.split()[1]) >= int(result[i-1].price.split()[1])
