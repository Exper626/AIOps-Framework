16 WAN architectures
This chapter covers

Connecting remote sites using wide area network technologies
Different types of internet connections
Creating virtual private networks over the public internet
In the previous chapter, we covered local area networks (LANs) of various types and scales, from SOHO networks, to two- and three-tier campus LANs and even specialized data center networks that are essential for hosting an enterprise’s key servers. But LANs are just one piece of the puzzle; most enterprise networks are not confined to a single physical location.

Take, for example, a multinational corporation that has its headquarters in New York, manufacturing facilities in China, and regional offices scattered across Europe. Each of these locations will have its own local network, tailored for its specific needs. But these dispersed networks need to function as a unified whole, communicating and sharing resources securely and efficiently. Similarly, consider a retail chain with hundreds of stores, each with its own point-of-sale system, security cameras, guest Wi-Fi, and other network-connected devices. These stores also need to be integrated into a centralized system for inventory management, security monitoring, and data analytics.

How can all of these geographically diverse LANs be connected to form a coherent whole? What role does the public internet play in all of this? These are the questions we’ll be answering in this chapter, picking up from the previous chapter’s coverage of LANs. Here are the exam topics we will cover:

1.2 Describe characteristics of network topology architectures.

1.2.d WAN

5.5 Describe IPsec remote access and site-to-site VPNs.

16.1 WAN concepts
A WAN is a network that extends over a large geographic area, often spanning distances between cities or even countries. Enterprises use WANs to connect their various LANs, whether they are offices, retail stores, data centers, or any other kind of LAN—enterprises of all kinds use WANs. Figure 16.1 shows an enterprise WAN connecting five LANs (four offices and a data center) via a service provider network.



Figure 16.1 An enterprise WAN connecting four offices and a data center via a service provider’s network infrastructure

Note Figure 16.1 represents the WAN service provider network as a gray box. The CCNA covers WANs from the perspective of the customer (the enterprise connecting their LANs over the WAN), not the service provider. If you’re interested in the details of how service provider networks work, consider the CCNP Service Provider certification in the future.

Using the WAN, hosts in one LAN can communicate with hosts in another LAN. For example, end-user devices in the office LANs can access files and applications hosted on servers in the data center. There are various WAN technologies that make this possible. In this section, we’ll cover two: leased lines and Multiprotocol Label Switching (MPLS). Then, we’ll move on to examine the public internet and its role in connecting remote sites.

16.1.1 Leased lines
A leased line is a dedicated physical connection between two sites, providing fixed bandwidth that is reserved for that specific connection. Figure 16.2 shows an example of leased lines connecting four office sites to a central data center in a hub-and-spoke topology.



Figure 16.2 Four leased lines providing dedicated connections between each of four office sites and a central data center in a hub-and-spoke topology

Note As mentioned in chapter 15, star and hub-and-spoke both refer to a topology in which all devices connect to one central device. Star is commonly used in a LAN context, and hub-and-spoke in a WAN context.

Because the connection is typically not shared with other customers, the available bandwidth is consistent; the connection won’t get clogged up with other customers’ traffic. The dedicated nature of a leased line also provides security benefits—it’s a truly private connection.

However, leased lines have their downsides compared to more modern solutions: higher cost and lower bandwidth. Due to their price, hub-and-spoke topologies are more common than mesh topologies; the hub-and-spoke topology shown in figure 16.2 requires 4 leased lines, whereas a full mesh would require 10. Considering that each leased line can cost hundreds or even thousands of dollars per month, a full mesh can often be cost prohibitive.

Traditionally, leased lines use serial connections, not Ethernet; I briefly mentioned serial connections in chapter 18 of volume 1 when covering the OSPF point-to-point network type. For reference, table 16.1 lists some different standards of serial leased lines.

Table 16.1 Serial leased line options

| North America | | Europe (and others) | |
|--------|---------------|--------|---------------|
| Name   | Speed         | Name   | Speed         |
| T1     | 1.544 Mbps    | E1     | 2.048 Mbps    |
| T2     | 6.312 Mbps    | E2     | 8.448 Mbps    |
| T3     | 44.736 Mbps   | E3     | 34.368 Mbps   |
| T4     | 274.176 Mbps  | E4     | 139.264 Mbps  |
| T5     | 400.352 Mbps  | E5     | 565.148 Mbps  |


