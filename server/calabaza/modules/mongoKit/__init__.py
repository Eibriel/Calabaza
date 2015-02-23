

class Connection():
    def register(self, documents):
        pass


class Document():
    _data = {}

    def __setitem__(self, key, value):
        print (key)
        if self.structure.get(key) and self.validators.get(key)(value):
            self._data[key] = value
            print(value)

    def safe(self):
        return self._data
