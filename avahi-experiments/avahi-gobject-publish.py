
# Attempt to publish a service through the Avahi GObject bindings

from gi.repository import Avahi, GLib


def connect_debug_callback(subject, signal):
    def callback(*args):
        print((subject, signal), args)

    subject.connect(signal, callback)


def on_client_state_changed(client, state):
    if state == Avahi.ClientState.GA_CLIENT_STATE_S_RUNNING:
        publish_service()


def publish_service():
    global group
    if group is None:
        group = Avahi.EntryGroup()
        group.connect('state-changed', on_group_state_changed)
        group.attach(client)

    # Missing: group.is_empty
    # Missing: group.add_service

    if True:  # group is empty
        # group.add_record(flags=0,
        #                  name='Potatis',
        #                  type='_potatis._tcp',
        # )

# add_record(self, flags:AvahiCore.PublishFlags, name:str, type:int, ttl:int, rdata, size:int)

def on_group_state_changed(*args):
    print('on_group_state_changed', args)


if __name__ == '__main__':
    group = None

    client = Avahi.Client()
    client.connect('state-changed', on_client_state_changed)
    client.start()

    GLib.MainLoop().run()
