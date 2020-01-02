import re

from base.config import Config


class RulesConfig(Config):
    def _parse_object(self, line):
        obj = super()._parse_object(line)
        line_s = line.strip()
        if line_s != '':
            match = re.match(
                '^SUBSYSTEM=="net", ACTION=="add", DRIVERS=="\?\*", ATTR\{address\}=="(?P<address>.*?)", NAME="(?P<name>.*?)"$',
                line_s)
            if match is not None:
                obj.extra.update(match.groupdict())
                obj.value = obj['name']

        return obj

    def _map_object(self, obj):
        if obj['address'] is not None:
            self.set_map(obj['address'], obj)


if __name__ == '__main__':
    with open('../test/90-eno-pix.rules') as io:
        content = io.read()
    c = RulesConfig(content)
    c['00:50:56:3a:78:ee'] = 'eno1'
    c['00:0c:29:72:41:10'] = 'eno2'
    print(c.text)
