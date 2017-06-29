
class TreeFormatter:
    def __init__(self):
        self.prettified_str = None

    def prettify(self, d, indent=0):
        if isinstance(d, dict):
            for key, value in d.items():
                self.prettified_str += '\n├─' * (indent + 1) + str(key)
                if isinstance(value, dict) or isinstance(value, list):
                    self.prettify(value, indent + 1)
                else:
                    self.prettified_str += '\n│  ├' + '─' * (indent + 1) + str(value)
        elif isinstance(d, list):
            for item in d:
                if isinstance(item, dict) or isinstance(item, list):
                    self.prettify(item, indent + 1)
                else:
                    if item == d[-1]:
                        self.prettified_str += '\n│  └' + '─' * (indent) + str(item)
                    else:
                        self.prettified_str += '\n│  ├' + '─' * (indent) + str(item)
        else:
            return Exception

