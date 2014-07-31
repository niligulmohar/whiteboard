
class ClearCanvas(object):
    def __init__(self):
        self.removed_paths = None

    def apply_to(self, canvas):
        self.removed_paths = canvas.paths
        canvas.paths = []

    def undo_for(self, canvas):
        canvas.paths = self.removed_paths
