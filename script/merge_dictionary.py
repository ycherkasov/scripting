import os
import sys
import argparse
import xml.etree.ElementTree as XmlTree
import xml.dom.minidom as minidom


class IdeaDictionaryProvider:

    def __init__(self, filename):
        self.filename = filename
        

def write_idea_dictionary(xml_file_path, new_dictionary):
    """
    :param xml_file_path: Path to standard IDEA dictionary or user-defined XML dictionary file
    :param new_dictionary: Merged dictionary thom that and other sources
    """
    doc = minidom.Document();

    component = doc.createElement("component")
    component.setAttribute("name", "ProjectDictionaryState")
    doc.appendChild(component)

    dictionary = doc.createElement("dictionary")
    dictionary.setAttribute("name", "atatat")
    component.appendChild(dictionary)

    words = doc.createElement("words")
    dictionary.appendChild(words)

    for item in new_dictionary:
        w = doc.createElement("w")
        dict_item = doc.createTextNode(item)
        w.appendChild(dict_item)
        words.appendChild(w)

    xml_text = doc.toprettyxml(indent="  ")
    with open(xml_file_path, "w") as idea_dict:
        idea_dict.write(xml_text)


def write_vassist_dictionary(text_file_path, new_dictionary):
    with open(text_file_path, 'w') as vassist_dict:
        vassist_dict.write("\n".join(new_dictionary))


def read_idea_dictionary(xml_file_path):
    """
    :param xml_file_path: Path to standard IDEA dictionary or user-defined XML dictionary file
    :return: list of dictionary items
    """
    idea_dictionary = []
    tree = XmlTree.parse(xml_file_path)
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
                        help='Add XML-based IDEA dictionary as a merge source',
                        action='append',
                        dest='idea_dictionary',
                        required=True)
    parser.add_argument('--vassist-dictionary',
                        help='Add plain text Visual Assist dictionary as a merge source',
                        action='append',
                        dest='text_dictionary',
                        required=False)

    args = parser.parse_args()
    merged_list = set()

    for idea_xml_file in args.idea_dictionary:
        idea_dict_path = os.path.abspath(idea_xml_file)
        print("IDEA dictionary file: %s" % idea_dict_path)
        if not os.path.isfile(idea_dict_path):
            return 1
        new_dictionary = set(read_idea_dictionary(idea_dict_path))
        print("Size of appended dictionary is %d words" % len(new_dictionary))
        merged_list = merged_list.union(new_dictionary)

    for text_file in args.text_dictionary:
        text_file_path = os.path.abspath(text_file)
        print("User VAssist file: %s" % text_file_path)
        if not os.path.isfile(text_file_path):
            return 1
        new_dictionary = set(read_vassist_dictionary(text_file_path))
        print("Size of appended dictionary is %d words" % len(new_dictionary))
        merged_list = merged_list.union(new_dictionary)

    merged_list = sorted(merged_list)
    print(merged_list)
    print("Size of resulting dictionary is %d words" % len(merged_list))

    print(args.idea_dictionary)
    print(args.text_dictionary)
    for idea_xml_file in args.idea_dictionary:
        idea_dict_path = os.path.abspath(idea_xml_file)
        print("Write new dictionary to %s" % idea_dict_path)
        write_idea_dictionary(idea_dict_path, merged_list)

    for text_file in args.text_dictionary:
        text_file_path = os.path.abspath(text_file)
        print("Write new dictionary to %s" % text_file_path)
        write_vassist_dictionary(text_file_path, merged_list)

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
