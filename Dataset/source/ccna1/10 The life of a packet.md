10 The life of a packet
This chapter covers

A review of the processes involved in delivering a packet from source to destination
How switches forward frames
Address Resolution Protocol
How routers forward packets
The concepts we have covered so far—the TCP/IP model, frame switching, ARP, IPv4 addresses, routing, etc.—are fundamental concepts we will build upon in the rest of this book’s two volumes. In this chapter, we will review many of those concepts and see the role each plays in delivering a packet from the sending host to the packet’s intended destination.

This chapter is unique among the others in this book in that it does not cover new information; everything in this chapter has been covered in previous chapters. Instead of introducing new concepts, the goal of this chapter is to take the most important concepts from previous chapters and tie them all together into one coherent whole.

Figure 10.1 shows the network we will use for this chapter; we used the same when looking at routing in chapter 9. Figure 10.1 also summarizes the different processes involved in delivering a packet from PC1 to PC3: ARP, switching, routing, etc. We will review these processes throughout this chapter.
Figure 10.1 A summary of actions taken by each device when PC1 sends a packet to PC3. PC1 prepares a packet addressed to PC3, uses ARP to learn the default gateway’s MAC address (R1 G0/1), and sends the packet in a frame to that MAC address. The switches learn the MAC addresses of connected devices and forward/flood frames as appropriate. The routers select the best route to forward the packet, use ARP to learn the next hop’s MAC address, and forward the packet in a frame addressed to that MAC address.
Note The arrows in figure 10.1 are a reminder that, at Layer 3, the packet is addressed to PC3 (IP address 192.168.3.11) throughout the whole journey. However, at Layer 2, the packet is encapsulated in a new frame at each hop, and each frame is addressed to the next hop (until R3 finally addresses its frame to PC3).

10.1 The life of a packet from PC1 to PC3
Figure 10.1 provides an outline of the different processes involved in delivering a packet from PC1 to PC3. Now let’s examine the process step by step to see how the different components we’ve covered in the book so far come together to enable communications over the network.

10.1.1 PC1 to R1
In our scenario, PC1 wants to send a packet to PC3. The type of packet is not significant for this example, so let’s assume it’s an ICMP echo request message sent by issuing the ping 192.168.3.11 command on PC1.
PC1’s IP address is 192.168.1.11, and it has a /24 prefix length (netmask 255.255.255.0), so it knows that its local network includes IP addresses 192.168.1.0 (the network address) through 192.168.1.255 (the broadcast address). Therefore, it knows that PC3 (192.168.3.11) is not in its local network. This means that PC1 must send the packet to its default gateway in a frame addressed to the default gateway’s MAC address (rather than the MAC address of PC3 itself).
PC1 knows that its default gateway’s IP address is 192.168.1.1 (most likely learned via DHCP, which we will cover in chapter 4 of volume 2), but the information it actually needs is the MAC address of the default gateway; it needs to send the packet (destined for PC3) in a frame addressed to R1 G0/1’s MAC address. To learn R1 G0/1’s MAC address, it will use ARP. Figure 10.2 outlines the ARP exchange between PC1 and R1.
Note ARP isn’t used to learn the MAC address of the packet’s destination (PC3), but the MAC address of the default gateway (R1 G0/1). Because PC1 and PC3 are in separate LANs, they do not need to know each other’s MAC address.
Figure 10.2 PC1 uses ARP to learn R1 G0/1’s MAC address. (1) PC1 sends an ARP request to 192.168.1.1. SW1 learns PC1’s MAC address and floods the frame due to the destination MAC address of ffff.ffff.ffff. (2) After receiving the ARP request, R1 adds an ARP table entry associating IP address 192.168.1.11 with PC1’s MAC address. R1 then sends an ARP reply to PC1. SW1 learns R1 G0/1’s MAC address and forwards the frame to PC1. (3) After receiving the ARP reply, PC1 adds an ARP table entry associating IP address 192.168.1.1 with R1 G0/1’s MAC address.
Note To reduce clutter, figure 10.2 only briefly mentions PC2. Upon receiving the ARP request from PC1 (which was flooded by SW1), PC2 simply drops the message—the ARP request is not addressed to PC2’s own IP address, so PC2 ignores it.
After the ARP exchange, PC1 now knows the MAC address of its default gateway (in the process, R1 also learns PC1’s MAC address and creates an ARP entry). PC1 can now encapsulate the packet to PC3 in a frame addressed to R1’s G0/1 interface. In the following section, we’ll see what actions R1 takes upon receiving the frame (and the packet inside the frame) from PC1.
SW1’s role is to learn the MAC addresses of connected devices and then forward or flood frames as necessary. It will flood broadcast frames (i.e., PC1’s ARP request) and unknown unicast frames. It will forward known unicast frames (i.e., R1’s ARP reply).
Exam Tip Know the difference between a switch’s MAC address table and an end host or router’s ARP table. A MAC address table maps MAC addresses to switch ports and is used to allow a switch to forward frames out of the correct port. An ARP table maps IP addresses to MAC addresses and is used to allow a router or end host to encapsulate packets in frames with the proper destination MAC address.
10.1.2 R1 to R2
When R1 receives the frame from PC1, it de-encapsulates it and examines the packet inside. As covered in chapter 9, it then performs a routing table lookup—it looks for the most specific matching route (the matching route with the longest prefix length). The following example shows R1’s routing table:

