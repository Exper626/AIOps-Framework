15 Rapid Spanning Tree Protocol
This chapter covers

The standard and Cisco-proprietary versions of Spanning Tree Protocol
A comparison of the port costs, states, and roles of STP and Rapid STP
How RSTP-enabled switches react to topology changes
How RSTP link types affect convergence
Optional STP features Root Guard, Loop Guard, and BPDU Filter
In this chapter, we will continue to look at Spanning Tree Protocol (STP). There’s a reason STP is enabled by default on almost any vendor’s switches: Layer 2 loops are disastrous for a LAN. However, there are some downsides to the original STP as defined by IEEE 802.1D, the main one being speed; it can take up to 50 seconds to converge and reach a new, stable state after a change in the LAN. When STP was first released, 50 seconds was an acceptable time frame, but expectations have changed by now.
The answer to the increased demand for speed in modern LANs is Rapid Spanning Tree Protocol (RSTP), the topic of this chapter. The good news is that since we covered the original STP in chapter 14, you’re already 80% of the way to understanding RSTP (from the perspective of the CCNA—there is more nuance when you dig deeper). In this chapter, we will continue from the previous chapter and finish covering exam topic 2.5: Identify basic operations of Rapid PVST+ Spanning Tree Protocol.

15.1 Spanning Tree Protocol versions
Before we look at the specifics of RSTP, let’s briefly look at some of the different versions of STP, including industry-standard and Cisco-proprietary versions. In chapter 14, I mentioned two versions of STP: the protocol standardized in IEEE 802.1D and Cisco’s PVST+. Cisco switches run PVST+, but the information in chapter 14 applies to both versions; the only difference is that PVST+ creates a separate spanning tree for each VLAN. This allows each VLAN to have a separate root bridge and a distinct topology of active and disabled links.
Likewise, RSTP was first standardized in IEEE 802.1w, and Cisco then developed Rapid Per-VLAN Spanning Tree Plus (Rapid PVST+), which runs on Cisco switches. The difference between 802.1w and Rapid PVST+ is the same as the difference between 802.1D and PVST+: whereas 802.1w creates a single spanning tree in the LAN, Rapid PVST+ creates a separate spanning tree for each VLAN, allowing traffic in different VLANs to use different links.
Modern Cisco switches can run both PVST+ and Rapid PVST+, but which version runs by default depends on the switch model and IOS version. To check which version is running on a switch, use the show spanning-tree command as in the following example; the line Spanning tree enabled protocol ieee indicates that PVST+ is running:

SW1# show spanning-tree 
VLAN0001
  Spanning tree enabled protocol ieee     ❶
. . .
❶ PVST+ is running.

To configure which version of STP the switch should use, use the spanning-tree mode {pvst | rapid-pvst} command in global config mode. In the following example, I configure the switch to use Rapid PVST+ and then confirm with show spanning-tree; the line Spanning tree enabled protocol rstp indicates that Rapid PVST+ is running:

SW1(config)# spanning-tree mode rapid-pvst     ❶
SW1(config)# do show spanning-tree
VLAN0001
  Spanning tree enabled protocol rstp          ❷
. . .
❶ Enables Rapid PVST+

❷ Rapid PVST+ is running.

Note The keyword used to enable each mode is different from how it appears in the output of show spanning-tree. PVST+ is configured with spanning-tree mode pvst but appears as Spanning tree enabled protocol ieee. Rapid PVST+ is configured with spanning-tree mode rapid-pvst but appears as Spanning tree enabled protocol rstp. Keep in mind that Cisco switches do not run the IEEE-standard versions of STP and RSTP—they run PVST+ and Rapid PVST+.
Although the ability to create a unique spanning tree for each VLAN is a benefit of PVST+ and Rapid PVST+ over their standard counterparts, there is a downside: in a LAN with many VLANs, a switch runs a separate STP instance and sends unique Bridge Protocol Data Units (BPDUs) for each VLAN. If there are 100 VLANs, each switch runs 100 STP instances and sends 100 BPDUs out of each designated port every 2 seconds. This taxes switch CPU and memory resources and can negatively affect network performance and stability.
Additionally, having many STP instances increases the complexity of managing the switches; configuring, monitoring, and troubleshooting 100 instances of STP can be unnecessarily complex. The reality is that in a LAN with 100 VLANs, there likely isn’t a need for 100 unique spanning trees; you’ll probably assign one switch as the root bridge for 50 of the VLANs and another switch as the root bridge for the remaining 50 VLANs, resulting in only two unique spanning trees.
In such a LAN, Multiple Spanning Tree Protocol (MSTP) might be preferred. With MSTP, you can group multiple VLANs into a single instance. For example, in a LAN with 100 VLANs, you might create two MSTP instances and group 50 VLANs in one instance and 50 VLANs in the other. This allows you to avoid congestion by balancing traffic over separate links, without using up resources by running 100 STP instances. And MSTP uses RSTP’s mechanics for quick convergence—no 50-second waits like in 802.1D. Figure 15.1 shows how MSTP groups multiple VLANs into each instance.

