10 Quality of service
This chapter covers

Enabling IP telephony with voice VLANs
Powering IP phones and other devices with Power over Ethernet
Prioritizing important network traffic in times of congestion with quality of service
Network resources—bandwidth, in particular—are not unlimited. This means that networks can become congested, and bottlenecks can occur, negatively affecting network performance and the experience of the network’s users. Some types of network communications are more sensitive to these problems. For example, users in a voice/video call, due to their real-time nature, are more likely to notice a network slowdown than users communicating via email.

Quality of service (QoS) is a set of technologies that enable the prioritization of more important traffic (and the de-prioritization of less important traffic) in times of network congestion. In this chapter, we will cover QoS and its various components. Before covering QoS itself, we will cover the topic of IP telephony, also called Voice over IP (VoIP)—telephones that communicate over a network using IP packets. Voice traffic is particularly sensitive to poor network performance and is usually prioritized in a QoS policy. We’ll also cover Power over Ethernet (PoE), which is used to power IP phones (and other devices) over Ethernet cables. Here are the exam topics we’ll cover:

1.1.h PoE

2.1.a Access ports (data and voice)

4.7 Explain the forwarding per-hop behavior (PHB) for QoS such as classification, marking, queuing, congestion, policing, shaping

10.1 IP telephony
Traditional telephones connect to the public switched telephone network (PSTN), a network separate from the computer networks that are the subject of this book—this is also called plain old telephone service (POTS). IP phones, or VoIP phones, on the other hand, connect to Ethernet switches and communicate by sending and receiving IP packets.

Many companies have migrated from POTS to IP telephony for a variety of reasons, such as the cost effectiveness and advanced features that IP telephony provides (i.e., voicemail-to-email, integration with other business software, etc.). However, this created its own problems: each desk would now have two end-user devices (a PC and an IP phone), doubling the required number of Ethernet UTP cables that must be installed to each desk and the number of switch ports required. As a solution to this problem, IP phones have a small, internal three-port switch, allowing the IP phone and PC to connect to a single switch port, as in figure 10.1.



Figure 10.1 An IP phone’s internal switch allows both the phone and a PC to connect to a single port on SW1. One port of this mini-switch connects to the PC, one to SW1, and one to the IP phone’s internals.

10.1.1 Voice VLANs
Although a PC and IP phone can share a single switch port, their traffic should be kept segmented—kept in separate subnets and separate VLANs. One major reason for this is QoS: voice calls are very sensitive to lost and delayed packets, so voice traffic should be prioritized over regular network traffic from the PCs—also called data traffic. By segmenting voice and data traffic into separate subnets and VLANs, you can more easily identify and prioritize each traffic type in QoS policies. This can be achieved using the voice VLAN feature, as shown in figure 10.2.



Figure 10.2 Segmenting voice and data traffic into separate subnets and VLANs

When covering access and trunk ports in chapter 12 of volume 1, I said that access ports belong to a single VLAN, whereas trunk ports can carry traffic from multiple VLANs, tagging frames with the 802.1Q protocol to differentiate between VLANs. Given that information, the configuration shown in figure 10.2—access ports carrying traffic in two VLANs—might seem incorrect. However, this case is an exception. When an access port is configured with a voice VLAN, it carries traffic in two VLANs:

One for the data VLAN (also called the access VLAN), which is untagged

One for the voice VLAN, which is tagged

In the following example, I configure SW1’s ports as access ports, with VLAN 10 as the data VLAN (switchport access vlan 10) and VLAN 20 as the voice VLAN (switchport voice vlan 20). I then use show interfaces f0/1 switchport to confirm that F0/1 is indeed considered an access port, despite carrying traffic in two VLANs:

JITL-SW1(config)# interface range f0/1-3
JITL-SW1(config-if-range)# switchport mode access             ❶
JITL-SW1(config-if-range)# switchport access vlan 10          ❷
JITL-SW1(config-if-range)# switchport voice vlan 20           ❷
JITL-SW1(config-if-range)# do show interfaces f0/1 switchport
Name: Fa0/1
Switchport: Enabled
Administrative Mode: static access                            ❸
Operational Mode: static access                               ❸
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: native
Negotiation of Trunking: Off
Access Mode VLAN: 10 (VLAN0010)                               ❹
Trunking Native Mode VLAN: 1 (default)
Administrative Native VLAN tagging: disabled
Voice VLAN: 20 (VLAN0020)                                     ❹
. . .
❶ Manually configures access mode

❷ Configures the data (access) and voice VLANs

❸ F0/1 is an access port.

❹ F0/1’s data and voice VLANs are listed.

10.1.2 Power over Ethernet
IP phones often take advantage of a technology called Power over Ethernet (PoE), which allows the phones to receive electrical power over the same Ethernet UTP cables that they use to transmit data—no need for separate power cables. This provides reduced costs (fewer power cable runs are required), less desk and office clutter (fewer cables and adapters), and the flexibility to place devices in locations without a power outlet nearby.

Note You may wonder how electrical power and data can be transmitted over the same cable. The short answer is that because of the different frequency ranges used for power and data transmissions, they don’t interfere with each other.

Figure 10.3 demonstrates how PoE works. Whereas SW1 and the PCs receive electrical power from wall outlets, the IP phones receive electrical power from SW1 using PoE. SW1 is the Power Sourcing Equipment (PSE)—the device that supplies power using PoE—and the IP phones are the Powered Devices (PDs).



Figure 10.3 SW1, the PSE, supplies electrical power to IP phones (PDs) using PoE.

Note In addition to IP phones, a variety of devices can use PoE: IP cameras, wireless access points, access control devices like badge readers, door locks, and many others.

