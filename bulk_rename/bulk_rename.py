import os
import sys
import re
import argparse
import logging
import log_helper


logger = log_helper.setup_logger(name="bulk_rename", level=logging.DEBUG, log_to_file=False)


class BulkRename:

    def __init__(self, input_dir, regexp):
        self.counter = 0
        self.regexp = regexp
        self.input_dir = input_dir
        logger.info(self.input_dir)

    def rename(self):
        """
        Rename file with leading two digits to leading 3 digits
        """
        for item in os.listdir(self.input_dir):
            if re.match(u"[0-9]{2}\\D.+\.jpg", item):
                old_item = item
                new_item = item.replace(item[:2], "{:03d}".format(self.counter), 1)
                self.counter = self.counter + 1
                logger.info("Rename %s to %s" % (old_item, new_item))



def main():
    """
    Perform backup or unpacking
    :return: Archiver system return code
    """
    parser = argparse.ArgumentParser(description='Command-line interface')
    parser.add_argument('--input-dir',
                        help='Directory to process',
                        dest='input_dir',
                        metavar='DIR',
                        required=True)

    parser.add_argument('--regexp',
                        help='Regular expression to filter files',
                        dest='regexp',
                        required=False)

    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    logger.info("Input directory: %s" % input_dir)

    # Input (backup source dir) check
    if not os.path.exists(input_dir):
        logger.warning("Source directory '{0}' does not exist".format(input_dir))
        return 1

    file_processor = BulkRename(input_dir=input_dir, regexp=args.regexp)
    file_processor.rename()

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())
