#!/usr/bin/python3
import sys
from pathlib import Path
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

try:
    from ..settings.base import VSpacer
    from ..plugins import antidote
except (ValueError, ImportError):
    from settings.base import VSpacer
    from plugins import antidote


class PagePlugins(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        Antidote = AntidoteWindows if sys.platform.startswith("win") else AntidoteLinux
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(Terminal())
        layout.addWidget(Antidote())
        layout.addItem(VSpacer())


class Terminal(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("QTermWidget")
        linuxBox = StatusCheckBox("Linux operating system")
        pyBox = StatusCheckBox("Python bindings")
        cppBox = StatusCheckBox("C++ backend")
        cppLabel = StatusLabel("/usr/lib/libqtermwidget5.so")
        cppLabel.setVisible(not sys.platform.startswith("win"))

        libPath = "/usr/lib/libqtermwidget5.so"
        cppBox.setChecked(Path(libPath).is_file())
        linuxBox.setChecked(not sys.platform.startswith("win"))
        pyBox.setChecked("QTermWidget" in sys.modules)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(linuxBox)
        layout.addWidget(cppBox)
        layout.addWidget(cppLabel)
        layout.addWidget(pyBox)


class AntidoteLinux(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Antidote grammar tool")
        binLabel_1 = StatusLabel("/usr/local/bin/AgentConnectix")
        binLabel_2 = StatusLabel("/usr/local/bin/Antidote")
        binBox = StatusCheckBox("C++ backend")

        isInstalled = Path(antidote.getBinaryPath()).is_file()
        binBox.setChecked(isInstalled)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(binBox)
        layout.addWidget(binLabel_1)
        layout.addWidget(binLabel_2)


class AntidoteWindows(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Antidote grammar tool")
        pyBox = StatusCheckBox("PyWin32 library")
        binBox = StatusCheckBox("C++ backend")
        binLabel = StatusLabel()

        pywin32 = True if "win32api" in sys.modules else False
        pyBox.setChecked(pywin32)

        antidotePath = antidote.getBinaryPath()
        binBox.setChecked(Path(antidotePath).is_file())
        binLabel.setVisible(bool(antidotePath))
        binLabel.setText(antidotePath)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(pyBox)
        layout.addWidget(binBox)
        layout.addWidget(binLabel)


class StatusLabel(QtWidgets.QLabel):
    def __init__(self, path: str = ""):
        super().__init__()
        font = QtGui.QFont()
        font.setItalic(True)
        font.setPointSize(7)
        self.setFont(font)
        self.setText(path)
        self.setIndent(20)
        self.setMouseTracking(True)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)


class StatusCheckBox(QtWidgets.QCheckBox):
    def __init__(self, text):
        super().__init__(text)
        self.setEnabled(False)
        self.setStyleSheet(
            """
            QCheckBox::indicator {
                width: 10px;
                height: 10px;
                border: 1px solid black;
            }
            QCheckBox:checked {
                color: darkgreen;
            }
            QCheckBox:unchecked {
                color: darkred;
            }
            QCheckBox::indicator:checked {
                    background-color: palegreen;
                }
                QCheckBox::indicator:unchecked {
                    background-color: darkred;
                }
                """
        )
