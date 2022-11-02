from PyQt5.QtSql import QSqlDatabase,QSqlQuery
 
def createDB():
    if QSqlDatabase.contains("qt_sql_default_connection"):
        db = QSqlDatabase.database("qt_sql_default_connection")
    else:
        db = QSqlDatabase.addDatabase("QSQLITE")
    #指定SQLite数据库文件名
    db.setDatabaseName('DB.db')#muttonDB.db之前的目录都要存在才可建立成功！数据库名字自己随便起
    if not db.open():
        print('无法建立与数据库的连接')
        return False

    query=QSqlQuery()
    #insert_many_sql = """insert into people values(id,user,mode,grade) values(?,?,?,?);"""
    query.exec('create table people(id INTEGER PRIMARY KEY ,user varcahr(10),mode varcahr(10),grade int(50))')
    """
    data_list=[4,"popcorn","mode3",58000]
    insert_many_sql = "INSERT INTO people (id,user,mode,grade)" "VALUES(:id,:user,:mode,:grade)"
    query.prepare(insert_many_sql)
    query.bindValue(":id", data_list[0])
    query.bindValue(":user", data_list[1])
    query.bindValue(":mode", data_list[2])
    query.bindValue(":grade", data_list[3])
    
    """
 
    

    query.exec_()
    query.next()
    #query.clear()
    db.close
    return True



 
 
if __name__=='__main__':
    createDB()