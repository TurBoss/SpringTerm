import os
import sys
import time

import yaml


from PyQt5 import QtNetwork
from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QHBoxLayout,\
    QLineEdit


class SpringTerm(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.tcpClient = QtNetwork.QTcpSocket()
        self.tcpClient.readyRead.connect(self.getData)
        self.tcpClient.error.connect(self.displayError)

        with open("config.yaml") as yml_file:
            self.cfg = yaml.load(yml_file)

        host = self.cfg["server"]["host"]
        port = str(self.cfg["server"]["port"])

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('SpringTerm')

        self.layout = QVBoxLayout(self)

        self.server_layout = QHBoxLayout(self)

        self.server_widget = QLineEdit(host)
        self.port_widget = QLineEdit(port)

        self.server_layout.addWidget(self.server_widget)
        self.server_layout.addWidget(self.port_widget)

        self.layout.addLayout(self.server_layout)

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

        self.list_layout = QHBoxLayout(self)

        self.list_widget = QListWidget(self)
        self.history_widget = QListWidget(self)
        self.history_widget.clicked.connect(self.history_clicked)

        self.list_layout.addWidget(self.history_widget)
        self.list_layout.addWidget(self.list_widget)

        self.layout.addLayout(self.list_layout)

        self.prompt_widget = QLineEdit()

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send)
        self.send_button.setEnabled(False)

        self.prompt_layout = QHBoxLayout(self)

        self.prompt_layout.addWidget(self.prompt_widget)
        self.prompt_layout.addWidget(self.send_button)

        self.layout.addLayout(self.prompt_layout)

    def add(self, text):
        """ Add item to list widget """
        self.list_widget.addItem(text)

    def store(self, text):
        """ Add item to history widget """
        self.history_widget.addItem(text)

    def getData(self):

        while self.tcpClient.bytesAvailable():
                   
            received_data = self.tcpClient.readLine(1024)

            if received_data:
                self.add(received_data.decode().rstrip())

    def send(self):
        text = self.prompt_widget.text()
        self.store(text)
        self.tcpClient.write('{}'.format(text).encode())

    def startAq(self):
        # Network stuff

        host = self.server_widget.text()
        port = int(self.port_widget.text())

        self.tcpClient.connectToHost(host, port)

        self.open_button.setEnabled(False)
        self.send_button.setEnabled(True)
        self.close_button.setEnabled(True)

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
            QMessageBox.information(self, "SpringTerm",
                                    "The remote host closed the connection")
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QMessageBox.information(self, "SpringTerm",
                                    "The host was not found. Please check the host name and "
                                    "port settings.")
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QMessageBox.information(self, "SpringTerm",
                                    "The connection was refused by the peer. Make sure the "
                                    "spring server is running, and check that the host name "
                                    "and port settings are correct.")
        else:
            QMessageBox.information(self, "SpringTerm",
                                    "The following error occurred: %s." % self.tcpSocket.errorString())

if __name__ == '__main__':
    # run
    app = QApplication(sys.argv)
    style_file = QFile("style.qss")
    style_file.open(QIODevice.ReadOnly)
    app.setStyleSheet(((style_file.readAll()).data()).decode("utf-8"))

    term = SpringTerm()
    term.show()
    app.exec_()
