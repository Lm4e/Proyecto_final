import os
from qt_compat import QPainter, QWidget, QMessageBox, QPixmap, loadUi

CARPETA_UI = os.path.join(os.path.dirname(__file__), "ui")


def poner_imagen(label, nombre_archivo):
    """Carga una imagen de la carpeta ui/ en un QLabel desde codigo."""
    pixmap = QPixmap(os.path.join(CARPETA_UI, nombre_archivo))
    if pixmap.isNull():
        print(f"AVISO: no se pudo cargar la imagen {nombre_archivo}")
        return
    label.setPixmap(pixmap)
    label.setScaledContents(True)


class VentanaBienvenida(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(CARPETA_UI, "bienvenida.ui"), self)
        poner_imagen(self.label_2, "fondo_bienvenida.png")  # fondo
        poner_imagen(self.lbl_imagen_app, "logo_app_ok.png")  # logo
        self._controlador = None
        if hasattr(self, "btn_iniciar"):
            self.btn_iniciar.clicked.connect(self.ir_login)

    def asignarControlador(self, c):
        self._controlador = c

    def ir_login(self):
        if self._controlador is not None:
            self._controlador.mostrar_login()


class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(CARPETA_UI, "login.ui"), self)
        self.setStyleSheet("")  # quita el fondo por recurso (:/...) que trae el .ui
        self._fondo = QPixmap(os.path.join(CARPETA_UI, "fondo_login.png"))  # fondo de toda la ventana
        if self._fondo.isNull():
            print("AVISO: no se pudo cargar la imagen fondo_login.png")
        poner_imagen(self.label, "logo_app_ok.png")  # logo
        self._controlador = None
        if hasattr(self, "btn_ingresar"):
            self.btn_ingresar.clicked.connect(self.ingresar)
        if hasattr(self, "btn_limpiar"):
            self.btn_limpiar.clicked.connect(self.limpiar)

    def asignarControlador(self, c):
        self._controlador = c

    def paintEvent(self, event):
        """Dibuja el fondo estirado a todo el tamano de la ventana."""
        if not self._fondo.isNull():
            pintor = QPainter(self)
            pintor.drawPixmap(self.rect(), self._fondo)
            pintor.end()

    def limpiar(self):
        if hasattr(self, "txt_usuario"):
            self.txt_usuario.setText("")
        if hasattr(self, "txt_password"):
            self.txt_password.setText("")

    def ingresar(self):
        u = self.txt_usuario.text() if hasattr(self, "txt_usuario") else ""
        p = self.txt_password.text() if hasattr(self, "txt_password") else ""
        if self._controlador is not None:
            self._controlador.login(u, p)

    def mensaje(self, texto, error=False):
        if error:
            QMessageBox.warning(self, "Aviso", texto)
        else:
            QMessageBox.information(self, "Información", texto)


class VentanaMenuImagenes(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(CARPETA_UI, "menu_imagenes.ui"), self)
        self._controlador = None
        if hasattr(self, "btn_imagenes"):
            self.btn_imagenes.clicked.connect(self.abrir_imagenes)

    def asignarControlador(self, c):
        self._controlador = c

    def poner_datos_usuario(self, info):
        if hasattr(self, "lbl_usuario"):
            self.lbl_usuario.setText(
                f"ID: {info['id']} | {info['nombre']} | Rol: {info['rol']} | {info['fecha']} {info['hora']}"
            )

    def abrir_imagenes(self):
        if self._controlador is not None:
            self._controlador.abrir_ventana_imagenes()


class VentanaMenuSenales(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(CARPETA_UI, "menu_senales.ui"), self)
        self._controlador = None
        if hasattr(self, "btn_csv"):
            self.btn_csv.clicked.connect(self.abrir_csv)
        if hasattr(self, "btn_mat"):
            self.btn_mat.clicked.connect(self.abrir_mat)

    def asignarControlador(self, c):
        self._controlador = c

    def poner_datos_usuario(self, info):
        if hasattr(self, "lbl_usuario"):
            self.lbl_usuario.setText(
                f"ID: {info['id']} | {info['nombre']} | Rol: {info['rol']} | {info['fecha']} {info['hora']}"
            )

    def abrir_csv(self):
        if self._controlador is not None:
            self._controlador.abrir_ventana_csv()

    def abrir_mat(self):
        if self._controlador is not None:
            self._controlador.abrir_ventana_mat()