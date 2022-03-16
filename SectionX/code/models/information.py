from multiprocessing import connection
import sqlite3

class InformationModel:
    def json(self):
        pass

    @classmethod
    def find_by_project_name(cls,info):
        connection=sqlite3.connect('data.db')
        cursor = connection.cursor()
        query="SELECT * FROM projects_info WHERE project_title=?"
        result=cursor.execute(query,(info,))
        row=result.fetchone()
        connection.close()
        if row is not None:
            return {'project': {'project title' : row[0],'business expense' : row[1]}}

    @classmethod
    def insert(cls,item):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="INSERT INTO projects_info VALUES (?,?)"
        cursor.execute(query,(item['Project_Name'],item['Business_Expense']))
        connection.commit()
        connection.close()
    
    @classmethod
    def update(cls,item):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="UPDATE projects_info SET business_expense=? WHERE project_title=?"
        cursor.execute(query,(item['Business_Expense'],item['Project_Name']))
        connection.commit()
        connection.close()
        
    