In many countries, leased lines are considered a legacy technology and have been largely replaced by Ethernet connections. However, leased lines can still be found in networks all over the world.

Note These days, the term leased line can be used more broadly to refer to any dedicated connection, such as a fiber-optic Ethernet connection. But from a CCNA perspective, a leased line is specifically a dedicated serial connection.

16.1.2 Multiprotocol Label Switching
As you’re well aware by now, routers forward packets based on their destination IP address. However, that isn’t always the case. Multiprotocol Label Switching (MPLS) is a common WAN technology that uses labels (not IP addresses) to route packets to their destination. The MPLS label is an additional header that is added to a message by a router at the edge of the MPLS network—typically, a router belonging to a WAN service provider. Figure 16.3 shows the position of the MPLS label in a message. Due to the label’s position between the Layer 2 and Layer 3 headers, MPLS is often called a Layer 2.5 protocol.



Figure 16.3 The MPLS label is inserted between the Layer 2 and Layer 3 headers.

Note Multiprotocol refers to the fact that MPLS can encapsulate a variety of packet types—not just IP packets. However, in modern networks, MPLS usually carries IP (IPv4 or IPv6) packets.

MPLS labels offer a more efficient way to route packets through a network, reducing the burden on routers. Instead of examining the entire packet header and performing a lookup in the routing table for each hop, routers simply read the fixed-length MPLS label and forward the packet based on a predetermined path.

Figure 16.4 shows a service provider’s MPLS network with four connected LANs belonging to two separate customers. This is an important point about MPLS: as opposed to a leased line, which provides a dedicated connection between two sites, a service provider’s MPLS network is a shared infrastructure over which multiple customers can connect.



Figure 16.4 Two customers connect their remote sites via a service provider’s MPLS infrastructure.

Figure 16.4 also introduces three different roles that routers can play in an MPLS WAN: customer edge (CE), provider edge (PE), and provider (P) routers:

CE router—A router located at the customer’s premises that connects the customer’s network to the service provider’s network. This is typically under the control of the customer, not the service provider.

PE router—A router located at the edge of the service provider’s network that connects to the customer’s network. PE routers are responsible for assigning and removing labels to/from the customer’s packets.

P router—A router that is internal to the service provider’s network. The router doesn’t connect to the customer’s network directly but is responsible for forwarding labeled packets across the service provider’s network.

Note The CE routers don’t actively participate in MPLS; they send and receive regular IP packets. MPLS labels are only used by the service provider routers (PE/P).

Although customers connect to the same MPLS infrastructure, MPLS labels offer a secure way to segregate the traffic of each customer through virtual private networks (VPNs). By assigning unique labels to different customer data streams, MPLS ensures that each customer’s traffic is kept separate and isolated within their own VPN, despite sharing the same MPLS infrastructure. Let’s look at two types of MPLS VPNs: L2VPN and L3VPN.

Note A virtual private network (VPN) is a secure virtual connection over shared infrastructure. In this chapter, we’ll examine two types of VPNs: MPLS VPNs and internet VPNs.

MPLS Layer 2 VPNs

In an MPLS Layer 2 VPN (L2VPN), the service provider network is transparent to the CE routers. In effect, the service provider network functions like a giant switch, forwarding frames between each customer’s CE routers (hence “Layer 2” in the name). Figure 16.5 shows two customers connected to a service provider’s MPLS L2VPN service.



Figure 16.5 Two customers connect their remote sites using a service provider’s MPLS L2VPN service. PE and P routers are not shown.

To exchange routing information, each customer’s routers form dynamic routing protocol neighbor relationships with each other over the MPLS infrastructure. In figure 16.5’s example, Customer A uses OSPF to exchange routing information between its Site 1 and Site 2 routers, and Customer B uses EIGRP between its routers. The service provider network functions like a switch, forwarding the OSPF/EIGRP messages between the routers. Here are a couple of other takeaways from figure 16.5:

Customers can use private IP addresses for their connections. The service provider’s MPLS infrastructure isn’t the internet—public addresses aren’t necessary.

Both customers use the 10.0.0.0/30 subnet for their connection. This isn’t a problem; it doesn’t matter if they overlap. Although they connect to shared MPLS infrastructure, each VPN functions as an isolated, private network.

MPLS Layer 3 VPNs

