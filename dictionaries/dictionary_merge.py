import os
import sys
import argparse
import logging
import log_helper
import xml.etree.ElementTree as XmlTree
import xml.dom.minidom as minidom

logger = log_helper.setup_logger(name="dictionary_merge", level=logging.DEBUG, log_to_file=False)


class BaseDictionaryProvider:
    """
    Base class for all dictionary providers
    """
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.isfile(self.file_path):
            raise RuntimeError("File does not exist: %s" % self.file_path)

        self.dictionary_name = os.path.splitext(os.path.basename(self.file_path))[0]

    def name(self):
        """
        :return: Dictionary name
        """
        return self.dictionary_name

    def path(self):
        """
        :return: Path to dictionary file
        """
        return self.file_path


class IdeaDictionaryProvider(BaseDictionaryProvider):
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

    def __init__(self, file_path):
        """
        Open IDEA XML dictionary file
        :param file_path: Relative or absolute path to file
        :raise: RuntimeError if file does not exist
        """
        super(IdeaDictionaryProvider, self).__init__(file_path)
        self.idea_dictionary = []
        logger.info("Parse dictionary %s" % self.name())
        tree = XmlTree.parse(self.path())
        root = tree.getroot()

        for child in root.findall("./dictionary/words/w"):
            self.idea_dictionary.append(child.text)

    def read(self):
        """
        :return: List of dictionary items
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
        dictionary.setAttribute("name", self.dictionary_name)
        component.appendChild(dictionary)

        words = doc.createElement("words")
        dictionary.appendChild(words)

        for item in new_dictionary:
            w = doc.createElement("w")
            dict_item = doc.createTextNode(item)
            w.appendChild(dict_item)
            words.appendChild(w)

        xml_text = doc.toprettyxml(indent="  ")
        with open(self.path(), "w") as idea_dict:
            idea_dict.write(xml_text)


class VAssistDictionaryProvider(BaseDictionaryProvider):
    """
    Provider class for dictionary in Visual Assist format.
    DictionaryProvider class has read() and write(new_dictionary) method.
    Visual Assist dictionary format is EOL-separated plain text
    """

    def __init__(self, file_path):
        """
        Open VAssist plain text dictionary file
        :param file_path: Relative or absolute path to file
        :raise: RuntimeError if file does not exist
        """
        super(VAssistDictionaryProvider, self).__init__(file_path)
        self.text_dictionary = []
        logger.info("Parse dictionary %s" % self.name())
        with open(self.path()) as f:
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
        with open(self.path(), "w") as vassist_dict:
            vassist_dict.write("\n".join(new_dictionary))


def main():
    """
    Merge dictionaries using provided command-line params.
    :return: System return code
    """
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--idea-dictionary',
                        help='Add XML-based IDEA dictionary as a merge source',
                        action='append',
                        dest='idea_dictionary',
                        required=True,
                        default=[])
    parser.add_argument('--vassist-dictionary',
                        help='Add plain text Visual Assist dictionary as a merge source',
                        action='append',
                        dest='text_dictionary',
                        required=False,
                        default=[])

    args = parser.parse_args()
    all_dictionaries = []
    merged_set = set()

    for idea_xml_file in args.idea_dictionary:
        idea_dict_path = os.path.abspath(idea_xml_file)
        logger.info("User IDEA dictionary file: %s" % idea_dict_path)
        if not os.path.isfile(idea_dict_path):
            return 1
        idea_dict = IdeaDictionaryProvider(idea_dict_path)
        all_dictionaries.append(idea_dict)

    for text_file in args.text_dictionary:
        vassist_file_path = os.path.abspath(text_file)
        logger.info("User VAssist dictionary file: %s" % vassist_file_path)
        if not os.path.isfile(vassist_file_path):
            return 1
        vassist_dict = VAssistDictionaryProvider(vassist_file_path)
        all_dictionaries.append(vassist_dict)

    logger.info("%d dictionaries to merge" % len(all_dictionaries))

    for dictionary in all_dictionaries:
        new_dictionary = set(dictionary.read())
        logger.info("Size of appended dictionary [%s] is %d words" % (dictionary.name(), len(new_dictionary)))
        merged_set = merged_set.union(new_dictionary)

    merged_list = sorted(merged_set)

    for dictionary in all_dictionaries:
        logger.info("Write new dictionary to %s" % dictionary.path())
        dictionary.write(merged_list)

    logger.info("Merge complete, size of resulting dictionary is %d words" % len(merged_list))

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