A PSE must be cautious about sending electrical power over an Ethernet cable; if a PSE were to incorrectly send electrical power using PoE to a device that is not designed to handle it, there is a risk of damaging the device. Similarly, if the PSE were to send too much power to a PD, that could damage the PD. For that reason, a PoE-enabled switch port doesn’t immediately send electrical power when a device is connected. Instead, it uses the following process:

Detection—When a device is connected, the PSE performs an initial check by applying a low voltage to the cable to detect if the device can handle PoE.

Classification—The PSE assesses the power needs of the connected PD, and allocates the required amount of power from its available supply.

Startup—The PSE supplies the appropriate voltage to start up the PD.

Normal operation—The PSE supplies power to the PD and monitors the electrical current to ensure safe and consistent delivery of power.

On a PoE-enabled switch, you can confirm the status of PDs with the show power inline command. The following example shows the output:

SW1# show power inline
Available:124.0(w)  Used:30.8(w)  Remaining:93.2(w)                 ❶
Interface Admin  Oper   Power   Device              Class Max
                        (Watts)                            
--------- ------ ---------- ------- ------------------- ----- ----
Fa0/1     auto   on      15.4    AIR-CAP3502I-E-K9   3     15.4     ❷
Fa0/2     auto   on      15.4    AIR-CAP3502E-E-K9   3     15.4     ❷
Fa0/3     auto   off      0.0    n/a                 n/a   15.4 
. . .
❶ Information about the available power budget

❷ The two PDs are class 3, meaning the switch allocates 15.4 watts each.

Note The class indicates the power needs of the connected device. The devices in the example are wireless access points. IP phones typically require less power and are often class 1 (in which the switch allocates 4 watts) or class 2 (7 watts).

You can modify the PoE settings of each switch port with the power inline command in interface config mode, which has various keywords. By default, the power inline auto command is applied. With this command enabled, the switch will automatically allocate power to the port after detecting a device that requires PoE connected to the port. However, power is allocated on a first come, first served basis; if there isn’t enough power remaining in the switch’s total budget, it will not be able to supply power to the device.

The power inline static [max milliwatts] command can be used to preallocate power to a port, reserving a certain amount of power for the port even when a PD isn’t connected. If you don’t specify a value in the command, the maximum value is allocated. When a device is connected to the port, the switch still waits to detect the PD, assess its power needs, and supply the appropriate amount of power, but the amount of power specified in this command is always allocated for this port, even when it’s not in use.

Note You should usually use the default mode of auto since it allocates only as much power as needed to each device and doesn’t require manual configuration. However, static can be used if the power budget is tight and you need to guarantee power to a particular device. Another option is never, which disables PoE on the port.

CDP and LLDP’s role in PoE

The Layer 2 discovery protocols Cisco Discovery Protocol (CDP) and Link Layer Discovery Protocol (LLDP) can be used to facilitate PoE by allowing devices to communicate their PoE requirements. These protocols help switches determine how much power a connected device, like an IP phone or wireless access point, needs. This negotiation process helps to prevent devices from drawing too much power while ensuring that each device is getting the power it needs.

If a PD draws too much power from the switch, it can damage the switch. One feature to protect against this is power policing (also called power classification override). You can enable this feature on a switch port with the power inline police command in interface config mode. In the following example, I configure it on two switch ports and confirm with show power inline police:

SW1(config)# interface range f0/1-2
SW1(config-if-range)# power inline police                         ❶
SW1(config-if-range)# do show power inline police
Available:124.0(w)  Used:30.8(w)  Remaining:93.2(w)
Interface Admin  Oper    Admin      Oper     Cutoff Oper  
          State  State   Police     Police   Power  Power 
--------- ------ ---------- ---------- ---------- ------ -----    ❷
Fa0/1     auto   On      errdisable ok       15.4   8.5           ❷
Fa0/2     auto   On      errdisable ok       15.4   8.5    
. . .
❶ Enables power policing

❷ The cutoff power is 15.4 watts.

With power policing enabled, if a PD draws too much power (more than the cutoff power), the switch will put the port into an error-disabled state (stopping data and power transmission on the port) and generate a Syslog message. To reenable an error-disabled port, you can use shutdown to administratively disable the port and then no shutdown to reenable it. Make sure to disconnect the device that caused the problem first!

10.2 QoS concepts
Voice traffic from IP phones is particularly sensitive to network congestion; if packets are getting delayed or dropped, the user experience can be severely impacted. The same applies to calls on Zoom and similar apps. However, other types of traffic are less affected. File downloads, for example, may take a bit longer to complete when the network is congested, but the overall user experience remains the same. Using QoS, we can prioritize some types of traffic and de-prioritize others to maintain a positive user experience when congestion occurs. In this section, we’ll examine some high-level QoS concepts before diving into the details in the following sections.

10.2.1 Bandwidth
Bandwidth refers to a link’s capacity—how much data it can carry per second. We covered this concept in chapter 16 of volume 1 on EtherChannel. Different areas of a network typically have different total bandwidths, which can lead to bottlenecks, as shown in figure 10.4.



Figure 10.4 Different areas of the network have different total bandwidths. The LAN has two 1 Gbps WAN connections, which are potential bottlenecks.

Whereas each end host typically has plenty of bandwidth over its connection to the network (e.g., a 1 Gbps link per host), wide area network (WAN) and internet connections are common bottlenecks. A significant reason for this is cost; connecting remote sites over a service provider’s network is expensive.

Fortunately, it’s not necessary to have a 1:1 ratio of bandwidth between end hosts and the WAN. End hosts aren’t always communicating over the WAN, and when they are, they usually aren’t all communicating at their full capacity at the same time. However, during peak usage, congestion can occur, leading to some negative effects: delay, jitter, and loss.

