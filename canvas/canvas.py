
import json

from .path import Path


class Canvas(object):
    def __init__(self):
        self.aspect_ratio = 1
        self.paths = []
        self.applied_actions = []
        self.undone_actions = []

    def apply_action(self, action):
        action.apply_to(self)
        self.applied_actions.append(action)
        self.undone_actions.clear()

    def undo(self):
        if len(self.applied_actions) > 0:
            action = self.applied_actions.pop()
            action.undo_for(self)
            self.undone_actions.append(action)

    def redo(self):
        if len(self.undone_actions) > 0:
            action = self.undone_actions.pop()
            action.apply_to(self)
            self.applied_actions.append(action)

    def to_json_dict(self):
        return dict(
            aspect_ratio=self.aspect_ratio,
            paths=self.paths
        )

    @classmethod
    def from_json(cls, dictionary):
        result = Canvas()
        result.aspect_ratio = dictionary['aspect_ratio']
        result.paths = dictionary['paths']
        return result


def load(fp):
    return json.load(fp, object_hook=json_object_hook)


def loads(string):
    return json.loads(string, object_hook=json_object_hook)


def dump(obj, fp):
    return json.dump(obj, fp, default=json_encode_default)


def dumps(obj):
    return json.dumps(obj, default=json_encode_default)


SERIALIZABLE_CLASSES = set((Canvas, Path))
SERIALIZABLE_CLASS_NAMES = set((x.__name__ for x in SERIALIZABLE_CLASSES))


def json_encode_default(obj):
    if obj.__class__ in SERIALIZABLE_CLASSES:
        result = obj.to_json_dict()
        result['__class__'] = obj.__class__.__name__
        return result
    else:
        raise TypeError('Not JSON encodable: {}'.format(obj))


def json_object_hook(dictionary):
    class_name = dictionary.get('__class__')
    if class_name in SERIALIZABLE_CLASS_NAMES:
        cls = globals()[class_name]
        return cls.from_json(dictionary)
    return dictionary
