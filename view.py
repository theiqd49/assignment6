from flask import Flask, redirect, url_for
from flask import render_template

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def view():
    return render_template(
        'view.html'
    )


@app.route('/view_one/', methods=('GET', 'POST'))
def view_one():
    return render_template(
        "view_one.html"
    )


if __name__ == '__main__':
    app.run(debug=True)