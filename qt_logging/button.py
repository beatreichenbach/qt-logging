from __future__ import annotations

from qtpy import QtCore, QtGui, QtWidgets

from .qt_material_icons import MaterialIcon

ColorRole = QtGui.QPalette.ColorRole
ColorGroup = QtGui.QPalette.ColorGroup


class CheckBoxButton(QtWidgets.QPushButton):
    def __init__(self, text: str = '', parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(text, parent)

        self._icon_size = self.iconSize().width()
        self._icon_on: QtGui.QIcon | QtGui.QPixmap | None = None
        self._icon_off: QtGui.QIcon | QtGui.QPixmap | None = None
        self._palette_on: QtGui.QPalette | None = None
        self._palette_off: QtGui.QPalette | None = None
        self._contents_margins = QtCore.QSize(int(0.5 * self._icon_size), 0)

        self.toggled.connect(self._checked_change)
        self.setCheckable(True)
        self.setIcon(MaterialIcon('check_box_outline_blank', fill=True))
        self.setIcon(MaterialIcon('check_box'), True)

    def sizeHint(self) -> QtCore.QSize:
        size_hint = super().sizeHint()
        size_hint += self._contents_margins
        return size_hint

    def setIcon(self, icon: QtGui.QIcon | QtGui.QPixmap, on: bool = False) -> None:
        if on:
            if self._palette_on and isinstance(icon, MaterialIcon):
                icon.set_color(self._palette_on.color(ColorRole.ButtonText))
            self._icon_on = icon
        else:
            self._icon_off = icon
            super().setIcon(icon)

    def set_color(self, color: QtGui.QColor | None) -> None:
        palette = self.palette()

        if color is None:
            button_color = QtGui.QPalette().color(ColorRole.Button)
            text_color = QtGui.QPalette().color(ColorRole.ButtonText)
        else:
            button_color = color.darker(110)
            text_color = palette.color(ColorRole.ButtonText)
            if text_color.valueF() > button_color.valueF() * 0.5:
                text_color = text_color.lighter(150)
            else:
                text_color = text_color.darker(150)

        disabled_color = button_color.darker(150)
        palette.setColor(ColorRole.Button, button_color)
        palette.setColor(ColorGroup.Disabled, ColorRole.Button, disabled_color)
        palette.setColor(ColorGroup.Normal, ColorRole.ButtonText, text_color)

        self._palette_on = palette
        self._palette_off = QtGui.QPalette(palette)
        self._update_color()

    def _checked_change(self, checked: bool) -> None:
        # BUG: fusion style does not recognize On/Off for QIcons
        # https://bugreports.qt.io/browse/QTBUG-82110
        icon = self._icon_on if checked else self._icon_off
        if icon is not None:
            super().setIcon(icon)
        self._update_color()

    def _update_color(self) -> None:
        if self._palette_on is None:
            return
        if self.isChecked():
            self.setPalette(self._palette_on)
        elif self._palette_off is not None:
            self.setPalette(self._palette_off)
