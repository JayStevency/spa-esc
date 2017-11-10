import re


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