10.2.2 Delay, jitter, and loss
The purpose of QoS is to minimize the delay, jitter, and loss of important traffic during times of congestion. Delay (or latency) is the amount of time it takes a packet to travel across the network from its source to its destination. A related term is round-trip time (RTT), which is a two-way delay—the amount of time it takes a packet to reach its destination and for the reply packet to be received by the original sender. Figure 10.5 demonstrates these concepts.



Figure 10.5 Delay and round-trip time (RTT). Delay is the amount of time it takes a packet to go from source to destination. RTT is the amount of time it takes a packet to go from source to destination and for the reply to arrive back at the source.

Delay is usually measured in milliseconds, and Cisco recommends that delay should be 150 ms or less for voice traffic. What happens if the delay gets much higher than that? It’s not hard to imagine. Think of a phone call in which the person you’re talking to only hears what you say 2 seconds after the fact—not a smooth conversation.

Jitter is the variation in delay in a series of packets. Some delay is inevitable; packets sometimes have to travel quite a long way and through quite a few intermediate devices to reach their destination. However, the delay should ideally remain fairly constant; too much jitter negatively affects user experience in real-time apps like voice and video calls. Like delay, jitter is measured in milliseconds. Cisco recommends that jitter should be 30 ms or less for voice traffic. Figure 10.6 demonstrates jitter.



Figure 10.6 Jitter is the variation in delay in a series of packets.

The final concept is loss, which is the percentage of packets lost over a period of time—packets that didn’t reach their destination. Under normal circumstances, loss should be close to zero. However, in times of congestion, some packets may have to be dropped. Cisco recommends loss of 1% or less for voice calls. TCP-based applications can deal with dropped packets through retransmissions. On the other hand, UDP-based VoIP protocols don’t retransmit dropped packets. This is intentional; waiting for a packet to be retransmitted in a voice call would only cause more delay and disrupt the conversation. However, if there are too many drops, users will experience the familiar issue of the call “breaking up,” resulting in choppy or interrupted audio.

IP Service-Level Agreement

Cisco IOS devices include a feature called IP Service-Level Agreement (IP SLA) that can be used to measure various aspects of network performance, including delay, RTT, jitter, and loss. A service-level agreement is a predefined set of performance metrics/standards that a service is expected to meet; this is usually agreed upon between a service provider and a customer. IP SLA helps verify these standards by using mechanisms such as ICMP echo requests (ping) to measure RTT and loss; this can be used to measure the effectiveness of QoS policies. Although IP SLA was part of older CCNA exams, it was removed in the current 200-301 version.

10.2.3 What QoS does
So, how does QoS help prioritize certain types of traffic in times of congestion, minimizing their delay, jitter, and loss? QoS consists of several different components that we will cover in the remaining sections of this chapter. Figure 10.7 gives a high-level overview of some of the key components that we will cover.



Figure 10.7 The QoS big picture. A router receives packets and makes a forwarding decision for each, classifies the packets based on their type, queues them for transmission, and uses scheduling methods to determine the order of transmission.

When packets arrive faster than the router can forward them out of a particular interface, it queues the packets waiting to be transmitted; this is when QoS is needed. By default, there is only a single queue, and packets are forwarded in a first in, first out (FIFO) manner, not prioritizing any packets over others. However, as shown in figure 10.7, QoS allows you to classify packets based on their type, queue them in separate queues, and use advanced scheduling methods such as Class-Based Weighted Fair Queuing (CBWFQ), Priority Queuing (PQ), and Low Latency Queuing (LLQ) to determine the order in which the packets are transmitted.

10.3 Classification and marking
Classification and marking are two components of QoS that are often confused. Classification is the process of sorting messages into different classes based on the kind of treatment you want to give them: high priority, low priority, etc. Marking is the process of setting the value of certain header fields to make the classification process simpler.

10.3.1 Classification
Classification is essential for QoS; to prioritize certain types of traffic, you have to identify those types of traffic—that is the role of classification. Figure 10.8 demonstrates classification: a device classifies packets into four different classes.



Figure 10.8 After making a forwarding decision, the device classifies each packet into a class: Real-Time (i.e., voice and video), Business Critical (important business apps), Default, and Scavenger traffic (low priority).

Note Scavenger traffic is low-priority, noncritical traffic that is left to “scavenge” for leftover bandwidth during network congestion. These packets are the first that should be dropped or delayed to prioritize more critical/delay-sensitive packets. For example, social media browsing would likely be classified as scavenger traffic.

Packets can be classified in a variety of ways. For example, ACLs can be used; packets permitted by one ACL are assigned to one class, and packets permitted by another ACL are assigned to another class. However, ACLs have their limitations—matching based on information in the Layer 3 and Layer 4 headers.

Sometimes, you have to look deeper to determine exactly what kind of packets are being sent. Network-Based Application Recognition (NBAR) makes this possible by performing a deep packet inspection, examining the actual contents of some of the packets in a particular exchange to accurately classify them.

10.3.2 Marking
Complex classification using ACLs/NBAR can be demanding on the device doing the classification and also complex to configure on every device in the network. Ideally, a packet should be classified with these methods early and then marked (using specific fields in the IP/Ethernet headers) to make the classification process simpler for the rest of the packet’s life. Figure 10.9 demonstrates this concept.



Figure 10.9 Complex classification and marking should be done early in a packet’s life. Subsequent devices can then simply classify it based on its marking.

Two fields have been specifically defined for QoS marking: the Differentiated Services Code Point (DSCP) field of the IPv4 and IPv6 headers and the Priority Code Point (PCP) field of the 802.1Q tag in the Ethernet header. After a packet has been marked, instead of examining the packet’s source/destination IP addresses and port numbers with ACLs, or examining the contents of the packet’s payload with NBAR, the device can simply look at the marking in the DSCP or PCP fields to make a classification decision. This reduces the burden on the device itself, and on the people who configure it.

