9 Network Address Translation
This chapter covers

Private IPv4 addresses
Using NAT to translate between private and public IPv4 addresses
The different types of NAT
Configuring NAT on Cisco routers
IPv4 address exhaustion is a major problem and has been for a long time. In chapters 20 and 21 of volume 1, we covered the long-term solution: IPv6. However, IPv4 is still dominant to this day thanks to a few solutions that have been very effective in extending IPv4’s lifespan. We covered one of these solutions in chapter 11 of volume 1 on subnetting with Classless Inter-Domain Routing (CIDR), which allows more flexibility than the rigid classful addressing system that came before it.

In this chapter, we will cover two more important solutions that, combined, have proven essential in preserving the IPv4 address space: private IPv4 addressing and Network Address Translation (NAT). Three ranges of IPv4 addresses have been reserved for free use in private networks without the need to be globally unique, and NAT provides a way to translate those private addresses into public addresses for communication over the internet. We will cover the following two CCNA exam topics:

1.7 Describe the need for private IPv4 addressing

4.1 Configure and verify inside source NAT using static and pools

9.1 Private IPv4 addresses
Private IPv4 addresses are IPv4 addresses that can be freely used by any organization or individual for their internal networks; they do not have to be globally unique. Three private IPv4 address ranges are defined in RFC 1918, Address Allocation for Private Internets:

10.0.0.0/8 (10.0.0.0–10.255.255.255)

172.16.0.0/12 (172.16.0.0–172.31.255.255)

192.168.0.0/16 (192.168.0.0–192.168.255.255)

Exam Tip Make sure you know the three ranges defined by RFC 1918. Additionally, remember the name RFC 1918; memorizing RFC numbers is unnecessary in most cases, but these addresses are often called RFC 1918 addresses.

Figure 9.1 shows three LANs connected to the internet. The LANs all use IPv4 addresses from the third private range (192.168.0.0/16). Notice that the three subnets overlap: 192.168.0.0/23 (192.168.0.0–192.168.1.255), 192.168.1.0/24 (192.168.1.0–192.168.1.255), and 192.168.1.0/25 (192.168.1.0–192.168.1.127). This is not a problem because the networks are never directly connected; their addresses don’t have to be unique.



Figure 9.1 Public and private IPv4 addresses. Private IPv4 addresses can be freely used for internal networks and do not have to be globally unique. Public IPv4 addresses, used for communication over the internet, must be globally unique.

IPv4 addresses that are not in the RFC 1918 ranges (or another reserved range) are public IPv4 addresses; these addresses must be globally unique because they are used to communicate over the internet. If two internet-connected hosts have the same IP address, other routers won’t be able to determine which of the two hosts is the intended recipient of a packet destined for their shared address. Anycast addresses (outlined in chapter 20 of volume 1) are an exception to this rule; they are purposefully assigned to multiple hosts.

Note The public IPv4 addresses in figure 9.1 are from reserved ranges too: 192.0.2.0/24, 198.51.100.0/24, and 203.0.113.0/24 are reserved for use in documentation and examples but are often used to represent public addresses.

Private IPv4 addresses are not routable over the internet—packets sourced from or destined for private addresses will be discarded by the Internet Service Provider (ISP). If you have a Windows PC, use ipconfig to check your PC’s IPv4 address (ifconfig if you’re using macOS/Linux)—it’s almost certainly a private address. So how can your PC communicate over the internet despite having a private address? The answer is NAT.

9.2 NAT concepts
Network Address Translation (NAT) is the process of modifying a packet’s source ">and/or destination IP addresses and is typically performed by a router (or firewall) at the network’s perimeter—a router that connects the internal network to the internet. By translating private IP addresses to public IP addresses, NAT allows hosts with private IP addresses to communicate over the internet.

9.2.1 The NAT process
Figure 9.2 demonstrates the NAT process. PC1, a host with a private IP address, sends a packet to the server at 8.8.8.8. R1 uses NAT to translate between PC1’s private IP address (which is not routable over the internet) and a public IP address.



Figure 9.2 R1 translates between PC1’s private IP address and a public IP address for use over the internet.

In step 1, PC1 sends a packet sourced from its private IP address—the IP address of its network interface. In step 2, R1 translates the source IP address of PC1’s packet to a public IP address before forwarding it over the internet. Then, in step 3, the server at 8.8.8.8 replies by sending a packet destined for the public IP address, which R1 translates back to PC1’s private IP address before forwarding the packet to PC1 in step 4.

