6 Ethernet LAN switching
This chapter covers

The definition of a LAN
The contents of the Ethernet header and trailer
How switches learn the MAC addresses of devices in the network
How switches forward frames to the appropriate destination
How network hosts use ARP to learn the MAC address of other hosts
The ping utility
In this chapter, we will cover Ethernet LAN switching, which is the process switches use to forward frames to their proper destinations within a LAN. A frame is a Layer 2 PDU, including the Layer 2 header, trailer, and payload; we covered PDUs in chapter 4. When a network host sends a frame out of its port, it is the switch’s role to make sure the frame reaches its proper destination.

This chapter covers material from domain 1.0 of the CCNA exam topics: Network Fundamentals. Specifically, we will cover the following topics:

1.13 Describe switching concepts
1.13a MAC learning and aging
1.13b Frame switching
1.13c Frame flooding
1.13d MAC address table
It is often said that switches are Layer 2 devices or that they operate at Layer 2. The reason for this is that switches use information in the Layer 2 header (the Ethernet header) to make forwarding decisions. This is in contrast to routers, which use information in the Layer 3 header (the IP header) to make forwarding decisions. We will cover how routers forward network traffic between LANs in part 2 of this book, but for now, we will focus on how switches forward traffic within a LAN.

6.1 Local area networks
In chapter 2, I defined a local area network (LAN) as a group of interconnected devices in a limited area, such as an office, and stated that the role of a switch is to connect devices within a LAN. The precise definition of a LAN can vary depending on the context, but for the purpose of this lesson, how the devices are connected is more significant than the actual physical distance between them. Figure 6.1 demonstrates this concept.
Figure 6.1 Two offices with two switches in each office. In Office A each switch is a separate LAN because the switches are connected via a router. In Office B both switches are in the same LAN because they are directly connected to each other.
There are two offices in the diagram, so you might say there are two LANs, which would not be incorrect if defining a LAN only by physical location. However, in Office A, the two switches are not directly connected to each other; each is connected to a different port on R1, and the purpose of a router is to provide connectivity between LANs. So, each switch in Office A can be considered its own LAN. For end hosts connected to SW1 to communicate with end hosts connected to SW2, their messages must pass through R1 because it separates the two LANs.
In Office B, however, SW3 and SW4 are directly connected to each other. End hosts connected to one switch can communicate with end hosts connected to the other switch without the messages having to pass through a router. SW3, SW4, and all of the end hosts connected to them are in a single LAN.
Another term for a LAN is a Layer 2 domain—a portion of a network where frames are switched, and hosts connected to the switch(es) can communicate with each other without the use of a router. Keep this definition in mind throughout this chapter; we will examine how switches forward frames within a Layer 2 domain.

6.2 The Ethernet header and trailer
Switches make forwarding decisions using information in the Ethernet header, so to understand switching, it’s important to understand the contents of that header (and trailer). Figure 6.2 shows the structure of an Ethernet frame. Note that the Preamble and Start Frame Delimiter (SFD) are included in the diagram but are not considered part of an Ethernet frame. We will examine why shortly.
Figure 6.2 The contents of the Ethernet header and trailer. They are split into multiple fields, each serving a different purpose. The fields of the header are the Destination, Source, and Type/Length. The trailer consists of a single field: the Frame Check Sequence (FCS). Although not considered part of the Ethernet frame, the Preamble and SFD are sent with each frame.

6.2.1 Preamble and SFD
The Preamble and SFD are sent with each Ethernet frame to allow the receiving device to synchronize its receiver clock and prepare to receive the incoming frame. This clock has nothing to do with the date and time but rather with how the receiving device interprets the incoming electrical signals—the receiving device needs to determine the precise length of 1 bit.

The device sending an Ethernet frame facilitates this by sending the Preamble and SFD. The Preamble is 7 bytes (56 bits—remember that 1 byte is 8 bits) in length and is simply a series of alternating 1s and 0s like this: 10101010. Then, the SFD is 1 byte in length and signals that the Preamble is done and the frame is going to start. The bit pattern of the SFD is 10101011.
The reason the Preamble and SFD are not considered part of the Ethernet frame, although they are sent with each frame, is that they are purely a function of Layer 1, the Physical Layer. They do not contain information that influences what the receiving device decides to do with the frame. As mentioned in previous chapters, Ethernet includes specifications at both Layers 1 and 2, but the Layer 1 aspects of Ethernet are not considered part of a frame, which is a Layer 2 concept.

