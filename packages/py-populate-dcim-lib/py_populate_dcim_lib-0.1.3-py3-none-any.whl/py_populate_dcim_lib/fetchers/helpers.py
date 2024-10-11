from argparse import Namespace


def print_inventory(item):
    """
    Display routine

    :param item: Object to print
    :return: None
    """
    print(item, " inventory:")
    for child in item.get_children():
        print_inventory(child)
    print(item.info())

def filter_info(bigData: dict, sharedAddrs: frozenset) -> dict:
    filteredData = {}
    for addr in sharedAddrs:
        if addr in bigData:
            filteredData[addr] = bigData[addr]
    return filteredData

def keys_exists(element: dict, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element: dict = element
    for key in keys:
        try:
            _element: dict = _element[key]
        except KeyError:
            return False
    return True

def xstr(str: None | str) -> str:
    if str is None:
        print("WARN: an empty string has been provided to template")
        return ""
    return str
    
def merge_two_dicts(starting_dict: dict, updater_dict: dict) -> dict:
    """
    Starts from base starting dict and then adds the remaining key values from updater replacing the values from
    the first starting/base dict with the second updater dict.

    For later: how does d = {**d1, **d2} replace collision?

    :param starting_dict:
    :param updater_dict:
    :return:
    """
    new_dict: dict = starting_dict.copy()   # start with keys and values of starting_dict
    new_dict.update(updater_dict)    # modifies starting_dict with keys and values of updater_dict
    return new_dict

def merge_args(args1: Namespace, args2: Namespace) -> Namespace:
    """

    ref: https://stackoverflow.com/questions/56136549/how-can-i-merge-two-argparse-namespaces-in-python-2-x
    :param args1:
    :param args2:
    :return:
    """
    # - the merged args
    # The vars() function returns the __dict__ attribute to values of the given object e.g {field:value}.
    merged_key_values_for_namespace: dict = merge_two_dicts(vars(args1), vars(args2))
    args = Namespace(**merged_key_values_for_namespace)
    return args