import logging

from qtpy import QtCore, QtWidgets

from qt_logging.logger import LogCache, LogBar
from tests import application

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Widget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle('Widget')
        self.resize(QtCore.QSize(1080, 256))

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(QtCore.QMargins())
        self.setLayout(layout)

        main_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(main_layout)

        button = QtWidgets.QPushButton('Screenshot')
        button.clicked.connect(self._screenshot)
        main_layout.addWidget(button)

        layout.addStretch()

        cache = LogCache()
        root_logger = logging.getLogger()
        cache.connect_logger(root_logger)

        for i in range(100):
            logger.debug('debug')
            logger.error('error')
            logger.info('info')
            logger.critical('critical')
            logger.warning('warning')

        logger2 = logging.getLogger('qt_extensions')
        for i in range(20):
            logger2.debug('debug')
            logger2.error('error')
            logger2.info('info')
            logger2.critical('critical')
            logger2.warning('warning')

        logger2.debug('<b>debug</b>')
        logger2.info('<span style="color: #ff00ff">info</span>')
        logger2.warning('<i>warning</i>')
        logger2.error('<span style="color: #00ffff">error</span>')

        self.log_bar = LogBar(cache)
        layout.addWidget(self.log_bar)

    def _screenshot(self) -> None:
        path = '../.github/assets/log_bar.png'
        pixmap = self.log_bar.grab()
        pixmap.save(path)

        viewer = self.log_bar.viewer()
        if viewer:
            path = '../.github/assets/viewer.png'
            pixmap = viewer.grab()
            pixmap.save(path)


def main() -> None:
    with application():
        widget = Widget()
        widget.show()

        widget.log_bar.show_viewer()
        viewer = widget.log_bar.viewer()
        if viewer:
            viewer.resize(1080, 480)

        logging.debug('debug')
        logging.error('error')
        logging.info('info')
        logging.critical('critical')
        logging.warning('warning')
        try:
            a = 1 / 0
            logger.info(a)
        except ZeroDivisionError as e:
            logging.exception(e)


if __name__ == '__main__':
    main()
