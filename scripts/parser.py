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


def parse_list():
    projects = {}
    tree = ET.parse('svn_list.xml')
    root = tree.getroot()
    for entry in root.iter('entry'):
        name = entry.find("name").text
        commit = entry.find("commit")
        projects[name] = {"author": commit.find("author").text,
                                             "date": commit.find("date").text,
                                             "version": commit.get("revision")}
        if entry.find("size") is not None:
            projects[name]["size"] = entry.find("size").text

    tree = ET.parse('svn_log.xml')
    root = tree.getroot()
    for logentry in root.iter('logentry'):
        version = logentry.get("revision")
        author = logentry.find("author").text
        date = logentry.find("date").text
        msg = logentry.find("msg").text
        paths = logentry.find("paths")
        for path in paths.findall("path"):
            file_path = "/".join(path.text.split("/")[2:])
            if file_path not in projects:
                continue
            if "summary" not in projects[file_path]:
                projects[file_path]["summary"] = msg
            if "revision" not in projects[file_path]:
                projects[file_path]["revisions"] = [{"version": version, "author": author, "date": date}]
            else:
                projects[file_path]["revisions"].append({"version": version, "author": author, "date": date})

    print projects["Chess/Framework/Pieces/Piece.java"]
parse_list()
