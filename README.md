# SDN Mininet Simulation - Linear Topology with Firewall

## 1. Problem Statement
The objective of this project is to deploy a custom OpenFlow SDN controller to manage a linear network topology. The controller is programmed with explicit match-action rules to handle dynamic forwarding, respond to link failures, and enforce access control (Firewall) by blocking specific MAC-to-MAC communications.

## 2. Setup and Topology Design
The network utilizes a Custom Linear Topology (`h1-s1-s2-s3-h3` with `h2` attached to `s2`). This design was chosen specifically to highlight the vulnerability of non-redundant networks during failure states, and to test multi-hop firewall rules.

**Execution:**

```bash
# Start Controller
python3 pox.py my_controller

# Start Mininet
sudo mn --custom topo.py --topo linear_fw --controller=remote,port=6633 --mac --switch=ovsk
```

## 3. Test Cases

* **Case 1 (Allowed):** Traffic between `h1` and `h2` is permitted. The controller installs standard forwarding rules.


* **Case 2 (Blocked):** The controller acts as a firewall. Any packet matching `src=h1` and `dst=h3` triggers a drop action (an OpenFlow rule with an empty action list), blocking communication.


* **Case 3 (Normal):** The core link between `s1` and `s2` is healthy, allowing full UDP throughput (`iperf`) and ICMP latency testing.


* **Case 4 (Failure):** The `link s1 s2 down` command is issued. The controller's `PortStatus` event detects the failure and logs the severance. Because this is a linear topology, no failover path exists, resulting in total packet loss.

## 4. Proof of Execution
*(Insert your 4 new screenshots here demonstrating the Allowed, Blocked, Normal, and Failure conditions)*

* **Case 1 (Allowed):**

* **Case 2 (Blocked):**

* **Case 3 (Normal):**

* **Case 4 (Failure):**
