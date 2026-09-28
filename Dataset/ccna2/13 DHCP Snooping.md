13 DHCP Snooping
This chapter covers

DHCP-based attacks such as DHCP poisoning
How DHCP Snooping protects against DHCP-based attacks
Configuring DHCP Snooping on Cisco IOS switches
DHCP is almost ubiquitous in modern networks, allowing for the automatic configuration of IP addresses, netmasks, default gateways, DNS servers, and other configuration information on hosts; we covered DHCP in chapter 4. However, DHCP contains vulnerabilities that can be exploited if sufficient care is not taken. We looked at one example in chapter 11: DHCP exhaustion, which is a type of DoS attack that prevents legitimate user devices from leasing IP addresses from a DHCP server.

In this chapter, we’ll cover DHCP Snooping, a security feature on Cisco switches that protects against DHCP-based attacks by inspecting DHCP messages as they are received by the switch. DHCP Snooping is part of CCNA exam topic 5.7: Configure and verify Layer 2 security features (DHCP Snooping, Dynamic ARP Inspection, and Port Security).

13.1 DHCP-based attacks
Although DHCP is an essential part of modern networks, attackers can exploit it to harm the confidentiality, integrity, and availability of a network. We have already covered DHCP exhaustion attacks and how Port Security can be used to mitigate against them. In this section, we’ll look at how DHCP can be exploited to perform a man-in-the-middle attack: DHCP poisoning.

In a DHCP poisoning attack, the attacker configures a rogue DHCP server (sometimes called a spurious DHCP server) to lease IP addresses to clients. The rogue server leases valid IP addresses, but the point of the attack is to tell the clients to use the rogue server as their default gateway—not the LAN’s legitimate router. This allows the rogue server to intercept clients’ communications, gaining access to (and possibly altering) their contents before relaying them to the router. Figure 13.1 demonstrates a DHCP poisoning attack.



Figure 13.1 A DHCP poisoning attack. The rogue DHCP server replies to PC1’s DHCP messages, assigning it an IP address and telling it to use the rogue server as its default gateway. The rogue server then intercepts PC1’s communications.

Note DHCP poisoning may remind you of a similarly named attack that we covered in chapter 11: ARP poisoning. Both attacks allow the attacker’s device to act as a man-in-the-middle, secretly intercepting targets’ communications.

DHCP clients tend to accept the first OFFER message they receive in response to their DISCOVER, so the rogue server’s goal is to respond before any legitimate DHCP servers. If both the rogue and legitimate DHCP servers are in the same LAN, it’s a race to reply first. But if the legitimate DHCP server is in a different LAN, introducing additional delay between the client and the server, the rogue server’s “poisoned” OFFER has a good chance of reaching the client first due to its lower latency.

Port Security, which we covered in chapter 12, doesn’t mitigate against DHCP poisoning attacks. The rogue server sends DHCP messages from a single MAC address, so limiting the number of MAC addresses on the port doesn’t help. To defend your network against DHCP poisoning attacks, you should use DHCP Snooping.

13.2 DHCP Snooping
DHCP Snooping works by examining and filtering DHCP messages received by the switch. That’s an important point: DHCP only filters DHCP messages—non-DHCP messages are unaffected by DHCP Snooping. Let’s look at how DHCP Snooping works and how to configure it on Cisco switches. Figure 13.2 shows the network we’ll configure.



Figure 13.2 Configuring DHCP Snooping on Cisco switches. Ports leading toward the DHCP Server are trusted, and ports leading toward users are untrusted. Only SW1’s configurations are shown, but the same commands should be configured on SW2.

The first step in configuring DHCP Snooping is to enable the feature; it is disabled by default. Doing so requires two separate commands:

Enable DHCP Snooping—ip dhcp snooping

Activate DHCP Snooping on each VLAN—ip dhcp snooping vlan vlans

ip dhcp snooping enables DHCP Snooping, but it won’t actually take effect until you use the second command (ip dhcp snooping vlan vlans) to activate it on each VLAN in the LAN. To keep things simple, the example network we will use in this chapter has a single VLAN (VLAN 1), but in a LAN with multiple VLANs, you should enable it on each VLAN that has hosts using DHCP. You can activate DHCP Snooping on multiple VLANs with a single command by using commas and hyphens in the vlans argument—for example:

All VLANs—ip dhcp snooping vlan 1-4094

VLANs 1, 3, 4, 5, 7, 9, 10, and 11—ip dhcp snooping vlan 1,3-5,7,9-11

In the following example, I configure DHCP Snooping on SW2 and verify with show ip dhcp snooping (I issued the same commands on SW1 too):

SW2(config)# ip dhcp snooping                       ❶
SW2(config)# ip dhcp snooping vlan 1                ❷
SW2(config)# do show ip dhcp snooping
Switch DHCP snooping is enabled                     ❸
. . .
DHCP snooping is configured on following VLANs:     ❹
1                                                   ❹
DHCP snooping is operational on following VLANs:    ❺
1                                                   ❺
. . .
❶ Enables DHCP Snooping

❷ Activates DHCP Snooping on VLAN 1

❸ DHCP Snooping is enabled.

❹ DHCP Snooping is configured on VLAN 1.

❺ DHCP Snooping is operational on VLAN 1.

Note A VLAN might appear as configured, but not operational, if you enable DHCP Snooping for the VLAN but the VLAN itself is disabled on the switch.

13.2.1 How DHCP Snooping filters DHCP messages
DHCP Snooping works by filtering DHCP messages. However, it doesn’t filter DHCP messages received on all ports; it only filters those received on untrusted ports. Messages received on trusted ports are not filtered. In this section, we’ll review the different DHCP message types that we covered in chapter 4 (and look at some new ones) and then examine the concepts of trusted/untrusted ports and how DHCP Snooping filters messages.

DHCP message types

You should already be familiar with the messages in the DHCP DORA exchange: DISCOVER, OFFER, REQUEST, ACK. However, there are some other DHCP message types that you should know (although not to the same level of detail as DORA). Figure 13.3 lists some of the different DHCP message types.



Figure 13.3 DHCP message types. Client messages include DISCOVER, REQUEST, DECLINE, and RELEASE. Server messages include OFFER, ACK, and NAK.

When DHCP Snooping filters DHCP messages, it differentiates between messages sent by DHCP clients and those sent by DHCP servers. Messages sent by DHCP clients include DISCOVER, REQUEST, DECLINE, and RELEASE. Messages sent by DHCP servers include OFFER, ACK, and NAK. Here’s a quick description of each message type we haven’t covered yet:

DECLINE—Used to tell the server that the leased IP address is already in use

RELEASE—Used to tell the server that the client no longer needs its IP address

NAK (negative ACK) —The opposite of ACK; used to decline a client’s REQUEST

Exam Tip You don’t have to know the details of these additional message types, but you should know which are sent by clients and which are sent by servers. Other DHCP message types exist, but I wouldn’t expect to see them on the CCNA exam.

DHCP Snooping trusted and untrusted ports

The concept of trusted and untrusted ports is fundamental to how DHCP Snooping works. DHCP Snooping filters DHCP messages received on untrusted ports based on a set of rules, and all ports are untrusted by default. All DHCP messages received on trusted ports, however, are allowed. You need to manually specify each trusted port with ip dhcp snooping trust. Figure 13.4 demonstrates trusted and untrusted ports.



Figure 13.4 DHCP Snooping trusted ports lead toward the DHCP server. Untrusted ports lead away from the DHCP server and block server messages like OFFER.

Ports that lead toward the DHCP server (the G0/1 ports of SW1 and SW2 in figure 13.4) should be trusted. DHCP Snooping forwards DHCP messages received on those ports without any further inspection.

Ports that lead away from the DHCP server—toward end hosts—should remain in the default untrusted state. When a DHCP message is received on an untrusted port, the switch will inspect it and act as follows:

If it is a DHCP server message (OFFER, ACK, or NAK), discard it.

This is why PC2’s OFFER is discarded in figure 13.4.

If it is a DHCP client message (DISCOVER, REQUEST, DECLINE, or RELEASE), inspect it further to determine if it is legitimate.

If a client successfully leases an IP address, create a new entry in the DHCP Snooping binding table—more on that later in this section.

Note Because all ports are untrusted by default, if you don’t configure any trusted ports, DHCP won’t work; all messages from DHCP servers will be discarded.

In the following example, I configure SW2 G0/1 as a trusted port and confirm by looking at some more output of show ip dhcp snooping:

