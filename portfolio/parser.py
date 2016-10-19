""" File to parse the SVN Materials to create a Projects Dictionary. """

import xml.etree.ElementTree as ET
import dateutil.parser

CODE_ENDINGS = [".py", ".java", ".c", ".cpp", ".h", ".js"]
IMAGE_ENDINGS = [".jpg", ".png"]
URL = "https://subversion.ews.illinois.edu/svn/fa16-cs242"
SVN_LIST_FILE = "portfolio/data/svn_list.xml"
SVN_LOG_FILE = "portfolio/data/svn_log.xml"


def parse_svn_list(svn_list):
    """ Parses the SVN List into a Projects dictionary.
    From the SVN List, parse the data about each of the files in the SVN repository.
    For help with parsing times:
    http://stackoverflow.com/questions/214777/how-do-you-convert-yyyy-mm-ddthhmmss-000z-time-format-to-mm-dd-yyyy-time-forma
    For help using XML Trees:
    https://docs.python.org/2/library/xml.etree.elementtree.html

    :param svn_list: File for the SVN List
    :return: Projects dictionary with the relevant information extracted.
    """
    projects = {}
    tree = ET.parse(svn_list)
    root = tree.getroot()
    for entry in root.iter('entry'):
        name = entry.find("name").text
        is_dir = entry.get("kind") == "dir"
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

        if author and date and version:
            current_directory[file_path_directories[-1]] = {"author": author,
                                                            "date": date,
                                                            "version": version,
                                                            "revisions": [],
                                                            "is_directory": is_dir}
        if entry.find("size") is not None:
            current_directory[file_path_directories[-1]]["size"] = entry.find("size").text
    return projects


def parse_svn_log(projects, svn_log):
    """Parse the SVN Log into the Projects dictionary.
    From the SVN Log, parse the data about each commit in the SVN Repository.

    :param projects: Projects dictionary after SVN list extraction
    :param svn_log: File for SVN Log
    :return: Projects dictionary after adding info from SVN Log
    """
    tree = ET.parse(svn_log)
    root = tree.getroot()
    for logentry in root.iter('logentry'):
        msg = logentry.find("msg").text
        parsed_date = dateutil.parser.parse(logentry.find("date").text)
        date = parsed_date.strftime('%m/%d/%Y %I:%M:%S %p')
        version = logentry.get("revision")
        author = logentry.find("author").text
        if not msg:
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
                continue
            if "is_directory" in current_directory[file_name]:
                is_dir = current_directory[file_name]["is_directory"]
                del current_directory[file_name]["is_directory"]
                if is_dir:
                    current_directory[file_name]["summary"] = msg
                    continue
            if "type" in current_directory[file_name]:
                if "version" not in current_directory[file_name]:
                    continue
                current_directory[file_name]["revisions"].append(
                    {
                        "version": version,
                        "author": author,
                        "summary": msg,
                        "date": date,
                        "url": current_directory[file_name]["url"] + "/?p=" + version
                    }
                )
                continue
            current_directory[file_name]["author"] = author
            current_directory[file_name]["date"] = date
            current_directory[file_name]["version"] = version
            current_directory[file_name]["summary"] = msg
            current_directory[file_name]["path"] = path.text
            current_directory[file_name]["url"] = URL + path.text
            if "test" in path.text.lower():
                current_directory[file_name]["type"] = "Test File"
            elif any(code_end in file_name for code_end in CODE_ENDINGS):
                current_directory[file_name]["type"] = "Code File"
            elif any(image_end in file_name for image_end in IMAGE_ENDINGS):
                current_directory[file_name]["type"] = "Image File"
            elif ".txt" in file_name:
                current_directory[file_name]["type"] = "Text File"
            else:
                current_directory[file_name]["type"] = "Other File"
    return projects


def parse_files(svn_list=SVN_LIST_FILE, svn_log=SVN_LOG_FILE):
    """ Function to parse data from the SVN List and the SVN Log

    :param svn_list: SVN List file to initialize projects with
    :param svn_log: SVN Log file to initialize projects with
    :return: Projects dictionary with information about all relevant files in SVN.
    """
    projects = parse_svn_list(svn_list)
    projects = parse_svn_log(projects, svn_log)
    return projects
