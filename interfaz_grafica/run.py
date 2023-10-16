from PyQt5 import QtWidgets

if __name__ == "__main__":
    from vistas.Busqueda import Ui_Busqueda
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Busqueda = QtWidgets.QMainWindow()
    ui = Ui_Busqueda(app)
    ui.setupUi(Busqueda)
    Busqueda.show()
    sys.exit(app.exec_())