from PyQt5 import QtWidgets
from vistas.VentanaInicio import Ui_Busqueda

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VentanaInicio = QtWidgets.QMainWindow()
    ui = Ui_Busqueda(app)
    ui.setupUi(VentanaInicio)
    VentanaInicio.show()
    sys.exit(app.exec_())