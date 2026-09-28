2 Network devices
This chapter covers

The definition of a network
Types of network devices, including clients, servers, switches, routers, and firewalls
This chapter is a high-level introduction to networks and some of the different types of devices that compose them. After looking at what a network is, we will examine clients, servers, switches, routers, and firewalls. We will look at the basic roles of each of these types of devices in a network, but we won’t get into any details about how they actually perform these roles—we’ve got the rest of the book to do that! By the end of this chapter, you will be able to identify each of the network devices in figure 2.1 and briefly explain their respective roles.

Figure 2.1 An enterprise network connecting multiple offices over the internet
Each office in figure 2.1 is a local area network (LAN), a group of interconnected devices in a limited area such as an office. Within each office in the diagram, you can find the kinds of network devices we will look at in this chapter: clients, servers, switches, routers, and firewalls. The connection between offices is called a wide area network (WAN)—a network that extends over a large geographical area (such as between cities). In volume 2 of this book, we will cover several WAN connection types. The internet, as represented by the cloud icon in figure 2.1, is just one of the options for connecting remote locations.

2.1 What is a network?
What is a network? As a general term, network can refer to many different things. A system of railways connecting towns and cities is a network. The veins and arteries in our bodies can be called a network. A group of people, such as business associates, can also be called a network. What do these all have in common? They are all about connecting people or things. In this book’s two volumes, we are looking at a specific kind of network: a computer network—a network that connects computers. A computer connected to a network can be many different things, including
A personal computer connected to the internet via a home network
A television that connects to the internet to stream Netflix
An iPhone connected to the internet via wireless 5G
A YouTube server that streams videos to devices all over the world
An enterprise’s servers that store private files and data
A security camera that saves footage to a server
We can define a computer network as a telecommunications network that allows nodes to share resources. That definition is certainly short and sweet, but you might be left with a couple of questions, like “What is a node?” and “What is a resource?”
A node is any device that connects to a network. It includes the previously listed examples, like a personal computer or an iPhone, as well as the network infrastructure that connects the devices—the routers, switches, firewalls, and various other types of devices that make up the network.
A resource is anything that can be accessed or used over the network. For example, if you use a web browser such as Google Chrome to access manning.com, the webpage that appears on your screen is a resource shared over the network. It is a file located on a server somewhere on the internet, and that server shares the webpage with the device you use to access the website. However, resources aren’t just files. There are countless examples, but here are a few:
A printer that is connected to the network and shared by users in an office
An online game server that supports multiplayer gaming
Cloud-based software like Gmail and Microsoft 365

2.2 Types of network devices
The previous discussion of nodes and resources leads us to this section. Let’s look at the types of nodes that share resources over a network, as well as the types of nodes that comprise the network infrastructure that facilitates the sharing of resources.

2.2.1 Clients and servers
First, we will look at the nodes that share resources over a network: clients and servers. We cannot understand one without understanding the other because they are defined by their relationship with each other: a client is a device that accesses a service provided by a server, and a server is a device that provides services for clients. Figure 2.2 shows the icons for clients and servers that we will be using throughout this book.
Figure 2.2 Icons representing a desktop computer and a file server. Icons like these are commonly used in network diagrams to represent clients and servers.
It’s important to note that clients and servers aren’t specific types of physical devices. Rather, they are roles that can be assumed by a variety of devices. If a device provides a service, such as hosting a webpage, that device is functioning as a server. If a device accesses a service, such as retrieving a webpage from a server, that device is functioning as a client.
Note The term server is also used to refer to a kind of device—a very powerful computer designed to be able to provide services to many clients, such as a YouTube server streaming video to thousands of clients over the internet. However, almost any kind of device can function as a server, so it’s better to think of a server as a role, not a specific kind of device.
Let’s list a few examples of client–server pairs:
Client—A network-enabled TV that streams a movie on Netflix
Server—A Netflix server that hosts the movie and sends it over the network

Client—An iPhone scrolling through X (formerly Twitter)
Server—X servers that host the tweets and send them to the iPhone
Client—A PC accessing an Excel spreadsheet located on an enterprise’s server
Server—An enterprise’s server containing spreadsheets and other internal files
Almost any node can be both a server and a client, depending on the context. For example, in a home network, it’s possible to share files among devices. You can transfer a movie file from one PC to another PC in the network. In that case, the PC where the movie file is located is a server, and the PC accessing the file is a client. If the file was shared in the opposite direction, the server and client roles would be reversed. And both PCs would be clients when they are accessing websites over the internet. Figure 2.3 shows a client–server relationship between two PCs.

Figure 2.3 Two desktop PCs sharing a file. The PC on the left is functioning as a client, and the PC on the right is functioning as a server.
Note Both devices in figure 2.3 use the client icon to emphasize that they are both PCs—the same kind of device—but their roles are different in this exchange.
Sometimes a network is as simple as two devices directly connected to each other. However, this type of connection is rare. To expand the network and allow more devices to communicate with each other, we need some specific types of devices to act as the network infrastructure and facilitate that communication.
Client and server nodes are often called endpoints or end hosts. These are general terms for devices that communicate over a network, as opposed to the network infrastructure devices that connect the end hosts.

