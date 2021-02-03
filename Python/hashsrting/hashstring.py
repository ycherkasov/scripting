import os
import sys
import hashlib
from tkinter import Tk

__doc__ = """The script creates a simple string hash, need for my personal purposes"""

def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage hashstring.py <string> [hash_length]")
        return 0

    hash_len = 8
    string_to_hash = sys.argv[1]
    if len(sys.argv) == 3:
        hash_len = sys.argv[2]
    my_hash = int(hashlib.sha1(string_to_hash.encode('utf-8')).hexdigest(), 16) % (10 ** hash_len)
    print(my_hash)
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(my_hash)
    # now it stays on the clipboard after the window is closed
    r.update()
    r.destroy()
    return 0

###########################################################################
if __name__ == '__main__':
    sys.exit(main())
