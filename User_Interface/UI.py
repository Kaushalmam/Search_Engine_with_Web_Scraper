import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QTextBrowser,QVBoxLayout
from PyQt5.QtCore import pyqtSlot

from tfidf import get_search_result

'''
A simple UI displays user a query input and the results of the query search engine
'''

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'UIC search Engine'
        self.left = 500
        self.top = 500
        self.width = 1200
        self.height = 700
        self.initUI()
        self.results_page = 10

    def initUI(self):
        self.setWindowTitle(self.title)
        html='<h1>WELCOME</h1>'
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(1500, 990)
        self.textbox.resize(500, 60)
        self.textbox.setToolTip("Enter Your Query here")
        self.textbox.setStyleSheet("background: white")
        

        # Create a button in the window
        self.button = QPushButton('Search UIC', self)
        self.button.move(2100, 1000)
        self.button.resize(200,50)
        self.button.setStyleSheet('color: white; background: blue')
        
        
        # connect TextView to function on_click
        self.button.clicked.connect(self.on_click)
        self.result_view = QTextBrowser(self)
        # self.result_view.setReadOnly(True)
        self.result_view.move(1400, 1100)
        self.result_view.resize(800, 500)
        self.result_view.setStyleSheet("background: white")
        self.result_view.hide()
        self.next10 = QPushButton('Search More results....', self)
        self.next10.move(1500, 1650)
        self.next10.resize(300, 50)
        self.next10.setStyleSheet('color: white; background: blue')
        self.next10.clicked.connect(self.on_click_label)
        self.next10.hide()
        self.result_view.append(html)
        self.setStyleSheet("background-image: url(p.jpg); background-repeat: no-repeat; background-position: center; background-attachment: stretch")
        self.showFullScreen()

    @pyqtSlot()
    def on_click(self):
        self.results_page = 10
        query = self.textbox.text()
        search_result = get_search_result(query, 500)
        display_html = '<p>Following are the relavant links</p>'
        self.url_list = []
        for url in search_result:

            display_html += self.add_href(url)
            self.url_list.append(self.add_href(url))

        urls = ''.join(self.url_list[:self.results_page])
        self.result_view.setText(urls)
        self.result_view.setOpenExternalLinks(True)
        # self.result_view.show()
        self.next10.setText('Show more Results....')
        self.next10.show()

        self.setStyleSheet("background-image: url(p.jpg); background-repeat: no-repeat; background-position: center; background-attachment: stretch")

        self.result_view.show()

        self.result_view.textCursor().insertHtml(display_html)
        self.result_view.append(display_html)

    def add_href(self, url):
        return '<a href="' + url + '">' + url + '</a><br><br>'

    @pyqtSlot()
    def on_click_label(self):
        self.results_page = self.results_page + 10
        self.result_view.setText(''.join(self.url_list[:self.results_page]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    
    sys.exit(app.exec_())
