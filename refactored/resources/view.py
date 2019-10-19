from flask_restful import Resource, reqparse
from flask import request
from libs.strings import gettext
from models.user_db_api import user_db_api
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api

theme_api = theme_db_api()
from libs import JSONEncoder


class ViewOne(Resource):

    def get(self, t_name):
        curr_theme = theme_api.get_theme_by_name(t_name)
        if not curr_theme:
            return {"message": gettext("theme_not_found")}, 404

        return {'theme name': str(curr_theme['t_name'])}, 200
