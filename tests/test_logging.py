from __future__ import annotations

import logging
from pathlib import Path

from qtpy import QtWidgets

from qt_logging import SUCCESS, LogBar, LogCache, LogViewer


def make_record(
    level: int, message: str = 'message', name: str = 'test'
) -> logging.LogRecord:
    return logging.LogRecord(name, level, __file__, 1, message, None, None)


def test_log_cache_add_and_clear(app: QtWidgets.QApplication) -> None:
    cache = LogCache()
    record = make_record(logging.INFO)

    cache.add(record)
    assert cache.records() == (record,)

    cache.clear()
    assert cache.records() == ()


def test_log_cache_save(app: QtWidgets.QApplication, tmp_path: Path) -> None:
    cache = LogCache()
    cache.add(make_record(logging.ERROR, 'boom'))

    path = tmp_path / 'log.txt'
    cache.save(str(path))
    assert 'boom' in path.read_text(encoding='utf-8')


def test_log_bar_show_message(app: QtWidgets.QApplication) -> None:
    bar = LogBar()
    bar.show_message('hello', level=logging.ERROR)
    assert bar.message_line.text() == 'hello'


def test_log_bar_success_level(app: QtWidgets.QApplication) -> None:
    bar = LogBar()
    bar.show_message('done', level=SUCCESS)
    assert bar.message_line.text() == 'done'


def test_log_bar_level_filter(app: QtWidgets.QApplication) -> None:
    bar = LogBar()
    bar.set_level(logging.ERROR)
    bar.show_message('info', level=logging.INFO)
    assert bar.message_line.text() == ''


def test_log_bar_names(app: QtWidgets.QApplication) -> None:
    bar = LogBar()
    bar.set_names(['package'])
    assert bar.names() == ('package',)


def test_log_viewer_levels(app: QtWidgets.QApplication) -> None:
    viewer = LogViewer()
    viewer.set_levels((logging.ERROR,))
    assert viewer.levels() == (logging.ERROR,)


def test_log_viewer_names(app: QtWidgets.QApplication) -> None:
    viewer = LogViewer()
    viewer.set_names(['package'])
    assert viewer.names() == ('package',)


def test_log_viewer_state_roundtrip(app: QtWidgets.QApplication) -> None:
    viewer = LogViewer()
    viewer.set_levels((logging.INFO,))
    viewer.set_names(['package'])

    other = LogViewer()
    other.set_state(viewer.state())
    assert set(other.levels()) == {logging.INFO}
    assert other.names() == ('package',)
