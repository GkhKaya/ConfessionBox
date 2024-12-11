from PyQt5.QtWidgets import QApplication
from Views.AuthView.AuthView import AuthView


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AuthView()
    window.show()
    sys.exit(app.exec_())