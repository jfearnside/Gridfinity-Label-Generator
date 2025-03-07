from PySide6.QtCore import QObject, Signal

class Worker(QObject):
    finished = Signal()
    error = Signal(str)

    def __init__(self, task, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.task(*self.args, **self.kwargs)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()