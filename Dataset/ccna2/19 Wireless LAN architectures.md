19 Wireless LAN architectures
This chapter covers

The structure of 802.11 frames and their types
Standalone, lightweight, and cloud-based AP architectures
The various wireless LAN controller deployment options
In the previous chapter, we covered the basic building blocks of wireless LANs, starting with the fundamentals of radio frequency (RF) and connecting devices wirelessly in different types of service sets. In this chapter, we will continue on that theme by examining 802.11 frames and message types. We will then zoom out and look at the bigger picture—the different ways wireless access points (APs) can be deployed and managed to provide wireless access to clients in networks of all sizes. Specifically, we will cover the following CCNA exam topics:

1.1 Explain the role and function of network components

1.1.e Controllers

2.6 Compare Cisco Wireless Architectures and AP modes

2.7 Describe physical infrastructure connections of WLAN components (AP, WLC, access/trunk ports, and LAG)

2.8 Describe network device management access (Telnet, SSH, HTTP, HTTPS, console, TACACS+/RADIUS, and cloud mnaged)

19.1 802.11 frames and message types
Like Ethernet, 802.11 encapsulates Layer 3 packets in frames before sending them over the physical medium—the air, in 802.11’s case. As we covered in the previous chapter, sending frames over the air is quite a bit different from sending them along a cable. For that reason, 802.11 defines its own frame format and a variety of message types necessary to facilitate wireless communications; those are what we’ll cover in this section.

19.1.1 The 802.11 frame format
Compared to the Ethernet frame format, the 802.11 frame format shown in figure 19.1 might seem a bit unusual. See if you can tell what’s different.



Figure 19.1 The 802.11 frame format. Field sizes in bytes are indicated above each field. Depending on the 802.11 standard being used and the message type, some of the fields might not be present in the frame.

The two major differences between the Ethernet and 802.11 frame formats are

Depending on the 802.11 standard and message type, some of the 802.11 header’s fields might not be present (those with a size of 0 or X bytes in figure 19.1).

There are up to four address fields instead of the typical two.

Let’s focus on the second point. Ethernet connects devices over a bounded medium—cables. Because of this, each frame needs only a source address and a destination address to identify the sender and receiver. Communicating via an AP over the air, an unbounded medium, adds some complexity that requires additional address fields; 802.11 frames contain up to four. These can identify some combination of the following addresses:

Basic service set identifier (BSSID)—The AP’s BSSID

Destination address (DA)—The final recipient of the frame

Source address (SA)—The original sender of the frame

Receiver address (RA)—The immediate recipient of the frame

Transmitter address (TA)—The immediate sender of the frame

Note Like Ethernet, 802.11 uses MAC addresses.

Figure 19.2 demonstrates one situation in which these addresses play their roles. As mentioned in the previous chapter, clients connected to the same AP must communicate via the AP—not directly with each other—even if they are physically close enough to directly receive each other’s signals. So to send a frame to PC2, PC1 must specify AP1 as the immediate recipient (RA) and PC2 as the final recipient (DA).



Figure 19.2 PC1 sends a frame to PC2. By specifying a different immediate and final recipient, PC1 sends its frame via AP1 instead of directly to PC2.

Note RA = BSSID in figure 19.2 means the RA and BSSID are identical: they are AP1’s MAC address, and it is specified in the Address 1 field when PC1 sends the frame. The same applies to TA = SA, RA = DA, and TA = BSSID.

Figure 19.2 shows just one example demonstrating that PC1 can specify a different immediate and final recipient. There are various possible patterns, and depending on the message type, there might be one, two, three, or four address fields in an 802.11 frame; such details are well beyond the scope of the CCNA exam.

The other fields of an 802.11 frame

Although not necessary for the CCNA exam, here’s a quick description of the remaining fields of an 802.11 frame:

Frame Control—Provides information such as the message type and subtype.

Duration/ID—Depending on the message type, this field can indicate