MPLS Layer 3 VPNs (L3VPN) take a different approach from L2VPNs. Instead of the service provider network acting like a giant switch connecting CE routers. The service provider routers actively participate in the routing process; the PE routers form dynamic routing protocol relationships with the CE routers. Figure 16.6 demonstrates this.



Figure 16.6 Two customers connect their remote sites using a service provider’s MPLS L3VPN service. CE routers form dynamic routing protocol neighbor relationships with PE routers.

Note As in the L2VPN example, the customers use overlapping private addresses in this example. This is not a problem; customer networks are isolated from each other despite connecting to the same MPLS infrastructure.

In MPLS L3VPNs, the service provider routers (specifically, the PE routers) maintain a separate routing table for each customer, ensuring traffic separation and security. This is achieved using Virtual Routing and Forwarding (VRF)—a topic we’ll cover in the next chapter.

The customer’s CE routers and the service provider’s PE routers establish routing protocol adjacencies, allowing for the exchange of routing information. As a result, the underlying infrastructure of the service provider becomes an extension of the customer’s IP network, offloading some of the routing complexities to the service provider.

The appropriate MPLS service—L2VPN or L3VPN—depends on the needs and preferences of each customer. If the customer wants to maintain complete control over their routing policies, L2VPN is likely the better choice. For example, security policy might dictate that routing must be strictly controlled, and information about internal networks should not be advertised to the service provider routers. If the customer is comfortable with letting the service provider participate in the routing process (and sharing routing information with the service provider), L3VPN might be appropriate.

Note In both cases (L2VPNs and L3VPNs), MPLS is the underlying technology that enables the VPN, although the implementation is different.

Connecting to an MPLS service provider

MPLS is a technology used by WAN service providers to enable customers to connect their remote sites. But how can customers connect their devices (CE routers) to the service provider’s MPLS infrastructure (PE routers)? There are various options, such as

Ethernet—This is the most common option, as Ethernet supports high speeds and long distances (especially fiber-optic Ethernet).

Leased line—A serial leased line can be used to connect the CE and PE routers.

Wireless (cellular 3G/4G/5G networks)—This option is convenient for temporary setups, mobile operations, and remote locations where wired access is impractical.

16.2 Internet connections
The internet is a vast, interconnected “network of networks” that spans the globe, enabling the exchange of information among billions of devices. It is the foundational infrastructure that supports countless applications and services, such as email, web browsing, and streaming. Figure 16.7 shows a simplified image of the internet.



Figure 16.7 The internet is a network of networks—thousands of ISP networks and customer networks connected to share resources.

The internet has become so ubiquitous in most of our lives that we take it for granted. The details of how it works—the inner workings of ISP networks—are beyond the scope of the CCNA exam. However, understanding the internet from the perspective of an ISP’s customers (an enterprise or consumer connected to the internet) is essential. Just as there are numerous ways to connect to a service provider’s MPLS infrastructure, multiple methods exist for a customer to connect to their ISP’s internet infrastructure.

In this section, we’ll look at a few methods of connecting to the internet. Then, in the next section, we’ll look at how to use VPNs to create private WAN connections over the internet, similar to the MPLS VPNs we covered in the previous section.

16.2.1 Digital subscriber line
Digital subscriber line (DSL) is a technology that transmits digital data over standard telephone lines and is a common method of connecting to the internet. A DSL modem (modulator-demodulator) is required to convert data into a format suitable to be sent over the phone lines. The modem might be a separate device, or it might be incorporated into the wireless home router. Figure 16.8 shows a SOHO network with a DSL internet connection.



Figure 16.8 A SOHO network connecting to the internet via DSL. A DSL modem translates between Ethernet and the signaling used on telephone lines. A splitter is used to allow both the telephone and modem to connect to a single phone line. The splitter is also called a DSL filter, as it serves to filter the DSL and telephone signals to prevent interference between them.

Note The wireless router is represented as a gray box with standard icons representing each of its different functions.

While it’s an older technology, DSL is still prevalent in many areas, especially in SOHO networks. One major advantage of DSL is that it uses existing telephone lines, so customers can connect without the need to install new cabling to their premises.

