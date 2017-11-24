import re
from flashtext import KeywordProcessor
from Crawler.util.category import standard

NAME = 0
KEYWORD_SET = 1

keywordprocessor = KeywordProcessor()
keywordprocessor.add_keywords_from_dict(standard.CATEGORY)


class Categorizing:
    def __init__(self, item):
        self.item = item
    
    def get_item(self):
        return self.item
    
    def _get_category_from_title(self, title):
        
        if title is None or len(title) is 0:
            return None
        
        str_list = re.split('\W+|_', title)
        if len(str_list) is 1:
            
            category = keywordprocessor.extract_keywords(str_list[0])
            
            if not category:
                return None
            else:
                return category[0]
        
        category = keywordprocessor.extract_keywords(str_list[-1])
        if not category:
            return self._get_category_from_title(' '.join(str_list[:-1]))
        else:
            return category[0]
    
    def convert_category(self):
        pattern = '(fw)|(ss)|\(.*?\)|\[.*?\]'
        dettach_patten = '([a-zA-Z]+|[가-힣]+|7부|9부)'
        title = self.item['title'].lower()
        title = re.sub(pattern, '', title)
        title = ' '.join(re.findall(dettach_patten, title))
        self.item['category'] = self._get_category_from_title(title)
