from bs4 import BeautifulSoup


def __read_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    except FileNotFoundError:
        raise RuntimeError(f"Error: File not found at {file_path}")


def __html_has_label(html_file, label_id):
    html_parsed = BeautifulSoup(html_file, 'html.parser')

    label = html_parsed.find('label', {'for': label_id})
    input = html_parsed.find('input', {'id': label_id})
    return label and input and label['for'] == input['id']


def find_label_in_html(route, label_id):
    """
    Searches if a label with the given
    ID is associated to an input in an HTML file.

    This function reads an HTML file from the
    specified route and checks if a label
    with the provided label ID exists within the file
    and if it is associated with an input.

    Args:
        route (str): The file path to the HTML file.
        label_id (str): The ID of the label to
        search for in the HTML file.

    Returns:
        bool: True if the label with the
        specified ID is found in the HTML file and if
        it is associated with an input,
        False otherwise.
    """
    html_file = __read_html_file(route)
    return __html_has_label(html_file, label_id)


def __has_html5_tag(html_file, tag, args):
    soup = BeautifulSoup(html_file, 'lxml')
    return bool(soup.find(tag, args))


def has_specific_html5_tag_with_args(route, tag, args):
    """
    Checks if an HTML file contains
    a specific HTML5 tag with given attributes.

    Args:
        route (str): The file path to the HTML file.
        tag (str): The HTML5 tag to search
        for (e.g., 'div', 'span', 'section').
        args (Dict[str, str]): A dictionary of attributes
        to match for the tag (e.g.,
        {'class': 'my-class', 'id': 'my-id'}).

    Returns:
        bool: True if the HTML file contains
        the specified tag with the provided
        attributes, False otherwise.
    """
    html_file = __read_html_file(route)
    return __has_html5_tag(html_file, tag, args)