16.2.2 Cable internet
Cable internet, also called cable TV (CATV) internet, is similar to DSL in that it takes advantage of preexisting infrastructure—cable TV lines that already connect to many homes—to connect to the internet. As with DSL, a modem is required to translate between Ethernet and the signaling used on the CATV lines. Figure 16.9 shows a SOHO network with a cable internet connection.



Figure 16.9 A SOHO network network connecting to the internet via the same CATV line used for television. A cable modem translates between Ethernet and the signaling used on CATV lines. A splitter is used to allow both the TV and modem to connect to a single CATV line.

Like DSL, cable internet is still quite common, particularly in SOHO networks. By enabling internet access over existing infrastructure, the financial cost of internet access is greatly reduced.

16.2.3 Fiber-optic Ethernet
Another option for internet connectivity that is gaining in popularity is fiber-optic Ethernet. Unlike DSL and cable internet, which use existing telephone and CATV lines, fiber-optic connections require the installation of fiber-optic cables to the customer’s premises. Furthermore, a device called an optical network terminal (ONT) or optical network unit (ONU) is typically needed to convert the light signals from the fiber into the electrical signals used by copper UTP cables. Figure 16.10 shows a SOHO network with a fiber-optic internet connection.



Figure 16.10 A SOHO network connecting to the internet via fiber-optic Ethernet. An ONT/ONU converts between light and electrical signals.

While the installation of fiber-optic cables might seem like a drawback due to the initial investment required, the benefits are significant; fiber-optic connections offer much higher speeds than DSL or CATV. As demand for high-speed internet continues to grow, fiber-optic Ethernet is increasingly popular in both SOHO and enterprise networks. In urban areas and new residential developments, fiber is quickly becoming the standard, with many ISPs offering fiber-to-the-home (FTTH) services.

Note Although figures 16.8, 16.9, and 16.10 use a SOHO network as an example, all three of these internet connection options can be used by larger enterprises, too.

16.2.4 Wireless 3G/4G/5G
The final option we’ll cover is wireless 3G, 4G, and 5G; these stand for third, fourth, and fifth generation, respectively. If you have a mobile phone with a data plan, it likely supports one or more of these technologies for mobile internet access.

Note You might have heard of Long-Term Evolution (LTE) as well. LTE is considered a part of the 4G family of standards. While initially LTE did not meet the strictest definitions of 4G, advancements in LTE technology have led to its widespread acceptance as a 4G standard, so the terms are sometimes used interchangeably.

Figure 16.11 shows a typical setup where mobile phones connect to the internet via a cell tower, which then connects to the ISP. It also shows another use case for these technologies: a router with the appropriate radio can connect to the internet in the same manner, providing internet access for devices in its connected LAN.



Figure 16.11 Wireless 3G/4G/5G internet access. Devices wirelessly connect to a cell tower, which connects to the ISP infrastructure.

Note 3G and 4G are rarely used as a LAN’s primary internet connection; they are more common for temporary setups, mobile operations, remote locations, or as a backup connection. However, more recently, the newer 5G standard has gained prominence as a primary internet connection in many networks.

16.2.5 Redundant internet connections
In many SOHO networks, temporarily losing access to the internet might be annoying and inconvenient, but it probably wouldn’t be a catastrophe. However, this is not the case for larger enterprises, for which even a short outage can have major negative effects in terms of reputation and revenue. In such networks, it is essential to have redundant internet connections. Figure 16.12 introduces some internet connection designs, from single-homed (no redundancy) to dual multi-homed (high redundancy).



Figure 16.12 internet connection designs. Single-homed = one connection to one ISP. Dual-homed = two connections to one ISP. Multi-homed = one connection to each of two (or more) ISPs. Dual multi-homed = two connections to each of two (or more) ISPs.

In a single-homed design, there is one connection to one ISP. This is common in SOHO networks; if you have internet access at home, it’s probably using a single-homed design. A simple way to improve the redundancy of such a design is to add a second connection to the same ISP; if there is a problem with one connection, the other can be used instead. This is called a dual-homed design.

Note Figure 16.12’s dual-homed design shows two routers, each with one connection to the ISP. Another option is to have two connections from a single router. However, the dual-router design provides better redundancy; if a hardware failure causes one router to go down, the other one is still available.

Although a dual-homed design provides superior redundancy to a single-homed design, it still relies on a single ISP. If that ISP has issues, both connections may be affected. To avoid such situations, you can employ a multi-homed design, which has one connection to each of two (or possibly more) ISPs. If one ISP has issues, the network can still operate via the other ISP’s connection.

