from flask_restful import Resource, reqparse
from flask import render_template, make_response, request
from libs.strings import gettext
from models.user_db_api import user_db_api
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api

theme_api = theme_db_api()
report_api = report_db_api()
from libs import JSONEncoder


class CreateReport(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('report_title', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('report_image', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('report_time', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('report_theme', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('report_location', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('report_description', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('report_tags', type=list, required=True, help="this field cannot be left blank")

    def get(self):
        return make_response(render_template("CreateReport.html"), 200)

    def post(self):
        data = CreateReport.parser.parse_args()
        print(data)
        user_id = data['user_id']
        report_title = data['report_title']
        report_image = data['report_image']
        report_time = data['report_time']
        report_theme = data['report_theme']
        report_location = data['report_location']
        report_description = data['report_description']
        report_tags = data['report_tags']

        inserted_id = report_api.add_report(user_id, report_title, report_image, report_time, report_theme, report_location,
                                            report_description, report_tags)
        if inserted_id is None:
            return {'message': gettext("fail in adding report")}, 404
        else:
            return {'inserted_id': str(inserted_id)}, 200


class CreateTheme(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('theme_name', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('theme_coverimage', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('theme_description', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('theme_image_list', type=list, required=True, help="this field cannot be left blank")

    def post(self):
        data = CreateTheme.parser.parse_args()
        print(data)
        theme_name = data['theme_name']
        theme_coverimage = data['theme_coverimage']
        theme_description = data['theme_description']
        theme_image_list = data['theme_image_list']

        inserted_id = theme_api.add_theme(theme_name, theme_coverimage, theme_description, theme_image_list)
        if inserted_id is None:
            return {'message': gettext("fail in adding theme")}, 404
        else:
            return {'inserted_id': str(inserted_id)}, 200