Note NAT was designed to translate between private and public IP addresses, but private–private and public–public translations are technically possible too. However, the use cases for private–private and public–public NAT are more limited than private–public NAT. For the CCNA exam, you can assume that NAT is private–public.

9.2.2 Cisco NAT terminology
When a host in an internal network communicates with a host in an external network via a NAT-enabled router, there are four addresses involved from the standpoint of the router:

The IP address of the internal host before NAT (inside local)

The IP address of the internal host after NAT (inside global)

The IP address of the external host before NAT (outside local)

The IP address of the external host after NAT (outside global)

Cisco uses four terms to describe each of these addresses: inside local, inside global, outside local, and outside global. In this section, we’ll examine the inside/outside distinction and the local/global distinction and then define these four terms, which are critical to understand for the CCNA exam.

Inside and outside

Cisco uses the terms inside and outside to refer to the internal and external networks, respectively. An inside address is the IP address of a host located in the router’s inside (internal) network, and an outside address is the IP address of a host located in an outside (external) network. Similarly, hosts in the inside network are called inside hosts, and hosts in the outside network are called outside hosts. Figure 9.3 demonstrates these concepts. R1’s G0/0 interface connects to the internal/inside network, and G0/1 connects to the external/outside network—the internet.

Note For consistency’s sake, I will use the terms inside and outside from now on since they are the terms that Cisco uses in the context of NAT. Their meanings are the same as internal and external.



Figure 9.3 The inside/outside distinction from the perspective of R1. The inside network is R1’s internal network, and the outside network is the external network (everything else).

Note All of these terms are dependent on perspective. From R1’s perspective, PC1 is an inside host and 8.8.8.8 is an outside host, but from the perspective of 8.8.8.8 and its router (not shown), the opposite is true.

We will cover NAT configuration in section 9.3, but figure 9.3 shows one important step in the process: specifying the router’s inside and outside interfaces with the ip nat {inside | outside} command. Because R1 G0/0 is configured with the ip nat inside command, PC1 is an inside host. And because R1 G0/1 is configured with ip nat outside, 8.8.8.8 is an outside host.

Local and global

When PC1 (an inside host) sends a packet to a destination in the outside network, the source IP address of that packet is the IP address configured on PC1—a private IP address. But what about after R1 uses NAT to translate the source IP address of PC1’s packet to a public IP address? The address after translation still represents PC1, so it remains an inside address, but another distinction is needed to differentiate between the pre- and post-NAT addresses: the local/global distinction.

A local address is an address before the router translates it, and a global address is an address after the router translates it. In other words, a local address is a host’s address from the perspective of the inside network, and a global address is a host’s address from the perspective of the outside network. Figure 9.4 demonstrates the local/global distinction.

Local/global and private/public

Local addresses and global addresses might seem similar to private addresses and public addresses. However, the concepts don’t always overlap. For example, in figure 9.4, 8.8.8.8 (a public address) is both a local address and a global address from R1’s perspective.

Local and global are NAT-specific terms that have specific meanings. Local addresses are used on the inside of a NAT network, while global addresses are used on the outside of a NAT network. NAT translates local addresses to global addresses when traffic flows from the inside to the outside of the network and vice versa, regardless of whether the addresses are private or public.



Figure 9.4 The local/global distinction. Local addresses appear in the inside network, and global addresses appear in the outside network.

From PC1’s perspective, and from the perspective of other hosts in the inside network, PC1’s IP address is a private IP address (i.e., 10.0.0.10). However, from the perspective of any hosts in the outside network, PC1’s IP address is a public IP address (i.e., 203.0.113.1). For example, when the server at 8.8.8.8 replies to PC1’s packet, it addresses its response to the public IP address, not PC1’s private IP address—the server isn’t even aware of PC1’s private IP address.

When we combine the inside/outside and local/global distinctions, we get the four terms mentioned at the beginning of this section: inside local, inside global, outside local, and outside global. Figure 9.5 illustrates these four addresses.



Figure 9.5 Inside local, inside global, outside local, and outside global addresses. The inside/outside distinction differentiates between hosts located in the inside and outside networks, and the local/global distinction differentiates between the perspectives of hosts in the inside and outside networks.

Note In our example, R1 doesn’t translate the external host’s IP address, so the outside local and outside global addresses are identical.

Now we can more accurately define those four terms:

Inside local—The IP address of a host located in the inside network from the perspective of the inside network

Inside global—The IP address of a host located in the inside network from the perspective of the outside network

