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

* **Case 1 (Allowed):**

<img width="940" height="295" alt="image" src="https://github.com/user-attachments/assets/e248d55d-081d-4354-af95-812a0f01cb63" />

* **Case 2 (Blocked):**

<img width="940" height="228" alt="image" src="https://github.com/user-attachments/assets/9f508033-2289-4d9f-801e-a5ce4d122f41" />

* **Case 3 (Normal):**

<img width="940" height="193" alt="image" src="https://github.com/user-attachments/assets/2307f7f2-0a0d-425b-ab9f-b47882a116e4" />

* **Case 4 (Failure):**

<img width="940" height="260" alt="image" src="https://github.com/user-attachments/assets/30c2d09f-3dca-419f-a4dc-25f00ead7d04" />
