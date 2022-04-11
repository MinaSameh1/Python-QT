# class TableWidget(QTableWidget):
#     def __init__(self):
#         super().__init__(1, 3)
#         self.setHorizontalHeaderLabels(["id", "product_name", "product_price"])
#         self.verticalHeader().setDefaultSectionSize(50)
#         self.horizontalHeader().setDefaultSectionSize(250)
#         self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
#
#     def _add_row(self):
#         row_count = self.rowCount()
#         self.insertRow(row_count)
#
#     def _remove_row(self):
#         if self.rowCount() > 0:
#             self.removeRow(self.rowCount() - 1)
#
#     def _add_item(self):
#         row_count = self.rowCount()
#         self.insertRow(row_count)
#         column_count = self.columnCount()
#         for j in range(column_count):
#             if not self.item(row_count - 2, j) is None:
#                 self.setItem(
#                     row_count - 1,
#                     j,
#                     QTableWidgetItem(self.item(row_count - 2, j), text()),
#                 )
#
#