The time (in milliseconds) the channel will be dedicated to transmission of a frame.

An identifier for the association (the connection between client and AP).

Sequence Control—Used to reassemble a fragmented message and identify retransmitted frames.

QoS Control—Used in QoS to prioritize certain traffic types.

HT (High Throughput) Control—Used to support the higher data transfer rates of 802.11n, 802.11ac, and later standards.

Frame Body—The message encapsulated inside of the frame.

FCS (Frame Check Sequence)—Like the Ethernet FCS, this allows the receiving device to check if the frame was corrupted in transit.

19.1.2 The client association process
In section 19.1.3, we’ll take a look at some 802.11 message types. But before that, let’s see some of them in action in the client association process. A client’s connection to an AP is called an association; for a client to send and receive wireless traffic via an AP, the client must be associated with the AP. And before the AP will allow the client to associate with it, it must authenticate the client; it must ensure that it is a valid client.

Note We’ll cover wireless LAN security, including authentication, in the next chapter.

Figure 19.3 shows a high-level overview of the process. It begins with PC1 sending a probe request to discover any APs (and the SSIDs they offer) within range. There are two ways to accomplish this:

Active scanning—The client sends probe requests and listens for probe responses from APs (as shown in figure 19.3). This helps clients discover APs more quickly, although constant active scanning can shorten the client’s battery life.

Passive scanning—The client listens for beacon messages from APs; APs send beacon messages periodically to advertise each BSS. This can conserve the client’s battery life, but it may take longer for the client to discover available APs.



Figure 19.3 The client association process. The probe request/response exchange allows PC1 to discover AP1. PC1 then authenticates and associates with AP1.

After the client discovers an AP, whether through active or passive scanning, it can then request to authenticate and associate with the AP. The client can only send data over the wireless LAN after successfully authenticating and associating with the AP.

A familiar experience

Although 802.11 active scanning and passive scanning are probably new terms to you, you’ve surely experienced them before. When you connect your phone or laptop to Wi-Fi at a new cafe or someone’s house and see a list of available SSIDs, those SSIDs are advertised by APs your device discovered through either active or passive scanning. Your device likely discovers unfamiliar APs/SSIDs even within your own home. If that happens, it means that your device either received beacons from those APs or exchanged probe requests/responses with them.

19.1.3 802.11 message types
802.11 defines three main types of messages:

Management—Used to establish communications in the wireless LAN

Control—Used to facilitate the delivery of frames over the medium

Data—Used to carry data payloads (typically, IP packets)

Let’s take a look at some examples of each message type, starting with management. The message types shown in the previous section—probe, beacon, authentication, and association—are all 802.11 management messages. Another example is disassociation, which a client sends to end its association with the AP. Management messages are used to establish communications in the wireless LAN and allow the AP to manage the BSS by controlling which clients can participate.

The second type is control, which is used to facilitate the delivery of frames over the medium. Three examples are request-to-send (RTS), clear-to-send (CTS), and acknowledgment (Ack). Figure 19.4 demonstrates how these messages are used.



Figure 19.4 RTS, CTS, and Ack messages facilitate smooth communication over the medium. RTS asks for permission to transmit a frame, and CTS grants permission. Ack acknowledges receipt of the frame.

The RTS/CTS mechanism of asking for and granting permission to transmit a frame helps to reduce collisions in the wireless LAN. However, it adds additional overhead: for each data frame to be sent, two extra frames (RTS and CTS) must be transmitted, which can reduce overall network efficiency. Modern networks usually do not use RTS/CTS.

Ack messages, on the other hand, are a necessity. The nature of wireless networks makes frame delivery less reliable than on wired networks, so the Ack mechanism is used to verify that frames have been properly delivered; after a device successfully receives a frame, it must send an Ack back to the sender. If an Ack isn’t received, the frame is retransmitted.

Data frames are the final 802.11 frame type; these are frames that carry the actual data to and from wireless clients that are communicating over the network. In most cases, the payload of these frames is an IP packet—IPv4 or IPv6.

