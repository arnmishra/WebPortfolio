from time import strftime
from flask import Flask, render_template, request, redirect
from portfolio import db, app
from models import Comment, Expletives
import parser
import re

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


@app.route('/<project>/<file_name>', methods=['GET'])
def access_subdirectory(project=None, file_name=None):
    """ Serves the Subdirectory and File pages.

    :param project: The directory path to the file/subdirectory
    :param file_name: The name of the file/subdirectory
    :return: file_page.html or project_page.html
    """
    comments = Comment.query.filter(Comment.file_path == project + file_name, Comment.parent_id == -1).all()
    comment_replies = []
    for comment in comments:
        comment_replies.append(Comment.query.filter_by(parent_id=comment.id).all())
    is_file = request.args.get("is_file")
    current_directory = projects
    project_dirs = project.split("_")
    for dirs in project_dirs:
        current_directory = current_directory[dirs]
    if is_file == "True":
        return render_template('file_page.html', file_name=file_name, project_name=project,
                               file_data=current_directory[file_name], comments=comments,
                               comment_replies=comment_replies)
    else:
        project_path = project + "_" + file_name
        return render_template('project_page.html', project_name=project_path, project=current_directory[file_name])


@app.route('/<project>/<file_name>', methods=['POST'])
def add_comment(project=None, file_name=None):
    if "id" in request.form:
        comment_id = request.form.get("id")
        comment = Comment.query.get(comment_id)
        comment.votes += 1
    else:
        project = request.form.get("project")
        file_name = request.form.get("file_name")
        comment_text = edit_expletives(request.form.get("comment"))
        username = request.form.get("username")
        parent_id = request.form.get("parent_id")
        timestamp = strftime("%Y-%m-%d %H:%M:%S")
        new_comment = Comment(username, comment_text, timestamp, project + file_name, parent_id)
        db.session.add(new_comment)
        current_directory = projects
        project_dirs = project.split("_")
        for dirs in project_dirs:
            current_directory = current_directory[dirs]
    db.session.commit()
    return redirect('/' + project + '/' + file_name + '?is_file=True')


def edit_expletives(comment_text):
    """
    http://stackoverflow.com/questions/13090806/clean-line-of-punctuation-and-split-into-words-python
    :param comment_text:
    :return:
    """
    words = re.findall(r'[^\s!\-,.?":;0-9]+', comment_text)
    print words
    for word in words:
        censor = Expletives.query.filter(Expletives.expletive == word.lower()).first()
        if censor:
            comment_text = comment_text.replace(word, censor.correction)
    return comment_text


@app.route('/revisions/<project>/<file_name>')
def access_revisions(project=None, file_name=None):
    current_directory = projects
    project_dirs = project.split("_")
    for dirs in project_dirs:
        current_directory = current_directory[dirs]
    revisions = current_directory[file_name]["revisions"]
    return render_template('revisions_page.html', revisions=revisions, file_name=file_name)
