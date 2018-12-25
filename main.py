import sys
import json
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextBrowser, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QDateTimeEdit, QListWidget
from PyQt5 import uic
from PyQt5.QtCore import QDate



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('app.ui', self)
        self.init_list()

        self.calendarWidget.clicked[QDate].connect(self.show_actual_page)
        self.pushButton_save.clicked.connect(self.save_text)
        self.pushButton_clear.clicked.connect(self.clear_text)
        self.pushButton_add.clicked.connect(self.add_to_do)
        self.pushButton_delete.clicked.connect(self.delete_to_do)

    def save_text(self):
        actual_date = self.calendarWidget.selectedDate().toString()
        date['diary'][actual_date] = self.textBrowser.toPlainText()

    def clear_text(self):
        self.textBrowser.setText('')

    def show_actual_page(self):
        actual_date = self.calendarWidget.selectedDate().toString()
        try:
            self.textBrowser.setText(date['diary'][actual_date])
        except KeyError:
            date['diary'][actual_date] = ''
            self.textBrowser.setText(date['diary'][actual_date])

    def add_to_do(self):
        text = self.textBrowser_2.toPlainText()
        number = self.listWidget.count() + 1
        self.listWidget.addItem(f'{number}) ' + text)
        date['to_do_list'].append(text)

    def delete_to_do(self):
        text = self.listWidget.takeItem(self.listWidget.currentRow()).text()
        number = ''
        for elem in text:
            if elem == ' ':
                break
            else:
                number += elem

        date['to_do_list'].pop(date['to_do_list'].index(text[len(number) + 1:]))

    def init_list(self):
        for elem in date['to_do_list']:
            number = self.listWidget.count() + 1
            self.listWidget.addItem(f'{number}) ' + elem)


if __name__ == '__main__':
    with open('data.json') as f:
        date = json.load(f)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    try:    
        sys.exit(app.exec())
    except SystemExit:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(date, f)