19.2 AP architectures
APs can be integrated into a network in multiple ways—for example, as standalone units that you configure and manage individually or centrally managed from a wireless LAN controller (WLC) or SaaS cloud platform. In this section, we will cover the three main AP architectures:

Autonomous APs—Self-contained units that operate independently of other APs, with each requiring individual configuration and management.

Lightweight APs—APs that are centrally managed by a WLC. Complex tasks such as client authentication, security policy enforcement, and RF management are offloaded to the WLC, simplifying AP deployment and management.

Cloud-based APs—APs that are managed remotely over the internet via a cloud service.

Autonomous, lightweight, and cloud based are not simply operational modes that any AP is capable of; they are different types of APs. For example, for an AP to function as an autonomous AP, it requires additional hardware and software capabilities that aren’t present in lightweight APs. Some APs can only be autonomous, some can only be lightweight, and some can be either. The same goes for cloud-based APs. A standard Cisco AP cannot operate as a cloud-based AP—only those sold by Cisco Meraki (a company Cisco acquired in 2012).

19.2.1 Autonomous APs
An autonomous AP is a self-contained unit. It has the necessary built-in intelligence to handle all aspects of wireless network operations, from client authentication to data encryption—an autonomous AP doesn’t rely on an external controller. Each autonomous AP functions as a standalone entity, requiring individual configuration and management. Autonomous APs are useful in small networks or in areas where only a few APs are needed, offering a simple setup without the need for additional centralized control systems. Figure 19.5 shows a LAN with two autonomous APs providing two ESSs for clients.



Figure 19.5 Two autonomous APs providing two ESSs for clients. Autonomous APs connect to the wired LAN via trunk links to support multiple SSIDs/VLANs.

Autonomous APs connect to the wired LAN via trunk links. This is because they typically support multiple SSIDs, each mapped to an Ethernet VLAN on the wired LAN. For example, one SSID may be for employee access while another is for guest access. In figure 19.5, one SSID is mapped to VLAN 10, and the other SSID is mapped to VLAN 20; the AP translates between each SSID and VLAN, serving as the bridge between the wireless and wired LANs. Trunk ports are necessary to support multiple VLANs on the wired network.

Figure 19.5 also lists a management VLAN (VLAN 99)—a VLAN dedicated to managing the APs themselves (and other network devices, like the switches in the LAN). As I mentioned in chapter 5 when covering Telnet and SSH, creating a separate VLAN to isolate management traffic is considered a best practice. This isolation streamlines device management and enhances network security by segregating management traffic from user data.

Autonomous APs require individual configuration, which is done directly through the CLI using the console port, Telnet, or SSH or through the GUI via a web browser using HTTP/HTTPS. Individually managing APs is feasible in a small network with only a few APs, but when the network grows beyond 5 to 10 APs, it becomes inefficient. And in larger networks, which can have thousands of APs spread across many LANs, individually managing autonomous APs is just not practical; centralized management becomes essential.

19.2.2 Lightweight APs
To support larger wireless LANs, a wireless LAN controller (WLC) is used to centralize control and simplify operations. An AP that is controlled by a WLC is called a lightweight AP (LWAP). LWAPs offload many of their functions to the WLC; this is called split-MAC architecture, where real-time media access control (MAC) operations are performed by the LWAPs and more complex, non-real-time functions are handled by the WLC.

Note Media access control (MAC) is one of the main functions of Layer 2 of the TCP/IP model that manages how devices uniquely identify themselves (MAC addresses) and communicate over a shared network medium, like Ethernet or Wi-Fi.

The WLC is responsible for management functions, such as RF management (setting each LWAP’s channel and transmit power), client authentication and association, and QoS and security policy enforcement. The LWAPs handle real-time functions like transmitting and receiving RF signals, encryption of 802.11 frames, sending beacon messages, responding to clients’ probe requests, etc. Figure 19.6 shows two LWAPs managed by a WLC. Note that the precise location of the WLC in the network can vary; it could be in a remote data center, connected to a core or distribution switch in the LAN or even incorporated into a switch or AP. Later in this section, we’ll examine these different options.



