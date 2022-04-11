"""Landing Page."""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class LandingPage(QDialog):
    """Landing Page."""

    user = None

    def __init__(self, user):
        """Construct object."""
        super().__init__()
        loadUi("UI/LandingPage.ui", self)
        self.user = user
        self.name_lbl.text = self.user.email