For most enterprises, a multi-homed design provides sufficient redundancy. However, networks for which continuous internet connectivity is absolutely critical may opt for a dual multi-homed design—two connections to each of two (or more) ISPs. This provides the highest level of redundancy.

Note Just as redundancy increases in the order we examined these designs (single-homed, dual-homed, multi-homed, dual multi-homed), so do cost and complexity. Although a dual multi-homed design provides the highest redundancy, its higher cost and complexity mean that it is not always the best choice.

16.3 Internet VPNs
So far, we’ve covered a couple of WAN technologies (leased lines and MPLS) and different types of internet connections. You might be wondering: “Is the internet a WAN?” The answer to that question is “both yes and no.”

The definition of WAN I gave earlier in this chapter is “a network that extends over a large geographic area.” In that sense, the internet absolutely is a WAN—it extends across the entire globe. However, the term WAN is typically used in the context of a private network that connects remote sites (branch offices, data centers, etc.) of a specific organization.

While the internet can serve that purpose, its public nature goes against the private aspect of most WANs. Although you can connect remote sites over the internet, additional steps are necessary to keep communications secure: you should use VPNs. Just as MPLS can create VPNs over shared infrastructure, there are multiple techniques to create VPNs over the public internet.

In this section, we’ll examine two types of internet VPNs: site-to-site VPNs and remote access VPNs. Table 16.2 summarizes their characteristics.

Table 16.2 Site-to-site and remote access VPNs

|                    | Site-to-site VPN                          | Remote access VPN                              |
|--------------------|-------------------------------------------|------------------------------------------------|
| Common protocol    | IPsec                                     | TLS                                            |
| Use case           | Permanent connection between two sites    | On-demand access to enterprise resources       |
| How many hosts served? | Serves many hosts within the connected sites | Serves the one host with the VPN client installed |

Exam Tip Internet VPNs are covered in CCNA exam topic 5.5: Describe IPsec remote access and site-to-site VPNs. Make sure you know the characteristics of each type.

16.3.1 Site-to-site VPNs (Internet Protocol Security)
A site-to-site VPN is a VPN between two devices for the purpose of (as the name suggests) connecting two sites over a non-private network (such as the internet). The most common protocol used for site-to-site VPNs is Internet Protocol Security (IPsec), which creates a secure VPN tunnel—a virtual pathway—between two devices, allowing for secure, private communications over the public internet. Figure 16.13 demonstrates how an IPsec tunnel works.



Figure 16.13 A site-to-site IPsec VPN provides a secure virtual pathway between two sites. Traffic is encrypted only when sent over the internet.

Note Although the message is shown going through the IPsec tunnel, keep in mind that the bits still physically pass through the internet connection. A tunnel is a virtual pathway, but it doesn’t create a new physical path for bits to travel over.

The concept of tunneling can be hard to wrap your head around at first. Basically, it’s the process of encapsulating a packet inside of another packet. Figure 16.14 illustrates how it works, representing a packet as a box:

R1 receives a packet destined for SRV1.

R1 encrypts the packet, concealing both its intended destination and its contents.

R1 encapsulates that encrypted packet inside of another packet that is destined for R2.

R1 forwards that packet over the internet toward R2.

R2 receives the packet and de-encapsulates it, revealing the encrypted packet inside.

R2 decrypts the internal packet.

R2 forwards the decrypted packet to its intended destination, SRV1.



Figure 16.14 A tunnel is created by encapsulating a packet inside of another packet. This outer packet provides a “tunnel” for the inner packet to travel through without being exposed to the internet.

Figure 16.15 provides a more technical image of the encryption and encapsulation process. The original IP packet is first encrypted, then encapsulated with an IPsec header and a new IP header, and then forwarded.



Figure 16.15 Tunneling an IP packet with IPsec. The IP packet is encrypted, encapsulated with an IPsec header and a new IP header, and then forwarded.

A site-to-site VPN tunnel is a permanent virtual connection between two devices; it remains until you remove the relevant configurations. The tunnel allows hosts in remote sites to communicate with each other without the need to create a VPN for themselves. Hosts can send unencrypted data to their site’s router, which will encrypt the data and forward it through the tunnel to the remote site. Thanks to the cryptographic technologies employed by IPsec, only the two routers that have formed the tunnel—R1 and R2, in our example—can decrypt packets encrypted by each other; only R2 can decrypt R1’s encrypted packets, and only R1 can decrypt R2’s encrypted packets.

