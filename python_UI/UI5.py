# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI5.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UI_mode4_choice(object):
    def setupUi(self, UI_mode4_choice):
        UI_mode4_choice.setObjectName("UI_mode4_choice")
        UI_mode4_choice.resize(1920, 1080)
        UI_mode4_choice.setStyleSheet("background-color: rgb(132, 163, 132);\n"
"")
        self.clear_high_button = QtWidgets.QPushButton(UI_mode4_choice)
        self.clear_high_button.setGeometry(QtCore.QRect(180, 400, 420, 420))
        self.clear_high_button.setStyleSheet("border-image: url(:/assets/high_clear.png);")
        self.clear_high_button.setText("")
        self.clear_high_button.setObjectName("clear_high_button")
        self.smash_button = QtWidgets.QPushButton(UI_mode4_choice)
        self.smash_button.setGeometry(QtCore.QRect(720, 400, 420, 420))
        self.smash_button.setStyleSheet("border-image: url(:/assets/drop.png);")
        self.smash_button.setText("")
        self.smash_button.setObjectName("smash_button")
        self.backButton = QtWidgets.QPushButton(UI_mode4_choice)
        self.backButton.setGeometry(QtCore.QRect(1650, 30, 250, 140))
        self.backButton.setStyleSheet("border-image: url(:/assets/back_button.png);")
        self.backButton.setText("")
        self.backButton.setObjectName("backButton")
        self.smash_button_2 = QtWidgets.QPushButton(UI_mode4_choice)
        self.smash_button_2.setGeometry(QtCore.QRect(1260, 400, 420, 420))
        self.smash_button_2.setStyleSheet("border-image: url(:/assets/smash.png);")
        self.smash_button_2.setText("")
        self.smash_button_2.setObjectName("smash_button_2")

        self.retranslateUi(UI_mode4_choice)
        QtCore.QMetaObject.connectSlotsByName(UI_mode4_choice)

    def retranslateUi(self, UI_mode4_choice):
        _translate = QtCore.QCoreApplication.translate
        UI_mode4_choice.setWindowTitle(_translate("UI_mode4_choice", "Dialog"))
import picture_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UI_mode4_choice = QtWidgets.QDialog()
    ui = Ui_UI_mode4_choice()
    ui.setupUi(UI_mode4_choice)
    UI_mode4_choice.show()
    sys.exit(app.exec_())
