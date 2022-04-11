"""Main."""

import os
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QApplication,
    QInputDialog,
    QListWidgetItem,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    qApp,
    QHeaderView,
)
from PyQt5.uic import loadUi
import logging
import dotenv

from utils.email import send_mail
from utils.logger import log_config
from user import service as user_service
from product.service import (
    get_products,
    create_product,
    update_product,
    delete_product,
)
from db import DbService

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"


def init():
    """Start required services."""
    DbService.connect()
    dotenv.load_dotenv(".env")
    log_config()


class Login(QDialog):
    """Login window."""

    def __init__(self):
        """Construct object."""
        super().__init__()
        loadUi(f"{LOCAL_DIR}UI/login.ui", self)
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
        user = user_service.login(email_value, pass_value)
        if user is not None and user:
            print("USER LOGGED IN.")
            self.go_to_main_page(user)
        else:
            QMessageBox.information(self, "Wrong", "Wrong Email or password")

    def go_to_reg(self):
        """Go to registeration page."""
        reg = Register()
        widget.addWidget(reg)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_main_page(self, user):
        """Go to landing page."""
        widget.setFixedWidth(1000)
        widget.setFixedHeight(800)
        mpage = MainPage(user)
        widget.addWidget(mpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MainPage(QDialog):
    """Appilcation."""

    user = None

    def __init__(self, user):
        """Construct object."""
        super().__init__()
        loadUi(f"{LOCAL_DIR}UI/main.ui", self)
        self.user = user
        self.welcome_lbl.setText("Welcome " + user.name)
        self.logout_but.clicked.connect(self.go_to_login)
        self.tbl.setColumnWidth(0, 100)
        self.tbl.setColumnWidth(1, 300)
        self.tbl.setColumnWidth(2, 250)
        self.tbl.setHorizontalHeaderLabels(
            ["id", "product_name", "product_price"]
        )
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.load_data()
        self.edit_but.clicked.connect(self._edit_item)
        self.sell_but.clicked.connect(self._sell_item)
        self.add_but.clicked.connect(self._add_row)
        self.del_but.clicked.connect(self._remove_row)
        self.finish_but.clicked.connect(self._receipt)

    def _add_row(self):
        """Add row to db and table."""
        row_count = self.tbl.rowCount()
        product_name, ok = QInputDialog.getText(
            self, "Product Name", "Enter Product Name"
        )
        if not ok:
            return
        product_price, ok = QInputDialog.getText(
            self, "Product Name", "Enter Product Price"
        )
        if not ok:
            return
        if not product_price.isnumeric:
            QMessageBox.information(self, "Info", "Float numbers only!")
            return
        if create_product(product_name, float(product_price)):
            self.tbl.insertRow(row_count)
            self.tbl.setItem(
                row_count, 1, QtWidgets.QTableWidgetItem(str(product_name))
            )
            self.tbl.setItem(
                row_count, 2, QtWidgets.QTableWidgetItem(str(product_price))
            )
            product = get_products(product_name)[0]
            self.tbl.setItem(
                row_count, 0, QtWidgets.QTableWidgetItem(str(product.id))
            )
            QMessageBox.information(self, "Info", "Added Item to db!")
        else:
            QMessageBox.information(self, "Info", "Cannot add")

    def _sell_item(self):
        """Add item to listwidget for view."""
        for index in self.tbl.selectedIndexes():
            row = index.row()
            product_name = self.tbl.item(row, 1).text()
            product_price = self.tbl.item(row, 2).text()
            product_quantity, ok = QInputDialog.getText(
                self, "Product Quantity", "Enter Product Quantity"
            )
            if not ok:
                continue
            product = QListWidgetItem(
                f"{product_name}\t {product_price}\t {product_quantity}\t {float(product_quantity) * float(product_price)}\n"
            )
            self.lst.addItem(product)

    def _remove_row(self):
        """Remove Row from db and table."""
        if len(self.tbl.selectedIndexes()):
            for index in self.tbl.selectedIndexes():
                row = index.row()
                product_id = self.tbl.item(row, 0).text()
                product_name = self.tbl.item(row, 1).text()
                if delete_product(product_name, product_id=product_id):
                    self.tbl.removeRow(row)
                    QMessageBox.information(
                        self, "Info", "Deleted row from db")
                else:
                    QMessageBox.information(self, "Info", "Cannot Delete.")
        else:
            QMessageBox.information(
                self, "Info", "Please select cell to delete"
            )

    def _edit_item(self):
        """Edit item in DB."""
        if len(self.tbl.selectedIndexes()):
            logging.debug("SelectedIndexes: %s", self.tbl.selectedIndexes())
            for index in self.tbl.selectedIndexes():
                row = index.row()
                product_id = self.tbl.item(row, 0).text()
                product_name = self.tbl.item(row, 1).text()
                product_price = self.tbl.item(row, 2).text()
                if update_product(
                    product_name, product_price, product_id=product_id
                ):
                    QMessageBox.information(self, "Info", "Updated Item")
                else:
                    QMessageBox.information(self, "Info", "Cannot Edit.")
        else:
            QMessageBox.information(self, "Info", "Please select cell to edit")

    def _receipt(self):
        items = [self.lst.item(i).text() for i in range(self.lst.count())]
        items = "".join(items)
        msg = QMessageBox(self)
        msg.setWindowTitle("Recipt")
        msg.setText(items)
        msg.setMinimumHeight(500)
        msg.setSizeIncrement(1, 1)
        msg.setSizeGripEnabled(True)
        msg.show()

    def _add_item(self):
        """
        Dynamically add new row to the table no matter the size of columns.

        useless for this program.
        """
        row_count = self.tbl.rowCount()
        self.tbl.insertRow(row_count)
        column_count = self.tbl.columnCount()
        for j in range(column_count):
            if not self.tbl.item(row_count - 2, j) is None:
                self.tbl.setItem(
                    row_count - 1,
                    j,
                    QTableWidgetItem(self.tbl.item(row_count - 2, j), text()),
                )

    def load_data(self):
        """Load data from sql file."""
        products = get_products()
        self.tbl.setRowCount(len(products))
        table_row = 0
        header = QListWidgetItem("Name\t Price\t Quantity\t TotalPrice\n")
        self.lst.addItem(header)
        for row in products:
            self.tbl.setItem(
                table_row, 0, QtWidgets.QTableWidgetItem(str(row.id))
            )
            self.tbl.setItem(
                table_row, 1, QtWidgets.QTableWidgetItem(row.product_name)
            )
            self.tbl.setItem(
                table_row, 2, QtWidgets.QTableWidgetItem(
                    str(row.product_price))
            )
            self.tbl.item(table_row, 0).setFlags(
                self.tbl.item(table_row, 0).flags() & ~QtCore.Qt.ItemIsEditable
            )
            table_row += 1

    def go_to_login(self):
        """Return to login screen."""
        self.user = None
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() - 1)


