
class Whiteboard(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def publish(self):
        self.parent.add_service_for_whiteboard(self)

    def unpublish(self):
        self.parent.remove_service_for_whiteboard(self)