SW2(config)# interface g0/1                                            ❶
SW2(config-if)# ip dhcp snooping trust                                 ❶
SW2(config-if)# do show ip dhcp snooping
. . .
DHCP snooping trust/rate is configured on the following Interfaces:
Interface                  Trusted    Allow option    Rate limit (pps)
-----------------------    -------    ------------    ----------------   
GigabitEthernet0/1         yes        yes             unlimited        ❷
❶ Configures G0/1 as a trusted port

❷ The Trusted column states yes.

Inspecting client messages

Untrusted ports only accept DHCP client messages. However, they don’t blindly accept all client messages; they perform additional checks to verify that the message is valid before accepting it. The checks that the switch performs depend on the message type:

Messages involved in the DORA process—DISCOVER and REQUEST. Check that the Ethernet source MAC address and DHCP chaddr match.

Messages sent after the client has leased an IP—RELEASE and DECLINE. Verify the message using the DHCP Snooping binding table.

For the first category, DISCOVER and REQUEST messages, the switch compares two fields: the source MAC address field of the Ethernet header and the chaddr (client hardware address) field of the DHCP message (which indicates the client’s MAC address). If the addresses in the two fields match, the switch permits the message. If the two addresses don’t match, the switch discards the message.

The purpose of the chaddr field

The chaddr field (written in lowercase to align with RFC 2131, which defines DHCP) represents the client’s hardware address, typically a MAC address in modern networks (where Ethernet dominates). You might wonder, why have this field when the client’s MAC address is already present in the Ethernet frame’s source MAC address field?

There are multiple reasons, but a primary one is to support situations where the DHCP client and server are in separate LANs (and a DHCP relay agent is used). In such situations, by the time the client’s DHCP message reaches the server, the source MAC address of the Ethernet frame won’t be the client’s MAC address. Instead, it will be the MAC address of the last router that forwarded the message to the server. The chaddr field ensures that the client’s MAC address is still conveyed to the server in such scenarios.

These two fields should match when the client’s message reaches the switch; they should only differ if the message is forwarded by a DHCP relay agent. However, an attacker might repeatedly send spoofed DHCP DISCOVER messages from a single source MAC address (to bypass Port Security’s MAC address limit), each with a unique address in the chaddr field to perform a DHCP exhaustion attack. Verifying that these fields match protects against such an attack, as shown in figure 13.5.



Figure 13.5 DHCP Snooping prevents a DHCP starvation attack by verifying that the source MAC address and chaddr of the attacker’s messages match.

The second category of DHCP client messages, RELEASE and DECLINE, are sent after the client has leased an IP address. DECLINE is used if after receiving the final ACK from the server, the client detects that the IP address is already in use by another device. RELEASE is used any time the client decides it no longer needs its leased IP address—for example, if it disconnects from the network.

However, these messages can be exploited by an attacker. For example, the attacker could send a RELEASE message to tell the server to release a particular client’s IP address, and then the attacker could attempt to lease that address for itself. To verify that RELEASE and DECLINE messages are legitimate, the switch will verify the message by checking the DHCP Snooping binding table, which we’ll cover next.

The DHCP Snooping binding table

As a DHCP Snooping-enabled switch observes DHCP exchanges between clients and servers, it builds a table of the clients that have successfully leased an IP address; that table is called the DHCP Snooping binding table, and you can view it with show ip dhcp snooping binding. The following example shows the DHCP Snooping binding table:

SW2# show ip dhcp snooping binding
MacAddress          IpAddress    Lease(sec)  Type           VLAN  Interface
------------------  -----------  ----------  -------------  ----  ---------
52:54:00:08:D3:E0   10.0.0.6     84617       dhcp-snooping   1    Gi0/2
52:54:00:02:F4:E1   10.0.0.7     84623       dhcp-snooping   1    Gi0/3
Total number of bindings: 2
The DHCP Snooping binding table includes information like the client’s MAC address, the leased IP address and duration of the lease, the VLAN, and the interface (or port—the terms are interchangeable) the client is connected to. When inspecting a RELEASE or DECLINE message received on an untrusted port, the switch ensures that the IP address of the message and the port it was received on match the entry in the binding table.

Note The DHCP Snooping binding table isn’t only used for verifying DHCP messages. It also plays a key role in Dynamic ARP Inspection (DAI), the topic of chapter 14.

