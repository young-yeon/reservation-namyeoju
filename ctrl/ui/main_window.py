"메인화면 (일정선택~)"
from datetime import date
import re

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from selenium.common.exceptions import NoAlertPresentException

from .time_parser import parser

form_class = uic.loadUiType("view/mainWindow.ui")[0]


class MainWindow(QMainWindow, form_class):
    "일정 조회하고 결정하는 화면(UI: mainWindow.ui)"

    def __init__(self, Macro, parent=None):
        self.macro = Macro
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.hide()
        self.set_today()
        self.searchButton.clicked.connect(self.search_time)
        # 예약 가능 시간 리스트
        self.data = list()
        # 예약 예정 시간
        # ['연(yyyy)', '월(MM)', '일(dd)', '시(hh)', '분(mm)', '초(ss)']
        self.target_time = None

    def set_today(self):
        "오늘 날짜로 설정"
        today = date.today()
        self.targetDate.setMinimumDate(today)

    def search_time(self):
        "예약 가능 시간 검색"
        target = self.targetDate.date().toString("yyyyMMdd")
        self.macro.driver.get(
            "https://www.namyeoju.co.kr/Reservation/Reservation.aspx?SelectedDate="+target)
        self.data = parser(self.macro.driver.page_source)
        for row in self.data:
            self.targetList.addItem(row[0])
        self.targetList.itemClicked.connect(self.load_resv)

    def load_resv(self):
        "예약 가능 시간 조회"
        current = self.targetList.currentRow()
        self.macro.driver.execute_script(self.data[current][1])
        try:
            result = self.macro.driver.switch_to_alert()
            self.target_time = re.findall(r'\d+', result.text)
            result.accept()
        except NoAlertPresentException:
            self.target_time = None


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(__import__('sys').argv)
    myWindow = MainWindow(0)
    myWindow.show()
    app.exec_()
