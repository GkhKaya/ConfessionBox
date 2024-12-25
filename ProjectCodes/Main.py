from PyQt5.QtWidgets import QApplication
from Views.AuthView.AuthView import AuthView
from Views.HomeView.HomeView import HomeView
from Views.PrivateConfessionView.PrivateConfessionView import PrivateConfessionView



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = HomeView()
    window.show()
    sys.exit(app.exec_())