Figure 15.1 MSTP groups multiple VLANs into each instance. VLANs 1 to 50 are grouped together in MSTP instance 1, and VLANs 51 to 100 are grouped together in MSTP instance 2. This allows the switches to balance traffic over the links in the LAN without requiring a separate STP instance for each VLAN.
The details of MSTP are beyond the scope of the CCNA exam, so a basic understanding of its benefit (grouping multiple VLANs per instance) is sufficient. Table 15.1 summarizes the different versions of STP you should be aware of for the CCNA.

Table 15.1 STP versions

| Version     | Standard or Cisco-proprietary | Description                                                                                       |
| ----------- | ----------------------------- | ------------------------------------------------------------------------------------------------- |
| STP         | Standard (802.1D)             | The original standard. Creates only a single spanning tree.                                       |
| PVST+       | Cisco-proprietary             | Cisco’s upgrade to 802.1D. Creates a separate spanning tree for each VLAN.                        |
| RSTP        | Standard (802.1w)             | Much faster convergence than 802.1D. Creates only a single spanning tree.                         |
| Rapid PVST+ | Cisco-proprietary             | Cisco’s upgrade to 802.1w. Creates a separate spanning tree for each VLAN.                        |
| MSTP        | Standard (802.1s)             | Uses RSTP mechanics for fast convergence. Groups multiple VLANs into each spanning tree instance. |


15.2 STP and RSTP comparison
As the word “rapid” in the name suggests, the fundamental difference between STP and RSTP is speed. Whereas 802.1D’s STP is a timer-based protocol in which a port can take up to 50 seconds to begin forwarding, 802.1w’s RSTP uses a synchronization mechanism in which RSTP-enabled switches communicate with each other to bring ports immediately to the forwarding state, without waiting for timers to count down.

Exam Tip The details of RSTP’s sync mechanism are beyond the scope of the CCNA exam. Instead, focus on learning the RSTP port costs, states, roles, and link types covered in this chapter.
Although we will cover the various differences between STP and RSTP, keep in mind that the algorithm for calculating the topology is identical:

1. Root bridge election (one per LAN)
	- Lowest bridge ID (BID)

2. Root port selection (one per switch, excluding root bridge)
	- Lowest root cost
	- Lowest neighbor BID
	- Lowest neighbor port ID

3. Designated port selection (one per segment)
	- Port on switch with lowest root cost
	- Port on switch with lowest BID

In STP, the remaining ports will all be nondesignated. In RSTP, they will be one of two roles: alternate or backup (we will cover them in section 15.2.3). Figure 15.2 shows the same LAN we looked at in chapter 14, this time using RSTP. The only difference is that the nondesignated ports are now alternate ports.
Figure 15.2 A LAN after RSTP has created a loop-free topology. The only difference in the topology between STP and RSTP is that the nondesignated ports are now called alternate ports.
Note A technical detail that could come up on the exam is how STP and RSTP handle BPDUs. In STP, the root bridge sends BPDUs every 2 seconds, and the other switches forward them out of their designated ports. In RSTP, all switches send BPDUs out of their designated ports every two seconds, whether they received a BPDU from the root bridge or not.

15.2.1 Port costs
STP defines port costs for speeds of up to 10 Gbps (with a cost of 2). RSTP, on the other hand, introduces a new set of port costs to accommodate ports of greater speeds—up to 10 Tbps. The original STP port costs are now called the short costs, and the new RSTP port costs are called the long costs. Table 15.2 lists the short and long costs of ports of various speeds.
Table 15.2 Short and long port costs

