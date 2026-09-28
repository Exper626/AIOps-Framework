15 LAN architectures
This chapter covers

Star and mesh topologies
Two- and three-tier campus LANs
The advantages of spine-leaf architecture in data center networks
Small office/home office networks
We have delved into the details of protocols like IPv4 and IPv6, Ethernet, Spanning Tree Protocol, and many others in previous chapters of this volume and volume 1. Now it’s time to zoom out. Instead of focusing on individual technologies, let’s take a holistic view of real-world network architectures—the blueprints for how computer networks are designed and built.

Although there are standard best practices in network design, many factors such as budget, scale, and specific needs influence the “right” approach; there are few universal correct answers to questions of network design. In the beginning stages of your networking career, you probably won’t be designing networks. However, to configure and troubleshoot networks, understanding the architectural principles behind them is essential.

This chapter and the following two align with CCNA exam topic 1.2: Describe characteristics of network topology architectures. This chapter focuses on various types of LANs, from data centers to home offices. Specifically, we will cover the following subtopics:

1.2.a Two-tier

1.2.b Three-tier

1.2.c Spine-leaf

1.2.e Small office/home office (SOHO)

15.1 Common topologies: Star and mesh
In chapter 14 of volume 1, I defined the term topology as “how devices are arranged and connected together in a network.” Some common topologies consistently emerge across different networks—common patterns of device connections. Figure 15.1 demonstrates three of those common topologies: star, full mesh, and partial mesh.



Figure 15.1 Common topologies. In a star topology, all devices connect to a central device. In a full mesh, each device is directly connected to each of the other devices. In a partial mesh, only certain devices are directly connected.

In a star topology, all devices connect to one central device. The most common example of a star topology, and the one shown in figure 15.1, is a group of end hosts connected to a switch.

Note Another name for a star topology is hub-and-spoke topology. The central device is the hub, and the devices connecting to it are the spokes. Star is more commonly used in a LAN context, and hub-and-spoke in a WAN context.

In a full mesh, each device in the topology is directly connected to each of the other devices. Full-mesh topologies provide high reliability because there are multiple possible paths to each destination; if there is a problem with one path, multiple other paths are available. Figure 15.1 shows six routers connected in a full mesh. Although they appear as direct connections, in reality, these would likely be secure virtual private network (VPN) connections over a service provider’s network—we’ll delve into VPNs in chapter 16.

Note You can calculate the number of connections between devices in a full mesh with the formula N(N-1)/2, where N is the number of devices. For example, with six devices, there are 15 links.

There is also partial mesh, in which certain devices, but not all, are directly connected to each other. You’ll see this pattern between the switches in the access layer and distribution layer of a campus LAN—the topic of the next section.

Most networks are a combination of these common topologies and others—a hybrid topology. These terms are all commonly used to describe how devices are connected in networks. Keep an eye out for these recurring patterns as we examine different network architectures in this chapter and the next.

15.2 Campus LAN architectures
A campus LAN is a network that is designed to serve the networking needs of local users within a certain area. Although the term campus evokes the idea of a network spread across multiple buildings in close proximity, like a university campus or office park, in this context, it doesn’t imply any particular geographic size. A campus LAN could be a small site with a single switch or a multibuilding campus stretching across an office park.

Cisco campus LANs use a hierarchical design, dividing the network into three modular layers, each playing a specific role. The three layers are

Access layer—Provides access to the network for end hosts

Distribution layer—Aggregates connections from the access layer and provides connectivity to the WAN and the internet

Core layer—Aggregates connections between distribution layers in large LANs

Cisco campus LAN architecture is not one-size-fits-all; depending on the site, one, two, or all three layers might be present. Figure 15.2 shows a simplified three-building campus LAN that includes all three layers: access, distribution, and core.

Note Figure 15.2 only shows one connection between each layer. This doesn’t represent the actual number of physical connections needed to connect all devices. Later diagrams will show the connections in greater detail.



Figure 15.2 A three-tier campus LAN spanning three buildings. End hosts connect to the access layer, the distribution layer aggregates connections from the access layer, and the core layer aggregates connections from the distribution layer.

As mentioned previously, the layers are modular, allowing for flexible scalability; these modular pieces are sometimes called blocks. Figure 15.2 shows three access layer blocks, each connected to its own distribution layer block. As the network expands, additional access and/or distribution blocks can be added as needed.

Exam tip Two- and three-tier architectures are exam topics 1.2.a and 1.2.b, respectively. For the exam, make sure you know the characteristics of each layer.

15.2.1 Two-tier (collapsed core) LAN architecture
The CCNA exam topics list states that you must be able to describe two- and three-tier campus LANs. We will start small, with two-tier campus LANs. This kind of design is also called collapsed core because the core layer is absent—only the access and distribution layers are present.