Outside local—The IP address of a host located in the outside network from the perspective of the inside network

Outside global—The IP address of a host located in the outside network from the perspective of the outside network

As pointed out in the previous note, the outside local and outside global addresses are identical in our example. This is because R1 only performs source NAT on PC1’s packet—it only translates the packet’s source IP address. R1 does not perform destination NAT on PC1’s packet—it does not translate the packet’s destination IP address. Destination NAT is not part of the CCNA exam, so we won’t cover it in this book.

It’s all about perspective

To repeat what I said in a previous note, these terms are all dependent on perspective; they are relative to R1, the router performing NAT in our example. As far as R1 is concerned, 8.8.8.8 is both an outside local and an outside global address. However, the server at 8.8.8.8 is likely connected to its own router performing NAT as well, with its own perspective on what’s inside and what’s outside, what’s local and what’s global. From that router’s perspective, 8.8.8.8 is the server’s inside global address, and its inside local address is a private IP address that is unknown to R1, PC1, or any other host outside of that network.

9.3 Types of NAT
There are multiple types of NAT. For the CCNA exam, you should know the following three:

Static NAT—Static one-to-one translations

Dynamic NAT—Dynamic one-to-one translations

Dynamic PAT (Port Address Translation)—Dynamic many-to-one translations

Each type has its own use cases, but dynamic PAT is by far the most widely used, potentially allowing thousands of hosts to share a single public IP address. In this section, we’ll examine each type and how to configure it on a Cisco router.

9.3.1 Static NAT
The first type of NAT we’ll cover is static NAT, which involves statically configuring one-to-one mappings of inside local (private) addresses to inside global (public) addresses. Figure 9.6 demonstrates static NAT and how to configure it in Cisco IOS.



Figure 9.6 Static NAT. Inside local addresses 10.0.0.11 and 10.0.0.12 are statically mapped to inside global addresses 192.0.2.1 and 192.0.2.2, respectively.

Note Figure 9.6 only shows the translations in one direction (from PC1/PC2 to the server), but R1 will translate the server’s replies too (as shown in previous figures).

By mapping PC1’s private IP address (10.0.0.11) to a public IP address (192.0.2.1), PC1 is able to communicate over the internet. To allow another inside host (PC2) to communicate over the internet, a second public IP address (192.0.2.2) is needed. This is the limitation of static NAT—it is one to one. As such, it does not help with the problem of IPv4 address exhaustion, although it is sometimes used to allow particular hosts to communicate over the internet. In the following example, I demonstrate the configurations:

R1(config)# interface g0/0                                      ❶
R1(config-if)# ip nat inside                                    ❶
R1(config-if)# interface g0/1                                   ❷
R1(config-if)# ip nat outside                                   ❷
R1(config-if)# exit
R1(config)# ip nat inside source static 10.0.0.11 192.0.2.1     ❸
R1(config)# ip nat inside source static 10.0.0.12 192.0.2.2     ❹
❶ Specifies G0/0 as an inside interface

❷ Specifies G0/1 as an outside interface

❸ Statically maps 10.0.0.11 to 192.0.2.1

❹ Statically maps 10.0.0.12 to 192.0.2.2

The first step is to configure the inside and outside interfaces with ip nat {inside | outside} in interface config mode, as we covered in the previous section. After that, all that’s left to do is create static mappings with the ip nat inside source static inside-local inside-global command. In the example, I mapped inside local addresses 10.0.0.11 and 10.0.0.12 to inside global addresses 192.0.2.1 and 192.0.2.2, respectively. Figure 9.7 clarifies the meaning of the command’s keywords.



Figure 9.7 Static NAT. Inside local addresses 10.0.0.11 and 10.0.0.12 are statically mapped to inside global addresses 192.0.2.1 and 192.0.2.2, respectively.

The inside keyword tells R1 to perform translations for IP addresses originating from the inside network. Specifically, R1 will translate inside local addresses to inside global addresses as packets move from the inside network to the outside network.

The source keyword that follows tells R1 to translate the source IP address of packets coming from hosts on the inside network. So when R1 forwards a packet from PC1, it will translate the packet’s source IP address from 10.0.0.11 to 192.0.2.1. However, it’s important to remember that the reverse is true of the reply from the outside host. When a reply comes from the outside host and is destined for 192.0.2.1, R1 will translate the packet’s destination IP address back to 10.0.0.11, allowing the packet to be correctly delivered to PC1.

