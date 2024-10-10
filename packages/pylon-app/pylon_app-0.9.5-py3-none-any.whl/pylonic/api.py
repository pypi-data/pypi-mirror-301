from PySide6.QtCore import QObject, Slot


class PylonicAPI(QObject):
    def __init__(self):
        super().__init__()


def Bridge(*args, **kwargs):
    return Slot(*args, **kwargs)