6.2.2 Destination and source
The Destination and Source fields are perhaps the most significant of the Ethernet header and trailer; the Destination field is the destination MAC address of the frame, and the Source field is the source MAC address of the frame.

Definition A media access control (MAC) address is a type of address used by Layer 2 protocols such as Ethernet and Wi-Fi. MAC addresses are 6 bytes (48 bits) in length and are typically written as a series of 12 hexadecimal characters. They are assigned by the device’s manufacturer and should be globally unique.
Layer 2 provides hop-to-hop delivery of messages, and MAC addresses enable that. At Layer 3, the message is addressed to the IP address of the final destination host, but at Layer 2, the message is addressed to the MAC address of the next hop. Within a LAN, it is a switch’s job to look at the destination MAC address of the frame and forward it to the appropriate destination. The source MAC address field is also important because it helps the switch learn which port each host is connected to (more about that shortly).
As indicated in figure 6.2, each of these fields is 6 bytes (48 bits) in length because 6 bytes is the length of a MAC address. However, when we represent MAC addresses, we typically don’t write them out in binary; a long string of 1s and 0s isn’t very human-readable or easy to remember. Instead, we write MAC addresses in hexadecimal.
The hexadecimal number system
The number system we typically use in our daily lives is the decimal number system, which uses 10 digits to represent all values: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9. Hexadecimal is a number system that uses 16 digits; it uses the same 10 digits in the decimal system and borrows 6 letters from the alphabet: A, B, C, D, E, and F.

Because more digits are available, hexadecimal can express large values in fewer characters. In decimal, to express the value after 9, we have to add another character—it becomes 10, a 1 and a 0. Hexadecimal can express that same value in a single character: A. The efficiency of hexadecimal over decimal becomes more significant as the values become greater. Table 6.1 lists some decimal numbers and their equivalent hexadecimal numbers.

Table 6.1 Decimal numbers and their hexadecimal equivalents

| Decimal | Hexadecimal |
| ------- | ----------- |
| 0       | 0           |
| 1       | 1           |
| 2       | 2           |
| 3       | 3           |
| 4       | 4           |
| 5       | 5           |
| 6       | 6           |
| 7       | 7           |
| 8       | 8           |
| 9       | 9           |
| 10      | A           |
| 11      | B           |
| 12      | C           |
| 13      | D           |
| 14      | E           |
| 15      | F           |
| 16      | 10          |
| 17      | 11          |
| 18      | 12          |
| 19      | 13          |
| 20      | 14          |
| 21      | 15          |
| 22      | 16          |
| 23      | 17          |
| 24      | 18          |
| 25      | 19          |
| 26      | 1A          |
| 27      | 1B          |
| 28      | 1C          |
| 29      | 1D          |
| 30      | 1E          |
| 31      | 1F          |

Note You can use a prefix to indicate whether a number is a decimal or hexadecimal number: 0d for decimal and 0x for hexadecimal. This can be useful in networking because we use multiple systems: binary, decimal, and hexadecimal. Ten in decimal is 10, but 10 in hexadecimal is equal to 16 in decimal. To clearly differentiate between the two, you can write 0d10 or 0x10.
In part 5 of this book (IPv6), we will practice converting between decimal, hexadecimal, and binary. For now, that is not necessary; it is enough to understand that MAC addresses are typically written in hexadecimal.

