import sys
import json
from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QTextBrowser
from PyQt5 import uic
from PyQt5.QtCore import QDate


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('app.ui', self)
        self.calendarWidget.clicked[QDate].connect(self.show_actual_page)
        self.pushButton_save.clicked.connect(self.save_text)
        self.pushButton_clear.clicked.connect(self.clear_text)

    def save_text(self):
        date = self.calendarWidget.selectedDate().toString()
        diary_date[date] = self.textBrowser.toPlainText()

    def clear_text(self):
        self.textBrowser.setText('')

    def show_actual_page(self):
        date = self.calendarWidget.selectedDate().toString()
        try:
            self.textBrowser.setText(diary_date[date])
        except KeyError:
            diary_date[date] = ''
            self.textBrowser.setText(diary_date[date])


if __name__ == '__main__':
    with open('data.json') as f:
        diary_date = json.load(f)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    try:    
        sys.exit(app.exec())
    except SystemExit:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(diary_date, f)
