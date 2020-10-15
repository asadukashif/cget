from json import dumps
from sys import argv, exit
from math import inf
import requests
from progress.bar import ChargingBar, FillingCirclesBar

MODE_PRINT = 0
MODE_FILE = 1
MODE_JSON = 2


def get_args():
    """
    Returns the Command Lines Arguments given by the user \n
        In the form of (URL, mode, filename)
    """
    filepath = None
    mode = None
    # To see if the URL is provided
    try:
        url = argv[1]
    except IndexError:
        usage()
        exit(1)

    # To see if the mode is provided
    try:
        mode_ = argv[2]
        if mode_ == '--json':
            mode = MODE_JSON
        elif mode_ == '--file':
            mode = MODE_FILE
        elif mode_ == '--print':
            mode = MODE_PRINT

        try:
            filepath = argv[3].strip()
        except IndexError:
            if mode == MODE_FILE and filepath == "":
                raise IndexError()
                usage()
                exit(1)

    except IndexError:
        filepath = get_filename_from_url(url).strip()
        if filepath == '':
            mode = MODE_PRINT
        else:
            mode = MODE_FILE

    if mode == MODE_FILE and filepath is None:
        usage()
        print("Enter a filename")
        exit(2)

    return url, mode, filepath


def usage():
    """ Prints how to use this program """
    print("Usage: cget <url> <mode (--file or --json --print)> <filename (optional)>")


def create_file(path):
    """ Creates an empty file in the path provided """
    try:
        f = open(path, 'w')
        f.close()
    except Exception:
        ...


def add_to_file(path, data, mode='ab'):
    """ Appends bytes to the file provided in the path with the data provided """
    try:
        with open(path, mode) as f:
            f.write(data)
            return True
    except Exception:
        return False


def get_filename_from_url(url):
    """ Returns the filename(if any) from the url provided """
    index = url.rfind("/")
    return url[index + 1:]


def to_KBs(bytes, decimal_places=2):
    """ Returns the bytes conversion into KBs """
    byte_length = 1024
    formatted = (bytes/byte_length).__round__(decimal_places)
    return formatted


def handle_file_mode(url, mode, filepath, json=False):
    """ Handles if the user requested the response to be stored in a file """
    BarType = ChargingBar
    CHUNK_SIZE = 1024 * 1024

    response = requests.get(url, stream=True)
    total_size = len(response.content)
    create_file(filepath)
    try:
        with BarType(filepath, max=total_size) as b:
            total_bytes = 0
            original_suffix = b.suffix
            for segment in response.iter_content(chunk_size=CHUNK_SIZE):
                segment_size = len(segment)
                total_bytes += segment_size
                b.suffix = original_suffix
                b.suffix += f"    {to_KBs(total_bytes)} KB - {to_KBs(segment_size)}KBs/sec"
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
