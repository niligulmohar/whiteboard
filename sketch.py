#! /usr/bin/env python3

from itertools import chain
import os
import sys

import cairo
from gi.repository import Gtk, Gdk, Gio

import canvas


def debugger():
    from IPython.core.debugger import Tracer
    Tracer()()


class SketchApp(object):
    def __init__(self):
        self.app = Gtk.Application()
        self.window = None
        self.da = None

        self.canvas = canvas.Canvas()
        self.current_path = None

        self.app.connect('activate', self.on_activate)
        self.app.connect('startup', self.on_startup)
        self.app.connect('shutdown', self.on_shutdown)

    def run(self, argv):
        self.app.run(argv)

    def on_activate(self, arg):
        if self.window:
            self.window.present()

    def on_startup(self, arg):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('window.ui')
        self.window = self.builder.get_object('appwindow')
        self.window.set_application(self.app)
        self.window.set_wmclass('Potatis', 'Potatis')
        screen = self.window.get_screen()
        self.window.set_default_size(screen.width() * 2/3,
                                     screen.height() * 2/3)

        self.da = self.builder.get_object('drawingarea')
        self.da.connect('configure-event', self.on_configure)
        self.da.connect('draw', self.on_draw)
        self.da.connect('button-press-event', self.on_button_press)
        self.da.connect('button-release-event', self.on_button_release)
        self.da.connect('motion-notify-event', self.on_motion_notify)
        self.da.set_events(self.da.get_events()
                           | Gdk.EventMask.BUTTON_PRESS_MASK
                           | Gdk.EventMask.BUTTON_RELEASE_MASK
                           | Gdk.EventMask.POINTER_MOTION_MASK)

        self.clear_action = Gio.SimpleAction(name='clear')
        self.clear_action.connect('activate', self.perform_clear)
        self.app.add_action(self.clear_action)

        self.undo_action = Gio.SimpleAction(name='undo')
        self.undo_action.connect('activate', self.perform_undo)
        self.app.add_action(self.undo_action)

        self.redo_action = Gio.SimpleAction(name='redo')
        self.redo_action.connect('activate', self.perform_redo)
        self.app.add_action(self.redo_action)

        # action = Gio.SimpleAction(name='preferences')
        # action.connect('activate', self.test_action)
        # self.app.add_action(action)

        # action = Gio.SimpleAction(name='quit')
        # action.connect('activate', self.test_action)
        # self.app.add_action(action)

        # self.builder.add_from_string(self.APP_MENU)
        # self.app.set_app_menu(self.builder.get_object('appmenu'))

        self.try_load_file()
        self.window.show_all()
        self.redraw()

    # def test_action(self, action, arg):
    #     print('test_action')

    def perform_clear(self, action, arg):
        self.canvas.apply_action(canvas.actions.ClearCanvas())
        self.redraw()

    def perform_undo(self, action, arg):
        self.canvas.undo()
        self.redraw()

    def perform_redo(self, action, arg):
        self.canvas.redo()
        self.redraw()

    def redraw(self):
        self.clear_action.set_enabled(len(self.canvas.paths) > 0)
        self.undo_action.set_enabled(len(self.canvas.applied_actions) > 0)
        self.redo_action.set_enabled(len(self.canvas.undone_actions) > 0)
        self.da.queue_draw()

    PERSIST_FILE_NAME = u'persisted_sketch.json'

    def try_load_file(self):
        if os.path.isfile(self.PERSIST_FILE_NAME):
            with open(self.PERSIST_FILE_NAME, 'r') as fp:
                self.canvas = canvas.load(fp)

    def on_shutdown(self, arg):
        self.save_file()

    def save_file(self):
        with open(self.PERSIST_FILE_NAME, 'w') as fp:
            canvas.dump(self.canvas, fp)

    def on_configure(self, arg, arg1):
        self.width = self.da.get_allocated_width()
        self.height = self.da.get_allocated_height()

    BACKGROUND = (1, 1, 1)
    FOREGROUND = (0, 0, 0)

    def on_draw(self, widget, context):
        context.set_source_rgb(*self.BACKGROUND)
        context.paint()

        context.set_source_rgb(*self.FOREGROUND)
        context.set_line_width(min(self.width, self.height) / 50)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        for path in chain(self.canvas.paths, self.extra_paths()):
            context.move_to(*self.transformed_node(path.nodes[0]))
            for node in path.nodes[1:]:
                context.line_to(*self.transformed_node(node))
        context.stroke()

    def extra_paths(self):
        if self.current_path is not None:
            yield self.current_path
        else:
            return iter([])

    def transformed_node(self, node):
        return (node[0] * self.width, node[1] * self.height)

    BUTTON = 1
    BUTTON_MASK = Gdk.ModifierType.BUTTON1_MASK

    def on_button_press(self, widget, event):
        if event.button == self.BUTTON:
            self.new_path(event)
            self.redraw()

    def on_button_release(self, widget, event):
        if event.button == self.BUTTON:
            self.finish_path(event)
            self.redraw()

    def on_motion_notify(self, widget, event):
        if event.state & self.BUTTON_MASK:
            self.append_to_path(event)
            self.redraw()

    def new_path(self, event):
        self.current_path = canvas.Path()
        self.current_path.append_node(*self.xy_from_event(event))

    def append_to_path(self, event):
        self.current_path.append_node(*self.xy_from_event(event))

    def finish_path(self, event):
        action = canvas.actions.AddPath(self.current_path)
        self.canvas.apply_action(action)
        self.current_path = None

    def xy_from_event(self, event):
        return (event.x / self.width, event.y / self.height)

    APP_MENU = """
        <?xml version="1.0"?>
        <interface>
          <!-- interface-requires gtk+ 3.0 -->
          <menu id="appmenu">
            <section>
              <item>
                <attribute name="label" translatable="yes">_Preferences</attribute>
                <attribute name="action">app.preferences</attribute>
              </item>
            </section>
            <section>
              <item>
                <attribute name="label" translatable="yes">_Quit</attribute>
                <attribute name="action">app.quit</attribute>
              </item>
            </section>
          </menu>
        </interface>
    """

if __name__ == '__main__':
    SketchApp().run(sys.argv)
