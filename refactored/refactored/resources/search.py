from flask_restful import Resource
from flask import render_template, make_response, request
from models.report_db_api import report_db_api
from models.user_db_api import user_db_api


class Search(Resource):
    def get(self):
        return make_response(render_template("search.html"), 200)

    def post(self):
        report_obj = report_db_api()
        user_obj = user_db_api()
        if request.method == 'POST':
            keyword = request.form['keyword']
            field = request.form['field']
            if field == 'Tag':
                report_list = report_obj.search_report_by_tag([keyword])
            elif field == 'Location':
                report_list = report_obj.search_report_by_location(keyword)
            elif field == "All fields":
                report_list_temp = report_obj.search_report_by_tag([keyword])
                report_list_temp += report_obj.search_report_by_location(keyword)

                # Remove duplicated reports.
                # Yeah... it's a duplicated process
                _repo = []
                report_list = []
                for _report in report_list_temp:
                    if _report["_id"] not in _repo:
                        report_list.append(_report)
                        _repo.append(_report["r_uid"])

            for _idx, _report in enumerate(report_list):
                _username = user_obj.get_user_by_uid(_report["r_uid"])[
                    "u_username"]
                report_list[_idx]["r_username"] = _username

            return make_response(render_template("search.html",
                                                 reports=report_list), 200)
