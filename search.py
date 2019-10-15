from flask import Flask
from flask import render_template
from flask import request
import time

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        return render_template("test.html")
    return render_template("search.html")