| Speed    | Short cost | Long cost |
| -------- | ---------: | --------: |
| 10 Mbps  |        100 | 2,000,000 |
| 100 Mbps |         19 |   200,000 |
| 1 Gbps   |          4 |    20,000 |
| 10 Gbps  |          2 |     2,000 |
| 100 Gbps |          – |       200 |
| 1 Tbps   |          – |        20 |
| 10 Tbps  |          – |         2 |

Exam Tip To remember the long costs, pick one as a point of reference (such as 10 Gbps = 2,000). Then you can easily calculate the long costs of ports of other speeds: increasing the speed by a factor of 10 reduces the cost by a factor of 10 and vice versa.
Although the long method of calculating port costs was introduced in RSTP, keep in mind that switches don’t necessarily use it by default, even when running RSTP—it depends on the switch model and software version. To view which method (short or long) a switch is using, use the show spanning-tree pathcost method command, and to modify which method the switch uses to calculate port costs, use the spanning-tree pathcost method {short | long} command in global config mode. As you can see in the following example, my switch uses the short costs by default:

SW1# show spanning-tree pathcost method                 ❶
Spanning tree default pathcost method used is short     ❶
❶ The default method is short.

15.2.2 Port states
Whereas STP has four main states (blocking, listening, learning, forwarding), RSTP combines the first two states into a single state called discarding. Table 15.3 compares the STP and RSTP port states.

Table 15.3 STP and RSTP port states

| STP port state | RSTP port state |
| -------------- | --------------- |
| Blocking       | Discarding      |
| Listening      | Discarding      |
| Learning       | Learning        |
| Forwarding     | Forwarding      |


When an RSTP port is first enabled, it will enter the discarding state. If it is decided that the port will be an alternate or backup port (more on that in section 15.2.3), it will remain in the discarding state, blocking traffic to prevent Layer 2 loops. However, if the port becomes a root or designated port, it will proceed to the forwarding state in one of two ways, as shown in figure 15.3.
Figure 15.3 An RSTP port can transition to the forwarding state in one of two ways. If the RSTP sync mechanism succeeds, the port immediately transitions to the forwarding state. If the RSTP sync mechanism fails, the port transitions from discarding to learning to forwarding, like a regular STP port.
If the RSTP sync mechanism succeeds, the port immediately transitions to the forwarding state—no need to wait for any timers. This is expected if the port is connected to another RSTP-enabled switch. However, the sync mechanism will not work in all situations—for example, if the port is connected to a device that doesn’t use RSTP, such as a router, a PC, or even a switch that is using STP instead of RSTP. In that case, the port will remain in the discarding state for 15 seconds (the duration of the forward delay timer), then transition to the learning state for another 15 seconds, and then finally transition to the forwarding state—this is like a regular STP port transitioning through the listening and learning states before forwarding.
Note RSTP and STP are compatible. However, a port on an RSTP-enabled switch that is connected to a port on an STP-enabled switch will not be able to take advantage of RSTP’s sync mechanism. The port on the RSTP-enabled switch will operate like a regular STP port.
These days, you can safely expect that all switches will support RSTP, so you should only expect the timer-based transition to the forwarding state on ports connected to a host like a PC. However, as we covered in chapter 14, PortFast can be configured on such ports to allow them to start forwarding frames immediately—we will cover PortFast again in section 15.3.

15.2.3 Port roles
The three port roles of STP are root, designated, and nondesignated; we covered these in chapter 14. In RSTP, the root and designated roles remain unchanged. A root port is a forwarding port that points toward the root bridge; it provides the switch’s only active path to reach the root bridge. A designated port is a forwarding port that points away from the root bridge, and all segments must have exactly one designated port. However, the nondesignated port role has been replaced by two distinct roles: alternate and backup. Like nondesignated ports, alternate and backup ports block traffic to prevent Layer 2 loops.

Alternate role
An RSTP alternate port can be thought of as an alternative for the switch’s root port; it provides an alternative path toward the root bridge and is ready to take over (by transitioning to the forwarding state) if the root port fails. The rule for becoming an alternate port is as follows: any port that is not a root or designated port is an alternate port if the switch is not the designated bridge for that segment.
Note Designated bridge is a new term; it is the switch that has the designated port for a particular segment. This term applies to both STP and RSTP.
In almost all cases, a port that is neither a root port nor a designated port will be an alternate port. Figure 15.4 explains why each of the alternate ports in the LAN is in that state.
Figure 15.4 A port will become an alternate port if it is neither root nor designated and if the switch is not the designated bridge for the segment. In almost all cases, a port that is neither root nor designated will be an alternate port.
Note A simple way to define an alternate port is as a port in the discarding state that is connected to a designated port on another switch.