The CCNA exam topics list states that you must be able to “configure and verify inside source NAT,” so all of the NAT statements that we configure will start with ip nat inside source. It is the rest of the command that differentiates between static NAT, dynamic NAT, and dynamic PAT. By using the static keyword, you can configure static inside local addresses to inside global address mappings, as in this example.

After configuring static NAT, you can use show ip nat translations to view the router’s translation table, as in the following example. One potentially confusing aspect of this command’s output is that the leftmost column is Inside global, followed by Inside local—I think the opposite makes more sense, but Cisco didn’t ask my opinion when they designed this command!

R1# show ip nat translations
Pro Inside global      Inside local       Outside local      Outside global
--- 192.0.2.1          10.0.0.11          ---                ---            ❶
--- 192.0.2.2          10.0.0.12          ---                ---            ❷
❶ PC1’s static mapping

❷ PC2’s static mapping

A static entry is created in the table for each mapping: 10.0.0.11 to 192.0.2.1 and 10.0.0.12 to 192.0.2.2—the other columns are empty. To see some information in these columns, I’ll open web browsers on PC1 and PC2 and access some websites. When an inside host communicates with an outside host, additional dynamic entries are created in the NAT table. These dynamic entries are tied to the static mapping but track the state of individual communication sessions. The following example shows a small portion of the output afterward:

R1# show ip nat translations
Pro Inside global      Inside local       Outside local      Outside global
tcp 192.0.2.1:54568    10.0.0.11:54568    34.117.65.55:443   34.117.65.55:443    ❶
--- 192.0.2.1          10.0.0.11          ---                ---                 ❷
tcp 192.0.2.2:53154    10.0.0.12:53154    34.117.65.55:443   34.117.65.55:443    ❶
--- 192.0.2.2          10.0.0.12          ---                ---                 ❷
❶ Dynamic entries created by PC1 and PC2 communicating with an HTTPS server

❷ PC1’s and PC2’s static entries

Note The numbers displayed after the IP addresses (separated by colons) indicate the TCP and UDP port numbers used by PC1/PC2 and the external hosts. That’s how you can identify that HTTPS (TCP port 443) is being used in the previous example.

Whereas the static entries are permanent, the dynamic entries will be removed after a certain period of inactivity. For example, if PC1 and PC2 stop communicating with the HTTPS server at 34.117.65.55, those entries will be automatically removed, leaving only the static entries. You can also use clear ip nat translation * in privileged EXEC mode to manually clear all dynamic entries from the NAT translation table.

Note Don’t confuse the static/dynamic entries in the translation table with static/dynamic NAT; all of the entries we just examined are the result of static NAT translations.

9.3.2 Dynamic NAT
The next type of NAT we’ll cover is dynamic NAT. Static NAT and dynamic NAT are similar in that they both involve one-to-one mappings of inside local addresses to inside global addresses. The difference is in how the mappings are assigned. In static NAT, you statically configure each mapping one by one. In dynamic NAT, the router dynamically creates the mappings itself from a pool of available addresses. Figure 9.8 demonstrates dynamic NAT; aside from the configuration commands, the NAT process is similar to that of static NAT.



Figure 9.8 Dynamic NAT. An ACL is used to identify a range of inside local addresses, and a NAT pool is used to identify a range of inside global addresses. Addresses in the pool are assigned on a first come, first served basis.

Dynamic NAT configuration consists of three main steps:

Define a range of inside local (private) addresses with an ACL

Define a range of inside global (public) addresses with a NAT pool

Map the ACL to the NAT pool

When the router forwards a packet from a host with an IP address in the range specified by the ACL, it will translate the source IP address to one of the available inside global addresses on a first come, first served basis. The following example shows the necessary configurations:

R1(config)# interface g0/0                                          ❶
R1(config-if)# ip nat inside                                        ❶
R1(config-if)# interface g0/1                                       ❶
R1(config-if)# ip nat outside                                       ❶
R1(config-if)# exit
R1(config)# access-list 1 permit 10.0.0.0 0.0.0.255                 ❷
R1(config)# ip nat pool POOL1 192.0.2.1 192.0.2.5 prefix-length 29  ❸
R1(config)# ip nat inside source list 1 pool POOL1                  ❹
❶ Specifies inside and outside interfaces

❷ Specifies the inside local addresses that will be translated

❸ Specifies a range of inside global addresses

❹ Maps ACL 1 to POOL1

