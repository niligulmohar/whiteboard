
from gi.repository import Whiteboard, GLib

wbs = Whiteboard.Whiteboards(service_name_prefix='potatis')
print(wbs.get_property('service_name'))
wbs.tomtar()
GLib.MainLoop().run()
