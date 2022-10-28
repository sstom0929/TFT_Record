import sqlite3

def ExecuteQuery(query):
    connection = sqlite3.connect("tftRecord.db")
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()
    connection.commit()
    connection.close()

def ExecuteQueryWithParameter(query, parameter):
    connection = sqlite3.connect("tftRecord.db")
    cursor = connection.cursor()
    cursor.execute(query, parameter)
    _id = cursor.lastrowid
    cursor.close()
    connection.commit()
    connection.close()
    return _id

def ExecuteQueryAndReturnResult(query):
    connection = sqlite3.connect("tftRecord.db")
    cursor = connection.cursor()
    cursor.execute(query)
    columnNames = [description[0] for description in cursor.description]
    result = cursor.fetchall()
    cursor.close()
    connection.commit()
    connection.close()
    result = [{columnNames[i]: row[i] for i in range(len(columnNames))} for row in result]
    return result

def CreateDB():
    # Create Main Table
    query = """CREATE TABLE Main (
        Key TEXT NOT NULL, 
        Value TEXT NOT NULL, 
        PRIMARY KEY(Key)
    )"""
    ExecuteQuery(query)

    # Create Record Table
    query = """CREATE TABLE Record (
        ID INTEGER NOT NULL, 
        Name TEXT NOT NULL, 
        Ranking INTEGER NOT NULL, 
        MMR INTEGER NOT NULL, 
        PRIMARY KEY(ID AUTOINCREMENT)
    )"""
    ExecuteQuery(query)

def InsertIntoMain(key, value):
    # Insert into Main Table
    query = """INSERT OR REPLACE INTO Main (Key, Value) 
        VALUES (:key, :value)"""
    parameter = {"key": key, "value": value}
    ExecuteQueryWithParameter(query, parameter)
    
def InsertIntoRecord(name, ranking, mmr):
    # Insert into Record Table
    query = """INSERT OR REPLACE INTO Record (Name, Ranking, MMR) 
        VALUES (:name, :ranking, :mmr)"""
    parameter = {"name": name, "ranking": ranking, "mmr": mmr}
    return ExecuteQueryWithParameter(query, parameter)

def UpdateRecord(_id, name, ranking, mmr):
    # Update Record Table
    query = """UPDATE Record SET Name = :name, 
        Ranking = :ranking, 
        MMR = :mmr 
        WHERE ID = :id
        """
    parameter = {"id": _id, "name": name, "ranking": ranking, "mmr": mmr}
    ExecuteQueryWithParameter(query, parameter)
    
def DeleteRecord(_id):
    # Delete Data in Record Table
    query = "DELETE FROM Record WHERE ID = :id" 
    parameter = {"id": _id}
    ExecuteQueryWithParameter(query, parameter)

def InsertDefaultValueIntoMain():
    InsertIntoMain("startMMRGroup", "鐵牌");
    InsertIntoMain("startMMRSubgroup", "IV");
    InsertIntoMain("startMMRValue", "0");
    InsertIntoMain("currentMMRGroup", "鐵牌");
    InsertIntoMain("currentMMRSubgroup", "IV");
    InsertIntoMain("currentMMRValue", "0");
    InsertIntoMain("mirageEffect", "閃電");
    InsertIntoMain("nomsyOrigin", "重砲手");
    
def InsertDefaultValueIntoRecord():
    InsertIntoRecord("戴迦", 1, 50);
    InsertIntoRecord("賽焚", 8, -30);

def SelectAllFromMain():
    query = "SELECT * FROM Main"
    return ExecuteQueryAndReturnResult(query)

def SelectAllFromRecord():
    query = "SELECT * FROM Record"
    return ExecuteQueryAndReturnResult(query)

def SelectAll():
    result = {}
    result["main"] = SelectAllFromMain()
    result["record"] = SelectAllFromRecord()
    return result