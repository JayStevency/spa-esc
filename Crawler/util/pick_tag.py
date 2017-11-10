class Picker:
    @classmethod
    def picker_fabric(cls, items):
        print(items)
        result = list(filter(lambda x: 'FABRIC' in x, items))[0]
        result = result.split(':')[1]
        return str.strip(result)
