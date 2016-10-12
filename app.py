from flask import Flask, render_template, request
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


@app.route('/<project_name>')
def access_project(project_name=None):
    """
    http://stackoverflow.com/questions/12871153/managing-parameters-of-url-python-flask
    :return:
    """
    return render_template('project_page.html', project_name=project_name, project=projects[project_name])


@app.route('/<project>/<name>')
def access_subdirectory(project=None, name=None):
    is_file = request.args.get("is_file")
    current_directory = projects
    project_dirs = project.split("_")
    for dirs in project_dirs:
        current_directory = current_directory[dirs]
    if is_file == "True":
        return render_template('file_page.html', file_name=name, file_data=current_directory[name])
    else:
        project_path = project + "_" + name
        return render_template('project_page.html', project_name=project_path, project=current_directory[name])


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