Note Another way to think of a collapsed core is that core and distribution layers are combined into one. For this reason, the second layer of a two-tier LAN is sometimes called the core-distribution layer.

The access layer is typically where end hosts connect to the network. That includes end-user devices like PCs and phones, security devices like security cameras and door locks, servers, and others. Given that, here are some features you can expect to find in the access layer of a campus LAN:

QoS marking is often done here. As mentioned in chapter 10, marking should be done early in a packet’s life.

Security services such as Port Security, DHCP Snooping, and DAI should be used here to secure the point where users connect to the network.

The switches will likely support PoE to provide electrical power to devices like IP phones, wireless access points, security cameras, etc.

With more than two or three access switches at a site, directly interconnecting them all quickly becomes impractical. Instead, distribution switches are used to aggregate connections from access switches. The distribution layer also typically connects to the corporate WAN and/or the internet. Figure 15.3 shows an example of a two-tier campus LAN with WAN and internet connections.



Figure 15.3 A two-tier campus LAN consists of access and distribution layers.

Note In figure 15.3, notice that there are two distribution switches, two WAN connections, two internet connections, etc. Redundancy is a critical aspect of an enterprise network.

The Layer 2–Layer 3 border

The distribution layer usually serves as the border between Layer 2 and Layer 3 of the TCP/IP model. Connections from the distribution layer to the access switches are Layer 2 connections (trunk links), but connections to other parts of the network are Layer 3 connections (routed ports configured with no switchport). The distribution switches are multilayer switches that support both Layer 2 and Layer 3 features. Figure 15.4 demonstrates this concept.



Figure 15.4 The distribution layer typically serves as the border between Layer 2 and Layer 3 of the TCP/IP model.

To provide a redundant IP address that hosts in each VLAN can use as their default gateway, the distribution switches should use a first hop redundancy protocol like HSRP on each of their SVIs. Furthermore, a routing protocol like OSPF can be used to share routing information with the rest of the network. The following example shows how you might configure the SVI of a distribution switch (named DSW1 for distribution switch 1):

DSW1(config)# interface vlan 10                    ❶
DSW1(config-if)# ip address 10.0.0.2 255.255.255.0 ❷
DSW1(config-if)# standby 1 ip 10.0.0.1             ❸
DSW1(config-if)# standby 1 priority 105            ❹
DSW1(config-if)# ip ospf 1 area 0                  ❺
❶ Configures the VLAN 10 SVI

❷ Configures an IP address

❸ Configures the HSRP virtual IP

❹ Increases this SVI’s HSRP priority

❺ Enables OSPF on the SVI

Connecting multiple distribution blocks

As a two-tier campus LAN expands, you may need to add an additional block of distribution switches. Perhaps your company is opening another office in a new building, and the number of access switches is more than the current distribution switches can handle—the current switches don’t have enough available ports. Figure 15.5 shows a campus LAN with two access-distribution block pairs.

Note The connections between the distribution switches form a full mesh, and the connections between the access and distribution switches form a partial mesh; the access switches connect to each distribution switch but not to each other.



Figure 15.5 A two-tier campus LAN with two distribution and two access blocks

15.2.2 Three-tier LAN architecture
Large campus LANs often face the challenge of managing connectivity as they grow. A full mesh between distribution switches, as we saw in figure 15.5, might work well for smaller networks with a couple of distribution blocks. However, with three, four, or even more distribution blocks, this approach quickly escalates in complexity and cost.

In a campus LAN with three or more distribution blocks, you should consider adding a core layer, making a three-tier architecture. Figure 15.6 shows how adding a core layer can greatly reduce the number of connections required.



Figure 15.6 Two-tier vs. three-tier architectures with four distribution blocks. In the two-tier LAN, each distribution switch has seven connections. In the three-tier LAN, each distribution switch has only three connections.

Note Another option to reduce the number of connections required is to use a partial mesh between distribution switches instead of a full mesh. However, Cisco’s recommendation is to add a core when there are three or more distribution blocks.

Just as the distribution layer aggregates connections from the access layer, the core layer aggregates connections from the distribution layer. Using high-end switches, the focus of the core layer is speed and reliability; it should forward packets as quickly as possible and be able to maintain consistent connectivity throughout the LAN even if failures occur.

CPU-intensive operations like security features (DAI, etc.) and QoS marking, which can slow down the forwarding process, should be avoided at the core layer; the switches in the core layer should trust and forward packets based on the packets’ existing QoS markings.