Backup role
An RSTP backup port provides a backup path to the same segment as a designated port on the same switch. This will only occur if two ports on the same switch are connected to the same segment (collision domain)—for example, with a hub. You will most likely never use a hub in a modern network, so I wouldn’t expect to encounter a backup port “in the wild.” However, backup ports are worth covering, even if just for the possibility of a question about them on the exam.
The rule for becoming a backup port is as follows: any port that is not a root or designated port is a backup port if the switch is the designated bridge for that segment. In figure 15.5, I have added a hub between SW1 and SW3 (and removed SW2 and SW4 from the diagram), connecting their four ports to the same segment. SW1 G0/1 becomes an alternate port (because SW1 isn’t the designated bridge for the segment), but SW3 G0/1 becomes a backup port (because SW3 is the designated bridge for the segment).
Note We can simplify this rule too: a backup port is a port in the discarding state that is connected to a designated port on the same switch (via a hub). In figure 15.5, SW3 G0/1 is connected to SW3 G0/0 (a designated port) via a hub.
Figure 15.5 SW1 and SW3 both have multiple ports connected to the same segment. SW1 G0/1 becomes an alternate port because SW1 is not the designated bridge for the segment. SW3 G0/1 becomes a backup (B) port because SW3 is the designated bridge for the segment.
In the following example, I use the show spanning-tree command on SW1 and SW3 to confirm their port roles; Altn stands for alternate, and Back stands for backup. Note that the Sts column states BLK in each case; even though the blocking state was renamed to discarding in RSTP, this command retains the “blocking” terminology:

SW1# show spanning-tree
. . .
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Root FWD 4         128.1    Shr           ❶
Gi0/1               Altn BLK 4         128.2    Shr           ❷
 
SW3# show spanning-tree
. . .
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    Shr           ❸
Gi0/1               Back BLK 4         128.2    Shr           ❹
❶ SW1 G0/0 is a root port.

❷ SW1 G0/1 is an alternate port.

❸ SW3 G0/0 is a designated port.

❹ SW3 G0/1 is a backup port.

Why does SW1 G0/0 become a root port instead of SW1 G0/1, and why does SW3 G0/0 become a designated port instead of SW3 G0/1? When multiple ports on the same switch are connected to the same segment, there is an additional tiebreaker for the root/designated port selection steps of the STP algorithm: the port with the lowest port ID on the local switch becomes root/designated. SW1 G0/0 has a lower port ID than SW1 G0/1, so G0/0 becomes a root port, and G0/1 becomes an alternate port. Likewise, SW3 G0/0 has a lower port ID than SW3 G0/1, so G0/0 becomes a designated port, and G0/1 becomes a backup port. With these tiebreakers added, the STP algorithm is as follows:

Root bridge election (one per LAN)
	- Lowest BID

Root port selection (one per switch, excluding root bridge)
	- Lowest root cost
	- Lowest neighbor BID
	- Lowest neighbor port ID
	- Lowest local port ID

Designated port selection (one per segment)
	- Port on switch with lowest root cost
	- Port on switch with lowest BID
	- Lowest local port ID

Note These tiebreakers apply to STP too. If SW1 and SW3 were running STP rather than RSTP, their alternate/backup ports would both be nondesignated ports; there is no such distinction of roles in STP.
In chapter 14, I mentioned that every port on the root bridge should be designated. This is almost always true, but as we just saw, if multiple ports on the root bridge are connected to the same segment, only one can be designated; the “one designated port per segment” rule wins out. So rather than “every port on the root bridge should be designated,” a more accurate rule is “the root bridge is the designated bridge for every segment.” However, because you will rarely (if ever) encounter a LAN using hubs, you’ll most often hear that every port on the root bridge should be designated.

