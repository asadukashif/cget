
"""
This piece of code is written by ShaderOX (https://github.com/ShaderOX/). It is open-source and freely available.
While using this kindly provide credits
Enjoy!
"""
from utils import *


def Main():
    """ Controls the main flow of the program """
    url, mode, filepath = get_args()
    if mode == MODE_JSON:
        if filepath:
            handle_file_mode(url, mode, filepath, json=True)
        else:
            handle_print_mode(url, mode, filepath, json=True)
    elif mode == MODE_FILE:
        handle_file_mode(url, mode, filepath)
    elif mode == MODE_PRINT:
        handle_print_mode(url, mode, filepath)


if __name__ == "__main__":
    Main()
