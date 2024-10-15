import ctypes
import ctypes.wintypes

class Row:
    def __init__(self, columns, data):
        self.columns = columns
        self.data = data

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.data[item]
        elif isinstance(item, str):
            return self.data[self.columns.index(item)]
        else:
            raise TypeError("Invalid argument type.")

    def __repr__(self):
        return str(dict(zip(self.columns, self.data)))