Figure 19.6 Two LWAPs managed by a WLC. The WLC handles management functions, and the LWAPs handle real-time functions.

Note Here’s a simple way to understand split-MAC architecture: the “intelligence” is centralized in the WLC, and an LWAP’s role is simply to handle real-time wireless interactions with clients.

A key difference between autonomous APs and LWAPs is how they connect to the wired network. Autonomous APs use trunk ports to handle multiple VLANs for different SSIDs (plus the management VLAN). In contrast, LWAPs typically connect to the wired LAN using access ports, which only support a single VLAN—the management VLAN, in this case. The job of translating between SSIDs and VLANs is offloaded to the WLC. To achieve this, a protocol called Control and Provisioning of Wireless Access Points (CAPWAP) is used to establish tunnels between the LWAPs and the WLC. Figure 19.7 shows how LWAPs tunnel frames from wireless clients to the WLC, which then translates them into Ethernet frames tagged in the appropriate VLAN.



Figure 19.7 LWAPs tunnel client data frames to the WLC, which translates them into Ethernet frames.

Note Remember what a tunnel is: a virtual communication pathway. Tunnels don’t make a new physical pathway; the bits still pass over the wired LAN. However, tunneled messages are encapsulated with additional headers, as we covered in chapter 16 when examining VPNs.

CAPWAP doesn’t just create one tunnel between each LWAP and the WLC. It creates two: a data tunnel and a control tunnel. The CAPWAP data tunnel is used to tunnel traffic sent to and from the wireless clients associated with the LWAP: laptops, smartphones, etc. The CAPWAP control tunnel is used to tunnel communications between the LWAP and the WLC; the WLC uses this tunnel to configure the LWAPs and manage their operations. Figure 19.8 illustrates these two tunnels.



Figure 19.8 CAPWAP creates two tunnels between each LWAP and the WLC: a control tunnel and a data tunnel. The control tunnel uses UDP port 5246, and the data tunnel uses UDP port 5247.

Note The CAPWAP control tunnel is encrypted by default, but the data tunnel isn’t; you can enable data tunnel encryption for additional security. CAPWAP encryption uses Datagram Transport Layer Security (DTLS)—a type of TLS that uses UDP instead of TCP.

Centralizing control of LWAPs with split-MAC architecture provides several advantages, not just in terms of scalability. For example, the WLC gathers information about the RF environment from the LWAPs it manages and can intelligently make decisions such as which channels each LWAP should use, the optimal transmit power of each AP, etc. This also allows for self-healing coverage: if one LWAP stops working, the WLC can make nearby LWAPs increase their transmit power to maintain the coverage area.

Another benefit is the centralization of security and QoS policies. Managing these key functions from a single point ensures consistent standards for access control, encryption, and data prioritization.

Note CAPWAP is an industry-standard protocol but is based on a protocol called Lightweight Access Point Protocol (LWAPP). LWAPP was developed by Airespace, a company that was purchased by Cisco in 2005.

WLC deployment options

In a network with more than 5 to 10 APs, you should consider using a WLC to centrally control your wireless LANs. However, there’s a big difference between a network with, for example, 20 to 30 APs and a network with thousands of them. For that reason, there is no one-size-fits-all WLC solution; there are a variety of WLC deployment options that meet different needs. Figure 19.9 illustrates four deployment options: unified, cloud, embedded, and Mobility Express.



Figure 19.9 WLC deployment options. A unified WLC is a dedicated hardware appliance. A cloud WLC is a VM deployed in a private or public cloud. An embedded WLC is integrated into a switch. A Mobility Express WLC is integrated into an AP.

