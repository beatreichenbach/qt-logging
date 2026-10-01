# qt-logging

[![PyPI version](https://img.shields.io/pypi/v/qt-logging.svg)](https://pypi.org/project/qt-logging/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://pypi.org/project/qt-logging/)
[![License](https://img.shields.io/pypi/l/qt-logging.svg)](https://github.com/beatreichenbach/qt-logging/blob/main/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/badge/type%20checked-ty-261230.svg)](https://github.com/astral-sh/ty)

The `qt-logging` package provides widgets to display the log output to the user.
The log viewer can be used to look at filtered logging output while the log bar offers
quick access and feedback to the user.

This package uses Material Icons from
[qt-material-icons](https://github.com/beatreichenbach/qt-material-icons).

![Header](https://raw.githubusercontent.com/beatreichenbach/qt-logging/refs/heads/main/.github/assets/header.png)

![Header](https://raw.githubusercontent.com/beatreichenbach/qt-logging/refs/heads/main/.github/assets/log_bar.png)

## Installation

Install using pip:

```shell
pip install qt-logging
```

## Usage

```python
import logging

from qtpy import QtWidgets
import qt_logging

app = QtWidgets.QApplication()

widget = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
widget.setLayout(layout)
log_bar = qt_logging.LogBar()
layout.addWidget(log_bar)
widget.show()

logging.error('Something went wrong!')
app.exec()
```

For more examples see the `examples` directory.

## Contributing

To contribute please refer to the [Contributing Guide](CONTRIBUTING.md).

## License

MIT License. Copyright 2024 - Beat Reichenbach. See the [License file](LICENSE) for details.
