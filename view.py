from flask import Flask, redirect, url_for, render_template
from theme_db_api import theme_db_api

app = Flask(__name__)
# access mongodb
server = theme_db_api()
theme = server.get_all_theme()


@app.route('/', methods=["GET", "POST"])
def view():
    global theme
    # can obtain data if refreshing page
    theme = list(server.get_all_theme())
    if len(theme) == 0:
        # when theme list is empty; 'length' is needed in html
        return render_template('view.html', theme=theme, length=len(theme))

    return render_template('view.html', theme=theme, length=len(theme))

# TODO should have a reports table with theme attribute
@app.route('/view_one/<name>', methods=["GET", "POST"])
def view_one(name):
    return render_template(
        "view_one.html"
    )


if __name__ == '__main__':
    app.run(debug=True)