Note The PCP field is also called Class of Service (CoS), which is commonly confused with QoS as a whole. However, CoS only refers to this specific field in the 802.1Q tag.

The three-bit PCP field can be used to mark 802.1Q-tagged Ethernet frames, allowing them to be easily classified based on the value in this field. For review, figure 10.10 shows the PCP field within the 802.1Q tag.



Figure 10.10 PCP is a three-bit field in the 802.1Q tag of the Ethernet header.

As a three-bit field, PCP provides eight possible values (23 = 8). For example, the standard PCP marking for voice traffic is 0b101 (0d5)—messages with this marking should be treated with high priority. On the other hand, the default value is 0b000 (0d0), meaning “best effort”—regular traffic that should not be given special treatment. For your reference, table 10.1 lists the eight PCP markings and their standard names; don’t worry about memorizing these for the exam.

Table 10.1 Standard PCP markings

| Decimal value | Traffic type          | Decimal value | Traffic type        |
|---------------|-----------------------|---------------|---------------------|
| 0             | Best effort (default) | 4             | Video               |
| 1             | Background            | 5             | Voice               |
| 2             | Excellent effort      | 6             | Internetwork control |
| 3             | Critical applications | 7             | Network control     |

The PCP field has one major limitation: it’s part of the 802.1Q tag, which is only present in frames traversing trunk links (or the voice VLAN of access links). Frames sent between two routers, for example, don’t include 802.1Q tags. Figure 10.11 demonstrates this concept.



Figure 10.11 The PCP field is in the 802.1Q tag and only present in tagged frames.

If a user is having a phone call on PH1, PH1 can send its packets in 802.1Q-tagged frames marked with a PCP value of 5; this allows SW1 and R1 to recognize them as high priority. However, the 802.1Q tag is only present until the packet reaches R1. When R1 forwards the packets to R2, it forwards them in untagged frames. For this reason, PCP’s utility is limited. Instead, most QoS policies make use of the DSCP field in the IP header.

10.3.3 Marking the DSCP field
Both IPv4 and IPv6 headers contain a 6-bit DSCP field. In the IPv4 header, it’s part of a byte called Differentiated Services (DiffServ). The DiffServ byte was formerly known as Type of Service (ToS). In the IPv6 header, this byte is called Traffic Class; its definition is the same as in IPv4: DSCP (6 bits) and ECN (2 bits). In the past, only 3 bits of this byte were used for QoS marking; this 3-bit field was called IP Precedence (IPP). Figure 10.12 compares the old and current definitions of the ToS/DiffServ byte.



Figure 10.12 The old and current definitions of the ToS/DiffServ byte. The old ToS byte defined the 3-bit IPP field for QoS marking. The current DiffServ byte defines the six-bit DSCP field for QoS marking.

Note The 2-bit Explicit Congestion Notification (ECN) field’s purpose is to notify the packet’s receiver of network congestion. However, its practical adoption has been somewhat limited, and it’s not part of the CCNA exam.

One major benefit of basing your QoS policies on DSCP markings, rather than PCP markings, is that DSCP markings stay with the packet end to end. Once a device marks a packet’s DSCP field, that marking will remain with the packet until it reaches its destination (unless another device modifies the marking).

As opposed to IPP and PCP, which are both 3 bits in size, DSCP is 6 bits, providing 64 (26) unique values. You are free to use these 64 values as you like in your QoS policies. For example, you could mark voice traffic with the highest value (63), scavenger traffic with the lowest value (0), and everything else with a value in between.

However, it would not be ideal for every network to use a totally different marking scheme; this would overcomplicate things and create challenges in maintaining consistent QoS policies when different networks connect with each other. To address this, standardized markings have been developed and are widely adopted in the industry. These standards provide a common “language” for QoS across various devices and vendors. Here are two examples of standard markings:

Default Forwarding (DF)—Default marking used for best-effort traffic

Expedited Forwarding (EF)—Used for delay/jitter/loss-sensitive traffic

DF uses a binary value of 000000 in the DSCP field (0 in decimal), and EF uses a binary value of 101110 in the DSCP field (46 in decimal). However, these are just two values; what about the other 62 values DSCP provides? There are two standardized sets of DSCP markings that you should know for the CCNA: Class Selector and Assured Forwarding.

Class Selector

Class Selector (CS) is a standardized set of DSCP markings created to be backward compatible with the older IPP system. Both IPP and CS use only the first three bits of the ToS/DiffServ byte, providing eight possible values. Figure 10.13 demonstrates how CS works. The three least-significant bits of the DSCP field are set to 0. Then, the three most significant bits—the same bits used by IPP—are used to create eight possible values.



Figure 10.13 The CS marking system. The most significant three bits are used to make eight possible values, and the three least significant bits are set to 0.

Figure 10.13 probably needs some explanation. In the middle, I show the DSCP field of the IP header. Above it, I show the decimal value of each bit. When looking at only the 3 bits used for CS, the decimal values are 1, 2, and 4. However, keep in mind that the DSCP field as a whole is still 6 bits; the decimal value of each of those 6 bits is written at the top (1, 2, 4, 8, 16, 32).

Finally, the figure compares the IPP and CS values, showing how they correspond to specific decimal values within the entire DSCP field. For example, an IPP value of 7 is equivalent to CS7 (0b111). This translates to a value of 56 (0b111000) when looking at the DSCP field as a whole.

The CS marking system is particularly useful when dealing with legacy systems or environments where older IPP values are still in use. Organizations that designed their QoS policies around IPP can simply translate those values to their equivalent CS values. In other words, CS was designed as a way to bridge the gap between the old IPP and the new DSCP (although you can’t really call DSCP “new” anymore—it was first defined in 1998).

