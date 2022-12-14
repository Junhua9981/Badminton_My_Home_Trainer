# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1920, 1080)
        Form.setStyleSheet("background-color: rgb(71, 160, 242);")
        self.modeButton2 = QtWidgets.QPushButton(Form)
        self.modeButton2.setGeometry(QtCore.QRect(510, 400, 420, 420))
        self.modeButton2.setStyleSheet("border-image: url(:/assets/modebutton2.png);")
        self.modeButton2.setText("")
        self.modeButton2.setObjectName("modeButton2")
        self.modeButton3 = QtWidgets.QPushButton(Form)
        self.modeButton3.setGeometry(QtCore.QRect(990, 400, 420, 420))
        self.modeButton3.setStyleSheet("border-image: url(:/assets/modebutton3.png);")
        self.modeButton3.setText("")
        self.modeButton3.setObjectName("modeButton3")
        self.modeButton4 = QtWidgets.QPushButton(Form)
        self.modeButton4.setGeometry(QtCore.QRect(1470, 400, 420, 420))
        self.modeButton4.setToolTipDuration(-5)
        self.modeButton4.setStyleSheet("border-image: url(:/assets/modebutton4.png);")
        self.modeButton4.setText("")
        self.modeButton4.setObjectName("modeButton4")
        self.modeButton1 = QtWidgets.QPushButton(Form)
        self.modeButton1.setGeometry(QtCore.QRect(30, 400, 420, 420))
        self.modeButton1.setStyleSheet("border-image: url(:/assets/modebutton1.png);")
        self.modeButton1.setText("")
        self.modeButton1.setObjectName("modeButton1")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(1729, 10, 151, 151))
        self.pushButton_2.setStyleSheet("border-image: url(:/assets/chatsbutton.png);")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 831, 131))
        self.label.setStyleSheet("border-image: url(:/assets/background.png);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
import picture_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