2.2.2 Switches
Let’s build out the network further by connecting our end hosts to a switch, as in figure 2.4.

Figure 2.4 Three end hosts connected to a switch

Devices connected to a switch are able to communicate with each other via the switch. Note that they do not typically communicate with the switch itself—the switch only serves as infrastructure over which communication can occur.
The role of a switch is to connect devices within a LAN. For example, all of the PCs, security cameras, printers, servers, and other devices in an office are probably connected to one or more switches. For this reason, it’s common for switches to have many ports for end hosts to connect to—usually from 24 to 48 per switch.
Note A port is a physical connector on a device. Devices are physically connected by connecting one end of a cable to each of two devices. A port serves as the interface between one device and the other devices in the network. For that reason, the terms port and interface are often used interchangeably.
Switches use a variety of technologies to facilitate communications between the devices connected to them. In chapter 6, we will begin to learn exactly how switches do this. For now, it’s sufficient to know their basic purpose. Note that the role of a switch is not to provide connectivity between LANs or to external networks. For example, you would not connect a switch directly to the internet. For that, we need another type of device.

2.2.3 Routers
So far, we’ve connected end hosts to a switch to allow them to communicate with each other. Switches provide connectivity among devices within a LAN, but chances are we want our end hosts to be able to communicate with external networks, too. For example, for end hosts to communicate over the internet, we need a device that provides connectivity between LANs and the internet. That type of device is called a router. Figure 2.5 shows how routers are used to connect LANs to external networks, such as the internet.

Figure 2.5 Two LANs connected to the internet via a router at the edge of each LAN

Note A cloud icon is used in a network diagram to represent parts of a network that are unknown or unimportant to the diagram. For example, a cloud is often used to represent the internet. For the purpose of figure 2.5, we just need to know that the two LANs are connected to the internet. We do not need any details about what the internet (a very large and complicated network) actually looks like.
Routers are not used to connect many end hosts within a LAN. Instead, they are placed at the edge of a LAN and used to enable communications between LANs and external networks, such as the internet.
Like switches, routers use a variety of technologies to play their role in the network—facilitating communications between LANs. We will begin to look at how routers work in chapter 7, which covers IP addresses.

Wireless routers
You might be wondering, “If that’s a router, what is the wireless router that connects my home network to the internet?” A wireless router (also known as a Wi-Fi router or home router) is not just a router; it’s a multifunctional network device that combines the roles of multiple different network devices.
These devices typically fill the roles of a router, switch, wireless access point (to provide Wi-Fi connectivity), and firewall all in one device. They are perfect for a small office/home office (SOHO) network with only a few users. However, in enterprise networks, it’s simply not feasible for a single device to fulfill all necessary roles.

2.2.4 Firewalls
Devices in the two LANs in figure 2.5 are perfectly capable of communicating with each other and with other devices over the internet. However, by allowing our devices to communicate over the internet, we are exposing them to potential security risks. The internet is a large public network, and anyone can connect to it, whether their intentions are good or not. To protect our networks, we should make use of firewalls. Figure 2.6 shows how firewalls can protect networks by denying certain kinds of network traffic.
Figure 2.6 A firewall between each LAN and the internet secures the network. Network communications between the two LANs are allowed, but malicious traffic from an attacker is denied.
You have probably heard the term firewall before regarding a piece of software on your PC. For example, Windows PCs use Microsoft Defender Firewall by default. This kind of firewall is a host-based firewall. It examines network traffic entering and exiting the host device and then decides to allow or deny (block) it. It makes these decisions based on a set of defined rules. However, this is not the kind of firewall you need to know for the CCNA. The kind of firewall we will cover is the network firewall.
A network firewall is a separate hardware appliance that serves a purpose similar to a host-based firewall but on a larger scale. It inspects all traffic entering and exiting a network and decides to allow or deny it based on a set of configured rules.
Firewalls are not a major focus of the CCNA. We will cover some of their functionality in chapter 11 of volume 2, which covers security concepts, but the majority of this book will focus on the previously discussed two device types: routers and switches.

Summary
A local area network (LAN) is a group of interconnected devices in a limited area, such as an office.
A wide area network (WAN) is a network that extends over a large geographical area, such as between cities.
A computer network is a telecommunications network that allows nodes to share resources.
A node is any device that connects to a network: a personal computer, an iPhone, a router, etc.
A resource is anything that is shared over a network, such as a web page.
Various types of network devices are used to facilitate network communications.
Clients and servers are defined by their functions in relation to each other: clients access services provided by servers, and servers provide services for clients. Most types of devices can be both a client and a server.
Switches provide connectivity between devices in a LAN. They typically have many ports (24 to 48) for devices to connect to.
Routers provide connectivity between LANs and external networks, such as the internet.
A wireless router (Wi-Fi router/home router) is a multifunctional device that combines the roles of router, switch, wireless access point, and firewall.
Firewalls secure the network by inspecting traffic that enters or exits the network and allowing or denying it based on a set of configured rules.