from flask_restful import Resource
from flask import request, render_template, make_response
from models.user_db_api import user_db_api
from models.report_db_api import report_db_api
from models.theme_db_api import theme_db_api

report_api = report_db_api()
theme_api = theme_db_api()
user_api = report_api.user_db_api
rindex = 0
report = report_api.search_report_by_location()

user = user_api.get_user_by_username("test")
themes = []
if user is not None:
    for theme in user['u_subscribed_themes']:
        themes.append(theme_api.get_theme_by_name(theme))

class Management(Resource):

    def get(self):
        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)

class Managedecr(Resource):

    def get(self):
        global rindex
        if rindex == 0:
            rindex = len(report) - 1
        else:
            rindex = rindex - 1
        
        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)
    
class Manageincr(Resource):

    def get(self):
        global rindex
        if rindex == len(report) - 1:
            rindex = 0
        else:
            rindex = rindex + 1

        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)

class Managedele(Resource):

    def get(self, index):
        global rindex
        global report
        report_api.delete_report_by_id(report[rindex]['_id'])

        report = report_api.search_report_by_location()

        if len(report) == 0:
            return make_response(render_template('manage.html', report=report, length=len(report), themes=themes), 200)

        if rindex == len(report):
            rindex = rindex - 1

        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)
                    
    def post(self, index):
        global rindex
        global report
        report_api.delete_report_by_id(report[rindex]['_id'])

        report = report_api.search_report_by_location()

        if len(report) == 0:
            return make_response(render_template('manage.html', report=report, length=len(report), themes=themes), 200)

        if rindex == len(report):
            rindex = rindex - 1

        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)

        
