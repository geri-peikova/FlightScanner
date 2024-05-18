import threading
import time


class LoadingThread(threading.Thread):
    """
    A thread that updates a loading label in the main
    window to indicate progress.
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
