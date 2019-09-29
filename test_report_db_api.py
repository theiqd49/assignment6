import datetime
import time
from report_db_api import report_db_api

if __name__ == "__main__":
    print("Test1: init a report_db_api object and connect to db.")
    report = report_db_api()
    now = datetime.datetime.now()
    time.sleep(1)
    print("Test2: add a new report with user id(u_id), target url and time. ")
    test_id = report.add_report("5d8eda3ee1b75277bae9e187", "url", now)
    time.sleep(1)
    print("Test3: get a detailed report by report id(r_id). ")
    print("Detailed report: ", report.get_report_by_rid(test_id))
    time.sleep(1)
    print("Test4: get a detailed report by location of the report. ")
    print("Detailed report: ", report.search_report_by_location("Mars"))
    time.sleep(1)
    print("Test5: delete a report by id. ")
    report.delete_report_by_id(test_id)
    time.sleep(1)
    print("Test6: delete a report which is not exist in the db. ")
    report.delete_report_by_id(test_id)