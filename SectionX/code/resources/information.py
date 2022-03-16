from multiprocessing import connection
import sqlite3
from models.information import InformationModel
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Information(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('project_title',type=str,required=True,help="Mandatory field")
    parser.add_argument('business_expense',type=float,required=True,help="Mandatory field")

    @jwt_required()
    def post(self,name):
        if InformationModel.find_by_project_name(name) is not None:
            return {"message" : "A project with the name '{}' alredy exist".format(name)},400
        else:
            data=Information.parser.parse_args()
            item={'Project_Name': name,'Business_Expense': data['business_expense']} ##
        try:
            InformationModel.insert(item)
            return item
        except:
            return {"message" : "An error occurred inserting the project"},500

    @jwt_required()
    def put(self,name):
        data=Information.parser.parse_args()
        info=InformationModel.find_by_project_name(name)
        updated_project={'Project_Name':name,'Business_Expense':data['business_expense']}
        if info is None:
            try:
                InformationModel.insert(updated_project)
            except:
                return {"message" : "An error occurred inseting the new porject"}
        else:
            try:
                InformationModel.update(updated_project)
            except:
                return {"message" : "An error occurred updating the new porject"}
        return updated_project

class InformatonList(Resource):
    @jwt_required()
    def get(self):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="SELECT * FROM projects_info"
        result=cursor.execute(query)
        infos=[]
        for row in result:
            infos.append({'Project Name' : row[0],'Business Expense' : row[1]})
        connection.close()
        return{'Project Information':infos}



