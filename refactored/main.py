import datetime
from flask import Flask, render_template, request
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api
from flask_restful import Api
from resources.view import ViewMain, ViewOne
from resources.user import User, UserRegister
from resources.search import Search
from resources.create import CreateTheme, CreateReport
from resources.management import Management
from resources.management import Manageincr
from resources.management import Managedele
app = Flask(__name__)
api = Api(app)


# access mongodb
report_server = report_db_api()
theme_server = theme_db_api()
# need api for getting report by user id to get a list of report of specified user
report = report_server.search_report_by_location()
rIndex = 0
# theme_server = theme_db_api()
# report_server = report_db_api()
# themes = theme_server.get_all_theme()


def get_all_themes():
    user = report_server.user_db_api.get_user_by_username("test")
    themes = []
    if user is not None:
        for theme in user['u_subscribed_themes']:
            themes.append(theme_server.get_theme_by_name(theme))
    return themes

def get_all_report():
    return report_server.search_report_by_location()

@app.route('/')
def root():
    themes = get_all_themes()
    report = get_all_report()
    if len(report) == 0:
        return render_template('manage.html', report=report, length=len(report), themes=themes)

    return render_template('manage.html', report=report[rIndex], length=len(report), themes=themes)


# @app.route('/createReport')
# def create_report():
#     theme_list = theme.get_all_theme_name()
#     return render_template('CreateReport.html', theme_list=theme_list)


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
        report_server.add_report("5d8eda3ee1b75277bae9e187", reportTitle, reportImage, datetime.datetime.now(),
                                 reportTheme, reportLocation,
                                 reportDescription, reportTags_list)
    result = request.form
    return render_template('result.html', result=result)



# @app.route('/createTheme')
# def create_theme():
#     return render_template('CreateTheme.html')


@app.route('/createTheme/result', methods=['GET', 'POST'])
def create_theme_result():
    if request.method == 'POST':
        global theme
        themeName = request.form['ThemeName']
        coverImage = request.form['CoverImage']
        themeDescription = request.form['ThemeDescription']
        theme_server.add_theme(themeName, coverImage, themeDescription)
    result = request.form
    return render_template('result.html', result=result)

# api.add_resource(ViewMain, '/') # this can't happen, since  ViewMain class is already used somewhere else
api.add_resource(CreateReport, '/createReport.html')
api.add_resource(CreateTheme, '/createTheme.html')
api.add_resource(ViewMain, '/view.html')
api.add_resource(ViewOne, '/viewone/<string:t_name>')
api.add_resource(User, '/user/<string:user_name>')
api.add_resource(UserRegister, '/user')
api.add_resource(Search, '/search.html')
api.add_resource(Management, '/manage.html')
api.add_resource(Manageincr, '/manageincr')
api.add_resource(Managedele, '/managedele/<int:index>')
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