Note To avoid showing the same network four times with the WLC in different locations, I included all four deployment options in figure 19.9. In practice, a network would typically employ one option suited to its specific needs.

A unified WLC is a dedicated hardware appliance; Cisco offers various hardware models that can support anywhere from a few hundred LWAPs to as many as 6,000 LWAPs and 64,000 clients with a single WLC—if your network has to support more WLCs and clients than that, you’ll have to deploy a second WLC.

A cloud WLC is a virtual machine (VM) deployed on a server in the cloud. It could be, for example, a private cloud in the company’s data center or a public cloud platform. Depending on the hardware resources available to the VM, a cloud WLC can support 1,000, 3,000, or even 6,000 LWAPs, and up to 64,000 clients—as much as a unified WLC.

An embedded WLC is a WLC integrated into a switch. Embedded WLCs are more suitable for smaller deployments, supporting up to 200 APs and 4,000 clients. For even smaller deployments, Cisco Mobility Express integrates the WLC within an AP, supporting up to 100 LWAPs and 2,000 clients. Table 19.1 summarizes these deployment options.

Table 19.1 WLC deployment options

| Name             | Description               | Max LWAPs | Max Clients |
|------------------|---------------------------|-----------|-------------|
| Unified          | Dedicated hardware appliance | 6,000  | 64,000      |
| Cloud            | VM deployed in the cloud  | 6,000     | 64,000      |
| Embedded         | Integrated into a switch  | 200       | 4,000       |
| Mobility Express | Integrated into an AP     | 100       | 2,000       |



Note In Cisco’s newer line of WLCs and APs, they have dropped the Mobility Express terminology, using the term embedded both for a WLC integrated into a switch and a WLC integrated into an AP; be aware of both terms for the CCNA exam.

Client-serving LWAP modes

In the previous chapter, we looked at a few additional AP operational modes: repeater, workgroup bridge, and outdoor bridge. LWAPs controlled by a WLC can also be configured to operate in various modes. In some modes, the LWAP provides network service to clients, and in others, it is dedicated to a more specialized network management role. First, let’s examine the client-serving modes:

Local—The standard operational mode, providing BSSs for clients. The LWAP tunnels all client traffic to the WLC via CAPWAP.

FlexConnect—Similar to Local, but client traffic doesn’t have to be tunneled to the WLC; the LWAP can locally switch client traffic between the wired and wireless LANs.

Bridge and Flex + Bridge—Used in mesh deployments.

Local is the default LWAP operational mode that we have covered so far. An LWAP in local mode offers BSSs for clients and tunnels all client traffic to the WLC via the CAPWAP data tunnel. However, this is not always desirable; tunneling all client traffic to the WLC can be inefficient, especially if the WLC and clients aren’t located in the same LAN.

FlexConnect offers a more flexible approach (hence the name) in which the LWAP can locally switch client traffic between the wired and wireless LANs—no need to tunnel it to the WLC. This reduces latency for the client traffic because it doesn’t have to travel all the way to the WLC and back and also conserves bandwidth on the WAN connections leading to the WLC. FlexConnect can be configured on a per-SSID basis. Figure 19.10 shows how FlexConnect works: FlexConnect is enabled for the Guest SSID but disabled for the Employee SSID.



Figure 19.10 With FlexConnect enabled, a LWAP can locally switch traffic between SSIDs and VLANs. FlexConnect can be enabled per SSID.

Note If FlexConnect is enabled, the LWAP should connect to the wired LAN via a trunk link; it must support multiple VLANs.

Another benefit of FlexConnect is that the LWAP can locally switch traffic between FlexConnect-enabled SSIDs and the wired LAN even if it loses its connection to the WLC. This allows clients using those SSIDs to maintain connectivity even if such a problem occurs.

