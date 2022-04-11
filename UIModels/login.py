"""Login window."""

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QDialog, QApplication, QMessageBox, qApp
from PyQt5.uic import loadUi

from UIModels.register import Register
from UIModels.landingpage import LandingPage
from user import service


class Login(QDialog):
    """Login window."""

    widget = None

    def __init__(self, widget):
        """Construct object."""
        super().__init__()
        self.widget = widget
        loadUi("UI/login.ui", self)
        exit_act = QAction(QIcon("exit.png"), "&Exit", self)
        exit_act.setShortcut("Ctrl+Q")
        exit_act.setStatusTip("Exit Application")
        exit_act.triggered.connect(qApp.quit)
        self.login_but.clicked.connect(self.login_func)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg_but.clicked.connect(self.go_to_reg)
        self.email.setToolTip("Enter a valid EMAIL.")
        self.password.setToolTip(
            "Your password is safe with us, Trust<sup>TM</sup> me."
        )

    def login_func(self):
        """Handle login."""
        email_value = self.email.text()
        pass_value = self.password.text()
        user = service.login(email_value, pass_value)
        if user is not None and user:
            print("USER LOGGED IN.")
            self.go_to_landing_page(user)
        else:
            QMessageBox.information(self, "Wrong", "Wrong Email or password")

    def go_to_reg(self):
        """Go to registeration page."""
        reg = Register(widget=self.widget)
        self.widget.addWidget(reg)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def go_to_landing_page(self, user):
        """Go to landing page."""
        land = LandingPage(user)
        self.widget.addWidget(land)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
