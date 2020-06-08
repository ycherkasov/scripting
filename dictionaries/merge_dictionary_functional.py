import os
import sys
import argparse
import xml.etree.ElementTree as XmlTree
import xml.dom.minidom as minidom


def pretty_formatting_xml(xml_file_path):
    dom = minidom.parse(xml_file_path)  # or xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = dom.toprettyxml()
    with open(xml_file_path, 'w') as xml_dict:
        xml_dict.write(pretty_xml_as_string)


def write_idea_dictionary(xml_file_path, new_dictionary):
    """
    :param xml_file_path: Path to standard IDEA dictionary or user-defined XML dictionary file
    :param new_dictionary: Merged dictionary thom that and other sources
    """
    doc = minidom.Document();

    component = doc.createElement("component")
    component.setAttribute("name", "ProjectDictionaryState")
    doc.appendChild(component)

    dictionary = doc.createElement("component")
    dictionary.setAttribute("name", "atatat")
    component.appendChild(dictionary)

    # TODO: the rest

    xml_text = XmlTree.tostring(component)
    with open(xml_file_path, "w") as idea_dict:
        idea_dict.write(xml_text.decode("utf-8"))


def write_idea_dictionary2(xml_file_path, new_dictionary):
    """
    :param xml_file_path: Path to standard IDEA dictionary or user-defined XML dictionary file
    :param new_dictionary: Merged dictionary thom that and other sources
    """
    component = XmlTree.Element("component")
    component.set("name", "ProjectDictionaryState")

    dictionary = XmlTree.SubElement(component, "dictionary")
    dictionary.set("name", "atatat")

    words = XmlTree.SubElement(dictionary, "words")
    for item in new_dictionary:
        w = XmlTree.SubElement(words, "w")
        w.text = item

    xml_text = XmlTree.tostring(component)
    with open(xml_file_path, "w") as idea_dict:
        idea_dict.write(xml_text.decode("utf-8"))


def write_vassist_dictionary(text_file_path, new_dictionary):
    with open(text_file_path, 'w') as vassist_dict:
        vassist_dict.seek(0)
        vassist_dict.writelines(new_dictionary)
        vassist_dict.truncate()


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
    debug = True

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

    print(merged_list)
    print("Size of resulting dictionary is %d words" % len(merged_list))

    for idea_xml_file in args.idea_dictionary:
        idea_dict_path = os.path.abspath(idea_xml_file)
        print("Write new dictionary to %s" % idea_dict_path)
        write_idea_dictionary(idea_dict_path, list(merged_list))

    if debug:
        return 0

    for text_file in args.text_dictionary:
        text_file_path = os.path.abspath(text_file)
        print("Write new dictionary to %s" % text_file_path)
        write_vassist_dictionary(text_file_path, list(merged_list))

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
