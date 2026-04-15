from mininet.topo import Topo

class LinearFirewallTopo( Topo ):
    def build( self ):
        # Add 3 Hosts and explicitly assign MACs so our firewall can target them
        h1 = self.addHost('h1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03')

        # Add 3 Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Create the Linear topology: h1-s1-s2-s3-h3 (with h2 in the middle)
        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h2)
        self.addLink(s2, s3)
        self.addLink(s3, h3)

topos = { 'linear_fw': ( lambda: LinearFirewallTopo() ) }
