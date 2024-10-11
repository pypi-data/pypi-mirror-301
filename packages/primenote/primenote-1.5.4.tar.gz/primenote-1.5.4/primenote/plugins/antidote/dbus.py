#!/usr/bin/python3
from typing import Callable, Union
from PyQt5 import QtCore, QtDBus
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit

try:
    from ...backend import logger
except (ValueError, ImportError):
    from backend import logger

log = logger.new(__name__)


class Adapter(QtDBus.QDBusAbstractAdaptor):
    QtCore.Q_CLASSINFO("D-Bus Interface", "com.druide.antidote.dbus.api")
    QtCore.Q_CLASSINFO(
        "D-Bus Introspection",
        ""
        '  <interface name="com.druide.antidote.dbus.api">\n'
        '    <method name="ActiveDocument"/>\n'
        '    <method name="CorrigeDansTexteur">\n'
        '      <arg direction="in" type="i" name="leDebut"/>\n'
        '      <arg direction="in" type="i" name="laFin"/>\n'
        '      <arg direction="in" type="s" name="laChaine"/>\n'
        '      <arg direction="in" type="b" name="automatique"/>\n'
        "    </method>\n"
        '    <method name="DonneBloc">\n'
        '      <arg direction="in" type="i" name="leDebut"/>\n'
        '      <arg direction="in" type="i" name="laFin"/>\n'
        '      <arg direction="out" type="s" name="_ret"/>\n'
        "    </method>\n"
        '    <method name="DonneDebutSelection">\n'
        '      <arg direction="out" type="i" name="_ret"/>\n'
        "    </method>\n"
        '    <method name="DonneFinDocument">\n'
        '      <arg direction="out" type="i" name="_ret"/>\n'
        "    </method>\n"
        '    <method name="DonneFinSelection">\n'
        '      <arg direction="out" type="i" name="_ret"/>\n'
        "    </method>\n"
        '    <method name="DonnePositionFinBoite">\n'
        '      <arg direction="in" type="i" name="unePos"/>\n'
        '      <arg direction="out" type="i" name="_ret"/>\n'
        "    </method>\n"
        '    <method name="DonneRetourDeCharriot">\n'
        '      <arg direction="out" type="s" name="_ret"/>\n'
        "    </method>\n"
        '    <method name="DonneTitreDocument">\n'
        '      <arg direction="out" type="s" name="_ret"/>\n'
        "    </method>\n"
        '    <method name="PermetsRetourDeCharriot">\n'
        '      <arg direction="out" type="b" name="_ret"/>\n'
        "    </method>\n"
        '    <method name="RetourneAuTexteur"/>\n'
        '    <method name="RompsLienCorrecteur"/>\n'
        '    <method name="RompsLienTexteur"/>\n'
        '    <method name="SelectionneIntervalle">\n'
        '      <arg direction="in" type="i" name="leDebut"/>\n'
        '      <arg direction="in" type="i" name="laFin"/>\n'
        "    </method>\n"
        "  </interface>\n",
    )

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setAutoRelaySignals(True)

    @QtCore.pyqtSlot()
    def ActiveDocument(self):
        self.parent.activeDocument()

    @QtCore.pyqtSlot(int, int, str, bool)
    def CorrigeDansTexteur(self, debut: int, fin: int, chaine: str, auto: bool):
        self.parent.corrigeDansTexteur(debut, fin, chaine, auto)

    @QtCore.pyqtSlot(int, int, result=str)
    def DonneBloc(self, debut: int, fin: int) -> str:
        return self.parent.donneBloc(debut, fin)

    @QtCore.pyqtSlot(result=int)
    def DonneDebutSelection(self) -> int:
        return self.parent.donneDebutSelection()

    @QtCore.pyqtSlot(result=int)
    def DonneFinDocument(self) -> int:
        return self.parent.donneFinDocument()

    @QtCore.pyqtSlot(result=int)
    def DonneFinSelection(self) -> int:
        return self.parent.donneFinSelection()

    @QtCore.pyqtSlot(int, result=int)
    def DonnePositionFinBoite(self, unePos: int) -> int:
        return self.parent.donnePositionFinBoite()

    @QtCore.pyqtSlot(result=str)
    def DonneRetourDeCharriot(self) -> str:
        return self.parent.donneRetourDeCharriot()

    @QtCore.pyqtSlot(result=str)
    def DonneTitreDocument(self) -> str:
        return self.parent.donneTitreDocument()

    @QtCore.pyqtSlot(result=bool)
    def PermetsRetourDeCharriot(self) -> bool:
        return self.parent.permetsRetourDeCharriot()

    @QtCore.pyqtSlot()
    def RetourneAuTexteur(self):
        self.parent.retourneAuTexteur()

    @QtCore.pyqtSlot()
    def RompsLienCorrecteur(self):
        self.parent.rompsLienCorrecteur()

    @QtCore.pyqtSlot()
    def RompsLienTexteur(self):
        self.parent.rompsLienTexteur()

    @QtCore.pyqtSlot(int, int)
    def SelectionneIntervalle(self, debut: int, fin: int):
        self.parent.selectionneIntervalle(debut, fin)