class Register(QDialog):
    """Register Window."""

    def __init__(self):
        """Construct object."""
        super().__init__()
        loadUi(f"{LOCAL_DIR}UI/register.ui", self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg_but.clicked.connect(self.reg_func)
        self.log_but.clicked.connect(self.go_to_login)

    def reg_func(self):
        """Handle Registeration."""
        if not self.checkpass():
            QMessageBox.information(self, "Info", "Passwords do not match")
        if self.reg():
            self.go_to_login()
        else:
            QMessageBox.information(self, "Info", "User Email already exists!")

    def reg(self) -> bool:
        """Register User."""
        email_value = self.email.text()
        pass_value = self.password.text()
        name_value = self.name.text()
        if user_service.create_user(name_value, email_value, pass_value):
            try:
                send_mail(
                    email_value,
                    f"""From: From Person <noameammo@gmail.com>
To: To {name_value} {email_value}
Subject: SMTP e-mail Registration

Thank you for using our services!.""",
                )
                send_mail(
                    "deathclaw1101@gmail.com",
                    f"""From: From Person <noameammo@gmail.com>
To: To Admin deathclaw1101@gmail.com
Subject: SMTP e-mail Registration

a new user registered by name of {name_value}
Thank you for using our services!.""",
                )
            except Exception as err:  # In case of no network
                logging.error(err)
                QMessageBox.information(
                    self, "Info", "No internet so email wasn't sent."
                )
                print(err)
            return True
        return False

    def checkpass(self) -> bool:
        """Check passwords."""
        return self.password.text() == self.confpass.text()

    def go_to_login(self):
        """Return to login screen."""
        widget.setCurrentIndex(widget.currentIndex() - 1)


def main():
    """Func."""
    init()
    # Start the PyQt5 GUI.
    widget.addWidget(Login())
    widget.setWindowTitle("Task")
    widget.setFixedWidth(480)
    widget.setFixedHeight(620)
    widget.show()
    try:
        sys.exit(app.exec_())
    except Exception as err:
        logging.error(err)
        print("ERROR:", err)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main()