Note IPsec is actually a suite of protocols, rather than a single protocol. There is some variability in how IPsec works depending on which protocols (and which operational mode) are used, but those details are beyond the scope of the CCNA exam.

GRE over IPsec

IPsec on its own has some limitations. One of those limitations is that it doesn’t support broadcast and multicast traffic—only unicast. This limitation can affect routing protocols like OSPF, which rely on multicast messages (sent to multicast addresses 224.0.0.5 and 224.0.0.6, as we covered in chapter 18 of volume 1).

One solution to this limitation is to combine IPsec with another tunneling protocol called Generic Routing Encapsulation (GRE). Like IPsec, GRE tunnels packets by encapsulating them with additional headers. However, GRE does not encrypt the original packet, so it is not secure; an attacker who gets access to a message traveling in a GRE tunnel can read the message’s contents. However, GRE has the advantage of supporting broadcast and multicast messages.

Note GRE creates tunnels but not VPNs. Because GRE doesn’t encrypt messages, its tunnels aren’t private or secure on their own.

To take advantage of both the flexibility of GRE and the security of IPsec, you can use GRE over IPsec. This does add some extra complexity, but it’s a common solution if you need to send multicast packets (i.e., OSPF messages to exchange routing information) over the tunnel.

Figure 16.16 shows how GRE over IPsec works. An IP packet is first encapsulated with a GRE header and a new IP header. Then, the entire GRE packet is encrypted and encapsulated with an IPsec header and additional IP header and then forwarded. Yes, this means that there are three IP headers in total: the original IP packet’s header, the IP header added by GRE, and the IP header added by IPsec.



Figure 16.16 GRE over IPsec works by encapsulating an IP packet with GRE and IP headers, encrypting the GRE packet, and encapsulating the encrypted packet with IPsec and IP headers.

Note The interior packet might be unicast, broadcast, or multicast, but the GRE packet itself is always unicast; it’s always destined for the router at the other end of the tunnel. This means that GRE can always be encapsulated by IPsec.

GRE over IPsec creates a tunnel within a tunnel. The original IP packet travels in the GRE tunnel, which is contained in the IPsec tunnel. Figure 16.17 illustrates this.



Figure 16.17 GRE over IPsec creates a tunnel within a tunnel. This combines the flexibility of GRE with the security of IPsec.

Dynamic Multipoint VPN

A second downside of IPsec is that it can be labor intensive to configure and manage IPsec tunnels, especially with a large number of routers. Each time you add a new branch or location to your network, you have to set up individual VPN tunnels between that new location and all other existing locations, leading to a substantial increase in configuration complexity, and an increased likelihood of configuration errors.

Dynamic Multipoint VPN (DMVPN), developed by Cisco, is a solution that facilitates the creation of a full mesh of tunnels between routers. With DMVPN, you only have to configure a hub-and-spoke topology of tunnels; DMVPN will do the rest to create a full mesh. Figure 16.18 illustrates how DMVPN can help create a full mesh of IPsec tunnels.

Note DMVPN doesn’t have to use IPsec; it uses unencrypted GRE tunnels by default. However, IPsec is recommended for secure, encrypted VPN tunnels over the internet; unencrypted GRE tunnels are not secure.

The DMVPN hub router distributes information to each spoke router about how to form IPsec tunnels with the other routers. This allows the routers to create a full mesh of IPsec tunnels without requiring manual configuration of each tunnel.

Exam Tip For the exam, just know the basic purpose of DMVPN: it allows routers to automatically create a full mesh of tunnels from a hub-and-spoke configuration.



Figure 16.18 DMVPN automatically creates a full mesh of IPsec tunnels after configuring a hub-and-spoke topology.

Hub-and-spoke vs. full-mesh

A full-mesh topology provides a couple of key advantages. The first is redundancy; if a failure causes one tunnel to go down, other tunnels can be used to reach the destination. The second is reduced latency. Because the routers in each site can communicate directly with each other, latency is reduced compared to a hub-and-spoke topology (in which traffic between spoke routers must pass through the hub router).

