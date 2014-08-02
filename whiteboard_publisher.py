from gi.repository import GLib

import whiteboard

if __name__ == '__main__':
    whiteboards = whiteboard.Whiteboards('potatis', 4711)
    my_whiteboard = whiteboards.new_whiteboard('Gurk')
    my_whiteboard.publish()

    GLib.MainLoop().run()
