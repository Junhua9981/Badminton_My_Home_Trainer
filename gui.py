from PyQt5 import QtWidgets, QtGui, QtCore
from UI import Ui_Badminton_My_Home_Trainer
from UI2 import Ui_Form

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Badminton_My_Home_Trainer()
        self.ui.setupUi(self)
        self.setup_control()
        self.sub_window = subWindow_controller()

    def setup_control(self):
        # TODO
        # qpushbutton doc: https://doc.qt.io/qt-5/qpushbutton.html
        #self.ui.pushButton.setText('Print message!')
        #self.clicked_counter = 0
        self.ui.play.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        #self.clicked_counter += 1
        #print(f"You clicked {self.clicked_counter} times.")
        self.hide()
        self.sub_window.show()
        #self.exec_()
        #self.close()

class subWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setup_control()   
    
    def setup_control(self):
        # TODO
        # qpushbutton doc: https://doc.qt.io/qt-5/qpushbutton.html
        #self.ui.pushButton.setText('Print message!')
        #self.clicked_counter = 0
        self.ui.pushButton_2.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        #self.clicked_counter += 1
        #print(f"You clicked {self.clicked_counter} times.")
        #execfile("main_mode1.py")
        #f = open('main_mode1.py','r',encoding="utf-8")
        #line = f.readline()
        #f.close()
        #f = open('main_mode1.py').read()
        #exec(open('main_mode1.py').read())
        #print("open")
        form.destroy()
        os.system('main_mode1.py')

    

        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec_())
