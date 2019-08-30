import sys
import argparse
import xml.etree.ElementTree as element_tree


def read_idea_dictionary(xml_file_path):
    """
    :param xml_file_path: Path to standard IDEA dictionary or user-defined XML dictionary file
    :return: list of dictionary items
    """
    idea_dictionary = []
    tree = element_tree.parse(xml_file_path)
    root = tree.getroot()

    for child in root.findall("./dictionary/words/w"):
        idea_dictionary.append(child.text)

    return idea_dictionary


def read_vassist_dictionary(text_file_path):
    """
    :param text_file_path: Path to Visual Assist dictionary or user-defined text dictionary file
    :return: list of dictionary items
    """
    with open(text_file_path) as f:
        text_dictionary = [item.strip() for item in f.readlines()]

    return text_dictionary


def main():
    """
    Uninstall applications based on list, or simply retrieve the list of installed applications
    :return: System return code
    """
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--idea-dictionary',
                        help='Redirecting output from the script with the --list-bloatware key you can create a file'
                             'with the list of applications to uninstall',
                        dest='idea_dictionary',
                        required=True)
    parser.add_argument('--visual-assist-dictionary',
                        help='Redirecting output from the script with the --list-bloatware key you can create a file'
                             'with the list of applications to uninstall',
                        dest='user_text_dictionary',
                        default='atatat.xml',
                        required=False)
    parser.add_argument('--user-dictionary',
                        help='Redirecting output from the script with the --list-bloatware key you can create a file'
                             'with the list of applications to uninstall',
                        dest='user_idea_dictionary',
                        default='UserWords.txt',
                        required=False)

    args = parser.parse_args()

    idea_dictionary_file = args.idea_dictionary
    user_dictionary_file = args.user_idea_dictionary
    user_vassist_file = args.user_text_dictionary

    print("IDEA dictionary file: %s" % idea_dictionary_file)
    print("User IDEA file: %s" % user_dictionary_file)
    print("User VAssist file: %s" % user_vassist_file)

    idea_dictionary = read_idea_dictionary(idea_dictionary_file)
    user_dictionary = read_idea_dictionary(user_dictionary_file)
    text_dictionary = read_vassist_dictionary(user_vassist_file)

    merged_list = list(set(idea_dictionary).union(set(user_dictionary)).union(set(text_dictionary)))
    print(merged_list)

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())