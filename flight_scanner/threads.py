import threading
import time


class LoadingThread(threading.Thread):
    def __init__(self, window, label_loading):
        super().__init__()
        self.window = window
        self.stopped = False
        self.label_loading = label_loading

    def run(self):
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
        self.stopped = True
