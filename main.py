
import sys
from qt_compat import QApplication
from Modelo import BaseDatos
from Vista import (
    VentanaBienvenida,
    VentanaLogin,
    VentanaMenuImagenes,
    VentanaMenuSenales,
    VentanaRegistro,
    VentanaImagenes,
)
from Controlador import Coordinador


def main():
    app = QApplication(sys.argv)

    modelo = BaseDatos()
    v_bienvenida = VentanaBienvenida()
    v_login = VentanaLogin()
    v_menu_img = VentanaMenuImagenes()
    v_menu_sen = VentanaMenuSenales()
    v_registro = VentanaRegistro(v_login)
    v_imagenes = VentanaImagenes()

    coordinador = Coordinador(modelo, v_bienvenida, v_login, v_menu_img, v_menu_sen, v_registro)
    coordinador.ventana_imagenes = v_imagenes

    v_bienvenida.asignarControlador(coordinador)
    v_login.asignarControlador(coordinador)
    v_menu_img.asignarControlador(coordinador)
    v_menu_sen.asignarControlador(coordinador)
    v_registro.asignarControlador(coordinador)
    v_imagenes.asignarControlador(coordinador)

    coordinador.iniciar()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()