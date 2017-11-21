from Crawler.util.category import standard

NAME = 0
KEYWORD_SET = 1


class FrequencyDict(dict):
    def __add__(self, other):
        result = self.copy()
        if other is None:
            return result
        result.update(other)
        for k, v in other.items():
            if k in self:
                result[k] += self[k]
        return result
    
    def __radd__(self, other):
        result = other.copy()
        if self is None:
            return other
        result.update(self)
        for k, v in self.items():
            if k in other:
                result[k] += other[k]
        return result
    
    def __mul__(self, number):
        result = self.copy()
        if result is None:
            return None
        for k in result.keys():
            result[k] *= number
        return result
    
    def __rmul__(self, number):
        result = self.copy()
        if result is None:
            return None
        for k in result.keys():
            result[k] *= number
        return result


class Categorizing:
    def __init__(self, item):
        self.item = item
    
    def get_item(self):
        return self.item
    
    def _give_score(self, str_data):
        result = FrequencyDict({})
        for key in standard.CATEGORY:
            for keyword in key[KEYWORD_SET]:
                score = str_data.count(keyword)
                if score is not 0:
                    result[key[NAME]] = score
        return result
    
    def convert_category(self):
        category_word = "".join(self.item['category'])
        title = self.item['title'].lower()
        title_result = self._give_score(title)
        category_result = self._give_score(category_word)
        result = category_result + 2 * title_result
        if any(result):
            self.item['category'] = max(result.keys(), key=(lambda k: result[k]))
        else:
            self.item['category'] = None
