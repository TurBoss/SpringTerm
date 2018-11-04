import sys
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QTextEdit, \
    QHBoxLayout, QBoxLayout, QSizePolicy, QScrollArea
from PyQt5 import QtNetwork, QtCore


class MyApp(QWidget):
    threadSignal = pyqtSignal(object)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.tcpClient = None

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('SpringTerm')

        self.layout = QVBoxLayout(self)

        self.open_button = QPushButton("Connect")
        self.open_button.clicked.connect(self.startAq)
        self.open_button.setEnabled(True)

        self.close_button = QPushButton("Disconnect")
        self.close_button.clicked.connect(self.stopAq)
        self.close_button.setEnabled(False)

        self.button_layout = QHBoxLayout(self)

        self.button_layout.addWidget(self.open_button)
        self.button_layout.addWidget(self.close_button)

        self.layout.addLayout(self.button_layout)

        self.list_layout = QHBoxLayout()

        self.list_widget = QListWidget(self)
        self.history_widget = QListWidget(self)
        self.history_widget.clicked.connect(self.history_clicked)

        self.list_layout.addWidget(self.history_widget)
        self.list_layout.addWidget(self.list_widget)

        self.layout.addLayout(self.list_layout)

        self.prompt_widget = QTextEdit()

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send)
        self.send_button.setEnabled(False)

        self.prompt_layout = QHBoxLayout(self)

        self.prompt_layout.addWidget(self.prompt_widget)
        self.prompt_layout.addWidget(self.send_button)

        self.layout.addLayout(self.prompt_layout)

        self.threadPool = []
        self.measure = True

        self.threadSignal.connect(self.add)

    def add(self, text):
        """ Add item to list widget """
        self.list_widget.addItem(text)
        self.list_widget.sortItems()

    def store(self, text):
        """ Add item to list widget """
        self.history_widget.addItem(text)
        self.history_widget.sortItems()

    def getData(self, delay=0.3):
        '''
        """ Add several items to list widget """
        while self.measure:
            self.threadSignal.emit('hallo')
            time.sleep(delay)  # artificial time delay
        '''
        self.add(self.tcpClient.readLine(1024).decode().rstrip())

    def startAq(self):
        # Network stuff

        self.tcpClient = QtNetwork.QTcpSocket()
        self.tcpClient.connectToHost('springrts.com', 8200)
        self.tcpClient.readyRead.connect(self.getData)
        self.tcpClient.error.connect(lambda x: print(x))

        self.open_button.setEnabled(False)
        self.send_button.setEnabled(True)
        self.close_button.setEnabled(True)

    def send(self):

        text = self.prompt_widget.toPlainText()

        self.store(text)
        self.tcpClient.write('{}\n'.format(text).encode())

    def stopAq(self):
        self.measure = False
        self.tcpClient.close()

        self.send_button.setEnabled(False)
        self.close_button.setEnabled(False)
        self.open_button.setEnabled(True)

    def history_clicked(self, index):
        self.prompt_widget.setText("")
        text = self.history_widget.currentItem().text()

        self.prompt_widget.setText(text)



    def displayError(self, socketError):
        if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QMessageBox.information(self, "Fortune Client",
                                    "The host was not found. Please check the host name and "
                                    "port settings.")
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QMessageBox.information(self, "Fortune Client",
                                    "The connection was refused by the peer. Make sure the "
                                    "fortune server is running, and check that the host name "
                                    "and port settings are correct.")
        else:
            QMessageBox.information(self, "Fortune Client",
                                    "The following error occurred: %s." % self.tcpSocket.errorString())


class GenericWorker(QObject):
    start = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, function, *args, **kwargs):
        super(GenericWorker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

    @pyqtSlot(str)
    def run(self, *args, **kwargs):
        self.function(*self.args, **self.kwargs)
        self.finished.emit()


if __name__ == '__main__':
    # run
    app = QApplication(sys.argv)
    test = MyApp()
    test.show()
    app.exec_()
