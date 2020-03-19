import os
import sys
import glob


def environment_value(environment_name):
    """
    :param environment_name: Name of the environment variable
    :return: Value of the environment variable or the empty string if not exists
    """
    try:
        return os.environ[environment_name]
    except KeyError:
        return ''


def files_with_compare(root_folder, file_name):
    """
    :param root_folder: Directory root project, where from we start looking for dictionaries
    :param file_name: Dictionary file name (should be the same for all IDEA projects)
    :return: List of paths to all dictionaries, including file name
    """
    dictionaries = []
    for filename in glob.iglob(os.path.join(root_folder, '*', file_name), recursive=True):
        dictionaries.append(filename)
    return dictionaries


def main():
    """
    Execute IDEA dictionaries synchronization as a pre-commit hook.
    Applicable to all IDEA-like projects (PyCharm, WebStorm etc)
    :return: System return code
    """
    projects_dir = environment_value("PROJECTS")
    if 0 == len(projects_dir):
        print("Environment variable PROJECTS is not found, exiting hook")
        sys.exit(0)

    print("Environment variable PROJECTS=%s", projects_dir)

    dictionaries_project = os.path.join(projects_dir, "personal_scripting/dictionaries")
    if not os.path.isdir(dictionaries_project):
        print("Personal IDEA dictionary directory is not found, exiting hook")
        sys.exit(0)

    print("Personal IDEA dictionary location %s", dictionaries_project)

    python_script = os.path.join(dictionaries_project, "dictionary_merge.py")
    personal_idea_dict = os.path.join(dictionaries_project, "idea/atatat.xml")

    if not os.path.isfile(python_script) or not os.path.isfile(personal_idea_dict):
        print("Python dictionary merger is not found, exiting hook")
        sys.exit(0)

    hook_dir = os.getcwd()
    project_dir = os.path.join(hook_dir, "..")

    print("Hook directory %s", hook_dir)
    print("Expected project directory %s", project_dir)

    dictionaries = files_with_compare(project_dir, "atatat.xml")
    merge_command = "python3 %s --idea-dictionary %s" % (python_script, personal_idea_dict)
    for dictionary in dictionaries:
        merge_command = merge_command + (" --idea-dictionary %s" % dictionary)

    os.system(merge_command)

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
