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


def replace_useless_chars(text, which_ones=('\xa0', '\t', '\r', '\n', '&nbsp'), replace_by=''):
    for uc in which_ones:
        text = text.replace(uc, replace_by)
    return text


class TakeUnique(object):
    def __call__(self, values):
        if '' in values:
            values.remove('')
        return values
