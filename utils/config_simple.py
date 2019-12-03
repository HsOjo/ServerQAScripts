import re

import common

TYPE_UNKNOWN = 0
TYPE_OPTION = 1


def parse_value(value: str):
    if common.str_compare_head_tail(value, '"') or common.str_compare_head_tail(value, '\''):
        return value[1:-1]
    else:
        return value


def parse_object(line):
    data = {'type': TYPE_UNKNOWN}
    if line.strip() != '':
        match = re.match('^\s*(?P<key>[^#\s]*?)\s*=\s*(?P<value>.*?)\s*$', line)
        if match is not None:
            data['type'] = TYPE_OPTION
            data.update(match.groupdict())
            data['value'] = parse_value(data['value'])

    data['raw'] = line
    return data


class SimpleConfig:
    def __init__(self, content: str):
        self._lines = content.split('\n')
        self._objects = []
        self._map = {}
        for line in self._lines:
            obj = parse_object(line)
            self._objects.append(obj)
            if obj['type'] == TYPE_OPTION:
                self._map[obj['key']] = obj

    def __getitem__(self, item):
        return self._map[item].get('modify') or self._map[item].get('value')

    def __setitem__(self, key, value):
        self._map[key]['modify'] = value

    def keys(self):
        return self._map.keys()

    def index(self, key):
        return self._objects.index(self._map[key])

    def insert(self, index, obj):
        self._objects.insert(index, obj)

    def pop(self, index):
        return self._objects.pop(index)

    def object(self, index):
        return self._objects[index]

    @property
    def text(self):
        objects = []
        for obj in self._objects:
            modify = obj.get('modify')
            if modify is not None:
                objects.append(obj['raw'].replace(obj['value'], obj['modify']))
            else:
                objects.append(obj['raw'])

        return '\n'.join(objects)
