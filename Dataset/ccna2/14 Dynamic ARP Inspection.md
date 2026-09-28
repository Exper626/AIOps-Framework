14 Dynamic ARP Inspection
This chapter covers

Address Resolution Protocol–based attacks such as ARP poisoning
How Dynamic ARP Inspection protects against ARP-based attacks
Configuring DAI on Cisco IOS switches
We first covered Address Resolution Protocol (ARP) in chapter 6 of volume 1, and it has come up several times throughout this book. ARP is an essential protocol in IP networks, serving as the bridge between Layer 2 and Layer 3 by mapping IP addresses to their corresponding MAC addresses. However, like many protocols, ARP is susceptible to exploitation that can compromise the security of a network. Dynamic ARP Inspection (DAI), the topic of this chapter, is a security feature on Cisco switches that we can use to mitigate such threats.

DAI is part of CCNA exam topic 5.7: Configure and verify Layer 2 security features. (These include DHCP Snooping, Dynamic ARP Inspection, and Port Security.) We have already covered Port Security and DHCP Snooping, so this is the final chapter addressing topic 5.7. As you read this chapter, I’m sure you’ll notice similarities between DAI and DHCP Snooping, both in functionality and Cisco IOS configuration. In fact, DAI relies on the DHCP Snooping binding table as one of its key components. Due to their similarities, this chapter will follow a structure similar to the previous one.

14.1 ARP and ARP-based attacks
Although we have covered ARP before, understanding DAI requires a deeper understanding of the contents of ARP messages. Figure 14.1 depicts a standard ARP exchange between two devices, showing some of the fields in each message. Notice that ARP messages include Sender MAC and Sender IP fields to indicate the MAC and IP addresses of the sender and Target MAC and Target IP fields to indicate the target’s addresses. The Target IP field of the ARP request is particularly important because it’s a broadcast message; a switch will flood the message to all hosts in the LAN, so this field is used to indicate the actual intended recipient of the message.



Figure 14.1 A standard ARP exchange. The important fields of each message are shown. The broadcast ARP request’s Target MAC is empty (0000.0000.0000) because PC1 doesn’t know R1’s MAC yet.

Note An ARP message is encapsulated directly in an Ethernet frame—it does not include an IP header. The sender and target IP fields are part of the ARP message itself, not part of an IP header.

In the ARP exchange, both hosts learn each other’s MAC address—that is ARP’s purpose, after all. Following the flow of figure 14.1, in step 1, PC1 broadcasts an ARP request. In step 2, R1 uses the information in the Sender MAC and Sender IP fields of PC1’s request to create an ARP table entry, mapping PC1’s IP address to its MAC address.

Then, in step 3, R1 sends a unicast ARP reply message to PC1. After receiving it, PC1 uses the information in the Sender MAC and Sender IP fields to create an entry for R1 in its own ARP table. The ARP process is complete, and both devices know each other’s MAC address.

ARP’s most significant vulnerability is how simple it is for an attacker to overwrite legitimate ARP table entries with “poisoned” entries—an ARP poisoning attack. Figure 14.2 reviews the process. After PC1 and R1 have learned each other’s MAC address, the attacker sends ARP replies to overwrite the legitimate entries with its own MAC address. As a result, PC1 and R1 will send frames to the attacker instead of each other, giving the attacker access to their communications; regarding the CIA triad, this affects the confidentiality of the communications.



Figure 14.2 An ARP poisoning attack. The attacker sends ARP replies to overwrite PC1 and R1’s ARP entries with the attacker’s own MAC address.

Note The ARP replies shown in figure 14.1 are gratuitous ARP (GARP) replies—ARP replies that were not prompted by ARP requests. We saw another example of GARP in chapter 19 of volume 1 when covering First Hop Redundancy Protocols.

