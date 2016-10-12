from flask import Flask, render_template
from scripts import parser

app = Flask(__name__)
projects = parser.parse_list()


@app.route('/')
def index():
    """
    http://jinja.pocoo.org/docs/dev/templates/
    Serves the website's home page
    :return: index.html
    """
    return render_template('index.html', projects=projects)


@app.route('/<project>')
def access_project(project=None):
    """
    http://stackoverflow.com/questions/12871153/managing-parameters-of-url-python-flask
    :return:
    """
    return render_template('project_page.html', project_name=project, project=projects[project])


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