However, a hub-and-spoke topology has its advantages, too. Because all traffic between two sites has to pass through the hub site, it’s easy to implement restrictions on those communications (for example, with a firewall at the hub site). Despite the advantages of full-mesh, security requirements may dictate that a hub-and-spoke topology is appropriate.

16.3.2 Remote access VPNs (Transport Layer Security)
A site-to-site VPN is a permanent virtual connection between two routers, providing a secure encrypted communication pathway for hosts connected to each router. A remote access VPN, on the other hand, is an on-demand VPN that allows an end user to securely access the company’s internal resources over the internet. The protocol of choice is typically Transport Layer Security (TLS), but IPsec is also an option. Figure 16.19 demonstrates remote access VPN connections.

Note TLS is often called Secure Sockets Layer (SSL). SSL is the name of a deprecated protocol that was replaced by TLS, but the SSL name is still common.



Figure 16.19 Remote access TLS VPNs provide secure access to the company’s internal resources over the internet.

Unlike a site-to-site VPN, which provides a virtual pathway for multiple hosts connected to the routers that establish the VPN, a remote access VPN establishes a VPN connection from each individual end-user device to the company’s firewall or router. This means that while multiple devices can simultaneously connect via remote access VPN, each device has its own encrypted tunnel that is not shared with other devices.

The end-user device runs a piece of software called a VPN client—Cisco’s offering is called Cisco AnyConnect Secure Mobility Client (usually just “AnyConnect”), but other vendors have their own offerings. This software allows the device to create its own tunnel to the company’s firewall or router, providing a secure communication pathway to reach resources on the company’s internal network (i.e., file servers). Remote access VPNs are particularly useful in remote work situations, which have become increasingly common.

Transport Layer Security and HTTPS

TLS, commonly used for remote access VPNs, is also the protocol that secures Hypertext Transfer Protocol Secure (HTTPS), which is used to securely access web pages. Whereas a remote access VPN creates a TLS VPN tunnel between your device and a firewall/router, HTTPS creates a TLS VPN tunnel between your device and the web server that hosts the web page you are accessing.

Exam Tip For the exam, know that a remote access VPN allows a single device to securely access internal resources through a TLS tunnel. The details of the TLS protocol itself are beyond the scope of the CCNA.

Summary
A wide area network (WAN) is a network that extends over a large geographic area, often spanning distances between cities or even countries. Enterprises use WANs to connect their various LANs.

A leased line is a dedicated physical connection between two sites, providing fixed bandwidth that is reserved for that specific connection.

Leased lines are secure because they are private; they are not shared with other customers. However, they are typically more expensive and offer lower bandwidth than more modern solutions.

Leased lines traditionally use serial connections, not Ethernet. However, service providers sometimes offer fiber-optic Ethernet leased lines.

Multiprotocol Label Switching (MPLS) is a common WAN technology that uses labels (not IP addresses) to route packets to their destination.

The MPLS label is an additional header that is added between the Layer 2 and Layer 3 headers of a message.

Unlike a leased line, a service provider’s MPLS network is shared infrastructure over which multiple customers can connect.

There are three main roles that routers can play in an MPLS WAN: customer edge (CE), provider edge (PE), and provider (P).

A CE router is located at the customer’s premises and connects the customer’s network to the service provider’s network. It is typically under the control of the customer, not the service provider.

A PE router is located at the edge of the service provider’s network and connects to the customer’s network. PE routers are responsible for assigning and removing labels to/from the customer’s packets.

A P router is internal to the service provider’s network and doesn’t connect to the customer’s network directly. P routers are responsible for forwarding labeled packets across the service provider’s network.

Although customers connect to the same MPLS infrastructure, MPLS labels offer a secure way to segregate the traffic of each customer through virtual private networks (VPNs).

There are two main types of MPLS VPNs: L2VPN and L3VPN.

In an MPLS Layer 2 VPN (L2VPN), the service provider network is transparent to the CE routers. In effect, the service provider network functions like a giant switch, forwarding frames between each customer’s CE routers.

To exchange routing information, CE routers form dynamic routing protocol neighbor relationships with each other over the MPLS infrastructure.

In an MPLS Layer 3 VPN (L3VPN), the service provider routers actively participate in the routing process. The PE routers form dynamic routing protocol neighbor relationships with the CE routers.

