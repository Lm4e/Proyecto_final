"""Importa Qt una sola vez para todo el proyecto.

- Intenta PyQt6 y, si no esta instalado o falla al cargar (por ejemplo el
  error "DLL load failed" de Anaconda), usa PyQt5 automaticamente.
- Con PyQt5, loadUi normaliza los .ui que guarda el Designer de Qt6
  (enums como Qt::TextFormat::AutoText o Qt::AlignmentFlag::AlignCenter),
  que PyQt5 no entiende. Asi da igual con que version de Designer se guarde.
"""
import io
import re

try:
    from PyQt6.QtGui import QPainter, QPixmap
    from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
    from PyQt6.uic import loadUi as _loadUi

    QT_VERSION = 6
except ImportError:
    from PyQt5.QtGui import QPainter, QPixmap
    from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
    from PyQt5.uic import loadUi as _loadUi

    QT_VERSION = 5

_ENUM_QT6 = re.compile(r"\b(\w+)::\w+::(\w+)\b")  # Qt::TextFormat::AutoText -> Qt::AutoText


def loadUi(ruta_ui, widget):
    if QT_VERSION == 6:
        return _loadUi(ruta_ui, widget)
    with open(ruta_ui, encoding="utf-8") as f:
        xml = _ENUM_QT6.sub(r"\1::\2", f.read())
    return _loadUi(io.StringIO(xml), widget)


__all__ = ["QApplication", "QWidget", "QMessageBox", "QPainter", "QPixmap", "loadUi", "QT_VERSION"]