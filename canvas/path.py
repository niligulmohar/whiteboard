
class Path(object):
    def __init__(self):
        self.nodes = []

    def append_node(self, x, y):
        self.nodes.append((x, y))

    def __str__(self):
        return str(self.nodes)

    def to_json_dict(self):
        return dict(nodes=self.nodes)

    @classmethod
    def from_json(cls, dictionary):
        result = Path()
        result.nodes = dictionary['nodes']
        return result