Assured Forwarding

CS is useful for its backward compatibility with IPP, but it doesn’t take advantage of the greater number of possible values that DSCP offers. Assured Forwarding (AF) defines 12 additional standardized marking values: four traffic classes, with three levels of drop precedence within each class. A packet marked with a higher drop precedence is more likely to be dropped during congestion. Packets are assigned to one of four queues, and within each queue, some packets are more likely to be dropped than others during congestion.

AF uses the five most significant bits of the DSCP field; the least significant bit is set to 0. Furthermore, the 5 bits are divided into a class value (3 bits) and a drop precedence value (2 bits), written as AFXY (X = class, Y = drop precedence). Figure 10.14 demonstrates how AF uses the bits of the DSCP field.



Figure 10.14 The AF marking system. The five most significant bits are divided into the class (3 bits) and drop precedence (2 bits). The sixth bit is always 0.

Note Although 3 bits allow for eight different values (0–7), AF only defines four traffic classes (1–4). Likewise, 2 bits allow for four different values (0–3), but AF only defines three drop precedence levels (1–3).

Figure 10.15 demonstrates the 12 AF markings with their decimal DSCP values in brackets. One counterintuitive thing is that a higher value doesn’t necessarily mean better. For example, AF41 (decimal 34) and AF43 (decimal 38) are both in the highest-priority class, but AF41 has a lower drop precedence than AF43.



Figure 10.15 The 12 AF markings (decimal DSCP values are in brackets)

A simple shortcut to calculate the decimal DSCP value of a particular AF marking is to multiply the class value by 8 and the drop precedence value by 2 and then add them together. Let’s use AF42 as an example:

The class is 4: 4 × 8 = 32.

The drop precedence is 2: 2 × 2 = 4.

Add them together: 32 + 4 = 36.

Recommended markings

In this section about marking the DSCP field, we’ve covered DF, EF, CS, and AF. This has probably left you with questions about which marking system should be used and in which situations. You’re not alone in that; others had the same questions, which led to RFC 4594. RFC 4594 provides standardized marking recommendations for various kinds of traffic. Table 10.2 lists some of those recommendations.

Table 10.2 RFC 4594 recommended markings

| Class name           | DSCP name | DSCP value | Examples                          |
|----------------------|-----------|------------|-----------------------------------|
| Network Control      | CS6       | 48         | OSPF, EIGRP, BGP messages         |
| Telephony            | EF        | 46         | Voice call traffic                |
| Real-Time Interactive | AF4x     | 34, 36, 38 | Interactive gaming                |
| Multimedia Streaming | AF3x      | 26, 28, 30 | Streaming video/audio             |
| Low-Latency Data     | AF2x      | 18, 20, 22 | Client-server interactions        |
| Standard             | DF (CS0)  | 0          | Default (best effort)             |
| Low-Priority Data    | CS1       | 8          | Scavenger traffic, guest Wi-Fi    |


RFC 4594 includes several more recommendations than those shown in table 10.2. Depending on the needs of the network, differentiating between so many traffic types may be unnecessary. The RFC recommends thinking of them as a toolkit; some tools are necessary for some jobs but unnecessary for others.

Exam Tip I include table 10.2 to give you a picture of how these different markings can be combined in a holistic QoS policy that differentiates various kinds of traffic. However, I wouldn’t expect any CCNA exam questions about these recommended markings, their decimal DSCP values, etc. I recommend knowing DF’s role as the default best-effort marking, EF’s role in marking delay/jitter/loss-sensitive traffic, CS’s use for backward compatibility with IPP, and AF’s class/drop precedence system.

10.3.4 Trust boundaries
A trust boundary is a logical division in a network. Markings from devices on one side of the boundary are trusted to be accurate, and markings from devices on the other side are not trusted. If a device trusts a marking, the device will forward the packet without modifying the marking. However, if a device doesn’t trust a marking, the device will re-mark the packet according to the configured policy. Figure 10.16 demonstrates typical trust boundaries.



Figure 10.16 Typical trust boundaries. IP phones mark their packets, and it is standard practice to trust them. Markings from PCs should usually not be trusted.

IP phones mark their packets—usually EF for the packets that contain the actual audio data. To simplify things for the switch, it is standard practice to trust the phone’s markings. However, markings from PCs are a different story; a tech-savvy user (who is aware of QoS concepts) could configure their PC to mark its packets with EF as well, resulting in the PC’s traffic receiving preferential treatment over that of other PCs.

To protect against such a situation, you should ensure that PCs are on the “untrusted” side of the trust boundary; if a packet from a PC is marked, the IP phone or switch should re-mark it to the appropriate value (according to the configured policy).

10.4 Queuing and scheduling
In times of congestion, an interface may not be able to transmit packets fast enough to keep up with the rate at which packets are assigned to be transmitted out of the interface. What happens to the excess packets that cannot immediately be transmitted? The answer is queuing; the device will store the excess packets in one or more queues as they wait their turn to be transmitted.

Without QoS, each interface uses a single egress queue, and the device will transmit packets in the queue in a first in, first out (FIFO) manner—in the order that they enter the queue. This is called scheduling—the process of determining the order in which queued packets are actually transmitted. Figure 10.17 demonstrates FIFO.



Figure 10.17 Packet forwarding without QoS. G0/2 has a single egress queue, and packets are transmitted in a FIFO manner.

Note In this chapter, we are looking at queuing from the perspective of a single interface, but keep in mind that each interface has its own queues.

FIFO is fine for simple networks without a lot of traffic, but to prioritize particular kinds of traffic—the goal of QoS—a different technique is needed. In this section, we will examine three queuing and scheduling techniques: Priority Queuing (PQ), Class-Based Weighted Fair Queuing (CBWFQ), and Low Latency Queuing (LLQ).