R1# show ip route
. . .
      192.168.1.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.1.0/24 is directly connected, GigabitEthernet0/1
L        192.168.1.1/32 is directly connected, GigabitEthernet0/1
S     192.168.3.0/24 [1/0] via 192.168.12.2, GigabitEthernet0/0      ❶
      192.168.12.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.12.0/24 is directly connected, GigabitEthernet0/0
L        192.168.12.1/32 is directly connected, GigabitEthernet0/0
❶ The most specific matching route

The most specific matching route is the static route to 192.168.3.0/24 via next hop 192.168.12.2 (actually, it’s the only matching route). However, just like how PC1 knew the IP address of its default gateway but not the MAC address (and therefore had to use ARP to learn the MAC address), R1 knows the IP address of the next hop but not its MAC address (and therefore has to use ARP).
R1 sends an ARP request to learn the MAC address of 192.168.12.2 (R2 G0/0), and R2 sends an ARP reply. In the process, they both learn each other’s MAC addresses and create entries in their ARP tables. R1 is now ready to encapsulate the packet in a frame addressed to R2 G0/0’s MAC address and forward it out of the G0/0 interface. Figure 10.3 outlines the process up to this point.
Note The ARP request sent from R1 to R2 is addressed to the broadcast MAC address (ffff.ffff.ffff). However, R2 is the only device that receives the message—there is no switch to flood the frame in the LAN between R1 and R2.
Figure 10.3 R1 receives PC1’s message, performs a routing table lookup, and uses ARP to learn the MAC address of the next hop. (1) R1 receives the frame/packet and performs a routing table lookup. The most specific matching route is to 192.168.3.0/24, next hop 192.168.12.2. (2) R1 uses ARP to learn the MAC address of 192.168.12.2 (R2 G0/0). R1 and R2 both add entries to their ARP tables. R1 is now ready to forward the packet to the next hop.
Note I have simplified the ARP exchange in figure 10.3, but remember that it consists of an ARP request from R1 to R2 and then an ARP reply from R2 to R1.

10.1.3 R2 to R3
When R2 receives the frame from R1, it de-encapsulates it and examines the packet inside. The process it then goes through is identical to the process R1 went through previously. First, it performs a routing table lookup to find the most specific matching route. The following example shows R2’s routing table:

R2# show ip route
. . .
S     192.168.1.0/24 [1/0] via 192.168.12.1, GigabitEthernet0/0
S     192.168.3.0/24 [1/0] via 192.168.23.2, GigabitEthernet0/1      ❶
      192.168.12.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.12.0/24 is directly connected, GigabitEthernet0/0
L        192.168.12.2/32 is directly connected, GigabitEthernet0/0
      192.168.23.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.23.0/24 is directly connected, GigabitEthernet0/1
L        192.168.23.1/32 is directly connected, GigabitEthernet0/1
❶ The most specific matching route

The only route that matches destination 192.168.3.11 is the static route to 192.168.3.0/24, via next hop 192.168.23.2 (R3’s G0/0 interface). To learn the MAC address of the next hop, R2 sends an ARP request, and R3 sends an ARP reply. In the process, R2 and R3 create entries in their ARP tables, and R2 is now ready to forward the packet in a frame addressed to R3 G0/0’s MAC address. Figure 10.4 outlines this process.
Figure 10.4 R2 receives the frame from R1, performs a routing table lookup and uses ARP to learn the MAC address of the next hop. (1) R2 receives the frame/packet and performs a routing table lookup. The most specific matching route is to 192.168.3.0/24, next hop 192.168.23.2. (2) R2 uses ARP to learn the MAC address of 192.168.23.2 (R3 G0/0). R2 and R3 both add entries to their ARP tables. R2 is now ready to forward the packet to the next hop.

