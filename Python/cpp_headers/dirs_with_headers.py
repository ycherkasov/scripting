import os
import sys
from sets import Set

__doc__ = """The script looking for all directories with c/C++ headers and prints output into file
in Visual Studio Code include format.
Requires Python 2.7 according to customer requirement, sorry.
"""

def main():
    if len(sys.argv) != 2:
        print "Usage dirs_with_headers.py <path>"
        return 0

    res = Set([])
    my_path = sys.argv[1]
    for root, dirs, files in os.walk(my_path):
        for f in files:
            if f.endswith(".h"):
                correct_path = root.replace(my_path, "${workspaceFolder}")
                correct_path = correct_path.replace('\\', '/')
                res.add(correct_path)

    f = open("out.txt", "w+")
    for line in res:
        f.write('"{0}",\n'.format(line))
    f.close()

###########################################################################
if __name__ == '__main__':
    sys.exit(main())
