from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import mineria

from LimitadorCantidad import Ui_LimitadorCantidad
class Ui_Busqueda(object):
    def __init__(self):
        self.soup = None
        self.busqueda = ''
        self.opcion = ''

    def VentanaLimitador(self):
        self.ventana = QtWidgets.QMainWindow()
        app.closeAllWindows()
        self.ui = Ui_LimitadorCantidad(self.soup[0], self.busqueda, app, self.opcion)
        self.ui.setupUi(self.ventana)
        self.ventana.show()

    def setupUi(self, VentanaInicio):
        VentanaInicio.setObjectName("VentanaInicio")
        VentanaInicio.resize(387, 388)
        self.centralwidget = QtWidgets.QWidget(VentanaInicio)
        self.centralwidget.setObjectName("centralwidget")
        self.BusquedaTextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.BusquedaTextBox.setGeometry(QtCore.QRect(20, 80, 351, 21))
        self.BusquedaTextBox.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.BusquedaTextBox.setFont(font)
        self.BusquedaTextBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.BusquedaTextBox.setObjectName("BusquedaTextBox")
        self.BusquedaLabel = QtWidgets.QLabel(self.centralwidget)
        self.BusquedaLabel.setGeometry(QtCore.QRect(20, 50, 351, 21))
        self.BusquedaLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        self.BusquedaLabel.setFont(font)
        self.BusquedaLabel.setObjectName("BusquedaLabel")
        self.SelecCondLabel = QtWidgets.QLabel(self.centralwidget)
        self.SelecCondLabel.setGeometry(QtCore.QRect(20, 130, 351, 21))
        self.SelecCondLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        self.SelecCondLabel.setFont(font)
        self.SelecCondLabel.setObjectName("SelecCondLabel")
        self.groupRadioButtons = QtWidgets.QGroupBox(self.centralwidget)
        self.groupRadioButtons.setGeometry(QtCore.QRect(20, 160, 351, 101))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.groupRadioButtons.setFont(font)
        self.groupRadioButtons.setTitle("")
        self.groupRadioButtons.setObjectName("groupRadioButtons")
        self.NuevoUsadoRB = QtWidgets.QRadioButton(self.groupRadioButtons)
        self.NuevoUsadoRB.setGeometry(QtCore.QRect(10, 10, 150, 20))
        self.NuevoUsadoRB.setObjectName("NuevoUsadoRB")
        self.NuevoUsadoRB.setChecked(True)
        self.SoloNuevoRB = QtWidgets.QRadioButton(self.groupRadioButtons)
        self.SoloNuevoRB.setGeometry(QtCore.QRect(10, 40, 111, 20))
        self.SoloNuevoRB.setObjectName("SoloNuevoRB")
        self.SoloUsadoRB = QtWidgets.QRadioButton(self.groupRadioButtons)
        self.SoloUsadoRB.setGeometry(QtCore.QRect(10, 70, 111, 20))
        self.SoloUsadoRB.setObjectName("SoloUsadoRB")
        self.Siguiente_1_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Siguiente_1_Button.setGeometry(QtCore.QRect(260, 300, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.Siguiente_1_Button.setFont(font)
        self.Siguiente_1_Button.setObjectName("Siguiente_1_Button")
        self.Siguiente_1_Button.clicked.connect(self.AccionSiguiente)
        VentanaInicio.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VentanaInicio)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 387, 22))
        self.menubar.setObjectName("menubar")
        VentanaInicio.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VentanaInicio)
        self.statusbar.setObjectName("statusbar")
        VentanaInicio.setStatusBar(self.statusbar)

        self.retranslateUi(VentanaInicio)
        QtCore.QMetaObject.connectSlotsByName(VentanaInicio)

    def AccionSiguiente(self):
        if self.NuevoUsadoRB.isChecked():
            self.opcion = '0'
        elif self.SoloNuevoRB.isChecked():
            self.opcion = '1'
        elif self.SoloUsadoRB.isChecked():
            self.opcion = '2'

        self.busqueda = self.BusquedaTextBox.text()
        self.soup = mineria.BusquedaInicial(self.BusquedaTextBox.text(), self.opcion)

        if self.soup == 1:
            # popup
            msg = QMessageBox()
            msg.setWindowTitle('Error de solicitud')
            msg.setText('Revise su conexión a internet.')
            x = msg.exec_()
        elif self.soup == 0:
            # popup
            msg = QMessageBox()
            msg.setWindowTitle('Error de solicitud')
            msg.setText('La búsqueda no devolvió resultados.\nPruebe con otra búsqueda.')
            x = msg.exec_()
        else:
            if self.soup[1]:
                msg = QMessageBox()
                msg.setWindowTitle('Condición no disponible')
                msg.setText('La búsqueda no tiene esa condición.\nVolviendo a "Nuevos y Usados" por default...')
                x = msg.exec_()
                app.closeAllWindows()
                self.VentanaLimitador()
                # return soup[0]
            else:
                # return soup[0]
                app.closeAllWindows()
                self.VentanaLimitador()


    def retranslateUi(self, MineriaLibre):
        _translate = QtCore.QCoreApplication.translate
        MineriaLibre.setWindowTitle(_translate("VentanaInicio", "Búsqueda Inicial"))
        self.BusquedaLabel.setText(_translate("VentanaInicio", "Ingrese su búsqueda aquí:"))
        self.SelecCondLabel.setText(_translate("VentanaInicio", "Seleccione la condición de los productos:"))
        self.NuevoUsadoRB.setText(_translate("VentanaInicio", "Nuevos y Usados"))
        self.SoloNuevoRB.setText(_translate("VentanaInicio", "Sólo Nuevos"))
        self.SoloUsadoRB.setText(_translate("VentanaInicio", "Sólo Usados"))
        self.Siguiente_1_Button.setText(_translate("VentanaInicio", "Siguiente"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VentanaInicio = QtWidgets.QMainWindow()
    ui = Ui_Busqueda()
    ui.setupUi(VentanaInicio)
    VentanaInicio.show()
    sys.exit(app.exec_())
