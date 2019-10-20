import datetime
from flask import Flask, render_template, request
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api
from flask_restful import Api
from resources.view import ViewOne
from resources.user import User, UserRegister
from resources.search import Search
from resources.create import CreateTheme, CreateReport
app = Flask(__name__)

# access mongodb
server_theme = theme_db_api()
server_report = report_db_api()
theme = server_theme.get_all_theme()
api = Api(app)


@app.route('/', methods=["GET", "POST"])
def view():
    global theme
    # can obtain data if refreshing page
    theme = list(server_theme.get_all_theme())
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
@app.route('/createReport')
def create_report():
    theme_list = theme.get_all_theme_name()

    return render_template('CreateReport.html', theme_list=theme_list)


@app.route('/createReport/result', methods=['GET', 'POST'])
def create_report_result():
    if request.method == 'POST':
        global report
        reportTheme = request.form['ThemeName']
        reportTitle = request.form['ReportTitle']
        reportDescription = request.form['ReportDescription']
        reportTags = request.form['ReportTags']
        reportImage = request.form['ReportImage']
        reportLocation = request.form['ReportLocation']
        reportTags_list = [x.strip() for x in reportTags.split(',')]
        # insert the report information to the database(report_db)
        server_report.add_report("5d8eda3ee1b75277bae9e187", reportTitle, reportImage, datetime.datetime.now(),
                              reportTheme, reportLocation,
                              reportDescription, reportTags_list)
    result = request.form
    return render_template('result.html', result=result)



@app.route('/createTheme')
def create_theme():
    return render_template('CreateTheme.html')


@app.route('/createTheme/result', methods=['GET', 'POST'])
def create_theme_result():
    if request.method == 'POST':
        global theme
        themeName = request.form['ThemeName']
        coverImage = request.form['CoverImage']
        themeDescription = request.form['ThemeDescription']
        server_theme.add_theme(themeName, coverImage, themeDescription)
    result = request.form
    return render_template('result.html', result=result)


api.add_resource(CreateReport, '/createReport.html')
api.add_resource(CreateTheme, '/createTheme.html')

api.add_resource(ViewOne, '/view/<string:t_name>')
api.add_resource(User, '/user/<string:user_name>')
api.add_resource(UserRegister, '/user')
api.add_resource(Search, '/search.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
