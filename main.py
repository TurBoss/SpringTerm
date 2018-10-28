import sys
import asyncio

from quamash import QEventLoop
from term import Application

try:
    # handle ctrl+c on Linux
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
except ImportError:
    pass


if __name__ == '__main__':
    app = Application(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    app.start()
    sys.exit(loop.run_forever())