Exam Tip Queuing is the process of storing packets in queues while they wait to be transmitted, and scheduling is the process of deciding in which order the queued packets will be transmitted. Remember this distinction!

10.4.1 Priority Queuing
Priority Queuing (PQ) supports up to four separate queues that are ranked by priority. Packets in a lower-priority queue will only be transmitted if the higher-priority queues are all empty. Figure 10.18 demonstrates PQ.



Figure 10.18 Priority Queuing (PQ). Packets are classified based on markings (the example markings in the figure are arbitrary) and added to a queue. The scheduler only services a lower-priority queue if all higher-priority queues are empty.

Note To service a queue is to transmit a packet (or packets) from that queue.

When the PQ scheduler decides which queue to service next, it scans the queues in order from highest to lowest priority. It makes this decision one packet at a time, scanning the queues in order each time. Depending on the amount of traffic in the higher-priority queues, this could mean that queue 4 is serviced very infrequently; this is called queue starvation. For that reason, PQ is rarely used anymore. It’s better than simple FIFO, but there are even better options available on modern devices.

10.4.2 Class-Based Weighted Fair Queuing
Class-Based Weighted Fair Queuing (CBWFQ) uses round-robin scheduling; it services each queue in cyclical order; for example, if there are four queues: 1, 2, 3, 4, 1, 2, 3, 4, 1, etc. However, simple round-robin scheduling treats all queues equally, which doesn’t fulfill the goal of prioritizing certain types of traffic.

Instead, CBWFQ uses weighted round-robin, which allows you to specify a guaranteed minimum amount of bandwidth for each queue. In times of congestion, the scheduler will ensure that each queue receives at least the specified amount of bandwidth. Figure 10.19 demonstrates CBWFQ.



Figure 10.19 Class-Based Weighted Fair Queuing (CBWFQ). Packets are classified and queued. The CBWFQ scheduler ensures that each queue receives at least its guaranteed bandwidth, even if other queues are congested.

Note CBWFQ supports up to 64 queues, although I’ll use 4 for the examples.

CBWFQ avoids the problem of queue starvation by guaranteeing a minimum amount of bandwidth to each queue. However, its round-robin scheduler is a problem for delay-sensitive traffic. Even if delay-sensitive traffic is given sufficient bandwidth, packets may have to wait to be transmitted as the scheduler services other queues. The next queuing/scheduling method we’ll cover addresses this concern.

10.4.3 Low Latency Queuing
Low Latency Queuing (LLQ) combines the strengths of PQ and CBWFQ; in fact, another name for it is PQCBWFQ (not a very elegant name—let’s stick with LLQ). To put it simply, LLQ is CBWFQ with a priority queue. Delay-sensitive traffic should be assigned to the priority queue; if packets are waiting in the priority queue, the scheduler will always service them first. If the priority queue is empty, the scheduler will serve the other queues using CBWFQ logic. Figure 10.20 demonstrates how LLQ works; you may recognize this from the QoS big picture in figure 10.7.



Figure 10.20 Low Latency Queuing (LLQ). Delay-sensitive packets are assigned to a priority queue that is always serviced first. The remaining queues are serviced using CBWFQ logic.

Notice that a bandwidth of 30% is applied to the priority queue at the top of figure 10.20. In the priority queue’s case, this isn’t the minimum guaranteed bandwidth—it’s the maximum. Because the priority queue is always serviced before other queues, there is a risk of queue starvation occurring if lots of packets are assigned to the priority queue.

By limiting the amount of traffic that is allowed to enter the priority queue (30% of the interface’s bandwidth in this example), you can avoid queue starvation. In figure 10.20’s example, EF-marked packets enter the priority queue. What happens if more than 30% of the bandwidth consists of EF-marked packets? In that case, the excess packets will either be dropped or re-marked and assigned to a lower queue; this is an example of policing, which we will cover in section 10.5.

10.5 Policing and shaping
Policing and shaping are two rate-limiting techniques—they limit the rate at which an interface sends or receives traffic. Both techniques work by defining a rate limit (e.g., 300 Mbps) and then taking action on traffic that exceeds the configured limit. Policing drops traffic that exceeds the rate limit. Shaping buffers traffic that exceeds the rate limit to smooth out the flow of data. Instead of dropping the packets, shaping queues them in a separate shaping queue and transmits them at a rate that conforms with the configured limit. Figure 10.21 demonstrates policing and shaping.



Figure 10.21 Policing and shaping. Policing drops traffic that exceeds the configured rate limit, and shaping buffers it to smooth out the traffic rate.

Note Traffic within the rate limit is considered conforming, and traffic that surpasses the rate limit is considered exceeding.

Instead of dropping packets that exceed the rate limit, policing also provides the option to re-mark them, causing the packets to be classified differently. We covered one example of this in the previous section: LLQ uses policing to limit the rate at which packets enter the priority queue. Excess packets are either dropped or re-marked and assigned to a different queue, depending on the configuration.

Policing and shaping can be configured on a per-class basis, so packets in each class (and, therefore, each queue) are policed/shaped separately. They can also be configured on a per-interface basis, applying to all packets transmitted or received by the interface. Figure 10.22 shows a common use case for shaping and policing.



Figure 10.22 A common use case for policing and shaping. The customer shapes outbound traffic to 300 Mbps to ensure that packets don’t get dropped by the ISP, which polices traffic to 300 Mbps.

An ISP’s customer has paid for a 300 Mbps connection, so the ISP router polices traffic received from the customer to a rate limit of 300 Mbps. Both routers are connected by GigabitEthernet interfaces, but because the ISP router polices incoming traffic, the customer router shouldn’t send packets out of G0/0 at full capacity; that would result in dropped packets. To ensure that packets don’t get dropped by the ISP’s router, the customer uses shaping to control the rate at which packets are sent to the ISP.

