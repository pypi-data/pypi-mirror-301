"""
iogp.gui.qtwidgets: Custom Qt widgets.

Author: Vlad Topan (vtopan/gmail)
"""
import ast
import functools
import html
import threading
import re
import time

from .qt import (Qt, QTextBrowser, QFontMetrics, QLineEdit, QTextEdit, QHBoxLayout, QLabel,
        QComboBox, QWidget, QPushButton, Signal)
from .qthexed import VHexEditor, VBinViewer



class VMessageLog(QTextBrowser):

    def __init__(self, *args, rows=4, hint='Log messages', log_timestamps=False,
                open_external_links=True, **kwargs):
        # todo: more flexible style control
        super().__init__(*args, **kwargs)
        self.setStyleSheet('QScrollBar:vertical {width: 10px;}')
        self.setPlaceholderText(hint)
        self.setReadOnly(1)
        if rows:
            rowheight = QFontMetrics(self.font()).lineSpacing()
            self.setFixedHeight(10 + rows * rowheight)
        self.setOpenExternalLinks(open_external_links)
        self.lock = threading.Lock()
        self.log_timestamps = log_timestamps

    def log(self, msg, escape=True):
        """
        Log a message.
        """
        self.lock.acquire()
        if escape:
            msg = html.escape(msg)
        if msg.startswith('[DEBUG]'):
            msg = f'<font color="#444">{msg}</font>'
        elif msg.startswith('[ERROR]') or msg.startswith('[CRASH]'):
            msg = f'<font color="#A00">{msg}</font>'
        if self.log_timestamps:
            msg = f'<font color="#777">{time.strftime("[%d.%m.%y %H:%M:%S]")}</font> {msg}'
        if escape:
            msg = msg.replace('\n', '<br>')
        self.append(msg)
        self.ensureCursorVisible()
        self.lock.release()



def VLabelEdit(label, value='', placeholder='', validator=None, cls=QLineEdit, cls_args=None,
            cls_kwargs=None, hint=None):
    """
    Returns a horizontal layout containing a label and an edit.

    The label and layout widgets are accessible as the `.label` / `.layout` attributes of the
    edit widget.

    :param cls: Base class for the edit component.
    :param cls_args: Positional args for the edit component initialization.
    :param cls_kwargs: Keyword args for the edit component initialization.
    """
    obj = cls(*(cls_args or []), **(cls_kwargs or {}))
    obj.label = QLabel(label)
    lay = obj.parent_layout = QHBoxLayout()
    lay.addWidget(obj.label)
    lay.addWidget(obj)
    obj.label.setBuddy(obj)
    if validator:
        obj.setValidator(validator)
    if isinstance(obj, QLineEdit):
        pass
    elif isinstance(obj, QTextEdit):
        obj.text = obj.toPlainText
        obj.setText = obj.setPlainText
    elif isinstance(obj, QComboBox):
        obj.text = obj.currentText
        obj.setText = obj.setCurrentText
    if value:
        if cls == VStarRating:
            obj.value = value
        else:
            obj.setText(value)
    if hint:
        obj.label.setToolTip(hint)
        obj.setToolTip(hint)
    if placeholder:
        obj.setPlaceholderText(placeholder)
    return obj



class VStarRating(QWidget):
    """
    Star rating widget.

    :param stars: Maximum number of stars.
    :param value: Initial value.
    :param hint: Per-widget hint (tooltip).
    :param hints: List of per-star hints (tooltips) of `stars` length.
    """
    valueChanged = Signal()

    def __init__(self, *args, value=0, label=None, stars=5, size=16, highlight_color='#FF0',
                hint="Right-click to set to 0.", hints=None, symbol='★', **kwargs):
        super().__init__(*args, **kwargs)
        self.stars = stars
        self.size = size
        self.highlight_color = highlight_color
        self.label = QLabel(label) if label else None
        self.buttons = [QPushButton(symbol) for i in range(stars)]
        self.lay = QHBoxLayout()
        self.button_lay = QHBoxLayout()
        self.button_lay.setSpacing(0)
        if self.label:
            self.lay.addWidget(self.label)
            if hint:
                self.label.setToolTip(hint)
        if hint:
            self.setToolTip(hint)
        for i, button in enumerate(self.buttons):
            self.button_lay.addWidget(button)
            button.clicked.connect(functools.partial(self.setValue, i + 1))
            button.setObjectName(f'star_rating_{hex(id(button))[2:]}')
            button.setMaximumSize(size, size)
            button.mousePressEvent = functools.partial(self.right_click_handler, i, button.mousePressEvent)
            if hint or hints:
                use_hint = f'{hints[i]}\n{hint}' if (hint and hints and len(hints) > i and hints[i]) else (hint or hints[i])
                button.setToolTip(use_hint)
        self.lay.addLayout(self.button_lay)
        self.setLayout(self.lay)
        self._value = 0
        self.update_buttons()

    def value(self):
        return self._value

    def setValue(self, value):
        if value > self.stars:
            raise ValueError(f'Invalid value {value} for {self.stars}-star widget!')
        old_value = self._value
        self._value = value
        self.update_buttons()
        if old_value != value:
            self.valueChanged.emit()

    def right_click_handler(self, index, original_handler, event):
        """
        Handle right-clicks on stars to reset to 0.
        """
        if event.button() == Qt.RightButton:
            self.setValue(0)
        else:
            original_handler(event)

    def update_buttons(self):
        """
        Update buttons according to the value.
        """
        for i in range(self.stars):
            button = self.buttons[i]
            css_marker = f'QPushButton#{button.objectName()}'
            stylesheet = button.styleSheet()
            color = f'color: {self.highlight_color};' if (i + 1) <= self._value else ''
            button_style = f'{css_marker} {{ {color} padding: 0; margin: 0; }}\n\n'
            if css_marker in stylesheet:
                stylesheet = re.sub(f'{css_marker}.+', button_style, stylesheet)
            else:
                stylesheet += '\n' + button_style
            button.setStyleSheet(stylesheet)