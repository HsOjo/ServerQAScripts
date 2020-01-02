import re

import common
from base.config import Config


class SimpleConfig(Config):
    def _parse_value(self, value: str):
        if common.str_compare_head_tail(value, '"') or common.str_compare_head_tail(value, '\''):
            return value[1:-1]
        else:
            return value

    def _parse_object(self, line):
        obj = super()._parse_object(line)
        line_s = line.strip()
        if line_s != '':
            match = re.match('^(?P<key>[^#\s]*?)\s*=\s*(?P<value>.*?)$', line_s)
            if match is not None:
                obj.extra.update(match.groupdict())
                obj.value = self._parse_value(obj['value'])

        return obj

    def _map_object(self, obj):
        if obj['key'] is not None:
            self.set_map(obj['key'], obj)


if __name__ == '__main__':
    with open('../test/ifcfg') as io:
        content = io.read()
    c = SimpleConfig(content)
    print(c)

    with open('../test/grub') as io:
        content = io.read()
    c = SimpleConfig(content)
    print(c)