An LWAP operating in Bridge mode can form a wireless mesh with other LWAPs without directly connecting each LWAP to the wired network infrastructure—an MBSS, as we covered in the previous chapter. LWAPs in Bridge mode can also function as bridges connecting wired LANs (like “outdoor bridge” mode, as covered in chapter 18). Flex + Bridge mode adds FlexConnect on top of Bridge mode, allowing the LWAPs to locally switch client traffic without tunneling it to the WLC.

Network management LWAP modes

Some LWAP operational modes are more specialized; instead of serving wireless clients, the LWAP assists in various network management tasks. The network management LWAP modes are

Monitor—The LWAP doesn’t transmit from its radios; it is dedicated to analyzing the RF environment and detecting unauthorized (“rogue”) devices.

Rogue Detector—The LWAP’s radios are entirely disabled; it is dedicated to analyzing traffic on the wired LAN to detect rogue devices.

Sniffer—The LWAP captures all wireless traffic on a specific channel. The captured messages are then sent to the WLC and can be redirected to analysis software such as Wireshark for detailed inspection and troubleshooting.

SE-Connect—The LWAP is dedicated to RF spectrum analysis on all channels. It feeds data to spectrum analysis software like Cisco Spectrum Expert for in-depth evaluation of the RF landscape.

Note A rogue is an unauthorized AP or client that has been connected to the network without the network administrator’s permission. Rogue devices can pose a security risk, so identifying and dealing with them is important.

Although these operational modes don’t directly serve clients, dedicating LWAPs to specific tasks such as RF spectrum analysis, rogue device detection, and traffic analysis can give important insights into the status of the network. This can help proactively identify and address problems in wireless LANs.

19.2.3 Cloud-based APs
In addition to autonomous and lightweight APs, there is a third option that can be considered a middle ground between the two: cloud-based. Cloud-based AP architecture uses a cloud platform to streamline the management of APs; essentially, it’s a public SaaS cloud service. Cisco’s offering is Cisco Meraki. Figure 19.11 shows how cloud-based APs, such as those offered by Meraki, work.



Figure 19.11 Cisco Meraki offers cloud-based APs. Meraki APs are managed using Meraki’s cloud platform, which connects to each AP using an encrypted tunnel. User data traffic from clients is not tunneled to the cloud—only management traffic.

Meraki APs communicate with the Meraki cloud platform over the internet in an encrypted tunnel. Each AP sends RF spectrum information, client statistics, and various other kinds of information to the Meraki cloud over this tunnel. The admin can log in to the Meraki dashboard—a web browser-based tool—to centrally manage the APs. User data, however, is not tunneled to the cloud; it goes straight to the wired LAN.

Cloud-based APs use cloud computing to offer a scalable, easy-to-manage wireless network solution. Unlike autonomous APs that are managed individually or lightweight APs that require a WLC, cloud-based APs connect to a SaaS cloud service for configuration and management. This architecture simplifies complex tasks such as deploying new APs, adjusting configurations, monitoring network health, and troubleshooting problems. Although centralized management is common to lightweight and cloud-based APs, the main advantages of the cloud-based approach are simplicity and ease of use.

Note Don’t mix up the concepts of cloud-based AP architecture and a cloud WLC deployment. Cloud-based AP architecture manages APs using an SaaS cloud platform. A cloud WLC deployment is a split-MAC architecture with the WLC deployed as a VM in a cloud.

Cloud-managed network devices

Although best known for their cloud-based APs, Cisco Meraki offers a variety of network devices that can be managed from their cloud platform: switches, firewalls, Internet of Things (IoT) devices like cameras and sensors, etc. In this section, let’s move our focus away from wireless LANs to consider the characteristics and benefits of cloud-based network management platforms like Meraki.

Note For an overview of how Cisco Meraki works, check out https://mng.bz/z8zB.

Cloud-managed network devices offer a centralized approach to network management, where configuration, monitoring, and troubleshooting are all handled through a cloud-based platform. This centralized approach is the key characteristic of cloud-managed devices; instead of managing devices one by one via the CLI, you can manage all devices from a single web-based dashboard. This offers a variety of benefits for many enterprises:

