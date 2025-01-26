# qt-logging

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

from PySide6 import QtWidgets
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

For more examples see the `tests` directory.

## Contributing

To contribute please refer to the [Contributing Guide](CONTRIBUTING.md).

## License

MIT License. Copyright 2024 - Beat Reichenbach.
See the [License file](LICENSE) for details.
