from dicttoxml import dicttoxml
import json
import re
from xml.dom.minidom import parseString


class NestedDict:
    _values = {}
    _value = None

    def __init__(self, value=None, values=None):
        self._value = value
        for key, value in values.items():
            self.set(key, value)
    
    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super().__setattr__(key, value)
        self.set(key, value)

    def __getattr__(self, key):
        if key.startswith('_'):
            return super().__getattr__(key)
        return self.get(key, value)

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def set(self, key, value):
        if '/' in key:
            key, sub_key = key.split('/', 1)
            self._values[key] = NestedDict(values={sub_key: value})
        else:
            self._values[key] = NestedDict(value=value)

    def get(self, key):
        return self._values[key]

    def get_values(self):
        return self._values


class OldNestedDict():
    def __init__(self, data={}):
        self.data = data

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def get(self, path):
        handler = self.data
        keys = path.split('/')
        for key in keys[:-1]:
            handler = handler[key]
        return handler[keys[-1]]

    def set(self, path, value):
        """
        >>> tags = NestedDict()
        tags.set('users[0]/lastname', 'kingbo')
        tags.set('users[0]/firstname', 'brunelle')
        tags.set('users[1]/lastname', 'bouchut')
        tags.set('users[1]/firstname', 'serge')
        tags.set('info', 'demo values')
        print(tags)
        {
            "users": [
                {
                    "lastname": "kingbo",
                    "firstname": "brunelle"
                },
                {
                    "lastname": "bouchut",
                    "firstname": "serge"
                },
            ],
            "info": "demo values"
        }

        """
        handler = self.data
        keys = path.split('/')
        for key in keys[:-1]:
            key, index = self.parse_index(key)
            if key not in handler.keys():
                handler[key] = {} if index is None else []
            handler = handler[key]
            if index is not None:
                while index >= len(handler):
                    handler.append({})
                handler = handler[index]

        last_key, index = self.parse_index(keys[-1])
        if index is not None:
            while index >= len(handler):
                handler.append(None)
            handler[last_key][index] = value
        else:
            handler[last_key] = value

    @staticmethod
    def parse_index(key):
        """
        >>> NestedDict.parse_index('key[0]')
        ('key', 0)
        >>> NestedDict.parse_index('key')
        ('key', None)
        """
        result = re.match('([^[]+)\[(\d+)]', key)
        if result:
            return result.group(1), int(result.group(2))
        return key, None

    def write_json(self, file_path):
        with open(file_path, 'w') as f:
            f.write(json.dumps(
                self.data,
                indent='\t',
            ))

    def write_xml(self, file_path):
        with open(file_path, 'w') as f:
            f.write(parseString(dicttoxml(
                self.data,
                attr_type=False,
                item_func=lambda parent_key: parent_key[:-1],
            )).toprettyxml())


def generate_demo_dict():
    tags = NestedDict()
    tags.set('users[0]/lastname', 'kingbo')
    tags.set('users[0]/firstname', 'brunelle')
    tags.set('users[1]/lastname', 'bouchut')
    tags.set('users[1]/firstname', 'serge')
    tags.set('info', 'demo values')
    print(tags)
    return tags
