
namespace Whiteboard {
	public class Whiteboards : Object {
		public string service_name_prefix { get; set; default = "potatis"; }
		public string service_name {
			owned get {
				return @"_$(service_name_prefix)_whiteboard._tcp";
			}
		}
		public uint16 port { get; set; default = 4711; }

		private AvahiServer avahi_server;
		private ServiceBrowser service_browser;

		public void tomtar () throws IOError {
			if (avahi_server == null) {
				AsyncReadyCallback on_found_service = (obj, res) => {
					int o_interf;
					int o_protocol;
					string o_name;
					string o_service_type;
					string o_domain;
					string o_fqdn;
					int o_address_protocol;
					string o_address;
					uint16 o_port;
					uchar[] o_txt;
					uint o_flags;
					try {
						avahi_server.resolve_service.end(res,
														 out o_interf,
														 out o_protocol,
														 out o_name,
														 out o_service_type,
														 out o_domain,
														 out o_fqdn,
														 out o_address_protocol,
														 out o_address,
														 out o_port,
														 out o_txt,
														 out o_flags);
						print (@"Resolved! $o_address:$port\n");
					} catch (IOError e) {
						print (@"Service resolution failed: $(e.message)");
					}
				};
				avahi_server = Bus.get_proxy_sync (BusType.SYSTEM, "org.freedesktop.Avahi", "/");
				var browser_path = avahi_server.service_browser_new(-1, -1, service_name, "local", 0);
				service_browser = Bus.get_proxy_sync (BusType.SYSTEM, "org.freedesktop.Avahi", browser_path);
				service_browser.item_new.connect((interf, protocol, name, service_type, domain, flags) => {
						avahi_server.resolve_service.begin(interf,
														   protocol,
														   name,
														   service_type,
														   domain,
														   -1,
														   0,
														   on_found_service);
						print (@"$name\n");
					});
			}
		}
	}

	[DBus (name = "org.freedesktop.Avahi.Server")]
	private interface AvahiServer : Object {
		public abstract string service_browser_new (int interface, int protocol, string type, string domain, uint flags) throws IOError;
		public abstract async void resolve_service (int interface, int protocol, string name, string service_type, string domain, int address_protocol, uint flags, out int o_interface, out int o_protocol, out string o_name, out string o_type, out string o_domain, out string host, out int o_address_protocol, out string address, out uint16 port, out uchar[] txt, out uint o_flags) throws IOError;
	}

	[DBus (name = "org.freedesktop.Avahi.ServiceBrowser")]
	private interface ServiceBrowser : Object {
		public signal void item_new (int interface, int protocol, string name, string service_type, string domain, uint flags);
	}
}