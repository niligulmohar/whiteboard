
class AddPath(object):
    def __init__(self, path):
        self.path = path

    def apply_to(self, canvas):
        canvas.paths.append(self.path)

    def undo_for(self, canvas):
        canvas.paths.pop()
