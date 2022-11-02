import sys
from UI4 import Ui_Dialog
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *




class forWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def initializeModel(self,model):
        model.setTable('people')
        #当字段变化时会触发一些事件
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        #将整个数据装载到model中
        model.select()
        #设置字段头
        model.setHeaderData(0, Qt.Horizontal,'ID')
        model.setHeaderData(1, Qt.Horizontal, '使用者')
        model.setHeaderData(2, Qt.Horizontal, '模式')
        model.setHeaderData(3, Qt.Horizontal, '分數')
 
    #创建视图
    def createView(self,title,model):
        view = QTableView()
        view.setModel(model)
        view.setWindowTitle(title)
        return view
 
    def findrow(self,i):
        #当前选中的行
        delrow = i.row()
        print('del row=%s' % str(delrow))

    def set_control(self):
        if QSqlDatabase.contains("qt_sql_default_connection"):
            db = QSqlDatabase.database("qt_sql_default_connection")
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('DB.db')
        model = QSqlTableModel()#MVC模式中的模型
        self.delrow = -1
        self.initializeModel(model)
        view =self.createView("展示数据",model)
        view.clicked.connect(self.findrow)
        self.ui.verticalLayout.addWidget(view)
        self.ui.pushButton.clicked.connect(lambda :model.removeRow(view.currentIndex().row()))
        self.ui.verticalLayout.addWidget(view)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window4 = forWindow_controller()
    window4.set_control()
    """
    if QSqlDatabase.contains("qt_sql_default_connection"):
        db = QSqlDatabase.database("qt_sql_default_connection")
    else:
        db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName('DB.db')
    model = QSqlTableModel()#MVC模式中的模型
    delrow = -1
    window4.initializeModel(model)
    view = window4.createView("展示数据",model)
    view.clicked.connect(window4.findrow)
    window4.ui.verticalLayout.addWidget(view)
    window4.ui.pushButton.clicked.connect(lambda :model.removeRow(view.currentIndex().row()))
    window4.ui.verticalLayout.addWidget(view)

    """
    
    
    window4.show()
    sys.exit(app.exec_())