Just like in static NAT, you must use ip nat {inside | outside} to specify which interface(s) connect to the inside network and which connect to the outside network. Next, create an ACL to identify a range of inside local addresses to be translated. Packets that are permitted by the ACL will be translated, and packets that are denied by the ACL will not be translated; they will be forwarded as is (however, if their source IP address is a private IP address, they will be dropped by the ISP).

Note The ACL isn’t being used to decide which packets should be forwarded and which should be blocked; it is only being used to decide which packets should be translated with NAT. This is another common use for ACLs, which are quite versatile.

The ACL I created is access-list 1 permit 10.0.0.0 0.0.0.255, which permits all IP addresses from 10.0.0.0 through 10.0.0.255 but denies all other IP addresses via the implicit deny. R1 will use NAT to translate packets with a source IP address in the permitted range, but packets with a source IP address that is not in that range will not be translated.

The next step is to specify a range of inside global addresses—the public IPv4 addresses that will be used for communication over the internet. This is done by creating a NAT pool with the ip nat pool name start-ip end-ip prefix-length length command. The start-ip and end-ip arguments identify the range; I configured 192.0.2.1 192.0.2.5 to specify a range of five public addresses: 192.0.2.1–192.0.2.5.

Note In a real network, you cannot freely use any public IPv4 addresses you want. Public addresses must be globally unique, and their assignment is governed by IANA and the RIRs below it (as we covered in chapter 20 of volume 1). To receive a range of public IP addresses, an enterprise must apply to an ISP or directly to an RIR.

In the ip nat pool command, you must also specify a prefix length; this is used to ensure that all addresses in the specified range are in the same subnet. I specified the 192.0.2.1–192.0.2.5 range with a /29 prefix length. This implies the 192.0.2.0/29 subnet (all host bits set to 0), which includes all addresses from 192.0.2.0 to 192.0.2.7. The specified range (192.0.2.1–192.0.2.5) is included in that subnet, so the command succeeds. Otherwise, the command would be rejected.

Note Instead of prefix-length, you can use the netmask keyword—for example, ip nat pool POOL1 192.0.2.1 192.0.2.5 netmask 255.255.255.248.

The final step is to combine the ACL and pool with a NAT statement, mapping the range of inside local addresses (the ACL) to the range of inside global addresses (the pool). The command is ip nat inside source list acl pool pool; I mapped ACL 1 to POOL1 in the example with ip nat inside source list 1 pool POOL1. After that command, the dynamic NAT configuration is complete.

It is worth repeating that dynamic NAT is one to one, just like static NAT. Multiple inside local addresses cannot be translated to the same inside global address at the same time. The inside global addresses are assigned on a first-come, first-served basis, and if the pool dries up, other hosts’ packets will not be able to be translated—they will be dropped! Those hosts will have to wait for an inside global address to become available again; this is a major downside of dynamic NAT.

Figure 9.9 demonstrates this. The first five inside local addresses are translated to inside global addresses, but the sixth cannot be translated, resulting in the packet being dropped. The seventh packet, from 10.1.1.2, is forwarded without being translated because its source IP address is denied by ACL 1.



Figure 9.9 The dynamic NAT pool dries up. Packets that match ACL but can’t be translated are dropped. Packets that are denied by the ACL are forwarded as is.

Exam Tip Packets that are permitted by the ACL but can’t be translated due to a lack of addresses in the pool will be dropped. Packets that are denied by the ACL will be forwarded as is, without being translated (likely resulting in them being dropped by the ISP due to their private IP addresses). Remember this distinction!

As with static NAT, you can view the router’s translation table with show ip nat translations. The output looks the same as when using static NAT. The following example shows a few entries in R1’s translation table. For each translation, one entry is added showing only the inside local to inside global mapping, and then additional entries are added for each communication session from an inside host to an outside host—in this case, a DNS session (UDP 53), an HTTPS session (TCP 443), and an HTTP session (TCP 80) are shown:

R1# show ip nat translations
Pro Inside global      Inside local       Outside local      Outside global
udp 192.0.2.2:58910    10.0.0.11:58910    8.8.8.8:53         8.8.8.8:53
--- 192.0.2.2          10.0.0.11          ---                ---
tcp 192.0.2.3:33630    10.0.0.12:33630    142.250.207.14:443 142.250.207.14:443
--- 192.0.2.3          10.0.0.12          ---                ---
tcp 192.0.2.1:32980    10.0.0.13:32980    34.107.221.82:80   34.107.221.82:80
--- 192.0.2.1          10.0.0.13          ---                ---
Of the types of NAT you need to know for the CCNA exam, dynamic NAT has the fewest real-world use cases. Like static NAT, it only provides one-to-one translations. However, unlike static NAT, it doesn’t let you control the translations. If the number of inside hosts is larger than the available pool of inside global addresses, there’s no easy way to control which hosts get to access the internet and which have to wait. Obtaining enough public IP addresses to support all inside hosts simply isn’t feasible for most enterprises these days, given the state of the IPv4 address exhaustion problem.