Characteristics of MAC addresses
We have already covered two characteristics of MAC addresses: they are 6 bytes in length and are usually written in hexadecimal. By writing them in hexadecimal, we can express the address in fewer characters; MAC addresses are written as 12 hexadecimal characters rather than 48 bits (1s and 0s). The details regarding how those 12 characters are notated can vary. The following is a single MAC address written using three different notational conventions. Of course, because this is a CCNA book, I will follow Cisco’s convention for writing MAC addresses, but it’s worth knowing that they can be written in other ways. For comparison, I have also included the address written in binary—I’m sure you’ll agree that the hexadecimal representations are easier to read:
0cf5.a452.b101 (used by Cisco IOS)
0C-F5-A4-52-B1-01 (used by Windows)
0c:f5:a4:52:b1:01 (used by macOS)
000011001111010110100100010100101011000100000001 (binary)
Unlike IP addresses (which we’ll cover in chapter 7), MAC addresses are not assigned by the network admin or engineer configuring the device. Instead, each port of a network device has a MAC address that is assigned to it by the manufacturer. For this reason, another name for a MAC address is a burned-in address (BIA): it is “burned into” the physical port. A MAC address is globally unique—it should not be shared by a port on any other device in the world.
Note It is possible to override a manufacturer-assigned MAC address with manual configuration, but it is extremely rare to do so.
To ensure that MAC addresses remain globally unique, the first half of each MAC address (the first 3 bytes) is an organizationally unique identifier (OUI) assigned to the manufacturer by the IEEE. Then, the manufacturer is free to use the second half to assign unique MAC addresses to each device they manufacture. For example, the MAC addresses of the first three ports of the Cisco switch in my home network are
0cf5.a452.b101
0cf5.a452.b102
0cf5.a452.b103
0cf5.a4 is Cisco’s OUI (actually, Cisco has many OUIs), and the second half is a unique identifier for each port on the switch. As you probably noticed, those three MAC addresses are quite similar—only the final digit is different. That’s because MAC addresses on the same device are typically assigned sequentially.
Let’s summarize MAC addresses before moving on:
MAC addresses are 6-byte (48-bit) addresses assigned to ports by the device’s manufacturer. Another name for a MAC address is burned-in address (BIA).
MAC addresses are globally unique.
The first 3 bytes are an organizationally unique identifier (OUI), assigned to the manufacturer by the IEEE.
The last 3 bytes are unique to the port itself.
MAC addresses are written as 12 hexadecimal characters.

6.2.3 Type/Length
The Type/Length field is a 2-byte field that can be used either to indicate the type of the encapsulated packet (e.g., an IP version 4 packet or an IP version 6 packet) or to indicate the length of the encapsulated packet (in bytes). There are historical reasons why this field can be used for two purposes, but both uses are now officially part of the Ethernet standard. These days, in almost all cases, this field is used to indicate the type of the encapsulated packet: instead of this field indicating length, the end of the frame is indicated by a special signal after the frame.
Note The original IEEE 802.3 standard used the Type/Length field exclusively to indicate the length of the encapsulated packet, and an additional header was used to indicate the type of encapsulated protocol: the Logical Link Control (LLC) header, sometimes with an additional Subnetwork Access Protocol (SNAP) extension to that header. However, this is beyond the scope of the CCNA exam.
A value of 1500 (decimal) or less in this field means that it indicates the length of the encapsulated packet in bytes. For example, if the value is 1500, it means the encapsulated packet is 1500 bytes in length.
A value of 1536 or greater in this field indicates the type of the encapsulated packet, which is usually IP version 4 (IPv4) or IP version 6 (IPv6). When used to indicate the type of the encapsulated packet, this field is called the EtherType field. For reference, here are the values in this field for IPv4 and IPv6, both of which are significant topics on the CCNA exam (usually hexadecimal notation is used; I’m including the decimal numbers for comparison):
IPv4: 0x0800 (0d2048)
IPv6: 0x86DD (0d34525)
Note Values between 1500 and 1536 should not be used in this field.

6.2.4 Frame Check Sequence
The Frame Check Sequence (FCS) is the only field of the Ethernet trailer. It is 4 bytes in length and is used to detect corrupted data in the frame. Before a device sends a frame, it uses an algorithm to calculate a checksum, a small block of data that is appended to the end of the frame as the FCS field.
Then, when the frame’s destination host receives the frame, it calculates its own checksum for the frame (with the same algorithm) and compares it to the one calculated by the sender. If the two checksums are the same, the receiver can safely assume that the data has not been corrupted in transit. However, if the checksums calculated by the sender and receiver are different, the receiver will discard the frame—the data has been corrupted in transit (perhaps because of electromagnetic interference).
FCS is the name of the field, but the name for this kind of checksum is cyclic redundancy check (CRC). The term cyclic refers to the kind of algorithm used to calculate the checksum. Redundancy means that the field is redundant—it expands the size of the message but doesn’t add any additional information. Check is self-explanatory—it is used to check if the frame traveled from source to destination without the data being corrupted.

