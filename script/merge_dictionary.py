import os
import sys
import argparse
import xml.etree.ElementTree as XmlTree
import xml.dom.minidom as minidom


class IdeaDictionaryProvider:
    """
    Provider class for dictionary in IDEA format.
    IDEA dictionary format is XML with pre-defined structure:
    <component name="ProjectDictionaryState">
        <dictionary name="username">
            <words>
                <w>Cortana</w>
                <w>Filesize</w>
            </words>
        </dictionary>
    </component>
    DictionaryProvider class has read() and write(new_dictionary) methods
    """

    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        if not os.path.isfile(self.xml_file_path):
            raise RuntimeError("File does not exist: %s" % self.xml_file_path)
        self.idea_dictionary = []
        tree = XmlTree.parse(xml_file_path)
        root = tree.getroot()

        for child in root.findall("./dictionary/words/w"):
            self.idea_dictionary.append(child.text)

    def read(self):
        """
        :return: list of dictionary items
        """
        return self.idea_dictionary

    def write(self, new_dictionary):
        """
        :param new_dictionary: New dictionary to write, normally merged from different sources
        """
        doc = minidom.Document()

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
        with open(self.xml_file_path, "w") as idea_dict:
            idea_dict.write(xml_text)


class VisualAssistDictionaryProvider:
    """
    Provider class for dictionary in Visual Assist format.
    DictionaryProvider class has read() and write(new_dictionary) method.
    Visual Assist dictionary format is EOL-separated plain text
    """

    def __init__(self, text_file_path):
        self.text_dictionary = []
        self.text_file_path = text_file_path
        with open(text_file_path) as f:
            self.text_dictionary = [item.strip() for item in f.readlines()]

    def read(self):
        """
        :return: list of dictionary items
        """
        return self.text_dictionary

    def write(self, new_dictionary):
        """
        :param new_dictionary: New dictionary to write, normally merged from different sources
        """
        with open(self.text_file_path, "w") as vassist_dict:
            vassist_dict.write("\n".join(new_dictionary))


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