Note Policing and shaping can both be configured to allow for bursts—temporary spikes in traffic that exceed the configured rate limit.

10.6 Congestion avoidance
The QoS techniques we have covered so far are all designed to help devices in the network deal with congestion, minimizing its impact on types of traffic that are particularly sensitive to delay, jitter, and loss. However, interfaces’ queues aren’t infinite; if the congestion reaches a certain point and the queues start to overflow, packet loss is inevitable. Congestion avoidance techniques attempt to reduce the amount of congestion by taking advantage of TCP’s mechanics. In this section, we’ll examine the effects of too much congestion and then look at two congestion avoidance techniques that aim to remedy the situation.

10.6.1 Tail drop and TCP global synchronization
When a packet is assigned to enter a queue but can’t because the queue is full, the packet will be dropped; this is called tail drop. Figure 10.23 demonstrates tail drop. Two of the queues are full, resulting in tail drop.



Figure 10.23 Tail drop occurs when queues fill up and cannot contain more packets.

Packet loss on its own isn’t such a bad thing; protocols that use TCP as their Layer 4 protocol can recover from dropped messages using retransmissions. However, tail drop in particular can lead to (and result from) an undesirable phenomenon called TCP global synchronization. To understand TCP global synchronization, let’s review the TCP window size mechanism we covered in chapter 22 of volume 1.

In a TCP exchange between hosts, each host specifies a window size; in effect, this tells the other host how much data to send before waiting for an acknowledgment. This mechanism allows the receiver to control how quickly the sender sends data to ensure that the receiver isn’t overwhelmed.

The window size is not static. Each time the receiver receives data, it will specify a larger window size in the acknowledgment message it sends in reply. However, when a segment is lost (e.g., as a result of tail drop), the receiver will immediately reduce the window to a much smaller size. The receiver will then gradually increase the window size again, and the process will repeat. The purpose is to find the optimal transmission rate that doesn’t result in packet loss and to dynamically adapt to network congestion.

Global synchronization occurs when many hosts simultaneously reduce and then increase their window sizes in response to packet loss; this is often the result of tail drop. Although packet loss on its own doesn’t have such negative effects, the effect is greater when it happens to many hosts at once, leading to the vicious cycle shown in figure 10.24: TCP global synchronization.



Figure 10.24 The vicious cycle of TCP global synchronization

Network congestion leads to tail drop, which leads to a global TCP window size decrease; all hosts who experience packet loss will immediately reduce their window sizes. This leads to network underutilization; all hosts are using very small window sizes, leading to slow transmission rates. This leads to a global TCP window size increase, which again leads to network congestion, and the vicious cycle repeats; this isn’t an efficient use of network bandwidth.

10.6.2 Random Early Detection and Weighted Random Early Detection
Instead of waiting for queues to fill up, resulting in tail drop and TCP global synchronization, a better tactic is to start dropping some packets before tail drop happens. That way, instead of all receivers reducing their TCP window sizes simultaneously, only those few hosts that have experienced packet loss will. That’s what Random Early Detection (RED) and Weighted Random Early Detection (WRED) do.

RED drops a percentage of packets once a queue starts filling up beyond a certain point. Hosts that experience dropped packets will reduce their window sizes, and that will hopefully reduce the overall traffic rate and size of the queue. WRED functions in the same manner but allows for more control over which packets are dropped. For example, think back to the AF markings we covered in section 10.3.3. Some AF markings are designated as having a high drop precedence, and some are designated as having a low drop precedence; this is one situation in which those drop precedences can be implemented.

The main advantage of using RED and WRED over simple tail drop is that they provide a more proactive approach to managing congestion. By dropping some packets before a queue is full, RED and WRED aim to prevent the queue from becoming full in the first place and avoid TCP global synchronization.

Note RED and WRED should not be used for traffic types that are sensitive to packet loss; the LLQ priority queue is not a good place to implement RED/WRED.

Per-hop behavior

Exam topic 4.7 specifies the per-hop behavior (PHB) of QoS. PHB describes how each device handles QoS individually. All of the QoS concepts we have covered in this chapter, from classifying packets to scheduling them for transmission, apply on a per-device basis. In other words, just because one router is configured to prioritize EF-marked packets, it doesn’t automatically mean that the other devices in the network will. Each device needs to be explicitly configured to treat these markings according to your QoS policy; an EF marking (or any other marking) is meaningless unless you tell each device how to treat packets with that specific marking.

When implementing QoS, the policy must be consistently applied across all devices in the network path for it to be effective from end to end. The details of designing and implementing QoS policies, including how to configure QoS on Cisco devices, are beyond the scope of the CCNA exam. However, it’s important to understand the per-hop behavior of QoS.

Summary
Quality of Service (QoS) is a set of technologies that enable the prioritization and de-prioritization of certain types of traffic in times of network congestion.

QoS is often used to prioritize sensitive traffic like voice traffic from IP phones.

IP phones, also called Voice over IP (VoIP) phones, connect to Ethernet switches and communicate by sending and receiving IP packets.

IP phones have an internal three-port switch that allows the IP phone and a PC to share a single switch port.

Access ports can be configured with a voice VLAN to carry traffic in two VLANs: the data/access VLAN (untagged) and the voice VLAN (tagged).

Use switchport voice vlan vlan-id to configure an access port’s voice VLAN.

Power over Ethernet (PoE) is often used to power IP phones and other smaller devices over the same Ethernet cable they use for network communication.

A switch is the PoE Power Sourcing Equipment (PSE)—the device that supplies power using PoE—and the IP phones are Powered Devices (PDs).

