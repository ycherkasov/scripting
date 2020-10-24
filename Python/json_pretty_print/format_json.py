import os
import sys
import json


def format_json(json_filename):
    """
    :param json_filename: Absolute path
    :return: Formatted contents of JSON file
    """
    with open(json_filename, 'r') as file_json:
        your_json = file_json.read()
        parsed = json.loads(your_json)
        return json.dumps(parsed, indent=2, sort_keys=True)


def main():
    """
    Uninstall applications based on list, or simply retrieve the list of installed applications
    :return: System return code
    """
    if len(sys.argv) != 2:
        print("Usage: format_json.py [path filename]")
        sys.exit()

    json_filename = os.path.abspath(sys.argv[1])
    if not os.path.isfile(json_filename):
        print("File %s does not exist" % json_filename)
        sys.exit()

    formatted_json = format_json(json_filename)
    print(formatted_json)

    return 0

###########################################################################
if __name__ == '__main__':
    sys.exit(main())
