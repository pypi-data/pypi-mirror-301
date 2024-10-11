#!/usr/bin/python3
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel

try:
    from ..__id__ import (
        APP_NAME,
        DATE,
        VERSION,
        DESC_AUTHOR,
        DESC_LONG,
        DESC_SHORT,
        LINK_AUR,
        LINK_DONATION,
        LINK_HOMEPAGE,
        LINK_SOURCE,
    )
    from ..settings.base import VSpacer
except (ValueError, ImportError):
    from __id__ import (
        APP_NAME,
        DATE,
        VERSION,
        DESC_AUTHOR,
        DESC_LONG,
        DESC_SHORT,
        LINK_AUR,
        LINK_DONATION,
        LINK_HOMEPAGE,
        LINK_SOURCE,
    )
    from settings.base import VSpacer


class PageAbout(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(About(self))
        layout.addItem(VSpacer())


class About(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        font = QtGui.QFont()
        font.setPointSize(32)
        self.titleLabel = QLabel(APP_NAME)
        self.titleLabel.setFont(font)

        font = QtGui.QFont()
        font.setPointSize(14)
        self.versionLabel = QLabel(f"Version {VERSION} — {DATE}")
        self.versionLabel.setFont(font)
        self.copyrightLabel = QLabel(DESC_AUTHOR)

        self.shortDescLabel = QLabel(DESC_SHORT)
        self.shortDescLabel.setWordWrap(True)
        self.longDescLabel = QLabel(DESC_LONG)
        self.longDescLabel.setWordWrap(True)

        self.landingLabel = Hyperlink(f"<a href='{LINK_HOMEPAGE}'>Homepage</a>")
        self.gitLabel = Hyperlink(f"<a href='{LINK_SOURCE}'>Source code</a>")
        self.aurLabel = Hyperlink(f"<a href='{LINK_AUR}'>Arch User Repository</a>")

        font = QtGui.QFont()
        font.setPointSize(12)
        style = "style='color: #A00040; text-decoration:none'"
        self.donateLabel = Hyperlink(
            f"<a href='{LINK_DONATION}' {style}>\u2764\ufe0f Please donate to support development</a>"
        )
        self.donateLabel.setFont(font)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.versionLabel, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.copyrightLabel, 2, 0, 1, 3)
        self.gridLayout.addItem(VSpacer(height=10), 3, 0, 1, 3)
        self.gridLayout.addWidget(self.shortDescLabel, 4, 0, 1, 3)
        self.gridLayout.addWidget(self.longDescLabel, 5, 0, 1, 3)
        self.gridLayout.addWidget(self.landingLabel, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.gitLabel, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.aurLabel, 6, 2, 1, 1)
        self.gridLayout.addItem(VSpacer(height=25), 7, 2, 1, 1)
        self.gridLayout.addWidget(self.donateLabel, 8, 0, 1, 3)
        self.gridLayout.setContentsMargins(25, 5, 25, 25)
        self.gridLayout.setSpacing(11)


class Hyperlink(QtWidgets.QLabel):
    def __init__(self, label: str):
        super().__init__()
        self.setText(label)
        self.setOpenExternalLinks(True)
        self.setMouseTracking(True)
        self.linkActivated.connect(self.openLink)

    def openLink(self, url: str):
        url = QtCore.QUrl(url)
        QtGui.QDesktopServices.openUrl(url)
