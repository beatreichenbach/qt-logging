# Contributing Guide

## Development

To get started:

```sh
uv venv --python 3.13
uv pip install -e ".[dev]"
pre-commit install
```

Run the checks:

```sh
ruff format qt_logging examples tests
ruff check --select I --fix qt_logging examples tests
ruff check qt_logging examples tests
ty check
pytest
```

### Updating Icons

The material icons are vendored into `qt_logging/qt_material_icons` with
[qt-material-icons]. To regenerate them after adding or removing an icon, run:

```sh
uv run qtmaterialicons -o qt_logging --names \
    article \
    backspace \
    check_box \
    check_box_outline_blank \
    check_circle \
    close \
    error \
    filter_alt \
    report \
    save \
    warning \
    wrap_text
```

[qt-material-icons]: https://github.com/beatreichenbach/qt-material-icons

### Releasing Changes

To version up using [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release):

```sh
semantic-release version
```