14.2 Dynamic ARP Inspection
The security features we have covered so far (Port Security and DHCP Snooping) don’t protect against ARP poisoning attacks. ARP poisoning is performed from a single source MAC address, so limiting the number of MAC addresses on a port with Port Security doesn’t help. And DHCP Snooping only filters DHCP messages—not ARP messages.

However, DHCP Snooping does produce a table of hosts who have leased an IP address using DHCP, mapping their IP addresses to their MAC addresses: the DHCP Snooping binding table. DAI uses this table as part of its inspection process. Figure 14.3 shows only the DAI-specific configurations, but the output that follows shows both the DHCP Snooping and DAI configurations for reference.



Figure 14.3 Configuring DAI. Note that a port can be untrusted by one feature but trusted by the other, as in SW1’s G0/2 case.

SW2(config)# ip dhcp snooping
SW2(config)# ip dhcp snooping vlan 1
SW2(config)# ip arp inspection vlan 1
SW2(config)# no ip dhcp snooping information option
SW2(config)# interface g0/1
SW2(config-if)# ip dhcp snooping trust
SW2(config-if)# ip arp inspection trust
 
SW1(config)# ip dhcp snooping
SW1(config)# ip dhcp snooping vlan 1
SW1(config)# ip arp inspection vlan 1
SW1(config)# no ip dhcp snooping information option
SW1(config)# interface range g0/1-2
SW1(config-if-range)# ip arp inspection trust
SW1(config-if-range)# interface g0/1
SW1(config-if)# ip dhcp snooping trust
Note The rest of this chapter will focus on DAI configuration, not DHCP Snooping, but keep in mind that the two features work together. Although DAI can be used without DHCP Snooping, it is rare.

To enable DAI, use the ip arp inspection vlan vlans command in global config mode. As with the ip dhcp snooping vlan command, you can enable DAI on multiple VLANs with a single command. Here are a couple of examples:

All VLANs—ip arp inspection vlan 1-4094

VLANs 2, 3, 4, 5, 7, 9, and 2028—ip arp inspection vlan 2-5,7,9,2028

Note Enabling DHCP Snooping requires two commands: ip dhcp snooping and ip dhcp snooping vlan, but DAI only requires one: ip arp inspection vlan.

In the following example, I enable DAI on SW2 and confirm with show ip arp inspection:

SW2(config)# ip arp inspection vlan 1                                ❶
SW2(config)# do show ip arp inspection
. . .
 Vlan     Configuration    Operation   ACL Match          Static ACL
 ----     -------------    ---------   ---------          ----------
    1     Enabled          Active                                    ❷
. . .
❶ Enables DAI on VLAN 1

❷ DAI is enabled and active on VLAN 1.

Note A VLAN might appear as Enabled but Inactive if you enable DAI for the VLAN but the VLAN itself is disabled (i.e., with the shutdown command).

14.2.1 How DAI filters ARP messages
A switch using DAI inspects and filters ARP messages it receives. Much like DHCP Snooping, DAI operates using the concept of trusted and untrusted ports. On a DAI-enabled switch, all ARP messages received on trusted ports are permitted, while ARP messages received on untrusted ports are inspected to determine whether they should be forwarded or discarded. In this section, we’ll examine how trusted/untrusted ports work in DAI and then how a DAI-enabled switch uses the DHCP Snooping binding table to filter ARP messages.

Note DAI only filters ARP messages. Non-ARP messages are not affected.

DAI trusted and untrusted ports

When DAI is enabled, all ports are untrusted by default; this means that DAI will inspect ARP messages received on all ports. Figure 14.4 shows which ports should be trusted in our example network.



Figure 14.4 Configuring DAI trusted ports. Ports connected to network infrastructure devices (switches, routers) should be trusted, and ports connected to end-user devices like PCs should remain untrusted.

Note Figure 14.4 shows both of SW1’s ports as trusted, meaning it will allow all ARP messages—DAI won’t filter them. Despite this, enabling DAI is still a valuable security measure. It ensures that any other ports connected to end hosts in the future will be protected against ARP-based attacks from the start.