9.3.3 Dynamic PAT
Dynamic Port Address Translation (PAT) is a type of NAT that translates both IP addresses and TCP/UDP port numbers (if necessary) to provide many-to-one mappings of inside local to inside global addresses. By using a unique port number for each communication session, a single public IP address can be shared by many inside hosts at the same time; the NAT-enabled router uses the port numbers to keep track of each individual session.

There are 65,536 (216) port numbers in total, meaning that a single public IP address can theoretically support tens of thousands of sessions from inside hosts—the actual number will depend on a number of factors, such as the router’s memory capacity. It is this type of NAT that, combined with private IPv4 address ranges, has greatly extended IPv4’s lifespan.

Note ICMP doesn’t use port numbers like TCP and UDP, but many ICMP message types use a 16-bit Identifier field for a similar purpose. When translating ICMP packets (i.e., ping), the Identifier plays the role that TCP/UDP port numbers do.

Dynamic PAT using a pool

One way to configure dynamic PAT is to simply add the overload keyword to the end of a dynamic NAT statement; in fact, another name for PAT is NAT overload. The following example demonstrates how to configure dynamic PAT in this way:

R1(config)# interface g0/0
R1(config-if)# ip nat inside
R1(config-if)# interface g0/1
R1(config-if)# ip nat outside
R1(config-if)# exit
R1(config)# access-list 1 permit 10.0.0.0 0.0.0.255
R1(config)# ip nat pool POOL1 192.0.2.1 192.0.2.5 prefix-length 29
R1(config)# ip nat inside source list 1 pool POOL1 overload         ❶
❶ Adds the overload keyword to the NAT statement

Figure 9.10 shows how the translations work after these configurations. When the router translates a packet, it will keep the pre- and post-translation port numbers the same if possible. However, if a packet’s pre-translation port number is already in use for another session, the router will translate the port number to an available one.



Figure 9.10 Dynamic PAT using a NAT pool. The router keeps the pre- and post-translation port numbers the same if possible but translates them if needed.

Note Once a session’s first packet has been translated, the same port number is used for the rest of the session; each individual packet doesn’t need a unique port number.

Notice that in figure 9.10’s example, R1 translates all three packets’ inside local addresses to the same inside global address, even though the NAT pool has five available addresses. The router will use up all available port numbers for one inside global address (i.e., 192.0.2.1) before translating to the next available address in the pool (i.e., 192.0.2.2).

When the router receives the reply packets, it is able to identify which session the packets belong to, thanks to the unique port numbers. The router can then translate each packet’s inside global address back to the appropriate inside local address. Figure 9.11 demonstrates this.



Figure 9.11 The router tracks each session and translates each reply’s destination address back to the appropriate inside local address.

Dynamic PAT using an interface’s IP address

Although dynamic PAT can be configured with a pool, PAT’s many-to-one translation capabilities mean that many organizations require only a single public IP address, not a pool of them. And if a router is connected to the internet, the router already has a public IP address assigned to it—the IP address of the internet-connected interface. With PAT, the router can translate inside hosts’ IP addresses to the IP address of the router’s own interface.

Figure 9.12 shows how to configure this in Cisco IOS. Packets from hosts in R1’s internal LAN are translated to the IP address of R1’s G0/1 interface: 203.0.113.2.



Figure 9.12 Dynamic PAT using an interface’s IP address. R1 translates inside local addresses to the IP address of its own G0/1 interface: 203.0.113.2.

This is how dynamic PAT is most often configured because it allows inside hosts to communicate over the internet using the IP address already configured on the router—no additional public addresses are needed. The following example shows the configuration steps; let’s walk through each command:

R1(config)# interface g0/0                                        ❶
R1(config-if)# ip nat inside                                      ❶
R1(config-if)# interface g0/1                                     ❶
R1(config-if)# ip nat outside                                     ❶
R1(config-if)# exit
R1(config)# access-list 1 permit 10.0.0.0 0.0.0.255               ❷
R1(config)# ip nat inside source list 1 interface g0/1 overload   ❸
❶ Specifies inside and outside interfaces

❷ Specifies the inside local addresses that will be translated