6.3 Frame switching
Now that we have looked at the information in the Ethernet header and trailer, let’s see how switches use the Source and Destination fields to build a MAC address table and forward frames to the appropriate destination(s) within a LAN.

6.3.1 MAC address learning
When a switch has to make a decision about how to forward a frame, it looks up the frame’s destination MAC address in its MAC address table, which is a list of the MAC addresses in the LAN and which port each is connected to. We will examine the frame-forwarding process in section 6.3.2, but first, how does a switch build its MAC address table?
Note Another name for a MAC address table is CAM table, named after the kind of memory the table is stored in (content addressable memory).
This is the role of the Source field of the Ethernet header. When a switch receives a frame on one of its ports, it examines the Source field and creates an entry for that MAC address in its MAC address table, associating that MAC address with the port the frame was received on. This entry says “To reach this MAC address, forward the frame out of this port.” This makes sense: if a switch receives a frame from MAC address X on port Y, the switch knows it can reach the host with MAC address X out of port Y. This process is called MAC address learning. Figure 6.3 shows a simple network with two switches, each with two PCs connected. By examining the Source field of frames that arrive on its ports, each switch has built a MAC address table that tells it which port each MAC address is connected to (directly or via another switch).
Definition MAC addresses learned by a switch in this manner are known as dynamic MAC addresses—they are automatically (dynamically) learned. This is in contrast to static MAC addresses, which are manually (statically) configured, although that is quite rare. A switch will remove a dynamic MAC address from its MAC address table after 5 minutes of inactivity (if it doesn’t receive a frame from that MAC address for 5 minutes); this is called MAC aging.

Figure 6.3 A network with two switches, each with two PCs connected. SW1 and SW2 have learned the MAC address of each PC by examining the Source field of frames received on their ports as the PCs communicate with each other. SW1 knows it can reach PC1 via its G0/1 port, PC2 via its G0/2 port, and PC3/PC4 via its G0/0 port. SW2 knows it can reach PC1/PC2 via its G0/0 port, PC3 via its G0/1 port, and PC4 via its G0/2 port.
Figure 6.3 shows the state of the network after the switches have learned the MAC addresses of the devices in the LAN. However, we are missing a few pieces of the puzzle, such as how switches forward traffic before they have built their MAC address tables and how the PCs learn each others’ MAC addresses.
Port names on Cisco devices
Ports on Cisco devices have a name indicating their maximum supported speed (Ethernet = 10 Mbps, FastEthernet = 100 Mbps, GigabitEthernet = 1 Gbps, TenGigabitEthernet = 10 Gbps), followed by one to three numbers. How many numbers are used depends on the model of the device.
In this book, I will use a two-number system (X/Y), where the first number is the slot on the device, and the second number is the port number within that slot. A slot is a group of ports on a network device. In many cases, the ports in a slot are modular, meaning you can insert modules with different kinds of ports depending on your needs. Additionally, I will shorten the names to use the first letter only: E = Ethernet, F = FastEthernet, G = GigabitEthernet, T = TenGigabitEthernet.
Furthermore, port numbers on physical Cisco switches start from 1 (G0/1, G0/2, G0/3, etc). However, for most examples in this book, I will use virtual devices running in Cisco’s emulation software CML (Cisco Modeling Labs), in which port numbers start from 0 (G0/0, G0/1, G0/2, etc).