When configuring DAI, ports connected to end hosts should remain in the default untrusted state. In figure 14.4, PC2’s spoofed ARP reply is discarded by DAI because it is received on an untrusted port.

Ports connected to network infrastructure devices, such as routers and other switches, should be trusted. These guidelines are slightly different from those for DHCP Snooping, leading to SW1 G0/2 being untrusted by DHCP Snooping but trusted by DAI. We’ll look at the rationale behind this discrepancy in the next section when we look at how DAI inspects and filters ARP messages.

Note The guidelines for DHCP Snooping are to make ports that lead toward the DHCP server trusted, and leave ports that lead toward end hosts in the untrusted state (default).

To make a port trusted, use the ip arp inspection trust command in interface config mode. In the following example, I configure SW2 G0/1 as a trusted port and verify with show ip arp inspection interfaces:

SW2(config)# interface g0/1                                    ❶
SW2(config-if)# ip arp inspection trust                        ❶
SW2(config-if)# do show ip arp inspection interfaces
 Interface        Trust State     Rate (pps)    Burst Interval
 ---------------  -----------     ----------    --------------
 Gi0/1            Trusted               None               N/A ❷
 Gi0/2            Untrusted               15                 1 ❸
 Gi0/3            Untrusted               15                 1 ❸
. . .
❶ Trusts SW2 G0/1

❷ G0/1 is trusted.

❸ G0/2 and G0/3 remain untrusted.

As with DHCP Snooping, trusting the correct ports is critical. Trusting ports that should remain untrusted exposes the network to potential threats (like ARP poisoning). On the other hand, failing to trust ports that should be trusted can disrupt network communications by blocking valid ARP requests. To understand why, let’s look at exactly how DAI inspects and filters messages.

Inspecting ARP messages

A DAI-enabled switch inspects ARP messages as they are received on untrusted ports; this includes both ARP requests and ARP replies. It then makes a filtering decision: should I forward or discard this message? It does this by examining the Sender MAC and Sender IP fields of the ARP message and comparing them to the DHCP Snooping binding table:

If there is a matching entry, the message is forwarded.

Without a matching entry, the message is discarded.

The following example shows SW2’s DHCP Snooping binding table with entries for PC1 and PC2:

SW2# show ip dhcp snooping binding 
MacAddress         IpAddress Lease(sec) Type           VLAN Interface
-----------------  --------- ---------- -------------  ---- ----------
52:54:00:08:D3:E0  10.0.0.6  84617      dhcp-snooping  1    Gi0/2      ❶
52:54:00:02:F4:E1  10.0.0.7  84623      dhcp-snooping  1    Gi0/3      ❷
Total number of bindings: 2
❶ PC1’s entry

❷ PC2’s entry

Note MAC addresses in the DHCP Snooping binding table are formatted differently from how Cisco normally formats them (XX:XX:XX:XX:XX:XX vs. xxxx.xxxx.xxxx).

Given this table, SW2’s untrusted ports will only accept ARP messages with

Sender MAC 5254.0008.d3e0 and Sender IP 10.0.0.6

Sender MAC 5254.0002.f4e1 and Sender IP 10.0.0.7

Figure 14.5 shows DAI in action. SW2 inspects and filters ARP messages, discarding any suspicious messages, like PC2’s message with a spoofed IP address.



Figure 14.5 A DAI-enabled switch inspects and filters ARP messages. PC2’s message with a spoofed IP address is discarded.

SW1’s DHCP Snooping binding table has the same entries as SW2’s. This is because SW1 also inspected PC1 and PC2’s DHCP exchanges with R1. Here’s SW1’s table:

SW1# show ip dhcp snooping binding 
MacAddress         IpAddress Lease(sec) Type           VLAN Interface
-----------------  --------- ---------- -------------  ---- ---------
52:54:00:08:D3:E0   10.0.0.6 68613      dhcp-snooping  1    Gi0/2    ❶
52:54:00:02:F4:E1   10.0.0.7 68613      dhcp-snooping  1    Gi0/2    ❷
Total number of bindings: 2
❶ PC1’s entry

❷ PC2’s entry

With this table, let’s consider why SW1’s G0/2 port should be trusted by DAI (despite being untrusted by DHCP Snooping). Figure 14.6 shows what happens if SW1 G0/2 is untrusted by DAI.



Figure 14.6 SW1 blocks SW2’s ARP request because there is no matching entry in SW2’s DHCP Snooping binding table.

For remote management via SSH, SW2 uses R1 (10.0.0.1) as its default gateway and has an IP address on its VLAN 1 SVI (10.0.0.3). SW2 sends an ARP request to learn the MAC address of R1, but SW1 blocks it—SW1 doesn’t have a matching entry in its DHCP Snooping binding table! The following output is a Syslog message displayed on SW1, indicating that an invalid ARP request was received:

%SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Req) on Gi0/2, vlan 1.
([5254.000c.8001/10.0.0.3/0000.0000.0000/10.0.0.1/05:16:13 UTC Wed Oct 
18 2023])
The first two values in square brackets (5254.000c.8001/10.0.0.3) are the Sender MAC and Sender IP of SW2’s ARP request. Because SW2’s VLAN 1 SVI has a manually configured IP address, SW1 had no opportunity to create a DHCP Snooping binding table entry for it. The same problem would occur for any device with a manually configured IP address; ports connected to such devices should be trusted.

ARP ACLs

In addition to the DHCP Snooping binding table, there is a second source that a DAI-enabled switch can check when deciding to forward or discard an ARP message: ARP ACLs. ARP ACLs can be used to manually configure IP-MAC mappings for devices that don’t use DHCP, allowing their ARP messages to pass through untrusted ports without being discarded by DAI. For your reference, the following example shows how to create and apply an ARP ACL to permit SW2’s VLAN 1 SVI:

SW2(config)# arp access-list ARP-ACL-1
SW2(config-arp-nacl)# permit ip host 10.0.0.3 mac host 5254.000c.8001
SW2(config-arp-nacl)# exit
SW2(config)# ip arp inspection filter ARP-ACL-1 vlan 1
ARP ACLs are beyond the scope of the CCNA exam, so this chapter focuses on DAI using the DHCP Snooping binding table. Even though ARP ACLs are an option, the general recommendation is still to trust ports connected to infrastructure devices.

14.2.2 Optional DAI checks
By default, DAI checks that an ARP message’s Sender MAC and Sender IP fields have a matching entry in the DHCP Snooping binding table (or ARP ACLs). However, an attacker can easily spoof these addresses. To prevent various kinds of spoofing attacks, you can enable additional checks with the ip arp inspection validate command. There are three keywords that can be used at the end of this command:

src-mac—The switch verifies that the Ethernet Source MAC and the ARP Sender MAC of requests and responses match. If they don’t match, the message is dropped.

dst-mac—The switch verifies that the Ethernet Destination MAC and the ARP Target MAC of ARP responses match. If they don’t match, the message is dropped.

ip—The switch will check for invalid/unexpected IP addresses in the ARP Sender IP or Target IP, such as 0.0.0.0 or 255.255.255.255. These should normally not appear in ARP messages, so their presence would indicate some kind of spoofing.

By default, all of these optional checks are disabled, but you can choose to enable one, two, or all three of them. In the following example, I enable all three on SW2:

SW2(config)# ip arp inspection validate src-mac dst-mac ip ❶
SW2(config)# do show ip arp inspection
Source Mac Validation      : Enabled                       ❷
Destination Mac Validation : Enabled                       ❷
IP Address Validation      : Enabled                       ❷
. . .
❶ Enables source MAC, destination MAC, and IP address validation