❸ Translates inside local addresses to R1 G0/1’s address

As in previous examples, you must first configure the inside and outside interfaces with ip nat {inside | outside} in interface config mode. Then, as in dynamic NAT, configure an ACL to determine which IP addresses should be translated. This ACL functions the same as the ones in NAT configurations we covered earlier: packets that are permitted by the ACL will be translated before being forwarded, but packets that are denied by the ACL will be forwarded as is.

Note If a packet is permitted by the ACL but can’t be translated due to a lack of addresses or port numbers, the packet will be dropped. However, you likely won’t encounter this with dynamic PAT because so many port numbers are available.

All that remains is to configure the NAT statement itself. The syntax in this case is ip nat inside source list acl interface interface overload. This tells the router to use PAT to translate packets permitted by the ACL to the IP address of the specified interface. Port numbers are used to keep track of each session, including the router’s own sessions (when the router sends its own packets using that IP address).

Note The overload keyword is optional. If you omit it, IOS will automatically add it.

The following example shows R1’s translation table after three inside hosts have communicated with an HTTPS server. The three inside local addresses are all translated to 203.0.113.2, but all have unique source ports, allowing R1 to keep track of them:

R1# show ip nat translations 
Pro Inside global      Inside local     Outside local      Outside global
tcp 203.0.113.2:44578  10.0.0.11:44578  34.117.65.55:443   34.117.65.55:443
tcp 203.0.113.2:33032  10.0.0.12:33032  34.117.65.55:443   34.117.65.55:443
tcp 203.0.113.2:39102  10.0.0.13:39102  34.117.65.55:443   34.117.65.55:443
One more useful NAT verification command is show ip nat statistics. The following example shows the output on R1:

R1# show ip nat statistics
Total active translations: 3 (0 static, 3 dynamic; 3 extended)     ❶
Peak translations: 292, occurred 02:54:25 ago                      ❷
Outside interfaces:                                                ❸
  GigabitEthernet0/1                                               ❸
Inside interfaces:                                                 ❸
  GigabitEthernet0/0                                               ❸
Hits: 179478  Misses: 0                                            ❹
CEF Translated packets: 175983, CEF Punted packets: 3495
Expired translations: 1566                                         ❺
. . .
❶ R1 has three active translations in its table.

❷ R1 had a peak of 292 active translations.

❸ R1’s inside and outside interfaces

❹ R1 has translated a total of 179,478 packets.

❺ A total of 1,566 expired translations have been removed from R1’s table.

Exam scenarios

NAT is a key technique that is employed in the vast majority of modern networks and is a critical CCNA exam topic. Here are a couple of questions that illustrate how your understanding of NAT might be tested in the CCNA exam:

1. (multiple choice, multiple answers)

You create an ACL as part of a dynamic NAT configuration. What is the role of this ACL?

A. define which packets should be forwarded and which should be dropped

B. define which packets should be translated

C. define the range of inside global addresses that will be used for communication over the internet

D. create a NAT pool

The key to this question is understanding that an ACL’s role in a dynamic NAT (or PAT) configuration is different from an ACL applied to an interface. Instead of determining which packets should be forwarded and which should be dropped, the ACL is used to define which packets should be translated. Packets that are permitted by the ACL are translated, and those that are denied by the ACL are forwarded as is (without translation). So B) is the correct answer.

2. (drag and drop)

Drag the NAT types on the left to the appropriate characteristics on the right. Each NAT type can be used more than once.

A) Static NAT

One-to-one translations

B) Dynamic NAT

One-to-many translations

C) Dynamic PAT

Automatic translations

Manual translations

Here are the correct answers:

One-to-one translations: A) and B)

One-to-many translations: C)

Automatic translations: B) and C)

Manual translations: A)

Static and dynamic NAT both offer one-to-one translations: each inside local address is translated to a unique inside global address. Dynamic PAT, on the other hand, provides many-to-one translations: many inside local addresses are translated to a single inside global address.

Static NAT requires manual configuration of each translation with the ip nat inside source inside-local inside-global command. Dynamic NAT and PAT, on the other hand, provide automatic translations; you simply need to specify a range of inside local addresses and a range of inside global addresses (or an interface), and the router automatically creates the translations as it forwards packets.

Summary
IPv6 is the long-term solution to IPv4 address exhaustion, but subnetting/CIDR, private IPv4 addresses, and NAT have greatly extended IPv4’s lifespan.

Private IPv4 addresses can be freely used by any organization or individual for their internal networks; they do not have to be globally unique.

