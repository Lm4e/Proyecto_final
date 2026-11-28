class Coordinador:
    def __init__(self, modelo, v_bienvenida, v_login, v_menu_img, v_menu_sen, v_registro):
        self._modelo = modelo
        self._v_bienvenida = v_bienvenida
        self._v_login = v_login
        self._v_menu_img = v_menu_img
        self._v_menu_sen = v_menu_sen
        self._v_registro = v_registro

        self.ventana_imagenes = None
        self.ventana_csv = None
        self.ventana_mat = None

    def iniciar(self):
        self._v_bienvenida.show()

    def mostrar_login(self):
        self._v_bienvenida.hide()
        self._v_login.limpiar()
        self._v_login.show()

    def login(self, usuario, password):
        datos = self._modelo.validar_usuario(usuario, password)
        if datos is None:
            self._v_login.mensaje("Usuario o contraseña incorrectos", error=True)
            return

        self._v_login.hide()
        if datos["rol"] == "imagenes":
            self._v_menu_img.poner_datos_usuario(datos)
            self._v_menu_img.show()
        elif datos["rol"] == "senales":
            self._v_menu_sen.poner_datos_usuario(datos)
            self._v_menu_sen.show()

    def abrir_registro(self):
        self._v_registro.limpiar()
        self._v_registro.exec()

    def registrar(self, nombre, usuario, password, confirmar, rol):
        nombre, usuario = nombre.strip(), usuario.strip()
        if not nombre or not usuario or not password:
            self._v_registro.mensaje("Completa todos los campos", error=True)
            return
        if password != confirmar:
            self._v_registro.mensaje("Las contraseñas no coinciden", error=True)
            return
        if len(password) < 4:
            self._v_registro.mensaje("La contraseña debe tener al menos 4 caracteres", error=True)
            return

        guardado, texto = self._modelo.registrar_usuario(usuario, password, nombre, rol)
        if not guardado:
            self._v_registro.mensaje(texto, error=True)
            return

        self._v_registro.mensaje(texto)
        self._v_registro.accept()  # cierra el formulario
        self._v_login.poner_usuario(usuario)  # deja listo el login para entrar

    def abrir_ventana_imagenes(self):
        if self.ventana_imagenes is not None:
            self.ventana_imagenes.show()
        else:
            QMessageBox_info = getattr(self._v_menu_img, "lbl_usuario", None)
            if QMessageBox_info is None:
                print("Módulo de imágenes pendiente por conectar.")

    def abrir_ventana_csv(self):
        if self.ventana_csv is not None:
            self.ventana_csv.show()

    def abrir_ventana_mat(self):
        if self.ventana_mat is not None:
            self.ventana_mat.show()