class API:  # API Antidote 10 (2020)
    def ignoreRuntimeError(default: Union[str, int] = None) -> Callable:
        """Logs API calls and ignores RuntimeError during execution. Return a default value on failure"""

        def rewrap(func: Callable, *args) -> Callable:
            def wrap(self, *args) -> any:
                try:
                    _return = func(self, *args)
                    log.debug(f"{func.__qualname__}{args} -> {repr(_return)}")
                    return _return
                except RuntimeError:
                    log.debug(f"RuntimeError in {func.__qualname__}{args}, returned {repr(default)}")
                    return default

            return wrap

        return rewrap

    @ignoreRuntimeError()
    def activeDocument(self):
        self.body.window().raise_()

    @ignoreRuntimeError()
    def corrigeDansTexteur(self, debut: int, fin: int, chaine: str, auto: bool):
        if debut >= 0 and fin >= 0:
            textCursor = self.body.textCursor()
            textCursor.setPosition(debut)
            textCursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, fin - debut)
            textCursor.insertText(chaine)

        if not auto:
            self.body.ensureCursorVisible()

    @ignoreRuntimeError(default="")
    def donneBloc(self, debut: int, fin: int) -> str:
        textCursor = self.body.textCursor()
        textCursor.movePosition(QTextCursor.Start)
        textCursor.movePosition(QTextCursor.NextCharacter, QTextCursor.MoveAnchor, debut)
        textCursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, fin - debut)
        return textCursor.selectedText()

    @ignoreRuntimeError(default=0)
    def donneDebutSelection(self) -> int:
        ancre = self.body.textCursor().anchor()
        position = self.body.textCursor().position()
        return min(ancre, position)

    @ignoreRuntimeError(default=0)
    def donneFinDocument(self) -> int:
        textCursor = self.body.textCursor()
        textCursor.movePosition(QTextCursor.End)
        return textCursor.position()

    @ignoreRuntimeError(default=0)
    def donneFinSelection(self) -> int:
        ancre = self.body.textCursor().anchor()
        position = self.body.textCursor().position()
        return max(ancre, position)

    def donnePositionFinBoite(self) -> int:
        return 0

    def donneRetourDeCharriot(self) -> str:
        return "\n"

    @ignoreRuntimeError(default="")
    def donneTitreDocument(self) -> str:
        return self.body.window().windowTitle()

    def permetsRetourDeCharriot(self) -> bool:
        return True

    @ignoreRuntimeError
    def retourneAuTexteur(self):
        self.body.window().activateWindow()
        self.body.window().raise_()

    @ignoreRuntimeError
    def rompsLienCorrecteur(self):
        pass

    def rompsLienTexteur(self):
        pass

    @ignoreRuntimeError
    def selectionneIntervalle(self, debut: int, fin: int):
        textCursor = self.body.textCursor()
        textCursor.setPosition(debut)
        textCursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, fin - debut)
        self.body.setTextCursor(textCursor)


class Antidote(QtCore.QObject, API):
    ready = QtCore.pyqtSignal()

    def __init__(self, uid: str, path: str, body: QPlainTextEdit):
        super().__init__()
        self.uid = f"{uid.lower()}_{id(self)}"
        self.path = path
        self.body = body

    def init(self):
        """Initializes DBus interface"""
        self.bus = QtDBus.QDBusConnection.sessionBus()
        if self._register():
            self.__dbusAdaptor = Adapter(self)
            self.ready.emit()

    def corrector(self):
        """Launches Antidote corrector"""
        self._tool("C")

    def dictionnary(self, tool: str = "D_Defaut"):
        """Launches Antidote dictionnary"""
        options = (
            "D",
            "D_Defnitions",
            "D_Synonymes",
            "D_Antonymes",
            "D_Cooccurrences",
            "D_ChampLexical",
            "D_Conjugaison",
            "D_Famille",
            "D_Citations",
            "D_Historique",
            "D_Illustrations",
            "D_Wikipedia",
        )
        tool = tool if tool in options else "D_Defaut"
        self._tool(tool)

    def guide(self, tool: str = "G_Defaut"):
        """Launches Antidote guide"""
        options = (
            "G",
            "G_Orthographe",
            "G_Lexique",
            "G_Grammaire",
            "G_Syntaxe",
            "G_Ponctuation",
            "G_Style",
            "G_Redaction",
            "G_Typographie",
            "G_Phonetique",
            "G_Historique",
            "G_PointsDeLangue",
        )
        tool = tool if tool in options else "G_Defaut"
        self._tool(tool)

    def _tool(self, tool: str):
        p = QtCore.QProcess()
        p.setStandardOutputFile(QtCore.QProcess.nullDevice())
        p.setStandardErrorFile(QtCore.QProcess.nullDevice())
        p.setProgram(self.path)
        p.setArguments(["--module", "API_DBus:v1.0", "--identificateur", self.uid, "--outil", tool])
        p.startDetached()

    def _register(self) -> bool:
        """Registers a session DBus service"""
        obj = f"/com/druide/antidote/dbus/api/v1/{self.uid}"
        if not self.bus.registerObject(obj, self):
            log.error(f"Could not register DBus object '{obj}'")
            return False

        service = f"com.druide.antidote.dbus.api.v1.{self.uid}"
        if not self.bus.registerService(service):
            log.error(f"Could not register DBus service '{service}'")
            return False
        return True
