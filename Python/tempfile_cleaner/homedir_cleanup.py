import os
import re
import sys
import stat
import shutil
import argparse
import logging
import log_helper


logger = log_helper.setup_logger(name="homedir_cleaner", level=logging.DEBUG, log_to_file=True)


def on_rm_error(*args):
    """
    In case the file or directory is read-only and we need to delete it
    this function will help to remove 'read-only' attribute
    :param args: (func, path, exc_info) yuple
    """
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    _, path, _ = args
    os.chmod(path, stat.S_IWRITE)
    logger.warning("Unable to delete %s" % path)
    os.unlink(path)


def environment_value(environment_name):
    """
    :param environment_name: Name of the environment variable
    :return: Value of the environment variable or the empty string if not exists
    """
    try:
        return os.environ[environment_name]
    except KeyError:
        return ''


class SystemCleaner:
    """
    Class composes lists of files_erase and dirs_erase could be considered like temporary,
    and try to perform actual erase if possible
    """

    # Add files_erase math these masks to erasure list
    FILE_MASKS_ERASE = ["\\.log$", "\\.tmp$", "\\.tlog$", "\\.dmp$", ".*cache.*"]

    # Add dirs_erase math these masks to erasure list
    DIR_MASKS_ERASE = [".*cache.*"]

    # Exceptions, applied to file erasure list
    FILE_MASKS_EXCEPTIONS = ["\\.dll$", "\\.so$"]

    # Exceptions, applied to directory erasure list
    DIR_MASKS_EXCEPTIONS = []

    def __init__(self, home_paths_list):
        """
        :param home_paths_list: List of user home dirs_erase
        General case is just current user
        """
        self.home_paths_list = home_paths_list
        self.files_erase = []
        self.dirs_erase = []

    def erase_home_directory(self):
        for home_dir in self.home_paths_list:
            self.homedir_lookup(home_dir)

    def homedir_lookup(self, home_dir):
        """
        :return:
        """
        for mask in SystemCleaner.FILE_MASKS_ERASE:
            self.search_files(mask, home_dir)
        for mask in SystemCleaner.DIR_MASKS_ERASE:
            self.search_dirs(mask, home_dir)
        for file in self.files_erase:
            for exception in SystemCleaner.FILE_MASKS_EXCEPTIONS:
                if re.search(exception, file):
                    logger.info("Remove exception: %s" % file)
                    self.files_erase.remove(file)

    @staticmethod
    def remove_file(file):
        """
        :param file:
        :return:
        """
        try:
            if os.path.isfile(file):
                os.remove(file)
            logger.info("Deleted %s" % file)
        except Exception as e:
            logger.info("Unable to delete {0}: {1}".format(file, str(e)))

    @staticmethod
    def remove_directory(directory):
        """
        :param directory:
        :return:
        """
        try:
            if os.path.isdir(directory):
                shutil.rmtree(directory, onerror=on_rm_error)
                logger.info("Deleted %s" % directory)
        except Exception as e:
            logger.info("Unable to delete {0}: {1}".format(directory, str(e)))

    @staticmethod
    def match_regexp(mask, file):
        """
        :param mask: Python regular expression
        :param file: File or directory name without a full path
        :return: True if "file" march regexp "mask"
        """
        return re.search(mask, file, re.IGNORECASE)

    @staticmethod
    def files_callback(root_dir, condition, action):
        """
        The method is pretty universal. It performs simple traverse over directory tree,
        check all files to be matched to some condition, and perform callback action to that file
        :param root_dir: Directory where walk performed from
        :param condition: Callback which should return Boolean,
        where True means file is a subject of condition
        :param action: Callback action to perform with the matched file
        """
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if condition(file):
                    action(os.path.join(root, file))

    @staticmethod
    def dirs_callback(root_dir, condition, action):
        """
        The directory traverse version of files_callback()
        :param root_dir: Directory where walk performed from
        :param condition: Callback which should return Boolean,
        where True means file is a subject of condition
        :param action: Callback action to perform with the matched directory
        """
        for root, dirs, files in os.walk(root_dir):
            for directory in dirs:
                if condition(directory):
                    action(os.path.join(root, directory))

    @staticmethod
    def stop_windows_update():
        os.system("net stop wuauserv")

    def cleanup(self):
        for file in self.files_erase:
            self.remove_file(file)
        for directory in self.dirs_erase:
            self.remove_directory(directory)

    def print_files(self):
        print("\n".join([str(x) for x in self.files_erase]))

    def print_dirs(self):
        print("\n".join([str(x) for x in self.dirs_erase]))


def main():
    """
    Uninstall applications based on list, or simply retrreive the list of installed applications
    :return: System return code
    """
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--home',
                        help='User home directory, current user unless provided',
                        dest='home',
                        default="",
                        required=False)

    args = parser.parse_args()
    home = args.home
    if 0 == len(home):
        home = environment_value("USERPROFILE")

    if 0 == len(home):
        logger.warning("Unable to detect home directory neither from $USERPROFILE of --home command like key")
        return 0

    logger.info("Home directory %s" % home)

    cleaner = SystemCleaner(home)
    cleaner.homedir_lookup(home)
    cleaner.cleanup()

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
