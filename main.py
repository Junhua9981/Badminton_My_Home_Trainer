from glob import glob
import argparse
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
from yaml import parse
from python_UI.UI import Ui_Badminton_My_Home_Trainer
from python_UI.UI2 import Ui_Form
from python_UI.UI3 import Ui_mode2_choice
from python_UI.UI4 import Ui_Dialog
from python_UI.UI5 import Ui_UI_mode4_choice
from python_UI.UI6 import Ui_UI_high_clear
from python_UI.UI7 import Ui_UI_smash
from python_UI.UI8 import Ui_UI_drop
from objectDetectionModule import ObjectDetection
from stages.mode1 import stage1
from stages.mode2_1 import stage2_1
from stages.mode2_2 import stage2_2
from stages.mode3 import stage3
from stages.mode4 import stage4
from SQL import createDB
from python_UI.SQL_UI import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


cap = None
detector = None

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Badminton_My_Home_Trainer()
        self.ui.setupUi(self)
        #self.setup_control()
        self.sub_window = subWindow_controller() 

class subWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        #self.setup_control()   
        self.tri_window = triWindow_controller()  
    
    def buttonClicked1(self):
        print("mode1")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        if detector is None:
            tmp = stage1( cap, detector )
            detector = tmp
        else:
            stage1( cap, detector )

    def buttonClicked2(self):
        print("mode2")
        self.hide()
        self.tri_window.show()

    def buttonClicked3(self):
        print("mode3")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        
        if detector is None:
            tmp = stage3( cap, detector )
            detector = tmp
        else:
            stage3( cap, detector )

    def buttonClicked_chats(self):
        print("chats")
        
class triWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_mode2_choice()
        self.ui.setupUi(self)
        #self.setup_control()   
        #self.sub_window2 = subWindow_controller()

    def buttonClicked1(self):
        print("mode2-1")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        if detector is None:
            tmp = stage2_1( cap, detector )
            detector = tmp
        else:
            stage2_1( cap, detector )
    
    def buttonClicked2(self):
        print("mode2-2")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        if detector is None:
            tmp = stage2_2( cap, detector )
            detector = tmp
        else:
            stage2_2( cap, detector )
    
    def back_buttonClicked(self):
        print("chats")
        
class forWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #self.set_control()
        if QSqlDatabase.contains("qt_sql_default_connection"):
            self.db = QSqlDatabase.database("qt_sql_default_connection")
        else:
            self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('DB.db')    
        self.title = "展示數據"
        self.model = QSqlTableModel()#MVC模式中的模型
        self.initializeModel()
        self.createView()
        #self.findrow()
        self.set_control()
               
    def initializeModel(self):
        self.model.setTable('people')
        #當data改變時會接觸一些事件
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        #將整個數據載入model中
        self.model.select()
        #設置header
        self.model.setHeaderData(0, Qt.Horizontal,'ID')
        self.model.setHeaderData(1, Qt.Horizontal, '時間')
        self.model.setHeaderData(2, Qt.Horizontal, '模式')
        self.model.setHeaderData(3, Qt.Horizontal, '分數')
 
    def createView(self):
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setWindowTitle(self.title)
        return self.view
 
    def set_control(self):
        self.delrow = -1
        self.initializeModel()
        self.view = self.createView()
        #調整QTtableview之大小
        self.header = QHeaderView(Qt.Horizontal)
        #self.header.ResizeToContents()
        #mode1自動調整其大小，無法由使用者或程式修改
        self.header.setSectionResizeMode(1)
        #self.header.setCascadingSectionResizes(False)
        #記得將QHeaderView加入QTableView
        self.view.setHorizontalHeader(self.header)
        #隱藏某行(Column)_此為第0行_自動產生之id排序
        self.view.setColumnHidden(0,True)
        #self.view.clicked.connect(self.findrow)
        #若無Widget則新增，有則先刪除舊的再新增(解決DB更新會增加Widget的問題)
        if self.ui.verticalLayout == None:
            self.ui.verticalLayout.addWidget(self.view)
        else :
            self.ui.verticalLayout.itemAt(0).widget().deleteLater()
            self.ui.verticalLayout.addWidget(self.view)
        self.ui.pushButton.clicked.connect(lambda :self.model.removeRow(self.view.currentIndex().row()))
        #self.ui.verticalLayout.addWidget(view)

class fivWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_UI_mode4_choice()
        self.ui.setupUi(self)
    
class sixWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_UI_high_clear()
        self.ui.setupUi(self)

    def buttonClicked4(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        video_path = r".\video\backcourt_architecture\step_1_prepare.wmv"
        csv_path = r".\stages\mode4_data\backcourt_architecture\step_1_prepare.csv"
        
        stage4(cap, video_path, csv_path)

    def buttonClicked5(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        video_path = r".\video\backcourt_architecture\step_2_racket_up.wmv"
        csv_path = r".\stages\mode4_data\backcourt_architecture\step_2_racket_up.csv"
        
        stage4(cap, video_path, csv_path)

    def buttonClicked6(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        
        video_path = r".\video\backcourt_architecture\step_3_elbow_up_and_invert_racket.wmv"
        csv_path = r".\stages\mode4_data\backcourt_architecture\step_3_elbow_up_and_invert_racket.csv"
        stage4(cap, video_path, csv_path)
    
    def buttonClicked7(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        
        video_path = r".\video\backcourt_architecture\step_4_swing_racket.wmv"
        csv_path = r".\stages\mode4_data\backcourt_architecture\step_4_swing_racket.csv"

        stage4(cap, video_path, csv_path)

class sevWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_UI_smash()
        self.ui.setupUi(self)
    
    def buttonClicked8(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        
    
        video_path = r".\video\forehand_drop_shot\step_1_racket_up.wmv"
        csv_path = r".\stages\mode4_data\forehand_drop_shot\step_1_racket_up.csv"
        stage4(cap, video_path, csv_path)

    def buttonClicked9(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        

        video_path = r".\video\forehand_drop_shot\step_2_elbow_up.wmv"
        csv_path = r".\stages\mode4_data\forehand_drop_shot\step_2_elbow_up.csv"

        stage4(cap, video_path, csv_path)

    def buttonClicked10(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        
        video_path = r".\video\forehand_drop_shot\step_3_serve.wmv"
        csv_path = r".\stages\mode4_data\forehand_drop_shot\step_3_serve.csv"
        stage4(cap, video_path, csv_path)

class eigWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_UI_drop()
        self.ui.setupUi(self)  

    def buttonClicked11(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        

        video_path = r".\video\smash\step_1_racket_posing.wmv"
        csv_path = r".\stages\mode4_data\smash\step_1_racket_posing.csv"

        stage4(cap, video_path, csv_path)

    def buttonClicked12(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        
        video_path = r".\video\smash\step_2_elbow_up.wmv"
        csv_path = r".\stages\mode4_data\smash\step_2_elbow_up.csv"
        stage4(cap, video_path, csv_path)

    def buttonClicked13(self):
        print("mode4")
        global cap, detector
        if cap is None:
            print("No camera detected")
            return
        # 把載入好的yolov5保存下來 下次不用重新載入
        
        video_path = r".\video\smash\step_3_serve.wmv"
        csv_path = r".\stages\mode4_data\smash\step_3_serve.csv"

        stage4(cap, video_path, csv_path)
  
if __name__ == '__main__':
    import sys
    # python main.py -i 0 -w 1080 -e 1440
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--Input', type=str, default='0', help='input webcam number')
    parser.add_argument('-w', '--Width', type=int, default=1280, help='input webcam number')
    parser.add_argument('-e', '--Height', type=int, default=720, help='input webcam number')
    args = parser.parse_args()
    webcam_input_num = int(args.Input)
    webcam_width = int(args.Width)
    webcam_height = int(args.Height)

    cap = cv2.VideoCapture(webcam_input_num + cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    print("Camera resolution: ", cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    app = QtWidgets.QApplication(sys.argv)
    #創建四個視窗pyQT5
    window1 = MainWindow_controller()
    window2 = subWindow_controller()
    window3 = triWindow_controller()
    window4 = forWindow_controller()
    window5 = fivWindow_controller()
    window6 = sixWindow_controller()
    window7 = sevWindow_controller()
    window8 = eigWindow_controller()
    #建立排行榜資料庫
    createDB()
    #第一個視窗產生
    window1.show()
    window1.ui.play.clicked.connect(window2.show)
    window1.ui.play.clicked.connect(window1.close)
    #主選單頁面的四個按鈕
    window2.ui.modeButton1.clicked.connect(window2.buttonClicked1)
    window2.ui.modeButton2.clicked.connect(window3.show)
    window2.ui.modeButton2.clicked.connect(window2.close)
    window2.ui.modeButton3.clicked.connect(window2.buttonClicked3)
    window2.ui.modeButton4.clicked.connect(window5.show)
    window2.ui.modeButton4.clicked.connect(window2.close)
    #成績表單view加入pyQT5
    window2.ui.pushButton_2.clicked.connect(window4.show)
    window2.ui.pushButton_2.clicked.connect(window4.set_control)
    window2.ui.pushButton_2.clicked.connect(window2.close)
    #模式2選擇功能頁面按鈕實現
    window3.ui.mode2_1button.clicked.connect(window3.buttonClicked1)
    window3.ui.mode2_2button.clicked.connect(window3.buttonClicked2)
    #模式4選擇功能頁面按鈕實現
    window5.ui.clear_high_button.clicked.connect(window6.show)
    window5.ui.clear_high_button.clicked.connect(window5.close)
    window5.ui.smash_button.clicked.connect(window7.show)
    window5.ui.smash_button.clicked.connect(window5.close)
    window5.ui.smash_button_2.clicked.connect(window8.show)
    window5.ui.smash_button_2.clicked.connect(window5.close)
    #back功能
    window3.ui.backButton.clicked.connect(window2.show)
    window3.ui.backButton.clicked.connect(window3.close)
    window4.ui.pushButton_2.clicked.connect(window4.close)
    window4.ui.pushButton_2.clicked.connect(window2.show)
    window5.ui.backButton.clicked.connect(window2.show)
    window5.ui.backButton.clicked.connect(window5.close)
    window6.ui.backButton.clicked.connect(window5.show)
    window6.ui.backButton.clicked.connect(window6.close)
    window7.ui.backButton.clicked.connect(window5.show)
    window7.ui.backButton.clicked.connect(window7.close)
    window8.ui.backButton.clicked.connect(window5.show)
    window8.ui.backButton.clicked.connect(window8.close)
    #模式4 高遠球分解動作選擇功能頁面實現
    window6.ui.step1_Button.clicked.connect(window6.buttonClicked4)
    window6.ui.step2_Button.clicked.connect(window6.buttonClicked5)
    window6.ui.step3_Button.clicked.connect(window6.buttonClicked6)
    window6.ui.step4_Button.clicked.connect(window6.buttonClicked7)
    #模式4 高遠球分解動作選擇功能頁面實現
    window7.ui.step1_Button.clicked.connect(window7.buttonClicked8)
    window7.ui.step2_Button.clicked.connect(window7.buttonClicked9)
    window7.ui.step3_Button.clicked.connect(window7.buttonClicked10)
    #模式4 殺球分解動作選擇功能頁面實現
    window8.ui.step1_Button.clicked.connect(window8.buttonClicked11)
    window8.ui.step2_Button.clicked.connect(window8.buttonClicked12)
    window8.ui.step3_Button.clicked.connect(window8.buttonClicked13)
    sys.exit(app.exec_())