6.3.2 Frame flooding and forwarding
Once the switches have learned the MAC address of each host in the LAN, as in figure 6.3, forwarding traffic is simple: when a switch receives a frame, it looks up the destination MAC address in its MAC address table and forwards the frame out of the appropriate port. For example, if PC1 sends a frame to PC2’s MAC address, SW1 will check its MAC address table and see that it should forward the frame out of its G0/2 port. This frame from PC1 is a known unicast frame.
Definition A frame addressed to a single destination host is called a unicast frame. If the switch already has an entry for the frame’s destination MAC address in its MAC address table, it is called a known unicast frame.
The action a switch takes upon receiving a known unicast frame is to forward it out of the appropriate port. Now let’s examine what happens when a switch receives a unicast frame and doesn’t have an entry for the frame’s destination MAC address in its MAC address table—an unknown unicast frame. Figure 6.4 shows what happens when PC1 sends a message to PC3, and both switches have an empty MAC address table.
Definition An unknown unicast frame is a frame addressed to a single destination host, but the switch doesn’t have an entry for the frame’s destination MAC address in its MAC address table.

Figure 6.4 PC1 sends a unicast frame to PC3, but neither SW1 nor SW2 have an entry for the destination MAC address in their MAC address table. (1) PC1 sends the frame, and SW1 learns PC1’s MAC address. (2) SW1 floods the frame. SW2 learns PC1’s MAC address. PC2 drops the frame. (3) SW2 floods the frame. PC4 drops the frame. PC3 receives and processes it.
PC1 sends a unicast frame addressed to PC3’s MAC address. SW1 uses the Source of the frame to learn PC1’s MAC address, and then it floods the frame—it sends the frame out of every port except the one it was received on (G0/1). SW1 doesn’t have an entry for the PC3’s MAC address in its MAC address table, so by flooding the frame, it hopes the frame will be able to reach PC3, and then it will later be able to learn PC3’s MAC address when PC3 sends a reply.
Definition To flood a frame is to send it out of all ports, except the port the frame was received on. Switches take this action on receiving an unknown unicast frame.
When SW1 floods the frame, both PC2 and SW2 receive it. Because the destination MAC address of the frame is not PC2’s, it drops the frame. SW2, on the other hand, will treat the frame just like SW1 did; it will learn PC1’s MAC address and then flood the frame out of its G0/1 and G0/2 ports.
When SW2 floods the frame, both PC3 and PC4 receive it. Like PC2, PC4 will drop the frame because the destination MAC address is not its own. However, PC3 sees that the frame is destined for its own MAC address, so PC3 will receive and process the message. Figure 6.5 shows what then happens when PC3 sends a reply back to PC1.
Figure 6.5 PC3 replies to PC1’s message. (1) PC3 sends the frame, and SW2 learns PC3’s MAC address. (2) SW2 forwards the frame out of its G0/0 port, and SW1 learns PC3’s MAC address. (3) SW1 forwards the frame out of its G0/1 port, and PC1 receives and processes it.
PC3’s reply to PC1 is also a unicast frame, but this time both SW1 and SW2 have an entry for the frame’s destination (PC1’s MAC address) in their MAC address tables, so rather than flooding the frame, each switch simply forwards it out of the port specified by the entry in its MAC address table. First, PC3 sends the frame, and SW2 learns PC3’s MAC address on its G0/1 port. SW2 then forwards the frame out of its G0/0 port, and SW1 learns PC3’s MAC address on its G0/0 port. Finally, SW1 forwards the frame out of its G0/1 port, and PC1 receives and processes the message. Remember what action a switch takes for each kind of unicast frame:
Known unicast frame (forward)—The switch will send the frame out of the port specified by the MAC address’s entry in the MAC address table.
Unknown unicast frame (flood)—The switch will send the frame out of all ports except the one it was received on.
Note A switch is transparent to its connected hosts; PC1 and PC3 address their messages directly to each other, not to SW1 or SW2, exactly as they would if they were directly connected with a single cable. This is why a message passing through a switch is not considered a hop (as stated in chapter 4). Also, switches do not modify the frames they switch in any way; they simply forward or flood them as appropriate.

6.3.3 The MAC address table in Cisco IOS
The command to view a Cisco switch’s MAC address table is show mac address-table (in user EXEC or privileged EXEC mode). As the following example shows, there are a few more columns than just the MAC address and port. The Type column indicates whether the MAC address was dynamically learned (DYNAMIC) or statically configured (STATIC). The Vlan column indicates which virtual LAN (VLAN) each MAC address was learned in. We will cover VLANs in chapter 12. For now, just note that all of the MAC addresses are in VLAN 1 by default:

SW1# show mac address-table                      ❶
          Mac Address Table
-------------------------------------------
  
Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   1    5254.0017.7cd2    DYNAMIC     Gi0/0      ❷
   1    d8bb.c1cc.ff01    DYNAMIC     Gi0/1      ❷
   1    d8bb.c1cc.ff02    DYNAMIC     Gi0/2      ❷
   1    d8bb.c1cc.ff03    DYNAMIC     Gi0/0      ❷
   1    d8bb.c1cc.ff04    DYNAMIC     Gi0/0      ❷
❶ Views SW1’s MAC address table

❷ A list of MAC addresses and the port each was learned on

Note Cisco abbreviates GigabitEthernet ports as “GiX/X,” not “GX/X.”
Above the MAC addresses of PC1, PC2, PC3, and PC4 in the previous example, there is an additional MAC address in SW1’s MAC address table (5254.0017.7cd2). This is the MAC address of SW2’s G0/0 port. Although the MAC addresses of a switch’s ports don’t play a role when it is forwarding traffic between hosts, switches periodically exchange messages with each other and learn each other’s MAC addresses in the process. We will cover some of these messages exchanged among switches in this book.
Although you can usually leave a switch to learn MAC addresses by itself and clear them as needed (after 5 minutes of inactivity), you can manually clear dynamic MAC addresses from a switch’s MAC address table with the clear mac address-table dynamic command. The following example shows this; I clear SW1’s MAC address table and then view it again, but it is empty:

SW1# clear mac address-table dynamic           ❶
SW1# show mac address-table                     
          Mac Address Table
-------------------------------------------
  
Vlan    Mac Address       Type        Ports    ❷
----    -----------       --------    -----    ❷
❶ Clears SW1’s dynamically learned MAC addresses

❷ SW1’s MAC address table is empty.
You can also specify a specific address to remove from the MAC address table or tell the switch to remove all MAC addresses learned on a specific port. To clear a specific dynamic MAC address from the table, you can use the clear mac address-table dynamic address mac-address command. To clear all dynamic MAC addresses learned on a specific interface, use the clear mac address-table dynamic interface interface-name command.
However, as stated previously, you usually will not have to manually interfere with a switch’s MAC address learning and aging processes. Note that this command uses the term interface instead of port. As you will see when we cover more configurations, this is true of most commands within Cisco IOS.
Note When I use bold and italics in a command, the bolded words indicate the command and its keywords that you must type. The italicized words indicate arguments for which you must provide a value. For example, in clear mac address-table dynamic address mac-address, you must type clear mac address-table dynamic address and then specify the mac-address to clear.

6.4 Address Resolution Protocol
Now we have looked at how switches forward frames and learn the MAC addresses of devices in their LAN. Next we will take a step back to fill in another piece of the puzzle—how the PCs know each other’s MAC address. For PC1 and PC3 to send messages to each other, they first need to learn each other’s MAC address. To do so, they use Address Resolution Protocol (ARP).
ARP allows a host to learn the MAC address of another host in the LAN. ARP involves two messages: an ARP request (used to ask another host what its MAC address is) and an ARP reply (used to inform another host of this host’s MAC address). The ARP request message is sent in a new kind of frame: not unicast but broadcast. The ARP reply is a unicast frame sent to the MAC address of the host that sent the ARP request.
Definition A broadcast frame is a frame addressed to the broadcast MAC address: ffff.ffff.ffff. A switch will flood broadcast frames, like unknown unicast frames. Broadcast frames are used by hosts to send messages to all other hosts in the LAN.
If an ARP request is broadcast (addressed to all other hosts in the LAN), how does the sender specify which host’s MAC address it wants to learn? It does so by specifying the IP address of the host it wants to know the MAC address of. Figure 6.6 demonstrates this. PC1 wants to send a message to PC3 but doesn’t know PC3’s MAC address. So, PC1 uses ARP to learn PC3’s MAC address.
Note The IP addresses of PC1, PC2, PC3, and PC4 are shown in figure 6.6, but it’s not necessary to understand the structure of IP addresses yet. We will cover IP addresses in the next chapter.