❷ All three optional checks are enabled.

Figure 14.7 visualizes these optional checks, as well as the mandatory check for a matching entry in the DHCP Snooping binding table.

Note One potential concern when enabling these additional checks is that they increase the load on the switch’s CPU. While this is generally not a concern with modern hardware, it’s a good practice to monitor CPU usage, especially in older or resource-constrained environments. Use the show processes cpu command to check the CPU load.



Figure 14.7 The mandatory and optional checks that DAI performs when inspecting ARP messages

14.2.3 Rate-limiting ARP messages
Like DHCP Snooping, DAI can be demanding on a switch’s CPU. A switch is very efficient at forwarding frames without taxing its CPU. However, when it has to stop and inspect an ARP message with DAI, the CPU gets involved. This means that an attacker can potentially overwhelm the switch with ARP messages, resulting in a denial of service.

To mitigate against such threats, DAI can limit the rate at which a port can receive ARP messages. Whereas DHCP Snooping rate limiting is disabled on all ports by default, DAI has the default rate-limiting settings:

Untrusted ports:—Rate limit of 15 packets per second (pps)

Trusted ports—No rate limit

You might have noticed these settings in the output of show ip arp inspection interfaces that we looked at earlier. Here it is again:

SW2# show ip arp inspection interfaces
 Interface        Trust State     Rate (pps)    Burst Interval
 ---------------  -----------     ----------    --------------
 Gi0/1            Trusted               None               N/A   ❶
 Gi0/2            Untrusted               15                 1   ❷
 Gi0/3            Untrusted               15                 1   ❷
. . .
❶ G0/1, a trusted port, has no rate limit.

❷ G0/2 and G0/3, untrusted ports, have a rate limit of 15 pps.

You can modify the rate limit on a per-port basis with ip arp inspection limit rate rate [burst interval seconds]. Specifying the burst interval is optional—the default is 1—but it lets you specify over how many seconds the packet rate is measured. Here are a couple of example commands to demonstrate:

ip arp inspection limit rate 20—Twenty packets per second (equivalent to burst interval 1).

ip arp inspection limit rate 40 burst interval 2—Forty packets every 2 seconds

Twenty packets per second and 40 packets every 2 seconds are the same average rate, but the latter allows for larger bursts of traffic (as long as the average rate doesn’t surpass 40 packets every 2 seconds). Can you guess what happens if the rate limit is exceeded? If you remember the previous chapter on DHCP Snooping, you probably know: the switch will error-disable the port. To demonstrate, in the following example, I set SW1 G0/2’s rate limit to 1 pps:

SW1(config)# interface g0/2                                ❶
SW1(config-if)# ip arp inspection limit rate 1             ❶
%SW_DAI-4-PACKET_RATE_EXCEEDED: 2 packets received in      ❷
➥559 milliseconds on Gi0/2.                                ❷
%PM-4-ERR_DISABLE: arp-inspection error detected on Gi0/2, ❸
➥putting Gi0/2 in err-disable state                        ❸
❶ Configures a DAI rate limit of 1 pps on G0/2

❷ The rate limit is exceeded.

❸ SW2 error-disables the port.

As with all error-disabled ports, those disabled by DAI can be reenabled in two ways: manually or automatically:

Manual—Issue shutdown and no shutdown on the error-disabled port.

Automatic—Enable ErrDisable Recovery for ports disabled by DAI rate limiting with errdisable recovery cause arp-inspection.

Because DAI rate limiting is enabled on untrusted ports by default, you probably won’t have to make any changes. Fifteen packets per second is more than enough for most end hosts but low enough to prevent DoS attacks from trying to overwhelm the switch’s CPU.

Exam Tip You should understand how DAI rate limiting works and how to configure it, but identifying an appropriate rate limit is beyond the scope of the CCNA exam.

