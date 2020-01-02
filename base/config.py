from typing import Dict, List
import common

class Object:
    def __init__(self, raw: str):
        self._raw = raw
        self._value = None  # type: str
        self._modify = None  # type: str
        self._text = None  # type: str
        self.extra = {}

    def __getitem__(self, key):
        return self.extra.get(key)

    def __setitem__(self, key, value):
        self.extra[key] = value

    @property
    def value(self):
        if self._modify is not None:
            return self._modify
        return self._value

    @value.setter
    def value(self, value):
        if self._value is None:
            self._value = value
        else:
            self._modify = value

    @property
    def text(self):
        if self._text is not None:
            return self._text

        if self._modify is not None:
            if self._raw.count(self._value) > 1:
                raise Exception('Too many value inline.')
            return self._raw.replace(self._value, '%s' % self._modify, 1)
        return self._raw

    @text.setter
    def text(self, text):
        self._text = text

    def __repr__(self):
        content = super().__repr__()
        if self.value is not None:
            return '%a' % self.value

        return '%s %s' % (content, self.text)


class Config:
    def __init__(self, content: str, sep='\n'):
        self._objects = []  # type: List[Object]
        self._map = {}  # type: Dict[str, Object]

        for line in content.split(sep):
            obj = self._parse_object(line)
            self.append(obj)

    def _parse_object(self, line):
        return Object(line)

    def _map_object(self, obj: Object):
        pass

    def set_map(self, k, v):
        self._map[k] = v

    def __getitem__(self, key):
        return self._map[key].value

    def __setitem__(self, key, value):
        self._map[key].value = value

    def keys(self):
        return self._map.keys()

    def index(self, key):
        return self._objects.index(self._map[key])

    def append(self, obj):
        self._objects.append(obj)
        self._map_object(obj)

    def insert(self, index, obj):
        self._objects.insert(index, obj)
        self._map_object(obj)

    def pop(self, index):
        obj = self._objects.pop(index)
        for k, v in self._map:
            if v == obj:
                return self._map.pop(k)

    def object(self, index):
        return self._objects[index]

    @property
    def text(self):
        lines = []
        for obj in self._objects:
            lines.append(obj.text)
        return '\n'.join(lines)

    def __repr__(self):
        content = super().__repr__()
        if len(self._map) != 0:
            return '%s\n\t%a' % (content, self._map)

        return '%s\n%s\n%s' % (content, self.text, content.replace('<', '</', 1))
