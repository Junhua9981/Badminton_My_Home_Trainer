from PyQt5.QtSql import QSqlDatabase,QSqlQuery

def addDB(user,mode,grade): 
    if QSqlDatabase.contains("qt_sql_default_connection"):
        db = QSqlDatabase.database("qt_sql_default_connection")
    else:
        db = QSqlDatabase.addDatabase("QSQLITE")
    #db=QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('DB.db')
    if not db.open():
        print('无法建立与数据库的连接')
        return False
    query=QSqlQuery()
    insert_many_sql = "INSERT INTO people (id,user,mode,grade)" "VALUES(:id,:user,:mode,:grade)"
    query.prepare(insert_many_sql)
    #query.bindValue(":id", id)
    query.bindValue(":user", user)
    query.bindValue(":mode", mode)
    query.bindValue(":grade", grade) 
    query.exec_()
    query.next()
    db.close
    return True

if __name__=='__main__':
    addDB("popcorn","mode3",3000) 
    addDB("yika","mode2",31000)
    addDB("gugu","mode3",2000)
    addDB("user8","mode4",3000)