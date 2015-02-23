

class Connection():
    def register(self, documents):
        pass


class Document():
    _data = {}

    def __setitem__(self, key, value):
        print (key)
        print (value)
        if self.structure.get(key) and self.validators.get(key)(value):
            self._data[key] = value
        else:
            raise ValueError("Validation Error")

    def safe(self):
        return self._data