13.2.2 DHCP option 82
If you’re following along in a lab as you read this chapter and have correctly enabled DHCP Snooping, activated it on the necessary VLANs, and trusted the appropriate ports, you might be confused as to why hosts are unable to lease IP addresses via DHCP and why your switches have empty DHCP Snooping binding tables. The following output of show ip dhcp snooping shows why:

SW2# show ip dhcp snooping
. . .
Insertion of option 82 is enabled            ❶
   circuit-id default format: vlan-mod-port
   remote-id: 5254.000c.8b85 (MAC)
Option 82 on untrusted port is not allowed   ❷
. . .
❶ Switches insert option 82 into DHCP requests by default.

❷ Switches do not accept messages with option 82 on untrusted ports.

DHCP defines various optional fields, called options, that can be included in its messages. One of those is the DHCP relay agent information option, usually called by its number, option 82. A DHCP relay agent can insert this option when forwarding DHCP client messages to a remote DHCP server, providing additional information to the server that can inform the IP allocation decision. The details of option 82 are beyond the scope of the CCNA exam, but option 82 is relevant to DHCP Snooping because of some default settings on Cisco routers and switches related to option 82.

Figure 13.6 demonstrates what happens when PC1 sends a DHCP DISCOVER message. SW2 adds option 82 to the message and forwards it to SW1. SW1, receiving a message with option 82 on an untrusted port, discards the message. If you check the CLI of SW1, it will display a Syslog message like the following:

%DHCP_SNOOPING-5-DHCP_SNOOPING_NONZERO_GIADDR: DHCP_SNOOPING drop message
 with non-zero giaddr or option82 value on untrusted port, message type:
 DHCPDISCOVER, MAC sa: 5254.0008.d3e0


Figure 13.6 SW2 adds option 82 to PC1’s DISCOVER. SW2 then discards the DISCOVER after receiving it on an untrusted port.

The previous output of show ip dhcp snooping stated Insertion of option 82 is enabled. This means that when DHCP Snooping is enabled, the switch will automatically insert option 82 into DHCP client messages received on untrusted ports. This behavior of inserting option 82 is useful if the switch is a multilayer switch acting as a DHCP relay agent, forwarding client messages to a remote DHCP server. The default settings are configured with this common scenario in mind.

However, if the switch is functioning as a regular Layer 2 switch (not a DHCP relay agent), this default setting can cause headaches; this is the case for SW1 and SW2 in this example. This is because of another default setting shown in the same output: Option 82 on untrusted port is not allowed. These two default settings mean that

The switch adds option 82 to DHCP messages received on untrusted ports.

The switch doesn’t accept DHCP messages that already have option 82 on untrusted ports.

This might seem contradictory, but there’s a reason: a DHCP client has no valid reason to add option 82 to its own messages. If the switch receives a DHCP message that already contains option 82 on an untrusted port, it’s likely that a rogue DHCP server or a misconfigured client is at play. For this reason, the switch doesn’t accept such messages.

To disable option 82 insertion, use the no ip dhcp snooping information option command in global config mode, as in the following example. With this command configured, SW2 will no longer insert option 82 into clients’ DHCP messages:

SW2(config)# no ip dhcp snooping information option ❶
SW2(config)# do show ip dhcp snooping
. . .
Insertion of option 82 is disabled                  ❷
. . .
❶ Disables option 82 insertion

❷ SW2 will no longer insert option 82.

However, in our example network, it’s not enough to disable option 82 insertion on SW2 alone. SW1, having received a DHCP client message on an untrusted port, will add option 82 itself before forwarding the message to R1. A Cisco router acting as a DHCP server or relay agent will drop such messages too. So make sure to disable option 82 insertion on SW1 too:

SW1(config)# no ip dhcp snooping information option
With option 82 insertion disabled on both switches, the client’s DISCOVER message will reach R1 as is, and the client will be able to lease an IP address. In figure 13.6’s example, R1 is functioning as a DHCP server. But if it were a DHCP relay agent, it could then insert option 82 before forwarding the DISCOVER to the remote DHCP server, providing the server with additional context about the request. This extra context can help the server make an informed IP allocation decision.

Exam Tip As far as the CCNA exam is concerned, just know that you should disable option 82 insertion, unless the switch itself is a multilayer switch acting as a DHCP relay agent. This is an often-forgotten step in configuring DHCP Snooping that can lead to frustration. Don’t forget!

