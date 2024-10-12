from PySide6.QtWidgets import QApplication

from .main_window import MainWindow


def main() -> int:
    """Run the application."""
    app = QApplication()
    main_window = MainWindow()
    main_window.resize(400, 400)
    main_window.show()
    return app.exec()


if __name__ == "__main__":
    main()