Figure 6.6 An ARP request and reply exchange between PC1 and PC3. PC1 wants to send a message to PC3 but does not know PC3’s MAC address, so PC1 uses ARP to learn PC3’s MAC address.

Here’s the process shown in figure 6.6:
PC1 sends an ARP request addressed to the broadcast MAC (ffff.ffff.ffff).
SW1 floods the frame. PC2 sees the ARP request is not for its own IP address, so it drops the message.
SW2 floods the frame. PC4 sees the ARP request is not for its own IP address, so it drops the message. PC3 sees the ARP request is for its own IP address.
PC3 sends an ARP reply to PC1.
SW2 forwards the ARP reply out of its G0/0 port.
SW1 forwards the ARP reply out of its G0/1 port. PC1 now knows PC3’s MAC address, so it will be able to send the original message to PC3.
Note The group of devices that will receive a broadcast frame sent by one of the group’s members are in the same broadcast domain. A broadcast domain can be thought of as equivalent to a LAN or Layer 2 domain. All of the devices in figure 6.6 are in the same broadcast domain because they receive each other’s broadcast frames.
After the ARP exchange is complete, PC1 knows PC3’s MAC address; it will store PC3’s MAC address in its ARP table, which is a list of IP addresses and their associated MAC addresses. ARP can be thought of as the bridge between Layers 2 and 3 of the TCP/IP model. ARP is used to map a known Layer 3 address (IP address) to an unknown Layer 2 address (MAC address).

Now PC1 will be able to send its message in a frame addressed to PC3’s MAC address. It is also worth mentioning that upon receiving PC1’s ARP request message, PC3 also stores PC1’s MAC address in its own ARP table.
Note that, thanks to the ARP request–reply exchange, SW1 and SW2 have already learned PC1 and PC3’s MAC addresses (the MAC address learning process was not shown in figure 6.6 to focus on the ARP process). So, when PC1 sends its message to PC3, the switches won’t flood it—they will simply forward it out of the appropriate port because it is a known unicast message.
Note Unicast messages can be thought of as one-to-one and broadcast as one-to-all. Additionally, there is another type of message called multicast, which is one-to-multiple (but not necessarily all). We will touch on multicast messages in later chapters of this volume and volume 2.
We have covered how switches learn MAC addresses, how they flood and forward frames, and how hosts learn the MAC address of another host in the LAN by sending an ARP request to that host’s IP address, but there is still one more part to the puzzle. How does a host know the IP address of the host it wants to send a message to? The answer is, “It depends.” We will cover some possibilities in this book—for example, the Domain Name System (DNS), which is used to convert hostnames (i.e., manning.com) into IP addresses. As another option, the user of the device could manually specify the IP address to send a message to, such as when using ping to test connectivity.
Note A device doesn’t have to use ARP every time it sends a message. After it has used ARP to learn another device’s MAC address, it stores that information in its ARP table for future use.

6.5 Ping
Ping is a software utility that tests the reachability of hosts over a network. It’s not directly connected to the topic of Ethernet switching, but it is a tool I’ll be referencing throughout the book, and it also serves to fill the final piece of the puzzle in this chapter—how a source host knows the IP address of the destination host it wants to send a message to.
To send a ping message to another host on the network, the command is ping ip-address (this is true for Cisco IOS, Windows, Linux, macOS, etc.). The IP address of the destination host is specified directly in the command, so that’s how the source host knows the IP address of the destination host.
Ping is a component of the Internet Control Message Protocol (ICMP), which plays a supporting role for the Internet Protocol (IP). In your networking career (or career in nearly any other area of IT), you’ll certainly use ping very frequently as a simple way to test whether two hosts can reach each other over the network; it is a very common diagnostic and troubleshooting tool. Like ARP, ping consists of two messages: an ICMP echo request and an ICMP echo reply. However, unlike ARP, both messages used by ping are unicast.
Ping can also be used to measure the round-trip time (RTT) between two hosts—the time it takes a message to travel from one host to another and back. The following example shows a ping from a Cisco router (R1) to another host on its local network. In Cisco IOS, a single ping command sends five ICMP echo requests. As highlighted, the output lists the minimum, average, and maximum RTT for those five requests:

