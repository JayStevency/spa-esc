def check_essential_element(items):
    essential_keys = ['url', 'thumbnail', 'brand', 'title', 'price', 'originalSizeLabel', 'category']
    for key in essential_keys:
        if items.get(key) is None:
            return True
    
    return False


def replace_useless_chars(text, which_ones=('', '\xa0'), replace_by=''):
    for uc in which_ones:
        text = text.replace(uc, replace_by)
    return text