All connections between the core and distribution layers should be Layer 3 connections—we don’t want STP disabling links that could otherwise be used to forward packets. A routing protocol like OSPF should be used to share routing information between the distribution and core switches. Figure 15.7 shows a core layer in the context of a whole three-tier LAN. It also shows a wireless LAN controller (WLC) and two wireless access points (WAPs), which are used to enable wireless LANs—a preview of the next part of this book.



Figure 15.7 A three-tier campus LAN with a core layer connecting three distribution blocks. One distribution block is used to connect to network services like a wireless LAN controller, the WAN, and the internet.

Note To avoid cluttering up the diagrams in this chapter, I only show a few access switches and end hosts in each diagram. In a large network, there could be 20+ access switches in each access block, each with 40+ end hosts connected.

15.3 Data center architectures: spine-leaf
A data center is a facility—either its own building or a dedicated space in a building—where an organization centralizes its IT infrastructure, particularly servers and the network infrastructure devices that support them. Data centers are vital for many modern enterprise networks, often housing thousands of servers, storage devices, and network devices. A Google search for “data center” will show you images of rows and rows of racks containing countless servers and other devices.

15.3.1 Traditional data center networks
Data center networks traditionally used a three-tier architecture similar to the campus LANs we saw in the previous section; figure 15.8 shows an example. Note that the distribution layer is typically called the aggregation layer in a data center context; their function is basically the same.



Figure 15.8 A three-tier data center LAN consisting of an access layer, aggregation layer, and core layer

Note Each group of servers and the access and aggregation switches that support them are called a pod.

However, the rise of virtual servers and distributed applications (applications that run on multiple computers and communicate through the network) led to an increase in the amount of east–west traffic in data centers. East–west traffic is traffic flowing between servers within the same data center—for example, communication between a server in pod 1 and a server in pod 3 in figure 15.8.

Note There is a related term—north–south traffic—that refers to traffic entering and exiting the data center (via the WAN or the internet).

The traditional three-tier architecture proved to be less than ideal for these kinds of applications, especially if traffic had to traverse multiple layers to reach another server in the same data center. This produces bottlenecks and variability in the server-to-server latency, leading to unpredictability in application performance.

15.3.2 Spine-leaf architecture
To better serve modern data center networks, spine-leaf architecture (also called Clos architecture, named after American engineer Charles Clos) has become the standard. Spine-leaf architecture provides high bandwidth with low and predictable latency for east–west traffic. Figure 15.9 demonstrates spine-leaf architecture, which consists of two layers: a layer of spine switches and a layer of leaf switches.



Figure 15.9 Spine-leaf architecture, a two-tier LAN architecture commonly used in modern data center networks

Note Leaf switches that connect to the WAN/internet or other external networks are sometimes called border leaves.

Here are some basic characteristics of spine-leaf architecture:

End hosts (servers) connect to leaf switches.

Every leaf switch connects to every spine switch.

Every spine switch connects to every leaf switch.

Leaf switches do not connect to other leaf switches.

Spine switches do not connect to other spine switches.

A key result of this architecture is that all leaf switches are the same number of hops apart. This means that the path a packet takes between two servers is always

Source server

Leaf switch

Spine switch

Leaf switch

Destination server

The consistent number of hops means that there should be consistent and predictable latency between servers in the network. The one exception is when the two servers are connected to the same leaf switch, in which case there is no need to traverse a spine switch, making the latency even shorter.

Another benefit of spine-leaf architecture is how simple it is to scale it to support large and complex data center networks. If you need to add more servers than the current network can handle, just add more leaf switches, connecting each new leaf to every spine switch.

Exam Tip Spine-leaf architecture is exam topic 1.2.c. Make sure you know its characteristics and benefits for the exam.

15.4 SOHO networks
In some networks, the complex designs we’ve looked at aren’t necessary. A network with only a few users, each with only a few devices, can often have its needs met by a single network device. A small office/home office (SOHO) network—a very small network with about 1 to 10 users—is an example.

Note A SOHO network can be a business or nonbusiness network. If your home has a network connected to the internet, it can be considered a SOHO network.

Because of their size and simplicity, it’s common for all networking functions in a SOHO to be provided by a single wireless router (also called a Wi-Fi router or home router). Figure 15.10 shows a photo of a simple wireless router.



Figure 15.10 A wireless router, including Wi-Fi antennas for wireless clients, switch ports for wired end-user devices, and a port for an internet connection

A wireless router combines the functions of various network devices into one:

A router that forwards packets between the LAN and the internet

A switch for wired end-user devices to connect to

A firewall that blocks connections from the internet

A wireless access point that allows wireless (Wi-Fi) clients to connect to the network

Figure 15.11 visually demonstrates this. The central gray box represents the wireless router, and the standard icons inside represent each of its functions.



Figure 15.11 A wireless router functions as a router, a switch, a firewall, and a wireless access point.

