""" File to run the App to put up the svn projects website. """

from flask import Flask, render_template, request
from scripts import parser

app = Flask(__name__)
projects = parser.parse_files()


@app.route('/')
def index():
    """ Serves the website's home page
    Used for templates:
    http://jinja.pocoo.org/docs/dev/templates/

    :return: index.html
    """
    return render_template('index.html', projects=projects)


@app.route('/<project_name>')
def access_project(project_name=None):
    """Serves the Project pages
    Used for passing parameters into routing:
    http://stackoverflow.com/questions/12871153/managing-parameters-of-url-python-flask

    :param project_name: The name of the project
    :return: project_page.html
    """
    return render_template('project_page.html', project_name=project_name, project=projects[project_name])


@app.route('/<project>/<name>')
def access_subdirectory(project=None, name=None):
    """ Serves the Subdirectory and File pages.

    :param project: The directory path to the file/subdirectory
    :param name: The name of the file/subdirectory
    :return: file_page.html or project_page.html
    """
    is_file = request.args.get("is_file")
    current_directory = projects
    project_dirs = project.split("_")
    for dirs in project_dirs:
        current_directory = current_directory[dirs]
    project_path = project + "_" + name
    if is_file == "True":
        return render_template('file_page.html', file_name=name, project_name=project, file_data=current_directory[name])
    else:
        return render_template('project_page.html', project_name=project_path, project=current_directory[name])


@app.route('/revisions/<project>/<file_name>')
def access_revisions(project=None, file_name=None):
    current_directory = projects
    project_dirs = project.split("_")
    for dirs in project_dirs:
        current_directory = current_directory[dirs]
    revisions = current_directory[file_name]["revisions"]
    return render_template('revisions_page.html', revisions=revisions, file_name=file_name)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
