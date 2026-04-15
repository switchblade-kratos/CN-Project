from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str

log = core.getLogger()

class CustomFirewallController(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.mac_to_port = {} 

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return

        packet_in = event.ofp
        
        # --- FIREWALL LOGIC (THE BLOCKED CASE) ---
        # Block traffic between h1 (00:00:00:00:00:01) and h3 (00:00:00:00:00:03)
        mac_src = packet.src.toStr()
        mac_dst = packet.dst.toStr()
        
        if (mac_src == "00:00:00:00:00:01" and mac_dst == "00:00:00:00:00:03") or \
           (mac_src == "00:00:00:00:00:03" and mac_dst == "00:00:00:00:00:01"):
            log.warning("FIREWALL ACTIVE: Dropping packet between %s and %s", mac_src, mac_dst)
            
            # Send an OpenFlow rule with NO actions (This drops the packet)
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            self.connection.send(msg)
            return
        # -----------------------------------------

        # NORMAL LEARNING & ROUTING (THE ALLOWED CASE)
        self.mac_to_port[packet.src] = packet_in.in_port

        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 10
            msg.hard_timeout = 30
            msg.actions.append(of.ofp_action_output(port = out_port))
            msg.data = event.ofp
            self.connection.send(msg)
        else:
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = packet_in.in_port
            self.connection.send(msg)

    def _handle_PortStatus(self, event):
        # FAILURE LOGIC
        if event.ofp.desc.state & of.OFPPS_LINK_DOWN:
            log.error("CRITICAL: Link Failure on Port %s. Linear network severed.", event.port)
            self.mac_to_port.clear()
            msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
            self.connection.send(msg)

def launch():
    def start_switch(event):
        log.info("Controlling switch: %s", dpid_to_str(event.dpid))
        CustomFirewallController(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