Rapid and simplified deployment—Cloud management platforms like Meraki use zero-touch provisioning (ZTP) to facilitate the deployment of new network devices without requiring manual configuration of each device. Newly connected devices automatically connect to the Meraki cloud and download their configurations. This is much simpler than the traditional process, which involves manually configuring new devices one by one via the console port before deploying them to the network.

Simplified management—With a unified interface for managing all devices in the network, adminstrators can spend less time on routine management tasks. Configuration changes can be applied to all devices at once through the cloud, eliminating the need for the manual configuration of each device.

Enhanced visibility and analytics—Cloud platforms provide detailed analytics and reporting tools that can help administrators understand network usage patterns, identify bottlenecks in the network, and optimize network performance.

Automated updates—Network device firmware updates and security patches can be automatically deployed to all devices, ensuring they are up-to-date. Out-of-date software can be a serious vulnerability, so this is a critical part of mainting a secure network.

Operational efficiency—By simplifying the overall process of deploying and managing a network through centralized management and automation, the operating expenses (OpEx)—the ongoing costs associated with maintaining the network—are reduced.

The two key takeaways are centralized management and simplicity. Cloud management solutions like Meraki offer a modern, efficient, and scalable approach to network management for many enterprises. However, it might not be ideal for organizations with highly specialized or complex networking requirements, stringent data privacy concerns that mandate keeping all management data on-premises, or those that require deep customization and control beyond what cloud platforms typically offer.

EXAM TIP Cloud-managed network devices are mentioned in exam topic 2.8, so make sure you can identify the characteristics and benefits of cloud-based management.

Summary
802.11 defines a frame format that differs from Ethernet in a couple of key ways. Depending on the 802.11 standard and message type, some fields might not be present, and there are up to four address fields instead of two.

The 802.11 address fields identify some combination of the following, depending on the message type:

Basic service set identifier (BSSID)—The AP’s BSSID

Destination address (DA)—The final recipient of the frame

Source address (SA)—The original sender of the frame

Receiver address (RA)—The immediate recipient of the frame

Transmitter address (TA)—The immediate sender of the frame

A client’s connection to an AP is called an association. For a client to send and receive wireless traffic via an AP, the client must be associated with the AP.

To discover nearby APs, a client can send a probe request. APs will respond with a probe response. This is called active scanning.

In passive scanning, the client listens for beacon messages that APs send periodically to advertise each BSS.

After discovering an AP, the client must send an authentication request and then, if successful, an association request.

802.11 defines three main types of messages: management, control, and data.

Management frames are used to establish and maintain communications in the wireless LAN. Examples include probe, beacon, authentication, and association messages.

Control frames are used to facilitate the delivery of frames over the medium and include request-to-send (RTS) and clear-to-send (CTS), which are used to request and grant permission to transmit a frame, and acknowledgment (Ack), which is used to acknowledge receipt of a frame.

Data frames carry actual data to and from wireless clients communicating over the network.

APs can be deployed in three main architectures: autonomous, lightweight, and cloud-based.

An autonomous AP is a self-contained unit with the built-in intelligence to handle all aspects of wireless network operations.

Autonomous APs connect to the wired LAN via trunk links; autonomous APs need to be able to translate each SSID to a VLAN on the wired LAN. Furthermore, a separate management VLAN should be used to connect to and manage the AP itself.

Autonomous APs require individual configuration, which is done through the CLI (console, Telnet, or SSH) or GUI via a web browser using HTTP/HTTPS.

Individually managing autonomous APs is not feasible in larger networks. To support larger wireless LANs, a wireless LAN controller (WLC) is used to centralize control and simplify operations.

An AP that is controlled by a WLC is called a lightweight AP (LWAP).

LWAPs offload many of their functions to the WLC; this is called split-MAC architecture.

Real-time operations (sending and receiving RF signals, encrypting frames) are handled by each LWAP, and non-real-time functions (RF management, client authentication and association, QoS and security policy) are handled by the WLC.

