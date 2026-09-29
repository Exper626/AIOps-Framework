4 The TCP/IP networking model
This chapter covers

What networking models are and why we need them
The OSI model
The TCP/IP model and its layers
How each layer plays a role in moving data across a network
Data encapsulation and de-encapsulation
In the previous chapter, we looked at Ethernet; specifically, we looked at the types of physical connections defined by the Ethernet standard. Ethernet also defines rules for how devices can communicate over those connections. However, Ethernet alone isn’t sufficient for two computers to communicate over a network (e.g., for a PC to retrieve a web page from a server over the internet). Communicating over a network is a complex process, and it requires a variety of protocols, each of which performs specific functions and, when brought together, enables network communications.
In this chapter, we will look at a couple of models that define the various functions required to enable computers to communicate over a network: the Open Systems Interconnection (OSI) model and the TCP/IP model (named after two key protocols of the model: Transmission Control Protocol and Internet Protocol). TCP/IP is the model currently used by modern networks all over the world.
Neither of these models is explicitly listed as a CCNA exam topic. However, the information in this chapter is fundamental networking knowledge. We will examine the functions of various network protocols throughout the two volumes of this book, so it’s important to have a framework to understand it all. That’s the role of these networking models—to provide a framework to organize the various functions that make a network work.
The purpose of this chapter is to provide a high-level overview of how data travels from source to destination across a network. In the rest of this book, we will fill in the gaps regarding the exact mechanisms that make network communications possible, but first we need a framework.

4.1 Conceptual models of networking
Since the beginning of computer networking, there have been several attempts to create models that define the various functions necessary for computers to communicate with each other. Several of these models were vendor-proprietary, meaning they were created by a specific vendor (i.e., IBM) to be used by their products. However, the vendor-proprietary approach was not ideal; each vendor designed its own communication protocols, so enabling communication between different vendors’ products was no simple task.

Definition A protocol is a set of rules defining how data should be communicated between devices in a network. Protocols can be thought of as the languages computers use to communicate; two computers using different networking protocols are like two humans speaking different languages—they won’t be able to communicate.
These days we all enjoy the benefits of the alternative approach: vendor neutral. In a vendor-neutral model, with vendor-neutral protocols that can be used by devices of all kinds, we don’t have to worry about whether an Apple MacBook will be able to access a website hosted on a Linux web server or whether a PC running Windows will be able to send an email that can be read on a smartphone running Android.
Networking models are frameworks that define the various functions needed to allow data to travel from source to destination over a network. These functions are typically divided into layers, with each layer describing a certain role required to enable network communications. Then, protocols can be designed to fill those roles.
Using layers allows for a modular design: at each layer of the model, there are several protocols that can fill the necessary roles of the layer. For example, in the previous chapter, we looked at some aspects of Ethernet (IEEE 802.3) and also briefly mentioned wireless LANs as defined by IEEE 802.11 (best known as Wi-Fi). Both protocols serve the same purpose: they define how data should be sent over a particular physical medium (UTP/fiber cables for Ethernet, radio waves for Wi-Fi). An email application on a computer doesn’t need to care about whether a message will be sent over the network via a wired Ethernet connection or a wireless Wi-Fi connection; as long as the email application performs its role, it can expect the other layers to perform their roles as well.
There are two networking models that network professionals should be familiar with: OSI and TCP/IP. Although the TCP/IP model is the model used in modern networks, the OSI model has also had a large influence on how we think and talk about networks and is still considered core knowledge for anyone involved in networking (despite not being in use in modern networks).

4.2 The OSI reference model
The Open Systems Interconnection reference model is a conceptual model of networking developed by the International Organization for Standardization (ISO). Most people simply call it the OSI model.
International Organization for Standardization
The ISO publishes standards related to various aspects of technology. Looking at the name, you may wonder why it’s abbreviated as ISO and not IOS. The ISO decided upon the abbreviation to have one shared abbreviation regardless of language. Rather than being an acronym for International Organization for Standardization, the organization states that ISO is derived from the Greek word isos, meaning “equal.”
The OSI model defines seven layers, each with its own functions that contribute to the process of communicating over a network. Table 4.1 lists the seven layers of the OSI model.
Table 4.1 The seven layers of the OSI model


