"""Tests for flight scanner"""

# pylint: disable=line-too-long
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments

from unittest.mock import MagicMock, patch
import threading
import pytest

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from flight_scanner.flight_scanner import adding_set_of_flights, search_flight


@pytest.fixture
def mock_input_data():
    """
    Fixture to provide mock input data.
    """
    return {
        'departure_weekday': 'Friday',
        'arrival_weekday': 'Sunday',
        'flight_from': 'Sofia',
        'flight_to': 'Rome',
        'dates_list': [{'End': 'Tue, Sep 3', 'Start': 'Mon, Sep 2'}]
    }


@pytest.fixture
def shared_list():
    """
    Fixture to provide a shared list.
    """
    return []


@pytest.fixture
def lock():
    """
    Fixture to provide a threading lock.
    """
    return threading.Lock()


@pytest.fixture
def mock_driver():
    """
    Fixture to mock the Selenium WebDriver.
    """
    mock_driver = MagicMock()
    return mock_driver


@patch('flight_scanner.flight_scanner.find_my_element_by_xpath')
def test_search_flight_success(mock_find_my_element_by_xpath, mock_input_data, mock_driver):
    """
    Test search_flight function with successful execution.
    """
    set_num = 0
    mock_depart_date_input = MagicMock()
    mock_return_date_input = MagicMock()
    mock_flight_to_input = MagicMock()
    mock_flight_from_input = MagicMock()
    mock_search_button = MagicMock()

    mock_find_my_element_by_xpath.side_effect = [
        mock_depart_date_input,
        mock_return_date_input,
        mock_flight_to_input,
        mock_flight_from_input,
        mock_search_button
    ]

    with patch.object(WebDriverWait, 'until', return_value=mock_flight_to_input):
        result = search_flight(mock_input_data, set_num, mock_driver)

    assert result == 0
    mock_depart_date_input.send_keys.assert_any_call(mock_input_data['dates_list'][set_num]['Start'])
    mock_return_date_input.send_keys.assert_any_call(mock_input_data['dates_list'][set_num]['End'])
    mock_flight_to_input.send_keys.assert_any_call(mock_input_data['flight_to'])
    mock_flight_from_input.send_keys.assert_any_call(mock_input_data['flight_from'])
    mock_search_button.click.assert_called_once()


@patch('flight_scanner.flight_scanner.find_my_element_by_xpath')
def test_search_flight_failure_to_input_to(mock_find_my_element_by_xpath, mock_input_data, mock_driver):
    """
    Test search_flight function when failing to input the flight_to.
    """
    set_num = 0
    mock_depart_date_input = MagicMock()
    mock_return_date_input = MagicMock()
    mock_flight_to_input = MagicMock()

    mock_find_my_element_by_xpath.side_effect = [
        mock_depart_date_input,
        mock_return_date_input,
        mock_flight_to_input
    ]

    with patch.object(WebDriverWait, 'until', side_effect=TimeoutException):
        result = search_flight(mock_input_data, set_num, mock_driver)

    assert result == 1
    mock_driver.quit.assert_called_once()


@patch('flight_scanner.flight_scanner.find_my_element_by_xpath')
def test_search_flight_failure_to_input_from(mock_find_my_element_by_xpath, mock_input_data, mock_driver):
    """
    Test search_flight function when failing to input the flight_from.
    """
    set_num = 0
    mock_depart_date_input = MagicMock()
    mock_return_date_input = MagicMock()
    mock_flight_to_input = MagicMock()
    mock_flight_from_input = MagicMock()

    mock_find_my_element_by_xpath.side_effect = [
        mock_depart_date_input,
        mock_return_date_input,
        mock_flight_to_input,
        mock_flight_from_input
    ]

    with patch.object(WebDriverWait, 'until', side_effect=[mock_flight_to_input, TimeoutException]):
        result = search_flight(mock_input_data, set_num, mock_driver)

    assert result == 1
    mock_driver.quit.assert_called_once()
    mock_flight_from_input.clear.assert_called_once()
    mock_flight_from_input.send_keys.assert_any_call(mock_input_data['flight_from'])


@patch('flight_scanner.flight_scanner.add_flights')
@patch('flight_scanner.flight_scanner.get_xpath_for_li')
@patch('flight_scanner.flight_scanner.sort_flights_by_price_driver')
@patch('flight_scanner.flight_scanner.search_flight')
@patch('flight_scanner.flight_scanner.find_my_element_by_xpath')
def test_adding_set_of_flights_success(mock_find_my_element_by_xpath, mock_search_flight,
                                       mock_sort_flights_by_price_driver, mock_get_xpath_for_li, mock_add_flights,
                                       mock_input_data, shared_list, mock_driver, lock):
    """
    Test adding_set_of_flights function with successful execution.
    """
    set_num = 0
    mock_search_flight.return_value = None
    mock_get_xpath_for_li.return_value = '//li[1]'
    mock_find_my_element_by_xpath.return_value = MagicMock()

    adding_set_of_flights(mock_input_data, set_num, shared_list, mock_driver, lock)

    mock_search_flight.assert_called_once_with(mock_input_data, set_num, mock_driver)
    mock_sort_flights_by_price_driver.assert_called_once_with(mock_driver)
    mock_get_xpath_for_li.assert_called_once_with(set_num, mock_driver)
    mock_find_my_element_by_xpath.assert_called_once_with(mock_driver, '//li[1]')
    mock_add_flights.assert_called_once()
    assert len(shared_list) == 0


@patch('flight_scanner.flight_scanner.add_flights')
@patch('flight_scanner.flight_scanner.get_xpath_for_li')
@patch('flight_scanner.flight_scanner.sort_flights_by_price_driver')
@patch('flight_scanner.flight_scanner.search_flight')
@patch('flight_scanner.flight_scanner.find_my_element_by_xpath')
def test_adding_set_of_flights_no_popup(mock_find_my_element_by_xpath, mock_search_flight,
                                        mock_sort_flights_by_price_driver, mock_get_xpath_for_li,
                                        mock_add_flights, mock_input_data, shared_list, mock_driver, lock):
    """
    Test adding_set_of_flights function when popup does not appear.
    """
    set_num = 0
    mock_search_flight.return_value = None
    mock_get_xpath_for_li.return_value = '//li[1]'
    mock_find_my_element_by_xpath.return_value = MagicMock()
    mock_driver.find_element.side_effect = Exception('Popup not found')

    adding_set_of_flights(mock_input_data, set_num, shared_list, mock_driver, lock)

    mock_search_flight.assert_called_once_with(mock_input_data, set_num, mock_driver)
    mock_sort_flights_by_price_driver.assert_called_once_with(mock_driver)
    mock_get_xpath_for_li.assert_called_once_with(set_num, mock_driver)
    mock_find_my_element_by_xpath.assert_called_once_with(mock_driver, '//li[1]')
    mock_add_flights.assert_called_once()
    assert len(shared_list) == 0