Summary
Dynamic ARP Inspection (DAI) is a security feature on Cisco switches that protects against ARP-based attacks by inspecting and filtering ARP messages.

ARP messages include Sender MAC and Sender IP fields to indicate the MAC and IP addresses of the sender, and Target MAC and Target IP fields to indicate the target’s (destination’s) addresses.

ARP’s most significant vulnerability is how simple it is for an attacker to overwrite legitimate ARP table entries by sending gratuitous ARP messages—ARP poisoning.

By telling devices in the LAN to send their frames to the attacker, the attacker gains access to their communications.

Port Security doesn’t protect against ARP poisoning because ARP poisoning is performed from a single source MAC address. DHCP Snooping doesn’t protect against ARP poisoning because it only filters DHCP messages.

DHCP Snooping produces a table of hosts who have leased an IP address using DHCP, mapping their IP addresses to their MAC addresses: the DHCP Snooping binding table.

DAI uses the DHCP Snooping binding table in its inspection and filtering process.

Use ip arp inspection vlan vlans in global config mode to enable DAI.

Use show ip arp inspection to view general information about DAI on the switch.

DAI uses the concepts of trusted and untrusted ports. All ARP messages received on trusted ports are permitted, while ARP messages received on untrusted ports are inspected to determine whether they should be forwarded or discarded.

All ports on a DAI-enabled switch are untrusted by default. Ports connected to end hosts should remain untrusted. Ports connected to network infrastructure devices, such as routers and other switches, should be trusted.

Use ip arp inspection trust in interface config mode to trust a port.

Use show ip arp inspection interfaces to view the DAI trust state and rate limit of each port.

DAI inspects ARP messages received on untrusted ports by examining the Sender MAC and Sender IP fields and looking for a matching entry in the DHCP Snooping binding table.

If there is a matching entry, the message is forwarded. Without a matching entry, the message is discarded.

If a device has a manually configured IP address (not learned via DHCP), the device won’t have a matching entry in switches’ DHCP Snooping binding tables, leading to the device’s ARP messages being discarded if received on an untrusted port.

For this reason, ports connected to devices with manually configured IP addresses should be trusted.

In addition to the DHCP Snooping binding table, you can use ARP ACLs to manually configure IP–MAC mappings for devices that don’t use DHCP, allowing their ARP messages to pass through untrusted ports without being discarded by DAI.

In addition to checking an ARP message’s Sender MAC and Sender IP fields for a matching entry in the DHCP Snooping binding table, DAI can optionally check other parameters. You can configure it with the ip arp inspection validate command.

The three keywords that can be used with ip arp inspection validate are

src-mac—Checks that the Ethernet Source MAC and ARP Sender MAC of ARP requests and responses match

dst-mac—Checks that the Ethernet Destination MAC and ARP Target MAC of ARP responses match

ip—Ensures that invalid/unexpected IP addresses (i.e., 0.0.0.0 or 255.255.255.255) are not present in the ARP Sender IP or Target IP fields

The three optional checks are all disabled by default, but you can enable one, two, or all three of them.

DAI inspection can be demanding on a switch’s CPU. This means that an attacker can potentially overwhelm the switch with ARP messages, resulting in a denial of service.

To mitigate against such threats, DAI can limit the rate at which a port can receive ARP messages.

By default, untrusted ports have a rate limit of 15 packets per second, and trusted ports have no rate limit.

Use ip arp inspection limit rate rate [burst interval seconds] to modify the rate limit on a per-port basis.

The optional burst interval lets you specify over how many seconds the packet rate is measured (i.e., 40 packets every 2 seconds).

If a port’s rate limit is exceeded, the switch will error-disable the port.

You can reenable a port disabled by DAI rate limiting in two ways:

Manual—Issue shutdown and no shutdown on the error-disabled port.

Automatic—Enable ErrDisable Recovery for ports disabled by DAI rate limiting with errdisable recovery cause arp-inspection.