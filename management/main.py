import datetime

from flask import Flask, render_template, request
from models.user_db_api import user_db_api
from report_db_api import report_db_api
from flask_restful import Api
from resources.user import User
import resources
app = Flask(__name__)

#access mongodb(open to discussion)
server = report_db_api()
report = server.search_report_by_location() #will change to search by id later
rIndex = 0 #current report index
api = Api(app)
@app.route('/')
def root():
    global report
    # can obtain data if refreshing page
    report = server.search_report_by_location()
    if len(report) == 0:
        # when report list is empty; 'length' is needed in html 
        return render_template('index.html', report=report, length=len(report))
    
    return render_template('index.html', report=report[rIndex], length=len(report))

@app.route('/incr', methods=["GET", "POST"])
def increment():
    global rIndex
    # make the list rotate
    if rIndex == len(report) - 1:
        rIndex = 0
    else:
        rIndex = rIndex + 1

    return render_template('index.html', report=report[rIndex], length=len(report))

@app.route('/decr', methods=["GET", "POST"])
def decrement():
    global rIndex
    if rIndex == 0:
        rIndex = len(report) - 1
    else:
        rIndex = rIndex - 1

    return render_template('index.html', report=report[rIndex], length=len(report))

@app.route('/delete', methods=["GET", "POST", "DELETE"])
def delete_report():
    global rIndex
    global report
    server.delete_report_by_id(report[rIndex]['_id'])
    #need to update report list after delete
    report = server.search_report_by_location()
    if len(report) == 0:
        return render_template('index.html', report=report, length=len(report))

    if rIndex == len(report):
        rIndex == rIndex - 1

    return render_template('index.html', report=report[rIndex], length=len(report))    

api.add_resource(User, '/user/<int:user_id>')
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

    
