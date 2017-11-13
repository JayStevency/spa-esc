def check_essential_element(items):
    essential_keys = ['url', 'thumbnail', 'brand', 'title', 'price', 'category', 'originalSizeLabel']
    for key in essential_keys:
        if items.get(key) is None:
            return True
        return False
