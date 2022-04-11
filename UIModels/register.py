"""Register Window."""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from utils.email import send_mail


class Register(QDialog):
    """Register Window."""

    widget = None

    def __init__(self, widget):
        """Construct object."""
        super().__init__()
        loadUi("UI/register.ui", self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg_but.clicked.connect(self.reg_func)
        self.widget = widget

    def reg_func(self):
        """Handle Registeration."""
        if not self.checkpass():
            print("WRONG PASS")
        if self.reg():
            self.go_to_login()

    def reg(self) -> bool:
        """Register User."""
        email_value = self.email.text()
        pass_value = self.password.text()
        name_value = self.name.text()
        if create_user(name_value, email_value, pass_value):
            try:
                send_mail(
                    "minasameh1@gmail.com",
                    "NEW USER REGISTERED EMAIL:" + email_value,
                )
            except Exception:  # In case of no network
                pass
            return True
        return False

    def checkpass(self) -> bool:
        """Check passwords."""
        return self.password.text() == self.confpass.text()

    def go_to_login(self):
        """Go to login form."""
        sys.exit(0)


# class OTP(QDialog):
#     """OTP Window."""
#
#     widget = None
#
#     def __init__(self, widget):
#         """Construct object."""
#         super().__init__()
#         loadUi("UI/OTP.ui", self)
#         self.otp_but.clicked.connect(self.otp_check)
#         self.widget = widget
#
#     def otp_check(self, otp):
#         """Check if otp works."""
#         if self.otp_text == otp:
#             self.go_to_login()
#
#     def go_to_login(self):
#         """Go to login form."""
#         log = Login(self.widget)
#         self.widget.addWidget(log)
#         self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
