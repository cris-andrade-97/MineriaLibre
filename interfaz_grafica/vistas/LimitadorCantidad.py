from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from lib import mineria
from vistas.Final import Ui_Final


class Ui_LimitadorCantidad(object):
    def __init__(self,soup, busqueda, app, opcion):
        self.soup = soup
        self.app = app
        self.busqueda = busqueda
        self.cantidad = 0
        self.limitador = 0
        self.opcion = opcion

    def VentanaFinal(self):
        self.ventanaFinal = QtWidgets.QMainWindow()
        self.uiFinal = Ui_Final(self.busqueda, self.soup, self.limitador, self.app, self.opcion)
        self.uiFinal.setupUi(self.ventanaFinal)
        self.ventanaFinal.show()

    '''def VentanaEspere(self):
        self.ventana = QtWidgets.QMainWindow()
        self.app.closeAllWindows()
        self.ui = Ui_Espere(self.app)
        self.ui.setupUi(self.ventana)
        self.ventana.show()'''

    def setupUi(self, LimitadorCantidad):
        LimitadorCantidad.setObjectName("LimitadorCantidad")
        LimitadorCantidad.resize(556, 388)
        self.centralwidget = QtWidgets.QWidget(LimitadorCantidad)
        self.centralwidget.setObjectName("centralwidget")
        self.LimitadorTextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.LimitadorTextBox.setGeometry(QtCore.QRect(90, 150, 381, 21))
        self.LimitadorTextBox.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.LimitadorTextBox.setFont(font)
        self.LimitadorTextBox.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.LimitadorTextBox.setObjectName("LimitadorTextBox")
        self.LimitadorLabel = QtWidgets.QLabel(self.centralwidget)
        self.LimitadorLabel.setGeometry(QtCore.QRect(20, 120, 521, 21))
        self.LimitadorLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        self.LimitadorLabel.setFont(font)
        self.LimitadorLabel.setObjectName("LimitadorLabel")
        self.Comenzar_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Comenzar_Button.setGeometry(QtCore.QRect(220, 300, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.Comenzar_Button.setFont(font)
        self.Comenzar_Button.setObjectName("Comenzar_Button")
        self.Comenzar_Button.clicked.connect(self.BotonComenzar)
        self.CantidadArtLabel = QtWidgets.QLabel(self.centralwidget)
        self.CantidadArtLabel.setGeometry(QtCore.QRect(20, 40, 521, 21))
        self.CantidadArtLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        self.CantidadArtLabel.setFont(font)
        self.CantidadArtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CantidadArtLabel.setObjectName("CantidadArtLabel")
        self.AclaracionLabel = QtWidgets.QLabel(self.centralwidget)
        self.AclaracionLabel.setGeometry(QtCore.QRect(20, 60, 521, 21))
        self.AclaracionLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(True)
        self.AclaracionLabel.setFont(font)
        self.AclaracionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AclaracionLabel.setObjectName("AclaracionLabel")
        LimitadorCantidad.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LimitadorCantidad)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 556, 22))
        self.menubar.setObjectName("menubar")
        LimitadorCantidad.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LimitadorCantidad)
        self.statusbar.setObjectName("statusbar")
        LimitadorCantidad.setStatusBar(self.statusbar)

        self.retranslateUi(LimitadorCantidad)
        QtCore.QMetaObject.connectSlotsByName(LimitadorCantidad)

    def BotonComenzar(self):

        try:
            self.limitador = int(self.LimitadorTextBox.text())
            if mineria.LimitadorCantidad(cantidadArticulos=self.cantidad, limiteArticulos=self.limitador):
                self.VentanaFinal()
            else:
                msg = QMessageBox()
                msg.setWindowTitle('Valor fuera de rango')
                msg.setText('El número ingresado está fuera de los límites.\nIntente nuevamente.')
                x = msg.exec_()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle('Error de tipo de dato')
            msg.setText('Sólo se admiten números en este campo.\nIntente nuevamente.')
            x = msg.exec_()

    def CambiarLabels(self):
        cantidadArticulos =  mineria.CalcularCantidad(self.soup)
        self.cantidad = cantidadArticulos[0]
        if cantidadArticulos[2]:
            self.CantidadArtLabel.setText(f'Hay exactamente {cantidadArticulos[0]} artículos con esa condición.')
        else:
            self.CantidadArtLabel.setText(f'Hay aproximadamente {cantidadArticulos[0]} artículos con esa condición.')
        self.LimitadorLabel.setText(f'Ingrese 0 si desea todos los artículos ó ingrese una cantidad entre 1 y {cantidadArticulos[0]}: ')

    def retranslateUi(self, LimitadorCantidad):
        _translate = QtCore.QCoreApplication.translate
        LimitadorCantidad.setWindowTitle(_translate("LimitadorCantidad", "Limitar la búsqueda"))
        self.CambiarLabels()
        self.Comenzar_Button.setText(_translate("LimitadorCantidad", "¡Comenzar!"))
        self.AclaracionLabel.setText(_translate("LimitadorCantidad", "Puede traerlos todos o parte de ellos"))



