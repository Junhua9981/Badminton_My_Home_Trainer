# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI3.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mode2_choice(object):
    def setupUi(self, mode2_choice):
        mode2_choice.setObjectName("mode2_choice")
        mode2_choice.resize(1920, 1080)
        mode2_choice.setStyleSheet("background-color: rgb(71, 160, 242);")
        self.mode2_1button = QtWidgets.QPushButton(mode2_choice)
        self.mode2_1button.setGeometry(QtCore.QRect(430, 400, 420, 420))
        self.mode2_1button.setStyleSheet("border-image: url(:/assets/mode2-1button-new.png);\n"
"")
        self.mode2_1button.setText("")
        self.mode2_1button.setObjectName("mode2_1button")
        self.mode2_2button = QtWidgets.QPushButton(mode2_choice)
        self.mode2_2button.setGeometry(QtCore.QRect(1140, 400, 420, 420))
        self.mode2_2button.setStyleSheet("border-image: url(:/assets/mode2-2button-new.png);")
        self.mode2_2button.setText("")
        self.mode2_2button.setObjectName("mode2_2button")
        self.backButton = QtWidgets.QPushButton(mode2_choice)
        self.backButton.setGeometry(QtCore.QRect(1650, 30, 250, 140))
        self.backButton.setStyleSheet("border-image: url(:/assets/back_button.png);")
        self.backButton.setText("")
        self.backButton.setObjectName("backButton")

        self.retranslateUi(mode2_choice)
        QtCore.QMetaObject.connectSlotsByName(mode2_choice)

    def retranslateUi(self, mode2_choice):
        _translate = QtCore.QCoreApplication.translate
        mode2_choice.setWindowTitle(_translate("mode2_choice", "Form"))
import picture_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mode2_choice = QtWidgets.QWidget()
    ui = Ui_mode2_choice()
    ui.setupUi(mode2_choice)
    mode2_choice.show()
    sys.exit(app.exec_())