RFC 1918 defines three private IPv4 address ranges: 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16.

IPv4 addresses that are not in an RFC 1918 range (or another reserved range) are public IPv4 addresses and must be globally unique.

Private IPv4 addresses are not routable over the internet—packets sourced from or destined for private addresses will be discarded by the ISP.

Network Address Translation (NAT) is the process of modifying a packet’s source and/or destination IP addresses. By translating private IP addresses to public IP addresses, hosts with private addresses can communicate over the internet.

NAT was designed to translate between private and public IP addresses, but private–private and public–public translations are technically possible too.

Cisco uses four terms to describe a packet’s source/destination addresses before/after NAT: inside local, inside global, outside local, and outside global.

The terms inside and outside refer to the internal and external networks, respectively—for example, inside/outside address and inside/outside host.

Use the ip nat {inside | outside} command to specify a router’s interfaces as connecting to the inside or outside networks. This step is required for all NAT types covered in the CCNA exam.

The terms local and global are used to distinguish between pre- and post-NAT addresses.

A device’s IP address from the perspective of the inside network is local (pre-NAT). A device’s IP address from the perspective of the outside network is global (post-NAT).

Inside local—The IP address of a host located in the inside network from the perspective of the inside network

Inside global—The IP address of a host located in the inside network from the perspective of the outside network

Outside local—The IP address of a host located in the outside network from the perspective of the inside network

Outside global—The IP address of a host located in the outside network from the perspective of the outside network

If a router does not perform destination NAT (does not translate the destination IP address of inside hosts’ packets), the outside local and outside global addresses will be identical.

There are three types of NAT to learn for the CCNA exam: static NAT (static one to one), dynamic NAT (dynamic one to one), and dynamic PAT (dynamic many to one).

Static NAT involves configuring static one-to-one mappings of inside local (private) addresses to inside global (public) addresses.

Use ip nat inside source static inside-local inside-global to configure a static NAT mapping.

Use show ip nat translations to view the NAT translation table. Permanent entries are made for each static mapping.

When a static mapping is used, dynamic entries are made to track each communication session between inside and outside hosts. These entries are cleared from the table after a period of inactivity.

Use clear ip nat translation * to manually clear all dynamic entries.

Dynamic NAT is similar to static NAT in that it involves one-to-one mappings of inside local to inside global addresses. However, in dynamic NAT, the router performs the mappings dynamically.

Dynamic NAT configuration consists of three main steps: (1) Define a range of inside local addresses with an ACL, (2) define a range of inside global addresses with a NAT pool, (3) map the ACL to the NAT pool.

The ACL’s purpose in dynamic NAT isn’t to decide which packets are forwarded or dropped. It is only used to decide which packets are translated and which are not.

Use ip nat pool name start-ip end-ip prefix-length length to create a NAT pool. Instead of prefix-length length, you can also use the netmask netmask.

Use ip nat inside source list acl pool pool to map the ACL to the pool.

If a packet is permitted by the ACL, its source IP will be translated to one of the addresses in the pool on a first come, first served basis.

Dynamic NAT mappings are one to one. Multiple inside local addresses cannot be translated to the same inside global address at the same time.

A packet that is permitted by the ACL but can’t be translated due to a lack of addresses in the pool will be dropped.

A packet that is denied by the ACL will be forwarded as is, without being translated (although the ISP will probably drop the packet because of its private address).

Dynamic Port Address Translation (PAT) is a type of NAT that translates both IP addresses and TCP/UDP port numbers (if necessary) to provide dynamic many-to-one mappings of inside local to inside global addresses.

It is this type of NAT that, combined with private IPv4 address ranges, has greatly extended IPv4’s lifespan.

Dynamic PAT can be configured with a pool, like dynamic NAT. Simply add the overload keyword to the end of the NAT statement: ip nat inside source list acl pool pool overload. Dynamic PAT is also called NAT overload.

When translating packets, the router keeps the pre- and post-translation port numbers the same if possible but translates them if needed. Unique port numbers are needed for the router to track each session.

The router will use up all available port numbers for one inside global address before translating to the next available address in the pool.

Instead of using PAT with a pool, it is more common to translate inside hosts’ IP addresses to the IP address of the routers’ own internet-connected interface.

Use ip nat inside source list acl interface interface overload to configure this. The router will translate packets that match the ACL to the IP address of the specified interface, using port numbers to track sessions.

Use show ip nat statistics to view statistics such as the total number of active translations, peak translations, packets translated, etc.