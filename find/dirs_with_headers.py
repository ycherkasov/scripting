import os
import sys
from sets import Set

__doc__ = """Script looking for headers and print containig directories in Visual Studio Code include format
"""

def main():
    res = Set([])
    my_path = "C:\\Users\\yuric\\Projects\\virtualbox\\VirtualBox-5.2.2\\src"
    for root, dirs, files in os.walk(my_path):
        for file in files:
            if file.endswith(".h"):
                correct_path = root.replace(my_path, "${workspaceFolder}")
                correct_path = correct_path.replace('\\', '/')
                res.add(correct_path)
    print res

###########################################################################
if __name__ == '__main__':
    sys.exit(main())
