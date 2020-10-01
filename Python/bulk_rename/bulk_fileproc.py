import os
import sys
import re
import argparse
import logging
import log_helper

__dec__ = """Bulk files processor. 
Does not intended to be universal, change the code every time you need different conditions.
Allows rename or remove, non-recursive or recursive 
"""

logger = log_helper.setup_logger(name="bulk_rename", level=logging.DEBUG, log_to_file=False)


class FileProcessor:

    def __init__(self, input_dir):
        """
        Counter is for mass renaming with a new index
        """
        self.counter = 0
        self.input_dir = input_dir

    def rename(self):
        """
        Rename file with leading 2 digits to leading 3 digits
        """
        for item in os.listdir(self.input_dir):
            if re.match(u"[0-9]{2}\\D.+\.jpg", item):
                old_item = item
                new_item = item.replace(item[:2], "{:03d}".format(self.counter), 1)
                self.counter = self.counter + 1
                os.rename(os.path.join(self.input_dir, old_item), os.path.join(self.input_dir, new_item))
                logger.info("Rename %s to %s" % (old_item, new_item))

    def remove(self):
        """
        Remove files start with "._"
        """
        for root, _, files in os.walk(self.input_dir):
            for filename in files:
                if filename.startswith("._"):
                    item = os.path.join(root, filename)
                    os.unlink(item)
                    logger.info("Removed %s" % item)


def main():
    """
    Perform directory processing
    :return: System return code
    """
    parser = argparse.ArgumentParser(description='Command-line interface')
    parser.add_argument('--input-dir',
                        help='Directory to process',
                        dest='input_dir',
                        metavar='DIR',
                        required=True)

    parser.add_argument('--rename',
                        help='Regular expression to filter files',
                        action='store_true',
                        required=False,
                        default=False)

    parser.add_argument('--remove',
                        help='Regular expression to filter files',
                        action='store_true',
                        required=False,
                        default=False)

    args = parser.parse_args()

    if args.rename and args.remove:
        logger.warning("Options --rename and --remove could not be selected at the same time")
        return 1

    if not args.rename and not args.remove:
        logger.warning("Choose either --rename or --remove option")
        return 1

    input_dir = os.path.abspath(args.input_dir)
    logger.info("Input directory: %s" % input_dir)

    # Input (backup source dir) check
    if not os.path.exists(input_dir):
        logger.warning("Source directory '{0}' does not exist".format(input_dir))
        return 1

    file_processor = FileProcessor(input_dir=input_dir)
    if args.rename:
        file_processor.rename()
    elif args.remove:
        file_processor.remove()

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