15.2.4 RSTP topology changes
In chapter 14, we covered an example in which a switch’s nondesignated port took 50 seconds to move to a forwarding state after a change in the topology (due to a hardware failure). Although the details of the topology change processes of STP and RSTP are beyond the scope of the CCNA exam, let’s take a brief look at one way that RSTP speeds up the process. Figure 15.6 shows the same example from chapter 14, this time using RSTP.
Whereas an STP-enabled switch waits 20 seconds (the max age timer) after ceasing to receive BPDUs on a port to react and initiate the topology change process, RSTP only waits until a port misses three BPDUs (6 seconds by default) to react. Then, as in figure 15.6, the next-best port can sync with its neighbor and immediately move to the forwarding state; a 50-second process has been shortened to just over 6 seconds.
Figure 15.6 RSTP speeds up convergence after a topology change like this from 50 seconds to just over 6 seconds. (1) Due to a hardware failure, SW1 stops receiving BPDUs on G0/1 (without the port going down). (2) G0/1 remains the root port for 6 seconds (3× the hello timer of 2 seconds). (3) G0/0 becomes the root port and, after performing the RSTP sync process, immediately moves to the forwarding state.
Note If the hardware failure caused SW1’s G0/1 port to go down (enter a disabled state), the process would be even faster; there would be no need to wait 6 seconds. In that case, SW1 G0/0 will immediately initiate the sync process, bringing the total downtime to less than 1 second.

15.3 RSTP link types
Another aspect of RSTP is the concept of link types. These types influence how ports transition through the RSTP port states and react to network changes. RSTP defines three link types:
Point-to-point—Full-duplex ports that can use the RSTP sync mechanism to immediately transition to the forwarding state.
Shared—Half-duplex ports that cannot use the RSTP sync mechanism. They must transition through the states like standard STP ports.
Edge—Ports connected to end hosts that can use PortFast to immediately transition to the forwarding state.
Figure 15.7 illustrates these three link types on three switches.
Figure 15.7 RSTP differentiates between three link types: point-to-point, shared, and edge. A full-duplex link is considered a point-to-point link. A half-duplex link is considered a shared link. A link between a switch and an end host that uses PortFast is considered an edge link.
An RSTP point-to-point link is a link that operates in full duplex, meaning that the connected ports (i.e. SW1 G0/3 and SW2 G0/0) operate in full duplex. These are the only links that can take advantage of RSTP’s sync mechanism to rapidly transition ports to the forwarding state. Although full-duplex ports will automatically use the point-to-point link type, you can also manually configure it with the spanning-tree link-type point-to-point command in interface config mode.
An RSTP shared link is a link that operates in half duplex. In figure 15.7, SW1 and SW3 are connected via a hub, and devices connected to a hub must operate in half-duplex; therefore, the link is an RSTP shared link. Ports connected to a shared link cannot use RSTP’s sync mechanism; in effect, they operate like regular STP links, taking 30 seconds to move to the forwarding state. Half-duplex ports will automatically use the shared link type, but if necessary, the spanning-tree link-type shared command can be used to manually configure it.
Note Like the backup port role, you probably won’t encounter the shared link type in a real network.
Finally, there is the edge link type. These are ports that connect to end hosts: SW1 F1/0 and SW2 F1/0. These ports don’t need to use the RSTP sync mechanism; there is no risk of a Layer 2 loop, so they can immediately transition to the forwarding state. Does a port connected to an end host immediately transitioning to the forwarding state sound familiar?
On Cisco switches, the edge link type must be manually configured by enabling PortFast on the appropriate ports (with the spanning-tree portfast command, as we covered in chapter 14)—not the spanning-tree link-type command like point-to-point and shared links. Note that this is the only link type that can’t be automatically determined by the switch based on the port’s duplex mode; you must manually configure it.
Note A port that is connected to an end host but hasn’t been configured with the spanning-tree portfast command won’t immediately transition to the forwarding state—it will have to wait 30 seconds like a regular STP port.
One more characteristic of edge ports is that RSTP doesn’t consider any activity on them (such as moving to the forwarding or discarding states) a topology change and doesn’t notify its neighbors of the activity. Because edge ports connect to end hosts (not switches), and therefore pose no risk of causing Layer 2 loops, there’s no need to notify other switches of activity on those ports; they don’t affect the rest of the RSTP topology.

Topology changes

STP and RSTP each have defined processes for reacting to changes in the topology, allowing switches to adapt to the new topology with minimal disruptions; the details of these processes are beyond the scope of the CCNA exam. STP triggers its topology change process in the following situations:
When any port transitions to the forwarding state
When a port in the learning state or forwarding state transitions to the blocking state or disabled state
Switches using RSTP, on the other hand, only trigger the topology change process when a port with a non-edge link type (point-to-point or shared) transitions to the forwarding state; they don’t trigger the process when an edge port transitions to the forwarding state or when any port transitions to the discarding state.
Exam Tip The details of STP/RSTP topology changes are beyond the scope of the CCNA exam, but remember this characteristic of RSTP edge ports: they don’t trigger the topology change process when moving to the forwarding state.

