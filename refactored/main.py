import datetime
from flask import Flask, render_template, request
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api
from flask_restful import Api
from resources.view import ViewOne


app = Flask(__name__)

# access mongodb
server = theme_db_api()
theme = server.get_all_theme()
api = Api(app)


@app.route('/', methods=["GET", "POST"])
def view():
    global theme
    # can obtain data if refreshing page
    theme = list(server.get_all_theme())
    if len(theme) == 0:
        # when theme list is empty; 'length' is needed in html
        return render_template('view.html', theme=theme, length=len(theme))

    return render_template(
        'view.html', theme=theme, length=len(theme)
    )


@app.route('/view_one/<t_name>', methods=["GET", "POST"])
def view_one(t_name):
    server1 = report_db_api()
    report = list(server1.get_report_by_tname(r_tname=t_name))
    return render_template(
        "view_one.html", report=report, length=len(report)
    )


api.add_resource(ViewOne, '/view/<string:t_name>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)