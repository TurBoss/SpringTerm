import sys
import os

import socket

from qtpy.QtCore import Qt, QObject, Signal, Slot, Property
from qtpy.QtGui import QGuiApplication
from qtpy.QtQml import QQmlApplicationEngine


class Manager(QObject):
    connectionEnabled = Signal()
    connectionDisable = Signal()
    promptAccept = Signal()

    def __init__(self):
        super(Manager, self).__init__()

        self.sock = None

        self.m_connection = False
        self.m_prompt = ""
        self.promptAccept.connect(self.on_promptAccept)
        self.connectionEnabled.connect(self.on_connectionEnabled)

    """
    Enable
    """

    @Property(bool, notify=connectionEnabled)
    def connection(self):
        return self.m_connection

    @connection.setter
    def setConnetion(self, val):
        print(val)
        if self.m_connection == val:
            return
        self.m_connection = val
        if self.m_connection:
            self.connectionEnabled.emit()
        else:
            self.connectionDisable.emit()

    @Slot()
    def on_connectionEnabled(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ("springrts.com", 8200)
        print('connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)


    @Slot()
    def on_connectionDisabled(self):
        # Create a TCP/IP socket
        print("close connection")
        self.sock.close()

    """
    Prompt
    """

    @Property(str, notify=promptAccept)
    def prompt(self):
        return self.m_prompt

    @prompt.setter
    def setPrompt(self, val):
        self.m_prompt = val
        self.promptAccept.emit()

    @Slot()
    def on_promptAccept(self):
        print(self.m_prompt)

        # Send data
        message = bytes(self.m_prompt.encode("utf-8"))
        print('sending {!r}'.format(message))
        self.sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = self.sock.recv(16)
            amount_received += len(data)
            print('received {!r}'.format(data))


if __name__ == "__main__":

    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    manager = Manager()
    ctx = engine.rootContext()
    ctx.setContextProperty("Manager", manager)
    engine.load('main.qml')
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