Whereas autonomous APs connect to the wired LAN via trunk ports, LWAPs connect via access ports in the management VLAN. The job of translating between SSIDs and VLANs is offloaded to the WLC.

The Control and Provisioning of Wireless Access points (CAPWAP) protocol is used to establish tunnels between LWAPs and the WLC. LWAPs tunnel frames from clients to the WLC, which translates them into Ethernet frames in the appropriate VLAN.

CAPWAP establishes two tunnels from each LWAP to the WLC. The data tunnel is used to tunnel traffic sent to and from wireless clients. The control tunnel is used to tunnel communications between the LWAP and WLC.

The CAPWAP control tunnel is encrypted by default, but the data tunnel is not. CAPWAP encryption uses Datagram Transport Layer Security (DTLS)—a type of TLS that uses UDP instead of TCP.

There are various WLC deployment options that meet different needs: unified, cloud, embedded, and Mobility Express.

A unified WLC is a dedicated hardware appliance; Cisco offers various hardware models that can support anywhere, from a few hundred LWAPS to as many as 6,000 LWAPs and 64,000 clients.

A cloud WLC is a VM deployed on a server in the cloud. Depending on the hardware resources available to the VM, it can support up to 6,000 LWAPs and 64,000 clients.

An embedded WLC is integrated into a switch. Embedded WLCs are more suitable for smaller deployments, supporting up to 200 APs and 4,000 clients.

A Mobility Express WLC is integrated into an AP, supporting up to 100 LWAPs and 2,000 clients.

LWAPs can operate in various modes, some of which provide network service to clients and some that play a network management role.

The default LWAP operational mode is Local, in which the LWAP provide BSSs for clients to connect to, tunneling their traffic to the WLC via CAPWAP.

FlexConnect offers a more flexible approach in which the LWAP can locally switch client traffic between the wired and wireless LANs—no need to tunnel it to the WLC. FlexConnect can be enabled on a per-SSID basis.

An LWAP operating in Bridge mode can form a wireless mesh with other LWAPs without directly connecting each LWAP to the wired network. LWAPs in Bridge mode can also form a bridge connecting two wired LANs.

Flex + Bridge mode adds FlexConnect on top of Bridge mode, allowing the LWAPs in the mesh to locally switch client traffic without tunneling it to the WLC.

In Monitor mode, the LWAP doesn’t transmit from its radios. It is dedicated to analyzing the RF environment and detecting rogue devices.

In Rogue Detector mode, the LWAP’s radios are entirely disabled. It is dedicated to analyzing traffic on the wired LAN to detect rogue devices.

In Sniffer mode, the LWAP captures all wireless traffic on a specific channel and sends it to the WLC for analysis.

In SE-Connect mode, the LWAP is dedicated to RF spectrum analysis on all channels, feeding data to spectrum analysis software like Cisco Spectrum Expert.

In addition to autonomous and lightweight APs, there is a third option that can be considered a middle ground between the two: cloud-based.

Cloud-based AP architecture uses a cloud SaaS platform to streamline the management of APs. Cisco’s offering is Cisco Meraki.

Meraki APs communicate with the Meraki cloud platform over the internet in an encrypted tunnel. Each AP sends RF information, client statistics, and various kinds of other information to the Meraki cloud over this tunnel.

The admin can log in to the Meraki dashboard—a web browser-based tool—to centrally manage the APs.

User data is not tunneled to the cloud; it goes straight to the wired LAN.

Cloud-managed network devices (e.g., Meraki’s APs, switches, and firewalls) offer a centralized approach to network management. Configuration, monitoring, and troubleshooting are all handled through a cloud-based platform like the Meraki dashboard.

Cloud-based management solutions like Meraki offer simplicity, efficiency, and scalability that is beneficial for many modern enterprises. However, it might not be ideal for organizations with highly specialized or complex networking requirements.