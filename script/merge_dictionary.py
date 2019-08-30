
def main():
    """
    Uninstall applications based on list, or simply retrieve the list of installed applications
    :return: System return code
    """
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--idea-directory',
                        help='Redirecting output from the script with the --list-bloatware key you can create a file'
                             'with the list of applications to uninstall',
                        dest='applications_file',
                        default=False,
                        required=False)
    parser.add_argument('--idea-dictionary',
                        help='Redirecting output from the script with the --list-bloatware key you can create a file'
                             'with the list of applications to uninstall',
                        dest='applications_file',
                        required=True)
    parser.add_argument('--visual-assist-dictionary',
                        help='Redirecting output from the script with the --list-bloatware key you can create a file'
                             'with the list of applications to uninstall',
                        dest='applications_file',
                        default='atatat.xml',
                        required=False)
    parser.add_argument('--user-dictionary',
                        help='Redirecting output from the script with the --list-bloatware key you can create a file'
                             'with the list of applications to uninstall',
                        dest='applications_file',
                        default='UserWords.txt',
                        required=False)

    args = parser.parse_args()

    idea_xml_file = args.idea_dictionary
    user_xml_file = args.user_dictionary

    print("IDEA dictionary file: %s" % idea_xml_file)
    print("User dictionary file: %s" % user_xml_file)

    return 0


###########################################################################
if __name__ == '__main__':
    sys.exit(main())