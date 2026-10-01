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


def test_log_bar_formatter(app: QtWidgets.QApplication) -> None:
    bar = LogBar()
    formatter = logging.Formatter('{message}', style='{')
    bar.set_formatter(formatter)
    assert bar.formatter() is formatter


def test_log_viewer_formatter(app: QtWidgets.QApplication) -> None:
    viewer = LogViewer()
    formatter = logging.Formatter('{message}', style='{')
    viewer.set_formatter(formatter)
    assert viewer.formatter() is formatter


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


def test_log_viewer_state_is_copy(app: QtWidgets.QApplication) -> None:
    viewer = LogViewer()
    viewer.set_levels((logging.ERROR,))

    state = viewer.state()
    state['levels'].add(logging.DEBUG)
    state['names'].add('package')

    assert viewer.levels() == (logging.ERROR,)
    assert viewer.names() == ()


def test_log_viewer_name_matching(app: QtWidgets.QApplication) -> None:
    viewer = LogViewer()
    viewer.set_levels((logging.ERROR,))
    viewer.set_names(['package'])

    viewer.add_record(make_record(logging.ERROR, 'exact', name='package'))
    viewer.add_record(make_record(logging.ERROR, 'child', name='package.module'))
    viewer.add_record(make_record(logging.ERROR, 'sibling', name='packager'))

    text = viewer.text_edit.toPlainText()
    assert 'exact' in text
    assert 'child' in text
    assert 'sibling' not in text


def test_log_bar_name_matching(app: QtWidgets.QApplication) -> None:
    cache = LogCache()
    bar = LogBar(cache)
    bar.set_names(['package'])

    cache.add(make_record(logging.ERROR, 'child', name='package.module'))
    assert bar.message_line.text() == '[ERROR] child'

    cache.add(make_record(logging.ERROR, 'sibling', name='packager'))
    assert bar.message_line.text() == '[ERROR] child'


def test_log_cache_connect_once_and_close(app: QtWidgets.QApplication) -> None:
    logger = logging.getLogger('qt_logging_test_cache')
    logger.setLevel(logging.DEBUG)
    cache = LogCache()

    cache.connect_logger(logger)
    cache.connect_logger(logger)
    logger.error('first')
    assert len(cache.records()) == 1

    cache.close()
    logger.error('second')
    assert len(cache.records()) == 1


def test_log_bar_set_cache_replaces(app: QtWidgets.QApplication) -> None:
    first = LogCache()
    second = LogCache()
    bar = LogBar(first)
    bar.set_names(['package'])
    bar.set_cache(second)

    first.add(make_record(logging.ERROR, 'old', name='package'))
    assert bar.message_line.text() == ''

    second.add(make_record(logging.ERROR, 'new', name='package'))
    assert bar.message_line.text() == '[ERROR] new'