In both cases (L2VPNs and L3VPNs), MPLS is the underlying technology that enables the VPN, although the implementation is different.

The internet is a vast, interconnected “network of networks” that spans the globe, connecting thousands of internet service providers (ISPs) and their customers. There are various methods for connecting to an ISP.

Digital subscriber line (DSL) is a technology that transmits digital data over standard telephone lines and is a common method of connecting to the internet.

A DSL modem (modulator-demodulator) is required to convert data into a format suitable to be sent over the phone lines. The modem might be a separate device, or it might be incorporated into the wireless home router.

One major advantage of DSL is that it uses existing telephone lines, so customers can connect to the internet without the need to install new cabling.

Cable internet is similar to DSL in that it takes advantage of preexisting infrastructure: cable TV lines that already connect to many homes.

Just as DSL uses a modem, a cable modem is required to translate between Ethernet and the signaling used on the CATV lines.

Fiber-optic Ethernet connections are another common internet connection method. Unlike DSL and cable internet, which use existing telephone and CATV lines, fiber-optic connections require the installation of fiber-optic cables.

Furthermore, a device called an optical network terminal (ONT) or optical network unit (ONU) is typically needed to convert the light signals from the fiber into the electrical signals used by copper UTP cables.

As demand for high-speed internet grows, fiber-optic Ethernet is an increasingly common internet connection method in both SOHO and enterprise networks.

Another option is wireless 3G, 4G/LTE (Long-Term Evolution), and 5G; these stand for third, fourth, and fifth generation, respectively.

Mobile phones often use 3G/4G/5G for internet access. A router with the appropriate radio can also use these technologies to connect to the internet.

Redundant internet connections are imperative for enterprises that rely on continuous internet connectivity.

A single-homed internet connect design involves one connection to one ISP. This does not provide redundancy but is common in SOHO networks.

A dual-homed design involves two connections to one ISP; this adds some redundancy but is still vulnerable to issues that affect the ISP as a whole.

A multi-homed design involves one connection to each of two (or more) ISPs, providing resilience to issues that affect one of the ISPs.

A dual multi-homed design involves two connections to each of two (or more) ISPs. This provides the highest level of redundancy but is not necessary for most networks.

Is the internet a WAN? Yes and no. The internet is a WAN in that it extends over a large geographic area—the entire globe. However, the term WAN is typically used in the context of a private network that connects an organization’s sites.

The public nature of the internet makes it inappropriate for WAN connections without additional security measures: you should use VPNs.

A site-to-site VPN is a VPN between two devices (routers) for the purpose of connecting two sites over a non-private network (such as the internet).

The most common protocol used for site-to-site VPNs is Internet Protocol Security (IPsec), which creates a secure VPN tunnel—a virtual pathway—between two devices, allowing for secure, private communications over the public internet.

Tunneling involves encapsulating a packet inside of another packet. The outer packet provides a tunnel for the inner packet to travel through without being exposed to the internet.

IPsec encrypts the original packet before encapsulating it with an IPsec header and a new IP header.

IPsec only supports unicast traffic. To support broadcast and multicast traffic, you can combine IPsec with Generic Routing Encapsulation (GRE).

GRE creates tunnels that support various kinds of traffic but doesn’t encrypt the contents. By combining GRE with IPsec, you take advantage of GRE’s flexibility and IPsec’s security; this is called GRE over IPsec.

Configuring a full mesh of IPsec tunnels between routers is labor intensive and prone to configuration errors. Dynamic Multipoint VPN (DMVPN) is a solution that facilitates the creation of a full mesh of tunnels between routers.

With DMVPN, you only have to configure a hub-and-spoke topology of tunnels. The hub router will then distribute information to the spoke routers, allowing them to form a full mesh of tunnels with each other.

A remote access VPN is an on-demand VPN that allows an end user to securely access the company’s internal resources over the internet. The protocol of choice is typically Transport Layer Security (TLS).

A remote access VPN establishes a VPN connection from each individual end-user device to the company’s firewall or router. While multiple devices can simultaneously connect, each device has its own encrypted tunnel that is not shared.

The end-user device runs a piece of software called a VPN client—Cisco’s offering is called Cisco AnyConnect Secure Mobility Client, or just AnyConnect. This software allows the device to create its own tunnel to the company’s firewall or router.