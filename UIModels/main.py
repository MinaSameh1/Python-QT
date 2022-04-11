"""Responsible for GUI."""


from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from UIModels.login import Login


class App(QApplication):
    """GUI Handling."""

    self.QtWidgets.QStackedWidget

    def __init__(self, argv):
        """Construct Object."""
        super().__init__(argv=argv)
        exit_act = QAction(QIcon("exit.png"), "&Exit", self)
        exit_act.setShortcut("Ctrl+Q")
        exit_act.setStatusTip("Exit Application")
        exit_act.triggered.connect(qApp.quit)
        self.widget = QtWidgets.QStackedWidget()
        main_window = Login()
        self.widget.addWidget(main_window)
        self.widget.setFixedWidth(480)
        self.widget.setFixedHeight(620)

    def exec(self):
        self.widget.show()
        return self.exce_()

    def reduce_stack(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

    def set_stack(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def add_to_stack(self, dialog):
        self.widget.addWidget(dialog)
