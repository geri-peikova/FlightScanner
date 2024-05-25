import threading
import time

from flight_scanner import adding_set_of_flights
from interpreters import driver_setup, find_my_element_by_xpath


class LoadingThread(threading.Thread):
    """
    A thread that updates a loading label in the main window to indicate progress.
    """

    def __init__(self, window, label_loading):
        """
        Initializes the LoadingThread with the given window and label.

        Parameters
        ----------
        window : QWidget
            The main window of the application.
        label_loading : QLabel
            The label that displays the loading message.
        """
        super().__init__()
        self.window = window
        self.stopped = False
        self.label_loading = label_loading

    def run(self):
        """
        Runs the thread, updating the loading label with a rotating message.
        """
        while not self.stopped:
            self.label_loading.setText("Loading")
            self.label_loading.repaint()
            time.sleep(1)
            self.label_loading.setText("Loading.")
            self.label_loading.repaint()
            time.sleep(1)
            self.label_loading.setText("Loading..")
            self.label_loading.repaint()
            time.sleep(1)
            self.label_loading.setText("Loading...")
            self.label_loading.repaint()
            time.sleep(2)

    def stop(self):
        """
        Stops the loading thread by setting the stopped flag to True.
        """
        self.stopped = True


class ScanningThread(threading.Thread):
    """
    A thread that scans for flights and adds them to a shared list.
    """

    def __init__(self, window, index, input_data, list_flights, lock):
        """
        Initializes the ScanningThread with the given parameters.

        Parameters
        ----------
        window : QWidget
            The main window of the application.
        index : int
            The index of the current scanning operation.
        input_data : dict
            The input data containing flight search parameters.
        list_flights : list
            The shared list to store the scanned flight data.
        lock : threading.Lock
            A lock to ensure thread-safe access to the shared list.
        """
        super().__init__()
        self.window = window
        self.index = index
        self.input_data = input_data
        self.list_flights = list_flights
        self.lock = lock

    def run(self):
        """
        Runs the thread, scanning for flights and adding them to the shared list.
        """
        driver = driver_setup('https://www.google.com/travel/flights')
        try:
            button_accept_all = find_my_element_by_xpath(
                driver,
                '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button'
            )
            button_accept_all.click()
            time.sleep(3)
        finally:
            adding_set_of_flights(self.input_data, self.index, self.list_flights, driver, self.lock)

        driver.quit()
        self.stop()

    def stop(self):
        """
        Stops the scanning thread by setting the stopped flag to True.
        """
        self.stopped = True
