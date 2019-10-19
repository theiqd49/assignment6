from flask_restful import Resource
from flask import request
from libs.strings import gettext
from models.user_db_api import user_db_api
user_api = user_db_api()
class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = user_api.get_user_by_uid(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        return {'user': user}, 200
    @classmethod
    def get(cls, user_name : str):
        user = user_api.get_user_by_username(user_name)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        return {'user': user}, 200

    @classmethod
    def delete(cls, user_id: int):
        user = user_api.delete_user_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        return {"user": user}, 200