You can view the type of link of each port with the show spanning-tree command. The final column on the right lists the link types: point-to-point (P2p), shared (Shr), and edge (Edge). In the following example, I use the command on SW1:

SW1# show spanning-tree
. . .
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Root FWD 4         128.1    Shr          ❶
Gi0/1               Altn BLK 4         128.2    Shr          ❶
Gi0/3               Desg FWD 4         128.4    P2p          ❷
Fa1/0               Desg FWD 19        128.9    P2p Edge     ❸
❶ Shr indicates a shared link.

❷ P2p indicates a point-to-point link.

❸ P2p Edge indicates a point-to-point edge link (a full-duplex link using PortFast).

Note F1/0’s type is listed as P2p Edge. In Cisco IOS, an edge port will appear as P2p Edge if it operates in full duplex or Shr Edge if it operates in half duplex.
In a modern network that uses only switches (not hubs), links between two switches should have the point-to-point type, and links between a switch and an end host should have the edge link type (more specifically, the point-to-point edge).

15.4 Root Guard, Loop Guard, and BPDU Filter
In chapter 14, we covered two optional STP features: PortFast and BPDU Guard. While these are the two most common features in the so-called STP toolkit, the CCNA exam expects you to know a few more tools that expand STP’s (or RSTP’s) functionality. In this section, we will discuss Root Guard, Loop Guard, and BPDU Filter.
Note All of these optional STP features—PortFast, BPDU Guard, Root Guard, Loop Guard, and BPDU Filter—work in both STP and RSTP.

15.4.1 Root Guard
Root Guard is a feature that enhances the stability of the STP topology by preventing external switches from becoming the root bridge. A common scenario where Root Guard is useful is when a LAN of switches is controlled by two different entities, such as a service provider and a customer (who connects to the service provider’s network). The service provider can use Root Guard to ensure that one of its switches remains the root bridge, maintaining a consistent STP topology even if a customer connects a switch with a lower bridge ID. Figure 15.8 illustrates this scenario.
Figure 15.8 Root Guard prevents a newly connected customer network from affecting the service provider’s STP topology. (1) The customer’s SW4 and SW5 are connected to the service provider’s SW2 and SW3. (2) SW4’s bridge ID is lower than SW1’s, so the BPDUs sent by SW4 and SW5 are superior to SW1’s BPDUs. (3) SW2 and SW3 use Root Guard to block their ports that receive the superior BPDUs.
When a Root Guard-enabled port receives a superior BPDU, the port will enter the root-inconsistent state; in effect, this disables the port, preventing the switch from accepting the superior BPDU. In this state, the customer is unable to access the service provider’s network. To fix this problem, the customer needs to configure a higher bridge ID on SW4, making the BPDUs it sends inferior to those of SW1. Once the superior BPDUs are no longer received, SW2’s and SW3’s ports automatically recover and return to their normal state.
The following example shows how to enable Root Guard on a port with the spanning-tree guard root command and the error message that appears when Root Guard blocks the port.

SW2(config)# interface g0/2                                              ❶
SW2(config-if)# spanning-tree guard root                                 ❶
*May 18 01:13:20.478: %SPANTREE-2-ROOTGUARD_BLOCK: Root guard blocking   ❷
port GigabitEthernet0/2 on VLAN0001.                                     ❷
SW2(config-if)# do show spanning-tree 
. . .
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- -------------------------
Gi0/0               Root FWD 4         128.1    P2p 
Gi0/1               Altn BLK 4         128.2    P2p 
Gi0/2               Desg BKN*4         128.3    P2p *ROOT_Inc            ❸
❶ Enables Root Guard on the port

❷ The port is blocked after receiving a superior BPDU

❸ The port’s status is BKN (broken) and ROOT_Inc (root-inconsistent)

By using Root Guard, you can ensure that your network’s STP topology remains stable and consistent, preventing external or misconfigured devices from disrupting the network.