DHCP options

DHCP options enable the client, server, and sometimes relay agents to exchange additional information that can support the DHCP process and extend its functionality. There are about 100 standard DHCP options defined in various RFCs, although not all are widely used. In addition to option 82, here are a few examples:

Option 3 (Router)—This is a very common option. It is used by the server to tell the client which router to use as its default gateway.

Option 6 (DNS Server)—Another very common option. This tells the client which DNS server(s) to use for name resolution.

Option 50 (Requested IP Address)—A client can include this option if it wants to request a specific IP address from the server (although the server is not obligated to fulfill this request). For example, a Windows PC will typically include this option to request the same IP address it had previously (i.e., before it was last shut down).

We already covered the fact that a DHCP server can inform a client about its default gateway and DNS servers in chapter 4, without mentioning the relevant DHCP options that enable this functionality; that’s because DHCP options are generally not something you need to know for the CCNA exam. Option 82 is relevant only due to its effect when DHCP Snooping is enabled.

13.2.3 Rate-limiting DHCP messages
The configurations we have covered so far are the minimum essentials for enabling DHCP Snooping without interfering with legitimate DHCP traffic:

Enable DHCP Snooping: ip dhcp snooping

Activate DHCP Snooping on each VLAN: ip dhcp snooping vlan vlans

Trust the appropriate ports: ip dhcp snooping trust

Disable option 82 insertion: no ip dhcp snooping information option

One more optional (but valuable) aspect of DHCP Snooping you can configure is rate limiting—limiting the rate at which a DHCP Snooping-enabled switch accepts DHCP messages. The combination of Port Security and DHCP Snooping is able to thwart most DHCP-related attacks like DHCP starvation.

However, inspecting DHCP messages with DHCP Snooping can be demanding of the switch’s CPU. This leads to another possible attack: overwhelming the switch’s CPU with countless DHCP messages, potentially leading to a denial of service. DHCP Snooping rate limiting can mitigate against such an attack.

You can enable DHCP Snooping rate limiting on a per-port basis with ip dhcp snooping limit rate rate; the rate argument is configured in packets per second (pps). Cisco recommends a rate limit of no more than 100 pps on untrusted ports, but the appropriate rate varies greatly, depending on the port. For example, a port connected to a single PC should receive much less DHCP traffic than a port connected to another switch with 40 of its own connected end hosts.

In figure 13.7, I configure DHCP Snooping rate limiting on SW1’s and SW2’s untrusted ports at rates of 100 pps and 25 pps, respectively. These numbers are quite generous, given that only two hosts are shown in the network—a single PC, for example, should only generate two messages in the typical DORA exchange. In a real network, it’s best to find a balance between protecting against attacks and not blocking legitimate traffic.



Figure 13.7 Configuring DHCP Snooping rate limiting on untrusted ports

You may be wondering, what happens if a port receives DHCP messages at a faster rate than its configured limit? In the following example, I configure a rate limit of 1 pps on SW2 G0/2 to demonstrate:

SW2(config)# interface g0/2                          ❶
SW2(config-if)# ip dhcp snooping limit rate 1        ❶
%DHCP_SNOOPING-4-DHCP_SNOOPING_ERRDISABLE_WARNING: DHCP Snooping received 1 
DHCP packets on interface Gi0/2
%DHCP_SNOOPING-4-DHCP_SNOOPING_RATE_LIMIT_EXCEEDED:  ❷
➥The interface Gi0/2 is receiving more than          ❷
➥the threshold set    
%PM-4-ERR_DISABLE: dhcp-rate-limit error detected on ❸
➥Gi0/2, putting Gi0/2 in err-disable state           ❸
❶ Configures IP DHCP Snooping rate limiting with a rate limit of 1 pps

❷ The rate limit is exceeded.

❸ SW2 error-disables the port.

Note DHCP Snooping doesn’t filter DHCP messages on trusted ports, but rate limiting is one aspect that can be configured on trusted ports (although it’s rare).

If the rate limit is exceeded, the switch will error-disable the port to prevent any further messages. As with the previous examples of error-disabled ports that we have covered (BPDU Guard, power policing, and port security), there are two ways to reenable a port that was disabled by DHCP Snooping rate limiting:

Manual—Issue shutdown and no shutdown on the error-disabled port.

