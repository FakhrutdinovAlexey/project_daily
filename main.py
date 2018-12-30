import sys
import json
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QDateTimeEdit, QListWidget
from PyQt5 import uic
from PyQt5.QtCore import QDate


def sorting(first):
    self_date = ''
    for elem in reversed(first):
        if elem == '\n':
            break
        else:
            self_date = elem + self_date
    month, day, year = self_date.split('/')
    time = year[3:]
    hour, minute = time.split(':')
    hour = int(hour) % 12
    minute, half_of_day = minute.split(' ')
    if half_of_day == 'AM':
        half_of_day = 0
    else:
        half_of_day = 1

    year = year[:2]

    return tuple(map(int, [year, month, day, half_of_day, hour, minute]))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('app.ui', self)
        self.init_list()
        self.listWidget.setSortingEnabled(True)

        self.calendarWidget.clicked[QDate].connect(self.show_actual_page)
        self.pushButton_save.clicked.connect(self.save_text)
        self.pushButton_clear.clicked.connect(self.clear_text)
        self.pushButton_add.clicked.connect(self.add_to_do)
        self.pushButton_delete.clicked.connect(self.delete_to_do)
        self.pushButton_leadtime.clicked.connect(self.sort_by_lead_time)
        self.pushButton_addtime.clicked.connect(self.sort_by_add_time)
        self.sorted = False

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
        date_time = f'\n{self.dateTimeEdit.textFromDateTime(self.dateTimeEdit.dateTime())}'
        text = self.textBrowser_2.toPlainText() + date_time
        number = self.listWidget.count() + 1
        self.listWidget.addItem(f'{number}) ' + text)
        date['to_do_list'].append(text)
        self.textBrowser_2.setText('')

    def delete_to_do(self):
        text = self.listWidget.takeItem(self.listWidget.currentRow()).text()
        number = ''
        for elem in text:
            if elem == ' ':
                break
            else:
                number += elem
        date['to_do_list'].pop(date['to_do_list'].index(text[len(number) + 1:]))

        for _ in range(self.listWidget.count()):
            self.listWidget.takeItem(0)
        self.init_list()

        if self.sorted:
            self.sort_by_lead_time()

    def init_list(self):
        for elem in date['to_do_list']:
            number = self.listWidget.count() + 1
            self.listWidget.addItem(f'{number}) ' + elem)

    def sort_by_lead_time(self):
        copy_list = date['to_do_list'][:]
        copy_list = sorted(copy_list, key=sorting)

        for _ in range(self.listWidget.count()):
            self.listWidget.takeItem(0)

        for elem in copy_list:
            number = self.listWidget.count() + 1
            self.listWidget.addItem(f'{number}) ' + elem)
        self.sorted = True

    def sort_by_add_time(self):
        for _ in range(self.listWidget.count()):
            self.listWidget.takeItem(0)

        self.init_list()
        self.sorted = False


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