To avoid damaging a connected device, the PSE waits to detect a PoE-enabled device, assess its power needs, and then supply electrical power to the PD.

Use show power inline to confirm the status of PDs, and power inline [auto | static [max milliwatts]] to control a port’s PoE settings.

Power policing can be used to error-disable a switch port if its connected device draws too much power. Use power inline police to enable it on a port, and show power inline police to check the status.

Bandwidth refers to a link’s capacity—how much data it can carry per second. Not all areas of the network have identical bandwidth; this can lead to bottlenecks.

The purpose of QoS is to minimize delay, jitter, and loss during network congestion.

Delay is the amount of time it takes a packet to travel from source to destination (one way), measured in milliseconds. Round-trip time (RTT) is two-way delay. Cisco recommends that delay should be 150 ms or less for voice traffic.

Jitter is the variation in delay in a series of packets. Cisco recommends that jitter should be 30 seconds or less for voice traffic.

Loss is the percentage of packets lost over a period of time. Cisco recommends that loss should be 1% or less for voice traffic.

When packets arrive faster than the router (or switch) can forward them out of a particular interface, it queues the packets that are waiting to be transmitted.

By default, there is only a single queue, and packets are forwarded in a first in, first out (FIFO) manner, not prioritizing any packets over others.

Classification is the process of sorting messages into different classes based on the kind of treatment you want to give them.

Packets can be classified in a variety of ways, for example, by using ACLs or Network-Based Application Recognition (NBAR), which performs a deep packet inspection on packets’ contents to accurately classify them.

Marking is the process of setting the value of certain header fields (802.1Q’s PCP/CoS, IP’s DSCP) to make classification simpler. Instead of using ACLs/NBAR, the device can simply look at the marking to determine a packet’s class.

The Priority Code Point (PCP) field, also called Class of Service (CoS), is a 3-bit field in the 802.1Q tag of an Ethernet frame used for QoS marking.

The downside of PCP is that it is only included in 802.1Q-tagged Ethernet frames. It does not stay with the packet for its entire life.

Previously, a 3-bit field in the IP header called IP Precedence (IPP) was used for QoS marking.

The modern IP header uses the 6-bit Differentiated Services Code Point (DSCP) field for QoS marking. As a 6-bit field, it provides 64 possible values (0–63).

Several marking schemes have been developed to standardize DSCP markings.

Default Forwarding (DF) uses a binary value of 000000 in the DSCP field (0d0). It is recommended for best-effort traffic—regular traffic that isn’t high priority.

Expedited Forwarding (EF) uses a binary value of 101110 in the DSCP field (0d46). It is recommended for delay/jitter/loss-sensitive traffic like voice traffic.

Class Selector (CS) is a standardized set of DSCP markings created to be backward compatible with the older IPP system.

In CS, the three least significant bits of the DSCP field are set to 0. The three most significant bits—the same bits used by IPP—are used for QoS marking.

Assured Forwarding (AF) defines twelve additional standardized marking values: four traffic classes, with three levels of drop precedence in each class.

AF uses the five most significant bits of the DSCP field, and the sixth is set to 0.

The 5 bits are divided into a class value (3 bits) and a drop precedence value (2 bits), written as AFXY (X = class, Y = drop precedence).

To calculate the decimal DSCP value of a particular AF marking, multiply the class value by 8 and the drop precedence by 2 (i.e., AF32 = 28).

RFC 4594 provides standardized marking recommendations for each traffic type.

A trust boundary is a logical division in a network. Markings from devices on one side of the line are trusted to be accurate, and markings from devices on the other side are not trusted.

If a device trusts a marking, it will forward the packet without modifying the marking. If a device doesn’t trust a marking, it will re-mark the packet itself.

Typically, markings from IP phones are trusted, but markings from PCs are not.

Queuing is the process of storing packets in queues while they wait to be transmitted, and scheduling is the process of deciding in which order the queued packets will be transmitted.

Priority Queuing (PQ) uses up to four queues. Packets in a lower-priority queue will only be transmitted if the higher-priority queues are all empty.

Although PQ is good for prioritizing certain traffic, lower-priority queues can suffer from queue starvation, in which they are serviced very infrequently.

Class-Based Weighted Fair Queuing (CBWFQ) uses weighted round-robin scheduling. It services each queue in cyclical order while guaranteeing each queue a minimum amount of bandwidth, even in times of congestion.

CBWFQ is not ideal for delay-sensitive traffic because packets may have to wait to be transmitted as the scheduler services other queues.

Low Latency Queuing (LLQ) combines CBWFQ with a priority queue. Packets in the priority queue are always serviced first. If the priority queue is empty, the scheduler will serve other queues using CBWFQ logic.

LLQ limits the rate at which packets can enter the priority queue to avoid queue starvation.

Policing and shaping are two rate-limiting techniques. Policing drops traffic that exceeds the rate limit, and shaping buffers excess traffic in a separate queue.

A service provider might police a customer’s traffic to provide only the bandwidth the customer paid for, and the customer might shape traffic to avoid exceeding it.

If a packet can’t enter a queue because it is full, tail drop occurs; it is dropped.

Tail drop can lead to TCP global synchronization, in which many hosts simultaneously reduce and then increase their transmission rates (window size) in response to packet loss.

TCP Global Synchronization is a vicious cycle: tail drop leads to a global TCP window size decrease, which leads to network underutilization, which leads to a global TCP window size increase, which leads to network congestion, which leads to tail drop.

Random Early Detection (RED) avoids tail drop by randomly dropping a percentage of packets after a queue fills up beyond a certain point.

Weighted Random Early Detection (WRED) is similar to RED but allows for more control over which packets are dropped.

RED and WRED should not be used for traffic types that are sensitive to packet loss.