Automatic—Configure errdisable recovery cause dhcp-rate-limit to enable ErrDisable Recovery for ports disabled by DHCP Snooping rate limiting.

Although rate limiting is optional and disabled by default, it’s a good idea to configure reasonable rate limits on untrusted ports as an extra layer of protection against threats. Make sure to test rate limits in a controlled environment (a lab) before rolling them out in a live network!

Summary
DHCP Snooping is a security feature on switches that protects against DHCP-based attacks by inspecting DHCP messages as they are received.

In a DHCP poisoning attack, the attacker configures a rogue DHCP server (sometimes called a spurious DHCP server) to lease IP addresses to clients.

The rogue server tells clients to use itself as their default gateway, resulting in a man-in-the-middle attack in which the attacker intercepts the clients’ communications.

Port Security doesn’t mitigate against DHCP poisoning because the rogue server sends DHCP messages from a single MAC address; DHCP Snooping is needed.

DHCP Snooping only filters DHCP messages—non-DHCP messages are unaffected.

Enable DHCP Snooping with ip dhcp snooping in global config mode. It also needs to be activated on each VLAN with ip dhcp snooping vlan vlans.

Use show ip dhcp snooping to verify DHCP Snooping settings.

DHCP Snooping only filters DHCP messages received on untrusted ports. All ports are untrusted by default. It doesn’t filter messages received on trusted ports.

DHCP Snooping differentiates between messages sent by DHCP clients and those sent by DHCP servers.

Messages sent by clients include DISCOVER, REQUEST, DECLINE, and RELEASE.

Messages sent by servers include OFFER, ACK, and NAK.

Ports that lead toward the DHCP server should be trusted. Ports that lead away from the DHCP server (toward end hosts) should remain in the default untrusted state.

Use ip dhcp snooping trust in interface config mode to configure a trusted port.

When a DHCP message is received on an untrusted port, the switch will inspect it and act as follows:

If it is a DHCP server message, discard it.

If it is a DHCP client message, inspect it further depending on the type.

If a client successfully leases an IP address, create a new entry in the DHCP Snooping binding table.

If the message is a DISCOVER or REQUEST message, the switch will check that the Ethernet source MAC Address and DHCP chaddr (client hardware address) match. If they match, it accepts the message. If not, it discards the message.

The source MAC address/chaddr check protects against DHCP exhaustion attacks in which the attacker sends spoofed DHCP DISCOVER messages from a single source MAC address, each with a unique address in the chaddr field.

If the message is a RELEASE or DECLINE message, the switch will check the DHCP Snooping binding table to verify the message.

As a DHCP Snooping-enabled switch observes exchanges between client and servers, it builds a table of the clients that have successfully leased an IP address: the DHCP Snooping binding table.

View the DHCP Snooping binding table with show ip dhcp snooping binding.

When a RELEASE or DECLINE message is received on an untrusted port, the switch ensures that the IP address of the message and the port it was received on match the entry in the binding table.

DHCP defines various optional fields, called options. DHCP options are beyond the scope of the CCNA exam, except for option 82, which can impede the DHCP process when DHCP Snooping is enabled.

Option 82 is the DHCP relay information option.

A DHCP relay agent can insert option 82 when forwarding DHCP client messages to a remote DHCP server, providing additional information to the server.

By default, a DHCP Snooping-enabled switch will automatically insert option 82 into DHCP client messages received on untrusted ports.

By default, a DHCP Snooping-enabled switch will discard DHCP messages with option 82 that are received on an untrusted port. A Cisco router acting as a DHCP server or relay agent will drop such messages too.

To prevent a DHCP Snooping-enabled switch from adding option 82 to client messages, use no ip dhcp snooping information option in global config mode.

You can optionally configure rate limiting on a per-port basis to limit the rate at which the port can receive DHCP messages.

Use ip dhcp snooping limit rate rate to configure rate limiting. The rate argument is configured in packets per second (pps).

Rate limiting can be configured on both untrusted and trusted ports, although it is rarely enabled on trusted ports.

If a port receives DHCP messages at a faster rate than its configured limit, the switch will error-disable the port.

Use shutdown and no shutdown to manually reenable an error-disabled port or errdisable recovery cause dhcp-rate-limit to enable ErrDisable Recovery for ports disabled by DHCP Snooping rate limiting.