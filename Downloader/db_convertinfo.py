import mysql.connector

class dbopen:
    def opendb():
        mydb = mysql.connector.connect(
        host="0.0.0.0",
        user="root",
        password="dbsGUR123@#",
        database="mysql",
        auth_plugin='mysql_native_password'
        )
        return mydb

class dbconverttable_insert:
    def dbinsertInfo(files, types): 
        mydb = dbopen.opendb()
     
        db_cursor = mydb.cursor()
        
        fileName = "filenametest.nc4"
        fileType = "nc4"
        insert_sql_query = "INSERT INTO converthistory(filename, filetype) VALUES (%s, %s)"        
        
        val = (files, types)
        
        # Execute cursor and pass query as well as student data
        try: 
            db_cursor.execute(insert_sql_query, val)
            # for table in db_cursor:
            # print(table)        
            mydb.commit()
            print(db_cursor.rowcount, "Convert record inserted")
            
        except Error as error:
            print(error)
        
        finally:
            db_cursor.close()
            mydb.close()
            
        # Get List of all databases
        # db_cursor.execute("SHOW DATABASES")
        
        # for db in db_cursor:
        # print(db)
class dbconverttable_delete:
    def dbdeleteInfo(file, type):
        mydb = dbopen.opendb()
        db_cursor = mydb.cursor()
        
        delete_sql_query = "DELETE FROM converthistory WHERE filename = %s"        
        #val = (files, types)
        val =(file)
        # Execute cursor and pass query as well as delete_sql_query data
        try:
            db_cursor.execute(delete_sql_query, (file,))
            
            mydb.commit()
            print(db_cursor.rowcount, "convert record delete")
        except Error as error:
            print(error)
        finally:
            db_cursor.close()
            mydb.close()
    
#dbtable.dbinsertInfo('AddFilenameHere1', 'AddFileTypeHere3')
#dbtable.dbdeleteInfo('AddFilenameHere2', 'AddFileTypeHere3')
