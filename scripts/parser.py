import xml.etree.ElementTree as ET

'''
The title of each of your projects
The date for each project
The version for each project
The summary for each project (the most recent commit message for that assignment)
A listing of each file in the project with
Its size
The type of the file: is one of code, test, image, documentation, resource, etc (feel free to add as many types as you wish).
The path is the path to your files in SVN.
The file itself loaded in an iframe only on demand
Each version of each file in the project
The number is the revision number for that commit
The author is the netid of the committer
The info is the commit message for that revision
The date is the date of that commit

https://docs.python.org/2/library/xml.etree.elementtree.html
'''
import dateutil.parser

URL = "https://subversion.ews.illinois.edu/svn/fa16-cs242"


def parse_list():
    """
    http://stackoverflow.com/questions/214777/how-do-you-convert-yyyy-mm-ddthhmmss-000z-time-format-to-mm-dd-yyyy-time-forma
    """
    projects = {}
    tree = ET.parse('svn_list.xml')
    root = tree.getroot()
    for entry in root.iter('entry'):
        name = entry.find("name").text

        commit = entry.find("commit")
        author = commit.find("author").text
        parsed_date = dateutil.parser.parse(commit.find("date").text)
        date = parsed_date.strftime('%m/%d/%Y %I:%M:%S %p')
        version = commit.get("revision")
        if not author or not date or not version:
            continue

        file_path_directories = name.split("/")
        current_directory = projects
        for directory in file_path_directories[:-1]:
            if directory in current_directory:
                current_directory = current_directory[directory]
            else:
                current_directory[directory] = {}
                current_directory = current_directory[directory]

        current_directory[file_path_directories[-1]] = {"author": author,
                                                        "date": date,
                                                        "version": version}
        if entry.find("size") is not None:
            current_directory[file_path_directories[-1]]["size"] = entry.find("size").text

    tree = ET.parse('svn_log.xml')
    root = tree.getroot()
    for logentry in root.iter('logentry'):
        version = logentry.get("revision")
        author = logentry.find("author").text
        date = logentry.find("date").text
        msg = logentry.find("msg").text
        if not version or not author or not date or not msg:
            continue
        paths = logentry.find("paths")
        for path in paths.findall("path"):
            action = path.get("action")
            if action == "D":
                continue
            file_path_directories = path.text.split("/")
            current_directory = projects
            for directory in file_path_directories[2:-1]:
                if directory in current_directory:
                    current_directory = current_directory[directory]
                else:
                    current_directory[directory] = {}
                    current_directory = current_directory[directory]
            file_name = file_path_directories[-1]
            if file_name not in current_directory:
                current_directory[file_name] = {}
            current_directory[file_name]["summary"] = msg
            current_directory[file_name]["revision"] = {"version": version, "author": author, "date": date}
            current_directory[file_name]["url"] = URL + path.text
    return projects
parse_list()
