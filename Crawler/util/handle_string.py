import re


class ExtractPrice(object):
    def __call__(self, values):
        value = ''.join(values)
        return ''.join(re.findall('\d', value))


class AddHttpString(object):
    def __call__(self, values):
        for value in values:
            return 'http:' + value


class StringToList(object):
    def __call__(self, values):
        for value in values:
            return value.replace(' ', '').split(',')


class HandleString:
    @classmethod
    def remove_whitespace(cls, data):
        result = str.strip(data)
        result = re.findall('\S*\S', result)
        result = ' '.join(result)
        return result
    
    @classmethod
    def extract_digit_from_price(cls, data):
        result = str.strip(data)
        result = re.sub('\d+%', '', result)
        result = re.findall('\d', result)
        result = ''.join(result)
        return result
    
    @classmethod
    def extract_digit_from_product_no(cls, data):
        result = str.strip(data)
        result = re.search('\d+', data).group()
        return result
    
    @classmethod
    def extract_product_id_from_url(cls, data):
        data = str.strip(data)
        data = data.lower()
        result = re.search('(id=|no=)\d+', data).group()
        result = re.search('\d+', result).group()
        return result