15.4.2 Loop Guard
Loop Guard, as the name implies, guards against Layer 2 loops in the LAN. The entire point of STP is to prevent loops, but Loop Guard provides an additional layer of protection against a switch port erroneously transitioning from the discarding state (the blocking state in classic STP) to the forwarding state. This can happen when the discarding port stops receiving BPDUs, causing the switch to believe that the port can move to the forwarding state without causing a loop. Figure 15.9 shows how this can cause a loop.
Figure 15.9 A loop is caused when SW3 stops receiving BPDUs from SW2. (1) A software malfunction on SW2 prevents it from sending BPDUs. (2) After the max age timer counts down, SW3’s port becomes a designated port and transitions to the forwarding state. (3) All three links between the switches are active, resulting in a Layer 2 loop.
To avoid such a problem, you can configure Loop Guard on SW3’s alternate port using the spanning-tree guard loop command. If a Loop Guard-enabled port stops receiving BPDUs, the port will move into the loop-inconsistent state, disabling the port instead of allowing it to transition to the forwarding state; this prevents a loop from forming. However, if SW2 recovers and starts sending BPDUs again, SW3’s port will automatically recover and transition back to its normal state (discarding).
The following example shows how to enable Loop Guard and the error message that appears when Loop Guard blocks the port to prevent a loop.

SW2(config)# interface g0/1                                                ❶
SW2(config-if)# spanning-tree guard loop                                   ❶
*May 18 01:29:31.261: %SPANTREE-2-LOOPGUARD_BLOCK: Loop guard blocking     ❷
port GigabitEthernet0/1 on VLAN0001.                                       ❷
SW2(config-if)# do show spanning-tree 
. . .
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- -------------------------
Gi0/0               Root FWD 4         128.1    P2p 
Gi0/1               Desg BKN*4         128.2    P2p *LOOP_Inc              ❸
❶ Enables Loop Guard on the port

❷ The port is blocked after ceasing to receive BPDUs

❸ The port’s status is BKN (broken) and LOOP_Inc (loop-inconsistent)

With Loop Guard, you can provide an additional safeguard against potential network loops, ensuring the stability and reliability of the LAN. A Layer 2 loop can bring down any LAN, so avoiding them is critical.
Note Root Guard and Loop Guard are mutually exclusive; you can’t enable both of them on the same port simultaneously. This is because they serve different roles: Root Guard takes action based on receiving superior BPDUs, while Loop Guard takes action based on not receiving BPDUs.

15.4.3 BPDU Filter
BPDU Filter is a feature that can be used to prevent BPDUs from being sent or received on specific ports. This can be desirable on ports where STP isn’t necessary, such as those connected to end hosts, since there is no risk of causing a loop. BPDU Filter can be enabled in two ways, with different behaviors depending on how you activate it:
Enabling BPDU Filter on a specific port
Use spanning-tree bpdufilter enable in interface config mode.
This enables BPDU Filter on the specific port.
The port will not send BPDUs and will ignore any BPDUs it receives.
This effectively disables STP on the port.
Enable BPDU Filter globally for all PortFast-enabled ports
Use spanning-tree portfast bpdufilter default in global config mode.
This enables BPDU Filter on all PortFast-enabled ports (RSTP edge ports).
The port will not send BPDUs.

If the port receives a BPDU, PortFast and BPDU Filter will be disabled. The port will then operate as a normal STP or RSTP port.
Of the optional STP features that we have covered in this chapter and the previous one—PortFast, BPDU Guard, Root Guard, Loop Guard, and BPDU Filter—BPDU Filter has the fewest use cases; I recommend avoiding it in general. Especially when enabled in interface config mode, BPDU Filter poses the risk of causing a Layer 2 loop if the port is connected to another switch; STP is effectively disabled on the BPDU Filter-enabled port, so it won’t move to the discarding state even if there is a loop in the LAN. Enabling BPDU Filter carelessly is a great way to bring down a network—use with extreme caution!

