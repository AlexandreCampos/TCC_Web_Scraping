import re

from datetime import datetime


def get_current_time():
    '''
    Get current time.

    Returns:
        current_time (str): The current time
    '''
    
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_current_day():
    '''
    Get current day.

    Returns:
        current_day (str): The current day
    '''
    
    return datetime.now().strftime('%Y-%m-%d')


def get_sku_from_url(url, regexes):
    '''
    Gets the SKU from product url using the configured regexes.

    Args:
        regexes (list): The configured regexes

    Returns:
        SKU (str): Product SKU
    '''
    
    for regex in regexes:
        regex_match = re.search(regex, url)

        if regex_match:
            try:
                return regex_match.group(1)
            except Exception:
                return regex_match.group(0)

    return None


def parse_br_price(price_string):
    return float(price_string.replace('.', '').replace(',', '.'))


def get_price(price_text):
    '''
    Gets the price in float format from string format.

    Args:
        price_text (str): Price in string format

    Returns:
        price (float): Price in float format
    '''
    
    price_match = re.search(r"[\d\.]+,\d{2}", price_text)
    if price_match:
        return parse_br_price(price_match.group(0))

    price_match = re.search(r"[\d\.]+", price_text.replace('.', ''))
    if price_match:
        return float(price_match.group(0))

    return None


def get_value_from_element(key, element):
    '''
    Gets value from element in a JSON.

    Args:
        key (str): Key of element. It can be an index in a list or a normal key
        element (dict): JSON element

    Returns:
        value (list/float/str): Value from element
    '''

    # example: '[0]'
    regex = r'^\[(\d+)\]$'
    
    regex_match = re.search(regex, key)
    
    if regex_match:
        # get from list
        index = int(regex_match.group(1))
        return element[index]
    else:
        # get from dict
        return element.get(key)


def parser_json(json_page , keys):
    '''
    Parsing JSON to find a value from keys sequence.

    Args:
        json_page (dict): JSON represented in a dict
        keys (dict): The key sequence to find the value

    Returns:
        value (list/float/str): Value from element
    '''

    value = json_page

    for key in keys.split():
        value = get_value_from_element(key, value)

    return value
