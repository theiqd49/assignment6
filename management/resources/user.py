from flask_restful import Resource, reqparse
from flask import request
from libs.strings import gettext
from models.user_db_api import user_db_api
user_api = user_db_api()
from libs import JSONEncoder
class User(Resource):


    def get(self, user_name):
        curr_user = user_api.get_user_by_username(user_name)
        if not curr_user:
            return {"message": gettext("user_not_found")}, 404

        return {'user_id' : str(curr_user['_id'])}, 200

    # @classmethod
    def delete(self, user_id: int):
        user = user_api.delete_user_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        return {"user": user}, 200

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_email', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('user_password', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('user_name', type=str, required=True, help="this field cannot be left blank")
    # @classmethod
    def post(self):
        data = UserRegister.parser.parse_args()
        print(data)
        user_name = data['user_name']
        user_email = data['user_email']
        user_password = data['user_password']
        inserted_id = user_api.add_user(user_name, user_email, user_password)
        if (inserted_id is None):
            return {'message' : gettext("fail in adding user")}, 404
        else:
            return {'inserted_id' : str(inserted_id)}, 200