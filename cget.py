
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


def handle_file_mode(url, mode, filepath, json=False):
    """ Handles if the user requested the response to be stored in a file """
    BarType = ChargingBar
    CHUNK_SIZE = 50 * 1024

    response = requests.get(url, stream=True)
    total_size = len(response.content)
    create_file(filepath)
    try:
        with BarType(filepath, max=total_size) as b:
            total_bytes = 0
            original_suffix = b.suffix
            for segment in response.iter_lines(chunk_size=CHUNK_SIZE):
                segment_size = len(segment)
                total_bytes += segment_size
                b.suffix = original_suffix
                b.suffix += f"    {to_KBs(total_bytes)} KB / {to_KBs(total_size)} KB"
                add_to_file(filepath, segment)
                b.next(segment_size)
        if json:
            add_to_file(filepath, dumps(response.json()), mode='w')
    except:
        print("An occurred during the process")


def handle_print_mode(url, mode, filepath, json=False):
    """ Handles if the user requested the response to be displayed to STD_OUT """
    response = requests.get(url)
    if not json:
        print(response.text)
    else:
        print(dumps(response.json()))


if __name__ == "__main__":
    Main()