10.1.4 R3 to PC3
After R2 forwards the message and it reaches R3, the packet is now at the final router before the destination. R3 goes through the same process as R1 and R2 did previously; it performs a routing table lookup to find the most specific matching route. The following example shows R3’s routing table:

R3# show ip route
. . .
S     192.168.1.0/24 [1/0] via 192.168.23.1, GigabitEthernet0/0
      192.168.3.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.3.0/24 is directly connected, GigabitEthernet0/1     ❶
L        192.168.3.1/32 is directly connected, GigabitEthernet0/1
      192.168.23.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.23.0/24 is directly connected, GigabitEthernet0/0
L        192.168.23.2/32 is directly connected, GigabitEthernet0/0
❶ The most specific matching route

The only matching route is the route to 192.168.3.0/24, which is a connected route. Because the packet’s destination is in a directly connected network, R3 will encapsulate the packet in a frame addressed to the destination host’s MAC address—the MAC address of PC3. To do that, it must use ARP.
SW2 floods the ARP request message to both PC3 and PC4; PC4 ignores it, but PC3 sends an ARP reply back to R3. In that process, SW2 learns the MAC addresses of R3 G0/1 and PC3. R3 and PC3 also learn each other’s MAC addresses and add entries to their ARP tables. Figure 10.5 demonstrates this process.

Figure 10.5 R3 receives the frame from R2, performs a routing table lookup and uses ARP to learn the MAC address of the next hop. (1) R3 receives the frame/packet and performs a routing table lookup. The most specific matching route is the connected route to 192.168.3.0/24. (2) R3 uses ARP to learn the MAC address of 192.168.3.11 (PC3). SW2 learns the MAC addresses of R3 G0/1 and PC3. R3 and PC3 both add entries to their ARP tables. R3 is now ready to forward the packet to the destination.
R3 is now able to forward the packet in a frame addressed to PC3’s MAC address. The packet has reached its final destination! Upon receipt of the packet, PC3 will process it as appropriate. Earlier I stated that PC1’s message was an ICMP echo request message. In that case, PC3 will send an ICMP echo reply message back to PC1.

10.2 The life of a packet from PC3 to PC1
The processes involved in delivering PC3’s response to PC1 are similar, but there are two major differences: the switches have already learned the necessary MAC addresses, and the PCs and routers already have the necessary ARP table entries. This simplifies the process a bit—because the devices already have the necessary information in their tables, there is no need for the switches to learn MAC addresses or the PCs and routers to use ARP. Figure 10.6 outlines how PC3’s packet is delivered to PC1, addressed to and from different MAC addresses at each hop.

Figure 10.6 PC3 sends a reply to PC1. PC3 sends the packet in a frame addressed to the default gateway (R3 G0/1), and SW2 forwards the frame to R3. R3 forwards the packet in a frame to R2 G0/1, and R2 forwards the packet in a frame to R1 G0/0. Finally, R1 forwards the packet in a frame to the destination (PC1), and SW1 forwards the frame to PC1.
Aside from the lack of MAC address learning and ARP, the process is the same as before. PC3 sends its packet in a frame addressed to the default gateway, which SW2 forwards out of the proper port. The routers in the path perform routing table lookups to forward the packet toward the next hop until R1 forwards it in a frame addressed to PC1 itself, and the frame is forwarded to PC1 by SW1.

Summary
To send packets to remote destinations, an end host (such as a PC) will send the packet to its default gateway (router). To do so, it will encapsulate the packet in a frame addressed to the default gateway’s MAC address. It uses ARP to learn the default gateway’s MAC address.
ARP involves two messages: ARP request (broadcast) and ARP reply (unicast).
When a device receives an ARP request, it doesn’t just send an ARP reply; it also makes an entry in its own ARP table, mapping the IP address of the host that sent the request to that host’s MAC address.
Switches learn MAC addresses and forward or flood frames as appropriate. They do not modify the frames they forward; their operations are transparent to the devices connected to them.
A switch will flood broadcast and unknown unicast frames. It will forward known unicast frames.
When a router receives a frame addressed to its own MAC address, it will de-encapsulate it and examine the packet inside. It then performs a routing table lookup to determine how to forward the packet (or drop the packet or receive it for itself).
A router will forward a packet according to the most specific matching route: the matching route with the longest prefix length.
To forward a packet to the next hop in the path, a router will forward the packet in a frame addressed to the next hop’s MAC address. It uses ARP to learn the next hop’s MAC address.
To forward a packet to the packet’s destination host, a router will forward the packet in a frame addressed to the destination host’s MAC address, using ARP to learn the MAC address.