    
def find_key_in_nested_dict(d:dict, serach_key:str):
    """
    Recursively search for a 'filename' key in a nested dictionary and return its value.

    Parameters
    ----------
    d : dict
        The dictionary to search.
    key : str
        The key to search for.

    Returns
    -------
    str or None
        The value of the 'filename' key, if found, or None if not found.
    """
    # Check if the current dictionary has the 'filename' key
    if serach_key in d:
        return d[serach_key]
    
    # Recursively search in nested dictionaries
    for key, value in d.items():
        if isinstance(value, dict):
            result = find_key_in_nested_dict(value, serach_key)
            if result:
                return result
    
    return None