PC1# ping 10.0.0.12                                                    ❶
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.0.0.12, timeout is 2 seconds:
!!!!!                                                                  ❷
Success rate is 100 percent (5/5), round-trip min/avg/max = 3/3/4 ms   ❷
❶ Sends five ICMP echo requests (pings) to the specified IP address
❷ Each exclamation mark indicates a successful ping.
The five exclamation marks (!!!!!) in the output indicate successful pings—ICMP echo requests that received an ICMP echo reply. If any of the requests do not receive a reply, a period (.) is displayed instead. For example, if the first request did not receive a reply, the output would be .!!!!.

Summary
A local area network (LAN) can be defined as a portion of a network where hosts can communicate with each other without the use of a router. This is also called a Layer 2 domain.
The Ethernet header has three fields: Destination, Source, and Type/Length. The Ethernet trailer has one field: the Frame Check Sequence (FCS).
Although they are not considered part of the Ethernet frame, the Preamble and Start Frame Delimiter (SFD) are sent with each frame.
The Preamble is a 7-byte series of alternating binary 1s and 0s. The SFD is a single byte in length and uses the bit pattern 10101011 to indicate the end of the Preamble and the beginning of the frame.
The Destination and Source fields are each 6 bytes in length and contain the MAC address of the frame’s sender (Source) and its intended receiver (Destination). MAC addresses are assigned by the manufacturer and should be globally unique.
MAC addresses are usually written in hexadecimal, a number system that uses 16 characters: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, and F. When written in hexadecimal, MAC addresses are 12 characters in length.
The first half of a MAC address is the organizationally unique identifier (OUI), which is assigned to the device’s manufacturer by the IEEE. The second half of the MAC address can be used freely by the manufacturer to assign a unique MAC address to each port of the devices it manufactures.
The Type/Length field either indicates the type of the encapsulated packet (i.e., IPv4 or IPv6) or the length of the encapsulated packet in bytes. If the value is 1500 or less, it indicates the length of the packet. If the value is 1536 or greater, it indicates the type (in this case, the name is EtherType).
The FCS field uses a cyclic redundancy check (CRC) to allow the receiving host to check for errors in the frame that might have occurred in transit.
A switch makes decisions about how to forward frames by looking up each frame’s destination MAC address in the switch’s MAC address table.
A switch builds its MAC address table by looking at the source MAC address field of frames it receives and creating an entry in the MAC address table, associating the MAC address with the port the frame was received on. This is called MAC address learning.
MAC addresses learned like this are called dynamic MAC addresses.
If a switch doesn’t receive a frame from a dynamic MAC address for 5 minutes, it will remove the entry from the MAC address table. This is called MAC address aging.
A frame addressed to a single host is called a unicast frame. If the switch already has an entry for the frame’s destination MAC in its MAC address table, it is a known unicast frame, and the switch will forward it out of the appropriate port. If the switch does not have an entry for the frame’s destination MAC in its MAC address table, it is an unknown unicast frame, and the switch will flood the frame, sending it out of all ports (except the one it was received on).
The show mac address-table command allows you to view the MAC address table of a Cisco switch. Dynamic MAC addresses can be cleared with clear mac address-table dynamic, clear mac address-table dynamic address mac-address, or clear mac address-table dynamic interface interface-name.
Address Resolution Protocol (ARP) allows a host to learn the MAC address of another host in the network. It uses two messages: an ARP request and an ARP reply.
The ARP request is sent to the broadcast MAC address (ffff.ffff.ffff), so it is flooded by switches. The ARP reply is a unicast message.
A broadcast domain is a group of devices that receive broadcast messages from each other. Devices connected to the same switch (or different switches, but the switches are connected) are in the same broadcast domain.
The ARP table is used to store IP address-to-MAC address mappings, so an ARP request doesn’t have to be sent before every single packet.
Ping is a utility that tests connectivity between two network hosts. It is a component of the Internet Control Message Protocol (ICMP) and is a common diagnostic and troubleshooting tool. To send a ping, use the ping ip-address command.
Ping uses two messages: an ICMP echo request and an ICMP echo reply. Both are unicast messages.