| Layer | Name         |
| ----- | ------------ |
| 7     | Application  |
| 6     | Presentation |
| 5     | Session      |
| 4     | Transport    |
| 3     | Network      |
| 2     | Data Link    |
| 1     | Physical     |

Because this chapter focuses on the TCP/IP model, we won’t cover the role of each of the seven layers listed in table 4.1. The OSI model is a relic of the past that I don’t recommend digging too deeply into unless you’re interested in the history of how networks developed.
Exam Tip Although we will focus on the TCP/IP model in this chapter, the terminology of the OSI model is still widely used, so it’s worth remembering the seven layers and their names. Most students use a mnemonic to help with this: for example, “Please Do Not Teach Students Pointless Acronyms,” using the first letter of each layer’s name from Layers 1 to 7.

4.3 The TCP/IP model
The TCP/IP model was born out of research and development funded by the US Department of Defense (DOD) Defense Advanced Research Projects Agency (DARPA). It was then called the ARPANET reference model, but it has since evolved into the Internet Protocol Suite, which was defined in Request for Comments (RFC) 1122. RFCs are documents published by the Internet Engineering Task Force (IETF) to define standard protocols for the internet. Some more common names for this model are the TCP/IP suite, TCP/IP model, or just TCP/IP. TCP and IP are two of the foundational protocols included in the model, so they are often used to refer to it.
RFCs and the IETF
The IETF is an organization that defines the standard protocols used by the internet. RFCs are the documents published by the IETF that define these protocols. Many of these documents are informational or experimental and sometimes humorous (e.g., check out RFC 1149 at https://datatracker.ietf.org/doc/html/rfc1149, which describes how to send network messages using birds).
However, some RFCs go on to be recognized as Internet Standards; these are the RFCs that define the protocols that make up the TCP/IP model. For example, TCP, IP, and other well-known protocols like HTTPS (which you’ll see at the beginning of the previous URL I copied) are Internet Standards.
The TCP/IP model as defined in RFC 1122 has four layers; however, network engineers typically reference a five-layer TCP/IP model. The five-layer version of the model, as indicated by the thick border in table 4.2, is what we will be using in this book. The table lists the layers of the TCP/IP model, their equivalent OSI model layers, and some example protocols that belong to each layer of the model.
Table 4.2 The TCP/IP model

| OSI model    | Four-layer TCP/IP model | Five-layer TCP/IP model | Example protocols        |
| ------------ | ----------------------- | ----------------------- | ------------------------ |
| Application  | Application             | Application             | HTTP, HTTPS, FTP, SSH    |
| Presentation | —                       | —                       | —                        |
| Session      | —                       | —                       | —                        |
| Transport    | Transport               | Transport               | TCP, UDP                 |
| Network      | Internet                | Network                 | IPv4, IPv6               |
| Data Link    | Link                    | Data Link               | Ethernet, 802.11 (Wi-Fi) |
| Physical     | Link                    | Physical                | —                        |


Note The similar layers of the OSI model and TCP/IP model are not entirely equivalent; although they have similarities, they are two independent models.
As table 4.2 shows, instead of the three upper layers (Application, Presentation, and Session) of the OSI model, TCP/IP uses a single layer called the Application Layer. Additionally, in the four-layer version of the TCP/IP model, the concerns of the bottom two layers of the five-layer version are addressed by a single layer called the Link Layer. However, for the purpose of the CCNA and understanding networking, the five-layer model is generally more useful, and it is the one we will refer to throughout this book.
The example protocols listed in table 4.2 are some of the protocols we will cover in this book; they are just a few of the protocols you should know for the CCNA exam. I included them in the table for reference, but we will cover how they function in the rest of this book. In this chapter, we will focus on understanding the role of each layer of the TCP/IP model.
Exam Tip The layers of the TCP/IP model can be referred to by their names or their numbers: the Physical Layer is Layer 1, the Data Link Layer is Layer 2, the Network Layer is Layer 3, the Transport Layer is Layer 4, and the Application Layer is Layer 7. As I mentioned previously, the terminology of the OSI model is still widely used (for better or for worse!), so even when referring to the TCP/IP model, the Application Layer is typically called Layer 7 rather than Layer 5 or 4.

4.3.1 The layers of the TCP/IP model
Each layer of the TCP/IP model provides an essential function in enabling computers to communicate over a network. The end goal is for an application on one computer to be able to communicate with an application on another computer over a network (e.g., a PC’s web browser communicating with a web server). Figure 4.1 demonstrates this process; a PC (PC1) accesses a web page hosted on a server (SRV1). As we examine each layer of the TCP/IP model in the following pages, we will see how the layers work together to enable this communication.
Figure 4.1 A web browser on PC1 uses a Layer 7 protocol (HTTPS) to request a web page from the web server on SRV1. Layers 2, 3, and 4 work together to deliver the message to the appropriate application on SRV1. Layer 1 is the medium over which the communication occurs.
The functions defined by each layer of the TCP/IP model include
Physical specifications, such as cables and radio waves
Communication between intermediate nodes in the path to the destination
End-to-end communication from the original source node to the final destination node
Addressing messages to a specific application on the destination node
How an application should interface with the network
Now let’s examine each layer of the TCP/IP model one by one to see how they enable network communications. The goal of this chapter is to provide a framework we can build upon in the rest of this book with details of how the different protocols of each layer fulfill their roles.

Layer 1: The Physical Layer
The Physical Layer is fairly self-explanatory; it defines the physical requirements for transmitting data (a series of bits) from one node to another. Those bits could be encoded as electrical signals traveling along a copper cable, light signals on a fiber-optic cable, or radio waves in a wireless connection.
We covered this in chapter 3: IEEE 802.3 (Ethernet) and IEEE 802.11 (Wi-Fi) both define specifications at the Physical Layer. For example, Ethernet defines connector and cable types, how data should be encoded into electrical (or light) signals, and countless other minutiae about how to communicate over UTP and fiber-optic cables. Likewise, Wi-Fi defines what radio frequencies should be used for wireless LAN communication, how radio waves should be modulated to encode data, etc.
To summarize, the Physical Layer of the TCP/IP model defines the physical requirements to enable a series of bits to travel from one node to another over a physical medium.
Layer 2: The Data Link Layer
Ethernet and Wi-Fi do not only define physical specifications; they also specify how data should be addressed and sent to another node connected to the same physical medium within a LAN. The Data Link Layer’s job is to prepare data for transmission over that physical medium so it can be received by the next node in the path to the final destination. That next node could be the final destination itself or the next router in the path. The journey from one node to the next in the path is called a hop, and the job of the Data Link Layer is to provide hop-to-hop delivery of messages.

Figure 4.2 demonstrates the concept of network hops. PC1 sends a message to SRV1, perhaps a request to access a file hosted on the server. For PC1’s message to reach SRV1, it must make three hops through the network: from PC1 to R1, from R1 to R2, and from R2 to SRV1. The Data Link Layer’s job is to forward the message from one hop to the next until the message reaches the destination host: SRV1. Notice that a message traveling through a switch does not count as a hop. We will examine why this is when we look at Ethernet LAN switching in chapter 6.
Note PC1, R1, R2, and SRV1 are examples of hostnames. A hostname is a name used to identify each device in the network. The hostname of each device in figure 4.2 follows the pattern I will use throughout this book: PCX for PCs, SWX for switches, RX for routers, and SRVX for servers.
Figure 4.2 TCP/IP Layer 2. A message sent from PC1 to SRV1 takes three hops through the network: from PC1 to R1, from R1 to R2, and from R2 to SRV1. At each hop, the message is addressed to the next hop’s MAC address. A message traveling through a switch does not count as a hop.
The Data Link Layer achieves this hop-to-hop delivery by using media access control (MAC) addresses, a kind of network address assigned to each port of a device. At each hop, the message is sent to the MAC address of the next hop. In the first hop, PC1 addresses the message to R1’s MAC address. In the second hop, R1 addresses the message to R2’s MAC address. In the final hop, R2 addresses the message to SRV1’s MAC address.
Note The roles of SW1 and SW2 may seem unclear in figure 4.2. As covered in chapter 2, the role of a switch is to provide many ports for end hosts to connect to the LAN. For the sake of avoiding clutter, I only show one end host connected to each switch (PC1 to SW1 and SRV1 to SW2). However, in reality, there could be 40+ end hosts connected to each of them. In chapter 6, we will examine how switches function.

Layer 3: The Network Layer
We just looked at how the Data Link Layer is used to forward a message from hop to hop until it reaches the final destination. At each hop, the message is sent to the MAC address of the next hop. However, we still need a way for the original source host to address the message to the final destination host. That is the role of the Network Layer: end-to-end delivery.
The type of address used at the Network Layer is the Internet Protocol (IP) address. Chances are you’ve heard of IP addresses before, although you might be unsure about how they work. We will cover IP addresses in chapter 7. Figure 4.3 shows how PC1 addresses a message to SRV1 by addressing it to SRV1’s IP address. The destination IP address of the message remains the same throughout the journey, whereas the destination MAC address is different at each hop.
Figure 4.3 TCP/IP Layer 3. PC1 addresses a message to SRV1’s IP address. Layer 3 is responsible for the end-to-end delivery of the message, whereas Layer 2 is responsible for the hop-to-hop delivery. The destination MAC address of the message changes at each hop, but the destination IP address remains the same throughout the journey.
IPv4 and IPv6
There are two versions of IP in use today: IP version 4 (IPv4) and IP version 6 (IPv6). Network engineers must be familiar with both, and both are part of the CCNA exam. IPv4 and IPv6 use different address formats. The following is an example of an IPv4 address and an IPv6 address:
IPv4 address: 203.0.113.255
IPv6 address: 2001:db8:1:1:2fe3:1:32a:af01
Although IPv4 has been the dominant version of IP for a long time, IPv6 is steadily gaining popularity. In recent years, IPv6’s adoption has accelerated as the number of available IPv4 addresses is running out. We will cover both address types in this book.
Understanding how Layers 2 and 3 work together to deliver a message to its destination is a fundamental concept you must understand for the CCNA exam. In this chapter, I provide a high-level overview of the concepts; we will review these concepts and dig deeper in later chapters of this volume. At this point, it is enough to know the following points:
Layer 2 uses MAC addresses to provide hop-to-hop delivery of messages.
Layer 3 uses IP addresses to provide end-to-end delivery of messages.
Layers 2 and 3 work together to allow a message to travel through the network to its final destination.
The destination IP address of a message remains the same throughout the journey, whereas the destination MAC address is different at each hop.

Layer 4: The Transport Layer
Layers 2 and 3 work together to deliver a message from the source host across a network to the destination host. You might think that’s the end of the story because the message has reached its destination, but it’s actually not all the way there. It’s not enough for the data to reach the correct destination host; we need a way to address data to a specific application process on the destination host (e.g., a service running on a server). That is the role of Layer 4, the Transport Layer.
Like Layers 2 and 3, Layer 4 also uses its own addressing scheme: port numbers. By addressing a message to a particular port, you can send messages to a particular application process on the destination host. Computers run many different applications simultaneously, so this is a very important function. For example, a PC can simultaneously run an online game, a web browser with various tabs that each access a different website, an antivirus application that communicates with an external server for updates, and countless other applications. Port numbers allow the PC to ensure that data it receives from the network reaches the proper destination process.
Note Layer 4 port numbers are not related to the physical ports on a device that we connect cables to (which are an aspect of Layer 1, the Physical Layer). Same name, different concept.
Figure 4.4 demonstrates this concept. Layers 2 and 3 work together to deliver PC1’s message to SRV1, and Layer 4 delivers the message to the appropriate application process on SRV1. SRV1 is a server that provides a few services to clients in the network. It is a name server using the Domain Name System (DNS) to convert website names to IP addresses for clients (that’s what happens when you type manning.com into a web browser). It is also a web server that uses Hypertext Transfer Protocol (HTTP) and Hypertext Transfer Protocol Secure (HTTPS) to allow clients to access the websites it hosts. DNS, HTTP, and HTTPS are Layer 7 (Application Layer) protocols, and they each accept messages using a different Layer 4 port number.

Figure 4.4 Layers 2 and 3 work together to deliver PC1’s message to SRV1. At Layer 4, PC1 addresses the message to port 443, which is used by the HTTPS protocol. Three ports are open on SRV1 (53, 80, 443), meaning it will accept messages addressed to any of those ports.
Note All three addresses—the MAC address (Layer 2), the IP address (Layer 3), and the port number (Layer 4)—are included in the same message. We will examine how this works in section 4.3.2.

TCP and UDP
The two most common Layer 4 protocols are Transmission Control Protocol (TCP)—the “TCP” in TCP/IP—and User Datagram Protocol (UDP). Both protocols allow computers to address messages to specific application services on the destination host, but there are several differences between the two.
For example, TCP implements checks to ensure that each message reaches its destination and is used by Application Layer protocols such as HTTP and HTTPS (used for accessing websites). UDP, on the other hand, takes a “send it and forget it” approach; it doesn’t check to ensure that every message reaches the destination. UDP is used by Voice over IP (VoIP) protocols—used for phone calls—and live video streaming protocols, among others. We will cover TCP and UDP in chapter 22 of this book.

Layer 7: The Application Layer
The Application Layer is the interface between the applications running on a computer and the network. Using Layer 7 protocols, an application running on a computer can prepare a message to be sent over the network. This message could be, for example, a request from a web browser to retrieve a web page that is hosted on a web server. Layers 2, 3, and 4 are then responsible for delivering that message to the appropriate application on the destination computer.
Note Although the TCP/IP model only has five layers (or four, in the original definition), Layer 7 is the most common term used for the Application Layer, so that is what I will use throughout this book. That is due to the influence of the OSI model, as mentioned previously.
Layer 7 protocols such as HTTPS are not user applications themselves; rather, they provide services for those applications to enable them to communicate with applications on other computers over the network. Figure 4.1 shows the complete process that enables a web browser on PC1 to send a message to request a web page from the web server running on SRV1. The process that the message goes through to reach SRV1 is as follows:
Layer 7—PC1’s web browser uses HTTPS to request the web page.
Layer 4—PC1 addresses the message to port 443, which is used by the HTTPS protocol. This ensures that the message reaches the correct application on SRV1.
Layer 3—PC1 addresses the message to the IP address of SRV1, and the destination IP address of the message remains the same as the message travels from PC1 across the network to SRV1.
Layer 2—PC1 addresses the message to the next hop in the path to SRV1, which is R1. After receiving the message, R1 forwards it to the next hop (R2) by addressing the message to R2’s MAC address. Finally, R2 forwards the message to the final destination (SRV1) by addressing the message to SRV1’s MAC address. Unlike the destination IP address of the message, the destination MAC address is changed at each hop.
Definition To forward a message is to send it to the next node in the path to the destination, whether that is the final destination node itself or the next router in the path to the destination. In later chapters of this volume, we will examine how routers and switches make forwarding decisions to deliver messages to the correct destination.

4.3.2 Data encapsulation and de-encapsulation
In this section, we’ll see how the layers of the TCP/IP model work together to allow computers to communicate with each other. By now, you should be familiar with the basic purpose of each layer of the TCP/IP model:
Layer 7 (Application)—The interface between applications and the network
Layer 4 (Transport)—Provides application-to-application delivery of messages
Layer 3 (Network)—Provides end-to-end delivery of messages
Layer 2 (Data Link)—Provides hop-to-hop delivery of messages
Layer 1 (Physical)—The physical medium over which communication happens

Data encapsulation
The process a host goes through to send data is a five-step process. It begins with the Layer 7 protocol preparing some data to be sent. In the second step, a Layer 4 protocol then adds a header to that data addressed to a certain port.
Definition A header is supplemental data added to the front of a message that is to be transmitted over a network. A protocol’s header contains the data used by that protocol. For example, a Layer 4 protocol will include a destination port number, as well as other information.
In the third step, the message is passed to Layer 3, which adds its own header to that data. This header will be addressed to the IP address of the destination host. In the fourth step, the message will then be passed to Layer 2, which adds both a header and a trailer.
Definition A trailer is also supplemental data added to a message that is to be transmitted over a network. Whereas a header is added to the beginning of a message, a trailer is added to the end. The Ethernet trailer contains a small block of data used to check for errors in the message. For example, errors can occur during transmission as a result of electromagnetic interference.
At Layer 2, the message is addressed to the next-hop device. Finally, in the fifth step, the host will transmit the bits over the physical medium, such as a UTP cable. The process of adding headers (and trailers) to data before sending it over a network is called encapsulation. To summarize that process:

The Application Layer protocol prepares data.
Layer 4 encapsulates the data with a header addressed to a port number on the destination host.
Layer 3 encapsulates the data with a header addressed to the IP address of the destination host.
Layer 2 encapsulates the data with a header addressed to the MAC address of the next hop. It also encapsulates the data with a trailer, used to check for errors.
The host transmits the bits of data over the physical medium (e.g., encoded as electrical signals over a UTP cable).
Figure 4.5 demonstrates the five-step process of encapsulation and transmission.



Figure 4.5 The five-step process of encapsulating and transmitting data: (1) the Application Layer protocol prepares some data, (2) Layer 4 encapsulates the data with a header, (3) Layer 3 encapsulates the data with a header, (4) Layer 2 encapsulates the data with a header and trailer, and (5) the host transmits the bits over the physical medium (i.e., a UTP cable).
Note The Layer 2 header is the beginning of the message; it is the first part sent. The Layer 2 trailer is the end of the message; it is the last part sent.

Data de-encapsulation
When the destination host receives the message, it goes through the opposite process: de-encapsulation. In the de-encapsulation process, the host receiving the message inspects the information in each header/trailer and then removes them until it gets to the data inside. Like encapsulating and transmitting a message, receiving and de-encapsulating a message can also be summarized into five steps, summarized as follows (also see figure 4.6):
The destination host receives the message.
It inspects the Layer 2 header and trailer, removes them, and passes the message to Layer 3.
It inspects the Layer 3 header, removes it, and passes the message to Layer 4.
It inspects the Layer 4 header, removes it, and sends the data to the appropriate application.
The application receives and processes the data.



Figure 4.6 The five-step process of receiving and de-encapsulating data: (1) the destination host receives bits (the message), (2) the Layer 2 header/trailer is inspected and removed, (3) the Layer 3 header is inspected and removed, (4) the Layer 4 header is inspected and removed, and (5) the data is received and processed by the application.

Protocol data units
At each stage in the encapsulation/de-encapsulation process, there is a name given to the message:
The combination of data and a Layer 4 header is called a segment.
The combination of a segment and a Layer 3 header is called a packet.
The combination of a packet and a Layer 2 header/trailer is called a frame.
We can also use an alternative term to describe the message at each stage—protocol data unit (PDU):

A segment is a Layer 4 PDU (L4PDU).
A packet is a Layer 3 PDU (L3PDU).
A frame is a Layer 2 PDU (L2PDU).
The contents of each PDU (everything encapsulated by that layer’s header/trailer) are called the payload. So, a frame’s payload is a packet, a packet’s payload is a segment, and a segment’s payload is the application data. Figure 4.7 illustrates the different PDUs and their payloads.



Figure 4.7 Application data encapsulated in a Layer 4 header is a segment (L4PDU); a segment encapsulated in a Layer 3 header is a packet (L3PDU); and a packet encapsulated in a Layer 2 header/trailer is a frame (L2PDU). The encapsulated contents of each PDU are that PDU’s payload.
Adjacent-layer and same-layer interactions

Within a computer, each layer of the TCP/IP model provides a service for the layer above it, called adjacent-layer interaction. Following is a summary of the interactions between adjacent layers of the TCP/IP model:
Layer 4 provides a service to Layer 7 by delivering data to the appropriate application on the destination host.
Layer 3 provides a service to Layer 4 by delivering segments to the correct destination host.
Layer 2 provides a service to Layer 3 by delivering packets to the next hop.
Layer 1 provides a service to Layer 2 by providing a physical medium for frames to travel over.

There is also a related concept called same-layer interaction. This refers to the communications between the same layer on different computers. Same-layer interactions work like this:

Application data from one computer is sent to an application on another computer.
When data is encapsulated with a Layer 4 header, the segment is addressed to Layer 4 of the destination host, where the information in the header will be inspected.
When a segment is encapsulated with a Layer 3 header, the packet is addressed to Layer 3 of the destination host, where the information in the header will be inspected.
When a packet is encapsulated with a Layer 2 header and trailer, the frame is addressed to Layer 2 of the next hop, where the information in the header and trailer will be inspected.
Signals sent out of a physical port of one device are received by a physical port of another device.
Figure 4.8 illustrates these adjacent-layer interactions between different layers on the same computer (on Host A and on Host B), and same-layer interactions between different computers that are communicating with each other (between Host A and Host B).
Figure 4.8 Each layer on a host provides services for the layer above it; this is called adjacent-layer interaction. When two hosts communicate, each layer on one host communicates with the same layer on the other host; this is called same-layer interaction.

Summary
Networking models provide frameworks to define the functions necessary to enable network communications.
Networking models are divided into layers; each layer describes a necessary function for network communications and includes multiple protocols that can fulfill the layer’s role.
The Open Systems Interconnection Reference (OSI) model is a networking model that influenced how we think and talk about networks but is not in use today.
The OSI model has seven layers: (1) Physical, (2) Data Link, (3) Network, (4) Transport, (5) Session, (6) Presentation, and (7) Application.
The Internet Protocol Suite (TCP/IP) model) is the networking model used in modern networks and is named after two of its key protocols: Transmission Control Protocol (TCP) and Internet Protocol (IP).
The original TCP/IP model has four layers, but a more popular version has five: (1) Physical, (2) Data Link, (3) Network, (4) Transport, and (5) Application (called Layer 7, not Layer 5).
Layer 1 (Physical) defines physical requirements for transmitting data, such as ports, connectors, and cables, and how data should be encoded into electrical/light signals.
Layer 2 (Data Link) is responsible for hop-to-hop delivery of messages. A hop is the journey from one node in the network to the next in the path to the final destination
Layer 2 uses media access control (MAC) addresses to address messages to the next hop.
Layer 3 (Network) is responsible for end-to-end delivery of messages, from the source host to the destination host.
Layer 3 uses Internet Protocol (IP) addresses to address messages to the destination host.
The destination MAC address of a message changes at each hop in the path to the destination, but the destination IP address remains the same.
Layer 4 (Transport) is used to address messages to the appropriate application on the destination host.
Layer 4’s addressing scheme uses port numbers (not related to physical ports). The port number identifies the Layer 7 protocol being used.
Layer 7 (Application) is the interface between applications and the network. Layer 7 protocols such as Hypertext Transfer Protocol Secure (HTTPS) are not applications themselves but provide services for applications to enable them to communicate over the network.
A host encapsulates application data with a Layer 4 header, Layer 3 header, and Layer 2 header/trailer before being transmitted over the physical medium (cable or radio waves).
After a message is received by a host, the host de-encapsulates it by inspecting and removing the Layer 2 header and trailer, inspecting and removing the Layer 3 header, inspecting and removing the Layer 4 header, and finally processing the data in the message.
The contents encapsulated inside each protocol data unit (PDU) are its payload.
The combination of data and a Layer 4 header is called a segment (L4PDU).
The combination of a segment and a Layer 3 header is called a packet (L3PDU).
The combination of a packet and a Layer 2 header/trailer is called a frame (L2PDU).
Within a computer, each layer provides a service for the layer above it; this is called adjacent-layer interaction.
Communication between the same layer on different computers is called same-layer interaction.