Summary
STP, standardized by IEEE 802.1D, was modified by Cisco to make PVST+. Likewise, RSTP, standardized by IEEE 802.1w, was modified by Cisco to make Rapid PVST+. PVST+ and Rapid PVST+ both run separate spanning tree instances for each VLAN.
Whether a switch runs PVST+ or Rapid PVST+ by default depends on the switch model and IOS version.
The running version of STP can be confirmed with show spanning-tree. The output Spanning tree enabled protocol ieee means PVST+, and Spanning tree enabled protocol rstp means Rapid PVST+.
You can configure a switch to use PVST+ or Rapid PVST+ with the spanning-tree mode {pvst | rapid-pvst} command in global config mode.
Multiple Spanning Tree Protocol (MSTP), standardized by 802.1s, allows multiple VLANs to be grouped together in each instance.
The fundamental difference between STP and RSTP is speed. Rather than relying on timers, RSTP-enabled switches can use a sync mechanism to rapidly transition their ports to the forwarding state.
The algorithm used to decide the root bridge, root ports, and designated ports in RSTP is identical to that of STP.
Whereas STP switches only forward BPDUs from the root bridge out of their designated ports, RSTP switches send BPDUs out of their designated ports every 2 seconds, even if they didn’t receive a BPDU from the root bridge.
The original STP port costs are called the short costs. RSTP introduced the long method of calculating port costs to accommodate ports of greater speeds.
With the long method, 10 Mbps = 2,000,000, and a 10-fold speed increase decreases the cost 10-fold (with a top speed of 10 Tbps, which has a cost of 2).
A switch may use the short or long method of calculating costs by default, depending on the switch model and IOS version. Use the show spanning-tree pathcost method command to confirm.
Use the spanning-tree pathcost method {short | long} command in global config mode to configure which cost-calculation method a switch will use.
RSTP uses three port states: discarding, learning, and forwarding. The STP disabled, blocking, and listening states were combined into the RSTP discarding state.
When an RSTP port is first enabled, it will enter the discarding state. Alternate and backup ports will remain in that state. Root and designated ports will transition to the forwarding state.
If the RSTP sync mechanism succeeds, the port will transition immediately to the forwarding state. If the sync mechanism fails, it will spend 15 seconds each in the discarding and learning states before reaching the forwarding state.
RSTP uses four port roles: root, designated, alternate, and backup. The alternate and backup roles are equivalent to the STP nondesignated role.
An alternate port provides an alternate path toward the root bridge. Any port that is not a root or designated port is an alternate port if the switch is not the designated bridge for the segment.
A backup port provides a backup path to the same segment as a designated port on the same switch. This will only occur if two ports on the same switch are connected to the same segment with a hub, which is extremely rare in modern networks.
Any port that is not a root or designated port is a backup port if the switch is the designated bridge for the segment.
If multiple ports on the same switch are connected to the same segment, the lowest local port ID is used as a tiebreaker for the root port and designated port selection processes.
Whereas an STP-enabled switch waits 20 seconds (the max age timer) after ceasing to receive BPDUs on a port to react, RSTP only waits until a port misses three BPDUs (6 seconds).
In some cases, RSTP can shorten the STP reconvergence process after a topology change to less than 1 second.
RSTP differentiates between three link types: point-to-point, shared, and edge.
A point-to-point link is a link that operates in full duplex. Ports with this link type can use the RSTP sync mechanism to rapidly transition to the forwarding state. Full-duplex ports will automatically use this link type.
A shared link is a link that operates in half duplex. Ports with this link type cannot use the RSTP sync mechanism. Half-duplex ports will automatically use this link type.
An edge link is a point-to-point link that connects to an end host and is configured to use PortFast. Ports with the edge link type can immediately transition to the forwarding state without using the RSTP sync mechanism.
To manually configure the point-to-point/shared link types, use the spanning-tree link-type {point-to-point | shared} command in interface config mode. To configure the edge link type, use the spanning-tree portfast command in interface config mode.
Root Guard enhances the stability of the STP topology by preventing external switches from becoming the root bridge. If a Root Guard-enabled port receives a superior BPDU, the port will enter the root-inconsistent state; in effect, this disables the port until it stops receiving superior BPDUs.
Use spanning-tree guard root in interface config mode to enable Root Guard.
Loop Guard guards against Layer 2 loops in a LAN by preventing a switch port from erroneously transitioning to the forwarding state. If a Loop Guard-enabled port stops receiving BPDUs, it will transition to the loop-inconsistent state. This disables the port until it starts receiving BPDUs again.
Use spanning-tree guard loop in interface config mode to enable Loop Guard.
BPDU Filter can be used to prevent BPDUs from being sent or received on specific ports.
Use spanning-tree bpdufilter enable in interface config mode to enable BPDU Filter on a specific port. The port will not send BPDUs and will ignore any BPDUs it receives, effectively disabling STP on the port.
Use spanning-tree portfast bpdufilter default in global config mode to enable BPDU Filter on all PortFast-enabled ports. The port will not send BPDUs, but if it receives a BPDU, PortFast and BPDU Filter will be disabled. The port will then operate as a normal STP or RSTP port.