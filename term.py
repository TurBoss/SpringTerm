import sys
import os

import logging
import asyncio
import yaml

from asyncspring import spring

from qtpy.QtCore import Qt, QObject, Signal, Slot, Property, QAbstractItemModel, QModelIndex, QUrl
from qtpy.QtGui import QGuiApplication
from qtpy.QtQml import QQmlApplicationEngine

from quamash import QEventLoop, QThreadExecutor

FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)"

logging.basicConfig(filename='spring-term.log', level=logging.DEBUG, format=FORMAT)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger(__name__)


class Application(QGuiApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainWindow = MainWindow(self)

    def start(self):
        self.mainWindow.show()


class MainWindow(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.engine = QQmlApplicationEngine(self)

        manager = Manager()

        ctx = self.engine.rootContext()
        ctx.setContextProperty('Manager', manager)

        self.engine.quit.connect(parent.quit)
        self.engine.load(QUrl.fromLocalFile(os.path.join('ui', 'main.qml')))

        self.window = self.engine.rootObjects()[0]

    def show(self):
        self.window.show()



class Manager(QObject):
    connectionEnabled = Signal()
    connectionDisable = Signal()
    promptAccept = Signal()

    def __init__(self):
        super(Manager, self).__init__()

        with open("config.yaml", 'r') as yml_file:
            self.cfg = yaml.load(yml_file)

        self.lobby_client = None

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
    async def setConnetion(self, val):
        log.debug(val)
        if self.m_connection == val:
            return
        self.m_connection = val
        if self.m_connection:
            await self.connectionEnabled.emit()
        else:
            self.connectionDisable.emit()

    @Slot()
    async def on_connectionEnabled(self):
        # Create a TCP/IP socket
        log.debug("open connection")
        self.lobby_client = await spring.connect(self.cfg["lobby"]["host"], port=self.cfg["lobby"]["port"])


    @Slot()
    def on_connectionDisabled(self):
        # Create a TCP/IP socket
        log.debug("close connection")

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
        log.debug(self.m_prompt)









#
#

#
#
# if __name__ == "__main__":
#
#     app = QGuiApplication(sys.argv)
#     loop = QEventLoop(app)
#     asyncio.set_event_loop(loop)
#
#     engine = QQmlApplicationEngine()
#     manager = Manager()
#     ctx = engine.rootContext()
#     ctx.setContextProperty("Manager", manager)
#     engine.load(os.path.join('ui', 'main.qml'))
#     if not engine.rootObjects():
#         sys.exit(-1)
#
#
#     log.debug("INIT")
#     with loop:  ## context manager calls .close() when loop completes, and releases all resources
#         loop.run_forever()
