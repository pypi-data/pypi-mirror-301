def _handle_list(data_list, keys):
    """
    Handles the traversal when the current level of data is a list.

    Parameters
    ----------
    data_list : list
        The list of data to traverse.
    keys : list
        The list of keys to follow in the data structure.

    Returns
    -------
    list
        A list of results found by traversing each item in the list.

    Notes
    -----
    - This function is called when the current level of data is a list.
    - When entering the `_traverse_keys` function, the first key is removed, since
        it has already been used to access the current level of data.
    """
    results = []
    remaining_keys = keys[1:]
    for item in data_list:
        result = _traverse_keys(item, remaining_keys)
        if result is not None:
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
    return results


def _traverse_keys(data, keys):
    """
    Traverses the data using the list of keys.

    Parameters
    ----------
    data : dict or list
        The nested dictionary or list to traverse.
    keys : list
        The list of keys to follow in the data structure.

    Returns
    -------
    any
        The value found at the specified path, or None if the path does not exist.
    """
    for key in keys:
        if data is None:
            return None

        if isinstance(data, list):
            return _handle_list(data, keys)

        if not isinstance(data, dict):
            return None

        data = data.get(key)

    return data


def get_value_by_path(data, path):
    """
    Recursively retrieves the value from a nested dictionary or list using a dot-separated path.

    Parameters
    ----------
    data : dict or list
        The nested dictionary or list to traverse.
    path : str
        A dot-separated string representing the path to the desired value.

    Returns
    -------
    any
        The value found at the specified path, or None if the path does not exist.
    """
    if not path:
        return data
    keys = path.split(".")
    return _traverse_keys(data, keys)


def matches_filter(response, filter_by):
    """
    Checks if a response matches all conditions specified in the filter_by dictionary.

    Parameters
    ----------
    response : dict
        A dictionary representing the JSON data of a JenkinsObject.
    filter_by : dict
        A dictionary where the keys are dot-separated paths to values in `response`,
        and the values are the expected values to match.

    Returns
    -------
    bool
        True if the `response` matches all the filter conditions, False otherwise.

    Notes
    -----
    - The function uses the `get_value_by_path` to traverse the `response` and
      retrieve the values based on the dot-separated paths provided in `filter_by`.
    - If the value retrieved from the `response` is a list, the function checks
      if the expected value is in the list. If the retrieved value is not a list,
      it is directly compared with the expected value.
    """
    for path, expected_value in filter_by.items():
        value = get_value_by_path(response, path)
        if isinstance(value, list):
            if expected_value not in value:
                return False
        elif value != expected_value:
            return False
    return True
