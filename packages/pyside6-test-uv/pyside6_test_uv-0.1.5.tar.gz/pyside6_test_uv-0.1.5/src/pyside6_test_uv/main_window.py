from PySide6.QtWidgets import QMainWindow, QWidget

from .main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the main window."""
        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