Note Some wireless routers also function as a modem (modulator/demodulator). A modem is necessary for some internet connection types. We’ll cover internet connections and modems in the next chapter.

In addition to relying on a single wireless router, most SOHO networks have only one internet connection. This lack of redundancy isn’t acceptable in enterprise networks like the ones we covered in previous sections. However, given the nature of most SOHO networks, a temporary loss of service would be more of an inconvenience than an emergency. The cost savings of a nonredundant setup are usually prioritized over the reliability of a redundant one.

Summary
Although there are standard best practices in network design, many factors such as budget, scale, and specific needs influence the “right” approach; there are few universal correct answers to questions of network design.

In a star topology, all devices connect to one central device. The most common example is a group of end hosts connected to a switch.

Another name for a star topology is hub-and-spoke topology. Star is more commonly used in a LAN context, and hub-and-spoke in a WAN context.

In a full-mesh topology, each device in the topology is directly connected to each of the other devices. A full mesh is often seen between the distribution switches of a two-tier campus LAN.

In a partial-mesh topology, certain devices, but not all, are directly connected to each other. You can find this pattern between the access and distribution switches of a two- or three-tier campus LAN.

Most networks are a combination of these common topologies and others—a hybrid topology.

A campus LAN is a network that is designed to serve the networking needs of local users within a certain area. Cisco campus LANs use a hierarchical design, dividing the network into three modular layers: access, distribution, and core.

The layers are modular, allowing for flexible scalability; these modular pieces are sometimes called blocks. Additional blocks can be added as the network expands.

In a two-tier campus LAN, only the access and distribution layers are present. For this reason, it’s sometimes called a collapsed-core architecture.

The access layer is typically where end hosts connect to the network. Some common features implemented at the access layer are QoS, security services (i.e. Port Security, DHCP Snooping, and DAI), and PoE.

The distribution layer aggregates connections from the access layer and also typically connects to the corporate WAN and/or the internet.

The distribution layer usually serves as the border between Layer 2 and Layer 3 of the TCP/IP model. Connections to the access switches are Layer 2 connections, but connections to other parts of the network are Layer 3 connections.

The distribution switches typically use an FHRP (like HSRP) on their SVIs to provide a redundant default gateway to hosts in the LAN and a routing protocol like OSPF to share routing information with the rest of the network.

In a campus LAN with three or more distribution blocks, you should consider adding a core layer—a three-tier architecture.

The core layer aggregates connections from the distribution layer, reducing the overall number of connections required.

The focus of the core layer is speed and reliability; it should forward packets as quickly as possible and be able to maintain consistent connectivity throughout the LAN even if failures occur.

CPU-intensive operations like security features and QoS marking, which can slow down the forwarding process, should be avoided at the core layer. All connections should be Layer 3.

A data center is a facility where an organization centralizes its IT infrastructure, particularly servers and the network infrastructure devices that support them.

Data center networks traditionally used a three-tier architecture similar to campus LANs (with the distribution layer being called the aggregation layer in data center contexts).

In a data center network, each group of servers and the access and aggregation switches that support them are called a pod.

The rise of virtual servers and distributed applications led to an increase in the amount of east–west traffic in data centers. East–west traffic is traffic flowing between servers within the same data center.

North–south traffic is traffic entering and exiting the data center (via the WAN or the internet).

The traditional three-tier architecture is not ideal for east–west traffic; it can lead to bottlenecks and variability in the server-to-server latency.

Spine-leaf architecture has become the standard in modern data center networks.

Spine-leaf architecture consists of two layers: a layer of spine switches and a layer of leaf switches. End hosts (servers) connect to leaf switches.

Leaf switches that connect to the WAN/internet or other external networks are sometimes called border leaves.

Every leaf switch connects to every spine switch, and every spine switch connects to every leaf switch.

Leaf switches do not connect to other leaf switches, and spine switches do not connect to other spine switches.

The result of this architecture is that all leaf switches are the same number of hops apart; they are all separated by one spine switch.

The consistent number of hops means that there should be consistent and predictable latency between servers in the network. The only exception is when the two servers are connected to the same leaf switch.

Spine-leaf architecture can be easily scaled by adding more leaf switches, connecting each new leaf to every spine switch.

A small office/home office (SOHO) network is a very small network, usually with 1 to 10 users (i.e., a small business or home network).

It’s common for all networking functions in a SOHO network to be provided by a single wireless router (also called a Wi-Fi router or home router).

A wireless router combines the functions of various network devices into one: router, switch, firewall, wireless access point, and sometimes modem (modulator-demodulator).

Most SOHO networks prioritize cost savings with a single router and internet connection, trading off the redundancy found in enterprise networks.