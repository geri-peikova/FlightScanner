"""Tests for loading animation and web scrapping for flights"""

# pylint: disable=no-name-in-module
# pylint: disable=redefined-outer-name

import threading
from unittest.mock import MagicMock
import time
import pytest
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

from flight_scanner.threads import LoadingThread, ScanningThread


@pytest.fixture
def app(qtbot):
    """Fixture to create the application instance."""
    test_app = QApplication([])
    qtbot.addWidget(test_app)
    return test_app


@pytest.fixture
def main_window(qtbot):
    """Fixture to create a main window with a QLabel for loading."""
    window = QWidget()
    label_loading = QLabel(window)
    window.label_loading = label_loading
    qtbot.addWidget(window)
    return window


@pytest.fixture
def loading_thread(main_window):
    """Fixture to create the LoadingThread instance."""
    thread = LoadingThread(main_window, main_window.label_loading)
    yield thread
    thread.stop()
    thread.join()


def test_loading_thread_run(qtbot, loading_thread, main_window):
    """Test the run method of the LoadingThread."""
    loading_thread.start()
    qtbot.waitUntil(lambda: main_window.label_loading.text() == "Loading")
    time.sleep(1.5)
    qtbot.waitUntil(lambda: main_window.label_loading.text() == "Loading.")
    time.sleep(1.5)
    qtbot.waitUntil(lambda: main_window.label_loading.text() == "Loading..")
    time.sleep(1.5)
    qtbot.waitUntil(lambda: main_window.label_loading.text() == "Loading...")
    loading_thread.stop()


def test_loading_thread_stop(loading_thread):
    """Test the stop method of the LoadingThread."""
    loading_thread.start()
    loading_thread.stop()
    assert loading_thread.stopped
    loading_thread.join()


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
def window():
    """
    Fixture to provide a mock window object.
    """
    return MagicMock()


@pytest.fixture
def scanning_thread(window, mock_input_data, shared_list, lock):
    """
    Fixture to create a ScanningThread instance.
    """
    return ScanningThread(window, 0, mock_input_data, shared_list, lock)


def test_stop(scanning_thread):
    """
    Test the stop method of ScanningThread.
    """
    scanning_thread.stop()
    assert scanning_thread.stopped is True
