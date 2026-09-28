21 Wireless LAN configuration
This chapter covers

Preparing a Cisco WLC for configuration via the GUI
The physical ports and logical interfaces of a Cisco WLC
Configuring simple wireless LANs with WPA2 PSK authentication
Over the past three chapters, we’ve covered the fundamentals of wireless LANs, starting with the basics of radio frequency (RF) communications and 802.11 standards, various wireless LAN architectures, and the many protocols used to secure communications over the airwaves. In this chapter, we’ll bring it all together and see how to configure basic wireless LANs in the graphical user interface (GUI) of a Cisco wireless LAN controller (WLC). Specifically, we will cover the following CCNA exam topics:

2.7 Describe physical infrastructure connections of WLAN components (AP, WLC, access/trunk ports, and LAG)

2.8 Describe network device management access connections (Telnet, SSH, HTTP, HTTPS, console, TACACS+/RADIUS, and cloud managed)

2.9 Interpret the wireless LAN GUI configuration for client connectivity, such as WLAN creation, security settings, QoS profiles, and advanced WLAN settings

5.10 Configure and verify WLAN within the GUI using WPA2 PSK

Wireless LAN configuration is the only CCNA exam topic that requires configuration via the GUI; you could be tested on your knowledge of the WLC GUI via any of the exam question formats (multiple choice, drag-and-drop, lab simulation). When configuring a WLC that potentially manages hundreds or even thousands of lightweight APs (LWAPs), the GUI is usually the tool of choice; it provides a more user-friendly experience, simplifying the configuration, monitoring, and troubleshooting of wireless LANs.

21.1 WLAN initial setup
Before we start looking at how to configure wireless LANs, let’s examine the network we will be configuring and do some initial setup. Figure 21.1 shows the simple network topology we will use for this chapter, consisting of one LWAP (AP1), one switch (SW1), and one WLC (WLC1). SW1 functions as a DHCP server, NTP server, and the default gateway for all subnets. Notice that WLC1’s ports are labeled P1 and P2; Cisco WLC ports are simply called Port 1, Port 2, Port 3, etc.



Figure 21.1 This chapter’s topology. WLC1 controls AP1, an LWAP. SW1 functions as a DHCP server, NTP server, and the default gateway for all subnets. AP1 tunnels client traffic to WLC1, which translates their 802.11 frames to Ethernet frames.

Note To keep the diagram as simple as possible, no external connections are shown. In a real network, SW1 would likely have connections to the internet, the corporate WAN, a larger wired LAN, etc.

The network consists of two WLANs, each mapped to a VLAN on the wired network. There is also a dedicated management VLAN that is used for remote management of network devices; the CAPWAP tunnels between AP1 and WLC1 use this VLAN. In this section, we’ll first configure SW1 to fulfill its role in this LAN. Then we’ll perform an initial configuration of WLC1 before moving on to the main topic: configuring the Guest and Internal WLANs in the GUI of WLC1.

What exactly is a WLAN?

Like the term LAN, the term WLAN can have different meanings depending on the context. For example, it can refer to an entire wireless network with its various APs providing BSSs and ESSs for clients using different SSIDs. In that sense, figure 21.1 depicts a single WLAN consisting of two BSSs, each with a unique SSID. However, a WLAN can also refer to a logical entity within the wireless network—not the wireless network as a whole. By this definition, each SSID is its own WLAN, and figure 21.1 shows two WLANs: one identified by the Internal SSID and one identified by the Guest SSID. We will use this latter definition in this chapter to remain consistent with the wording of the Cisco WLC GUI.

21.1.1 Switch configuration
SW1 fulfills some important roles in this LAN: it’s the wired infrastructure that AP1 connects to, a DHCP server that AP1 and its wireless clients will lease IP addresses from, an NTP server that enables devices in the LAN to keep consistent time, and the default gateway for hosts in each subnet. To configure SW1, let’s start by creating the three VLANs we need:

SW1(config)# vlan 10
SW1(config-vlan)# name Management                 ❶
SW1(config-vlan)# vlan 100
SW1(config-vlan)# name Internal                   ❶
SW1(config-vlan)# vlan 200
SW1(config-vlan)# name Guest                      ❶
❶ Gives each VLAN a descriptive name

Because this LAN uses a split-MAC architecture, AP1 should connect to SW1 via an access port (F0/8) in the management VLAN. I will also configure an additional access port (F0/7) for my own PC; this will allow my PC to connect to WLC1’s GUI over the network when we configure WLANs later in this chapter. To allow the ports to immediately move to the Spanning Tree Protocol (STP) forwarding state, I will enable PortFast as well:

SW1(config)# interface range f0/7-8                ❶
SW1(config-if-range)# switchport mode access       ❶
SW1(config-if-range)# switchport access vlan 10    ❶
SW1(config-if-range)# spanning-tree portfast       ❷
❶ Configures F0/7 and F0/8 as access ports in the management VLAN

❷ Enables PortFast

In a split-MAC architecture, the WLC is responsible for translating between VLANs and WLANs (SSIDs), so it must connect to SW1 via a trunk link to support multiple VLANs. For redundancy and additional throughput capacity, it’s common to connect the WLC to the network via a Link Aggregation Group (LAG). In the following example, I configure SW1 F0/1 and F0/2 as members of a static LAG and configure it as a trunk.

Note Cisco WLCs use the industry-standard terminology LAG instead of EtherChannel—they’re the same thing. Also, note that WLCs only support static LAGs (configured with mode on); they cannot use the negotiation protocols PAgP or LACP.

SW1(config-if-range)# interface range f0/1-2             ❶
SW1(config-if-range)# channel-group 1 mode on            ❶
SW1(config-if-range)# interface port-channel 1           ❷
SW1(config-if)# switchport mode trunk                    ❷
SW1(config-if)# switchport trunk allowed vlan 10,100,200 ❷
❶ Configures F0/1 and F0/2 as members of a static LAG

❷ Configures the LAG as a trunk and allows only the three VLANs used in the LAN

To function as the default gateway for hosts in each subnet, SW1 needs some switch virtual interfaces (SVIs). Routing also must be enabled to allow SW1 to route packets between subnets. In the following example, I enable routing on SW1 and configure an SVI for each of the VLANs we created previously:

SW1(config)# ip routing                                  ❶
SW1(config)# interface vlan 10                           ❷
SW1(config-if)# ip address 192.168.1.1 255.255.255.0     ❷
SW1(config-if)# interface vlan 100                       ❸
SW1(config-if)# ip address 10.0.0.1 255.255.255.0        ❸
SW1(config-if)# interface vlan 200                       ❹
SW1(config-if)# ip address 10.1.0.1 255.255.255.0        ❹
❶ Enables routing

❷ Configures the Management VLAN’s SVI

❸ Configures the Internal WLAN/VLAN’s SVI

❹ Configures the Guest WLAN/VLAN’s SVI

Figure 21.2 illustrates the internal logic of SW1 after configuring these SVIs: three virtual switches (VLANs) connected to a virtual router that can forward traffic between them.



Figure 21.2 The logical internals of SW1, a multilayer switch. Messages from wireless clients are tunneled to WLC1, which sends them over the trunk link to the appropriate SVI on SW1.

Finally, SW1 provides a couple of services to the network: NTP and DHCP. Not only will wireless clients lease their IP addresses from SW1 but so will AP1; LWAPs’ IP addresses are usually not manually configured. In the following example, I configure SW1 as an NTP server and create three DHCP pools: the Management pool (to lease IP addresses to LWAPs) and the Internal and Guest pools (to lease IP addresses to wireless clients). Note that I configure two DHCP options: option 42 and option 43. In all three pools, I configure option 42, which can be used to tell DHCP clients which NTP server they should use (SW1 itself, in this case). Option 43 can be used to tell LWAPs the IP address of their WLC:

SW1(config)# ntp master                               ❶
SW1(config)# ip dhcp pool Management                  ❷
SW1(dhcp-config)# network 192.168.1.0 255.255.255.0   ❷
SW1(dhcp-config)# default-router 192.168.1.1          ❸
SW1(dhcp-config)# option 42 ip 192.168.1.1            ❹
SW1(dhcp-config)# option 43 ip 192.168.1.100          ❺
SW1(dhcp-config)# ip dhcp pool Internal               ❻
SW1(dhcp-config)# network 10.0.0.0 255.255.255.0      ❻
SW1(dhcp-config)# default-router 10.0.0.1             ❻
SW1(dhcp-config)# option 42 ip 10.0.0.1               ❻
SW1(dhcp-config)# ip dhcp pool Guest                  ❼
SW1(dhcp-config)# network 10.1.0.0 255.255.255.0      ❼
SW1(dhcp-config)# default-router 10.1.0.1             ❼
SW1(dhcp-config)# option 42 ip 10.1.0.1               ❼
❶ Makes SW1 an NTP server

❷ Creates a pool for the Management VLAN and assigns its IP range

❸ Specifies SW1 as the default gateway

❹ Tells DHCP clients to use SW1 as their NTP server

❺ Tells DHCP clients (AP1) to use WLC1 as their WLC

❻ Configures a pool for the Internal WLAN/VLAN

❼ Configures a pool for the Guest WLAN/VLAN

Exam Tip Aside from DHCP options 42 and 43, we have covered all of these configurations in previous chapters. The main point to take away is that the WLC only supports static LAG; it can’t use PAgP or LACP to negotiate.

21.1.2 WLC initial configuration
SW1 is configured and ready to go, but we aren’t ready to start configuring WLANs in WLC1’s GUI yet. We need to do some initial configurations on WLC1 first. To do so, I will connect my PC to WLC1’s console port and go through the Cisco Wizard Configuration Tool—a series of CLI prompts. The exam topics are clear that you need to know how to configure WLANs in the GUI, not how to set up a WLC from scratch, so you can expect any WLC configuration questions to start from an already-setup WLC. However, the steps in this section cover some important concepts and are essential to get a WLC up and running.

The output is quite long, so I’ll split it up into several sections. The first prompt asks if you would like to terminate autoinstall—a feature that allows the WLC to automatically download its configuration from a server. In the following example, I press Enter to accept the default choice of yes (as indicated in square brackets):

Welcome to the Cisco Wizard Configuration Tool
Use the '-' character to backup
Would you like to terminate autoinstall? [yes]:
❶ Press Enter to accept the default yes, and terminate autoinstall.

Next, the wizard prompts for the WLC’s system name (hostname) and an admin username/password:

System Name [Cisco_10:65:64] (31 characters max): WLC1            ❶
Enter Administrative User Name (24 characters max): admin
Enter Administrative Password (3 to 24 characters): ***********   ❷
Re-enter Administrative Password                 : ***********    ❷
❶ Configures the WLC’s hostname

❷ Creates an admin username and password

The next prompt asks if you would like to enable link aggregation. I type yes to enable it; I will connect SW1 and WLC1 via a LAG:

Enable Link Aggregation (LAG) [yes][NO]: yes             ❶
❶ Enables link aggregation on WLC1’s ports

The next few prompts ask for information about the management interface—a virtual interface in the WLC that is used to manage it. This is the interface I will connect to later to access WLC1’s GUI. The final setting (DHCP Server IP Address) allows you to specify the DHCP server to which the WLC will forward wireless clients’ DHCP messages (SW1 in this example):

Management Interface IP Address: 192.168.1.100            ❶
Management Interface Netmask: 255.255.255.0               ❶
Management Interface Default Router: 192.168.1.1          ❷
Management Interface VLAN Identifier (0 = untagged): 10   ❸
Management Interface DHCP Server IP Address: 192.168.1.1  ❹
❶ Configures the management interface’s IP address and netmask

❷ Specifies SW1 as WLC1’s default gateway

❸ Configures VLAN 10 as the management VLAN

❹ Specifies SW1 as the DHCP server

Note Specifying a VLAN ID for the management interface means that the WLC will tag all traffic sent from that interface with the specified VLAN ID.

The next few prompts cover some settings whose details are beyond what you need to know for the CCNA exam, but you must enter them to complete the initial configuration. The Virtual Gateway IP Address is used in communications between the WLC and wireless clients and is used for specific purposes like relaying DHCP messages. It should be unique in the network but doesn’t have to be reachable by any other devices. Cisco recommends using an address in one of the ranges reserved for documentation/examples (192.0.2.0/24, 198.51.100.0/24, or 203.0.113.0/24):

Virtual Gateway IP Address: 192.0.2.1
The Multicast IP Address is used by the WLC to send multicast messages to clients. This should be in the multicast (class D) range of 224.0.0.0 to 239.255.255.255. Specifically, it should be in the private (“administratively scoped”) multicast range: 239.0.0.0/8:

Multicast IP Address: 239.239.239.239
The Mobility/RF Group Name is actually two separate settings. The first is the WLC’s mobility group, which is used to allow multiple WLCs to coordinate to support clients that roam between APs controlled by different WLCs. The RF group is used to manage and coordinate RF settings like power levels and channel selections across multiple WLCs. These are usually the same group, but you can change them individually from the GUI later:

Mobility/RF Group Name: ManningCCNA
With those three prompts out of the way, the remaining ones are more familiar. In the next prompt, we have to create a WLAN, specifying its SSID. I’ll delete this later and create the Internal and Guest WLANs, so I named it TEST:

Network Name (SSID): TEST   
The following prompt determines how the WLC will handle DHCP traffic from wireless clients. If you type yes to enable bridging mode, the WLC will forward clients’ DHCP messages as is, simply translating the 802.11 frames to Ethernet frames without any further changes. If you accept the default NO option (the default option is indicated with uppercase letters), the WLC will function in proxy mode—basically, it will function like a DHCP relay agent. I pressed Enter to accept the default:

Configure DHCP Bridging Mode [yes][NO]: 
The wizard then asks if you want to allow clients to use static (manually configured) IP addresses or not. If you select no, all clients will be required to lease an IP address via DHCP. I pressed enter at this prompt to accept the default YES:

Allow Static IP Addresses [YES][no]:
Next up is RADIUS server configuration, which is necessary if using WPA-Enterprise authentication with 802.1X/EAP. The CCNA exam topics state that you need to be able to configure PSK authentication (WPA-Personal), so I’ll type no here:

Configure a RADIUS Server now? [YES][no]: no
The wizard then prompts you for a country code. This is necessary because, as we covered in chapter 18, different countries have different laws governing the use of the RF frequency bands. You might be tempted to enter the country you live in, but if you bought secondhand hardware for a home lab like I did, you need to make sure that the country code you enter matches the regulatory domain of the APs you are using. The regulatory domain of my APs is “-E,” so I entered the code of a country in that regulatory domain: FR (France):

Enter Country Code list (enter ‘help’ for a list of countries) [US]: FR
Note The regulatory domain is indicated in the AP model’s name, i.e., AIR-CAP3502I-E-K9. To view a list of countries and their regulatory domains, go to https://mng.bz/0GBN. If the WLC’s country code isn’t in the same regulatory domain as an AP, the WLC won’t be able to manage the AP.

The following series of prompts asks if you want to enable each of a series of 802.11 standards. I press Enter to accept the default for each. The final Enable Auto-RF option allows the WLC to automatically control each LWAP’s transmit power and channel assignment—it’s usually a good idea to leave this on:

Enable 802.11b Network [YES][no]:
Enable 802.11a Network [YES][no]:
Enable 802.11g Network [YES][no]:
Enable Auto-RF [YES][no]:
We’ve reached the final prompts! In the following prompts, I specify SW1 as WLC1’s NTP server, configure its polling interval (how frequently WLC1 will query the NTP server for the time), and then save the configuration, causing WLC1 to reboot:

Configure a NTP server now? [YES][no]:
Enter the NTP server’s IP address: 192.168.1.1
Enter a polling interval between 3600 and 604800 secs: 3600
Configuration correct? If yes, system will save it and reset. [yes][NO]: yes
21.1.3 Connecting to the WLC
Exam Tip Connecting to a WLC to manage and configure it is CCNA exam topic 2.8: Describe network device management access connections (Telnet, SSH, HTTP, HTTPS, console, TACACS+/RADIUS, and cloud managed).

Now that WLC1’s initial configuration is complete, we can connect to it and configure some WLANs. There are various ways to connect to and configure a WLC. In this section, we’ll cover those different methods and also configure a CPU ACL to restrict which devices can manage the WLC.

Management connections

You can configure a Cisco WLC via either the CLI or the GUI using protocols you’re already familiar with: Telnet, SSH, HTTP, HTTPS, or a console connection. The WLC also has multiple methods of authenticating users who want to connect to it: its own local user database or a RADIUS/TACACS+ AAA server. Figure 21.3 illustrates these different connection methods.

Note The PC needs network access to the WLC to connect via Telnet/SSH or HTTP/HTTPS. Earlier in this chapter, I configured SW1 F0/7 as an access port in the management VLAN, allowing my PC to connect to the network and access WLC1.



Figure 21.3 WLC management connection methods. The CLI can be accessed via the console port or a network connection (Telnet/SSH). The GUI can be accessed over the network via HTTP/HTTPS. The WLC can authenticate users by checking its local user database or a TACACS+/RADIUS server.

The management connection and authentication methods shown in figure 21.3 apply not only to Cisco WLCs, but to other network devices as well. For example, in addition to the familiar CLI, Catalyst switches (Cisco’s line of enterprise-grade switches) have a GUI called the Web User Interface (WebUI) that you can use for configuration and management. However, there’s a reason the CCNA doesn’t test you on how to configure routers and switches using the GUI: it is quite limited compared to the CLI and is rarely used. Instead, the CLI is usually the tool of choice when configuring routers and switches.

While GUI configuration for devices like routers and switches is less common, the opposite is true of WLC management. To connect to WLC1’s GUI, open a web browser, and type the IP address of the WLC’s management interface (192.168.1.100) in the address bar. After logging in with the admin username/password, you’ll be greeted with a screen like that shown in figure 21.4.



Figure 21.4 The Cisco WLC GUI. An image of the WLC is displayed, showing active and inactive ports. WLC settings are organized into various tabs at the top.

Note To more clearly display the relevant sections of the output, I will zoom and crop the screenshots as necessary.

This first screen is the Monitor tab, which shows an overview of the system’s status (such as active and inactive ports). The WLC’s settings are organized into various tabs at the top of the screen, and we will use six of them:

Monitor—Provides an overview of system status and client/AP statistics

WLANs—Manages individual WLAN settings including SSID configuration, security, QoS, and advanced WLAN features

Controller—Configures global settings for the WLC itself, like network interfaces, IP addresses, NTP, etc.

Wireless—Settings related to the LWAPs managed by the WLC

Security—Security settings like ACLs and authentication methods

Management—WLC management settings like management connections (Telnet, SSH, HTTP, HTTPS, console), SNMP, and Syslog

To configure and verify the WLC’s management settings, we’ll first click the Management tab at the top of the screen. From the Management tab, you can see which kinds of connections are allowed by default; this is shown in figure 21.5. By default, HTTP, HTTPS, and SSH connections are allowed—Telnet connections aren’t. You can change these settings from the HTTP-HTTPS and Telnet-SSH menus on the left. For example, you might want to disable HTTP connections because HTTP isn’t a secure protocol; it doesn’t encrypt messages.



Figure 21.5 The Management tab. HTTP, HTTPS, and SSH connections are allowed by default, but Telnet connections aren’t. You can change these settings from the HTTP-HTTPS and Telnet-SSH menus on the left.

The WLC can authenticate users using its local user database (i.e., the admin account created during the initial configuration), a RADIUS server, or a TACACS+ server (or some combination of those three). To check the default settings, click the Security tab, expand the Priority Order dropdown menu, and then select Management User. Figure 21.6 shows the default settings.



Figure 21.6 The default management user authentication methods. The WLC will authenticate users by checking its local user database and, if that fails, by contacting its configured RADIUS server(s).

When a user tries to log in, the WLC will check the user’s credentials against the local user database. If no matching credentials are found, it will check any configured RADIUS servers. If both methods fail, the user won’t be able to log in. You can change which authentication methods are used, and in which order, from this screen.

In addition to the Management User menu, the Security tab includes various other security-related menus. Notably, if using WPA-Enterprise authentication, you can configure the relevant RADIUS settings from the AAA dropdown menu. We will stick to the CCNA exam topics, so we won’t look at the AAA menu, but let’s look at the Access Control Lists dropdown menu to secure access to the WLC with a CPU ACL.

Configuring a CPU ACL

When covering Telnet and SSH in chapter 5, we looked at how to configure an ACL and apply it to the VTY lines of a router or switch to limit which hosts can connect to and configure the device. You can do the same thing on a WLC with a CPU ACL—an ACL that filters traffic destined for the WLC itself, such as HTTP/HTTPS/Telnet/SSH management connections. There are two steps to configuring a CPU ACL: create the ACL, and then apply it as a CPU ACL.

Note This two-step process is identical to configuring ACLs on routers/switches. First you create the ACL, and then you apply it (i.e., to an interface or the VTY lines).

Figure 21.7 shows how to create an ACL. From the Security tab, expand the Access Control Lists dropdown menu, and click Access Control Lists. Click New… to create an ACL (you will be prompted for the ACL’s name), and then click the ACL’s name (MGMT) to edit it and configure some rules.



Figure 21.7 Creating a new ACL. Click New… to create and name it, and then click the ACL’s name to edit it and configure rules.

Clicking the newly created ACL’s name brings you to the Edit page, from which you can create a new rule by clicking Add New Rule at the top right.

Note When covering ACLs in chapters 23 and 24 of volume 1, we used the term access control entry (ACE) for each of the entries in an ACL—the WLC GUI uses the term rule.

Now we can specify the rule’s parameters, as shown in figure 21.8. To secure management access to the WLC, let’s create a rule permitting only IP addresses in the Management subnet (192.168.1.0/24). To finish configuring the rule, click Apply.



Figure 21.8 Configuring an ACL rule’s parameters

Like routers and switches, a WLC’s ACLs have an “implicit deny” rule at the end. Any packets not explicitly permitted by the ACL (packets not sourced from the Management subnet) will be denied, so there’s no need to configure any further rules. The one rule we configured permits the Management subnet, and the implicit deny blocks all other traffic.

We have now created the ACL—all that’s left is to apply it. To do so, click CPU Access Control Lists under the same Access Control Lists dropdown menu, check the Enable CPU ACL box, select the ACL’s name, and click Apply.

Note In addition to filtering HTTP/HTTPS/Telnet/SSH management traffic to the WLC, the CPU ACL also filters CAPWAP traffic from LWAPs to the WLC. When configuring a CPU ACL, make sure you don’t deny CAPWAP traffic from legitimate LWAPs!

21.2 WLC ports and interfaces
Now that we’ve connected to WLC1’s GUI and secured it with a CPU ACL, we are almost ready to configure the Internal and Guest WLANs—but not quite. Each WLAN needs an interface on the WLC that serves to connect the WLAN to a VLAN on the wired network. In this section, we’ll examine the different port and interface types on a WLC and then configure dynamic interfaces to map WLANs to VLANs.

21.2.1 Physical ports and logical interfaces
In chapter 8 of volume 1 on router and switch interfaces, I said that the terms port and interface are often used interchangeably. This is generally true, but in the context of Cisco WLCs, they are strictly different. A WLC port is a physical port—typically an RJ45 port—that cables connect to. A WLC interface is a logical entity in the WLC, like an SVI on a switch. Figure 21.9 illustrates some of the physical port and logical interface types that we will cover.



Figure 21.9 WLC ports and interfaces. Ports are physical connectors that connect to other devices, and interfaces are logical entities in the WLC.

Note The service port and service-port interface shown in figure 21.9 aren’t present in the network we’re using for this chapter.

WLC ports

There are four types of physical ports on a WLC:

Console port—A standard console port like on a router or switch (RJ45 or USB).

Service port—A dedicated management port. This can be used for out-of-band (OOB) management—connecting to and managing the WLC via a dedicated connection that is separate from the DS ports. The service port doesn’t support VLAN tagging; it must connect to an access port on the switch.

Redundancy port—Used to connect two WLCs together to form a redundant pair.

Distribution system port—Standard network ports that connect to the distribution system (DS). DS ports can form a LAG for increased bandwidth and redundancy. WLC1’s LAG connection to SW1 in our example uses DS ports (Port 1 and Port 2).

Note that not all WLC models have all of these port types. The WLC model I’m using for this chapter only has one console port and four DS ports—no service or redundancy ports. In section 21.1.1, I connected my PC directly to WLC1’s console port to perform the initial configuration. WLC1’s two connections to SW1, which form a LAG, are DS ports.

Note If you enable link aggregation (as we did in WLC1’s initial configuration), all of the WLC’s DS ports will be included in the LAG. However, you don’t need to use all of the ports; as long as there is at least one functioning physical port in the LAG, it will be operational.

WLC interfaces

Whereas ports are physical, interfaces are logical entities. Cisco WLCs have a variety of interface types, each used for specific purposes: connecting to and managing the WLC, mapping WLANs to VLANs, communicating between the WLC and its APs, etc. The different interface types are as follows:

Management interface—This is the default interface for in-band management; it maps to a management VLAN (VLAN 10 in this chapter’s network) and sends and receives traffic via the same DS ports as other network traffic.

AP-manager interface—An interface that the WLC uses to communicate with LWAPs via CAPWAP tunnels. The management interface acts as the AP-manager interface by default, but you can optionally configure a separate AP-manager interface to separate CAPWAP traffic from other management traffic (SSH, etc).

Redundancy management interface—When two WLCs are connected by their redundancy ports, one WLC is “active” and the other is “standby.” This interface can be used to connect to and manage the standby WLC.

Service-port interface—This interface corresponds to the physical service port and is used for OOB management.

Virtual interface—The Virtual Gateway IP Address we configured during WLC1’s initial configuration is applied to this interface. It is used for specific purposes like relaying client DHCP messages.

Dynamic interface—A dynamic interface is similar to an SVI on a switch. Each dynamic interface is mapped to a VLAN and a corresponding WLAN. For example, traffic from the Internal WLAN will be sent to the wired network from the WLC’s Internal dynamic interface, tagged in the appropriate VLAN.

21.2.2 Configuring dynamic interfaces
Each WLAN must be mapped to a corresponding dynamic interface. In this section, we’ll create the two dynamic interfaces we need: one for the Internal WLAN and one for the Guest WLAN. Figure 21.10 shows how to create a dynamic interface: from the Controller tab, click the Interfaces menu, and then click New… to create a new interface.



Figure 21.10 Creating a new dynamic interface. From the Interfaces menu in the Controller tab, click New….

Note We will only look at the Interfaces menu, but the Controller tab includes various other settings related to the WLC itself: IP addresses, Ports, DHCP and NTP settings, etc.

The first screen, shown in figure 21.11, prompts you for the interface name and VLAN ID. Although not necessary, I recommend keeping interface, VLAN, and WLAN naming consistent for simplicity’s sake. I named this interface Internal and assigned it to VLAN 100. To move to the next screen, click Apply.



Figure 21.11 Naming an interface and assigning a VLAN ID

Figure 21.12 shows the next screen, where you can configure the interface’s IP address, netmask, and gateway—the address of the router (or multilayer switch, in this case) that can be used to reach external destinations. After that, you can specify the DHCP server that the WLC should forward client DHCP messages to. In this case, the gateway and DHCP server are both SW1’s VLAN 100 SVI.



Figure 21.12 Configuring interface details. SW1’s VLAN 100 SVI (10.0.0.1) functions as both the default gateway and DHCP server. Afterward, click Apply in the top-right corner (not shown).

After creating the dynamic interface for the Internal WLAN, you can repeat the same process for the Guest WLAN’s dynamic interface. When you’re done, you’ll see both interfaces displayed alongside the Management and Virtual interfaces in the Interfaces menu’s list.

21.3 Configuring WLANs
Now that we have created two dynamic interfaces, we can create our two WLANs. When performing WLC1’s initial configuration, the wizard prompted us to create a WLAN—I named it TEST. Instead of editing that WLAN, I’ll delete it and start from a clean slate. Figure 21.13 shows how to do that: from the WLANs tab, select the TEST WLAN, select Remove Selected from the dropdown menu, and click Go. Then, to create a new WLAN, select Create New, and click Go once again.

Exam Tip Configuring WLANs is covered in exam topics 2.9 and 5.10; make sure to familiarize yourself with the basic steps we cover in this section.



Figure 21.13 Deleting the TEST WLAN (created during initial configuration) and creating a new WLAN

The next page, as shown in figure 21.14, asks for three different identifiers for the WLAN: the Profile Name, the SSID, and the ID. The SSID is the name of the WLAN as seen by clients. The Profile Name and ID aren’t seen by clients; they are used only by the WLC. The Profile Name can be any descriptive name—I kept it the same as the SSID. Finally, the ID is a unique numeric identifier. After configuring these three settings, click Apply to move to the next screen.



Figure 21.14 Configuring the Profile Name, SSID, and ID of a WLAN

Figure 21.15 shows the next page, with a series of tabs allowing you to configure various aspects of the WLAN, starting with the General tab. There are two main things to point out here. First, make sure to check the Status box to enable the WLAN; if you don’t do this, the WLAN will be disabled and clients won’t be able to connect to it. Second, make sure to select the appropriate interface. This is the Internal WLAN, so I selected the Internal dynamic interface that we created earlier.



Figure 21.15 The General tab on the WLANs page. Make sure to enable the WLAN, and select the appropriate interface.

21.3.1 WLAN Security settings
Let’s configure the Internal WLAN’s security settings next. As shown in figure 21.16, the Security tab has its own series of tabs, starting with Layer 2; this is where you configure settings like WPA authentication and encryption. These are considered Layer 2 security settings because they control the client’s access to the LAN before the client has its own IP address and is able to participate in Layer 3 communication.



Figure 21.16 WLAN Layer 2 security settings. For the CCNA, you must configure WPA2 with PSK authentication.

CCNA exam topic 5.10 says that you must be able to configure WPA2 PSK authentication, so that’s what we’ll do. From the top dropdown menu, select WPA + WPA2. I’ve also highlighted Protected Management Frame (PMF); as I stated in chapter 20, PMF is mandatory in WPA3 but can optionally be enabled in WPA2 to secure management frames—I’ll leave it disabled since it’s optional. Under WPA + WPA2 Parameters, make sure that WPA2 Policy and AES Encryption are checked. The original WPA is no longer considered secure, and neither is TKIP; leave them disabled. Finally, under Authentication Key Management, notice that 802.1X is enabled by default. The CCNA exam topics list specifies PSK authentication, so I change 802.1X to PSK in figure 21.17.



Figure 21.17 Enabling PSK authentication. The PSK can be configured as an 8- to 63-character ASCII passphrase or a 64-character hexadecimal string.

As we covered in chapter 20, the PSK is 256 bits in length. You can configure it as a string of 64 hexadecimal characters, but it’s much easier to configure an 8- to 63-character ASCII passphrase—the Wi-Fi password that users will use to authenticate. The WLC will convert the passphrase into a 256-bit PSK for you.

Note ASCII, short for American Standard Code for Information Interchange, is a character-encoding standard that represents text in computers. Each ASCII character is 8 bits in length, allowing for 256 (28) unique characters.

From the Layer 3 tab, you can configure additional security measures that take place after the client has connected to the network and received an IP address—hence the name Layer 3. Select Web Policy to view the options, as shown in figure 21.18.



Figure 21.18 Layer 3 security measures take effect after the client has completed any Layer 2 security measures and has an IP address.

The following is a brief description of each. Some of them probably sound familiar; they are often used in public Wi-Fi (i.e., at Starbucks):

Authentication—After the client receives an IP address and tries to access a web page, the user will have to enter a username and password to authenticate.

Passthrough—The user can access the network after accepting certain terms and conditions or viewing a mandatory message. No actual authentication is performed (although an email address might be required).

Conditional Web Redirect—The user will be redirected to a specific web page only under certain conditions (i.e., their password has expired or they need to pay a bill to continue using the network).

Splash Page Web Redirect—The client is shown a particular web page upon connecting to the network.

Exam Tip Although you don’t have to know the details of these Layer 3 security measures, I recommend being able to differentiate between Layer 2 (WPA with PSK or 802.1X) and Layer 3 (web policies like passthrough or redirects) security measures.

21.3.2 WLAN QoS settings
The next tab on the WLANs page after Security is QoS. Wireless QoS is its own can of worms that you don’t have to open for the CCNA. However, you should know the four QoS levels supported by a Cisco WLC, as shown in figure 21.19.



Figure 21.19 The four QoS levels: Platinum, Gold, Silver, and Bronze

The dropdown menu gives a brief description of each. For the Internal WLAN that we are configuring, the default Silver level is appropriate. For the Guest WLAN, Bronze is appropriate; this gives guest user traffic lower priority than internal user traffic:

Platinum—Used for voice (VoIP) traffic, which is sensitive to delay/loss/jitter.

Gold—Used for video traffic.

Silver—Described as “best effort”; this is the default setting and should be used for standard user data traffic.

Bronze—This is the lowest level of service. It should be used for guest services or other low-priority traffic.

Exam Tip Make sure you know the four QoS levels and their descriptions: Platinum = voice, Gold = video, Silver = best effort, and Bronze = background.

21.3.3 WLAN advanced settings
After QoS, we will skip Policy-Mapping and move on to the final tab: Advanced. As figure 21.20 shows, many different settings can be enabled here. Let’s highlight a few of them:

Client Load Balancing—If a client tries to associate with a busy LWAP (with lots of clients) and another less-busy LWAP is in range, the WLC’s response will encourage the client to seek a less-busy LWAP.

Client Band Select—If a client supports both the 2.4 GHz band and the 5 GHz band, LWAPs will delay responses to probes in the 2.4 GHz band, encouraging the client to use the 5 GHz band, which is usually less crowded with devices.



Figure 21.20 The Advanced tab allows you to enable features like Client Load Balancing and Client Band Select.

However, there’s more to the advanced tab. Figure 21.21 scrolls down a bit to where you can enable a familiar feature: FlexConnect. As we covered in chapter 19, FlexConnect can be enabled per WLAN. FlexConnect Local Switching means that the LWAP can switch client traffic between the wired and wireless networks on its own—no need to tunnel it to the WLC. FlexConnect Local Auth allows the LWAP to authenticate clients on its own, instead of relying on the WLC.



Figure 21.21 FlexConnect features can be enabled on a per-WLAN basis from the Advanced tab.

As you can see in figures 21.20 and 21.21, there are plenty of other features in the Advanced tab, but I recommend knowing the few that we covered. Once all configurations are complete, click the Apply button at the top right (you can see it in figure 21.20).

We’ve walked through how to configure the Internal WLAN; the process to configure the Guest WLAN is the same. Figure 21.22 shows the WLANs tab again after creating both WLANs.



Figure 21.22 The WLANs tab with the Internal and Guest WLANs, both of which use WPA2 with PSK authentication

21.3.4 Connecting an LWAP
With the Internal and Guest WLANs configured, let’s see what happens when I connect an LWAP (AP1) to the network. After connecting AP1 to SW1, I waited for a few minutes for it to boot up. Figure 21.23 shows the result: in the Wireless tab of WLC1’s GUI, AP1 is listed. Without any manual configuration of AP1, it joined with and is now managed by WLC1.



Figure 21.23 AP1 (with its default hostname) automatically joined with and is managed by WLC1 without any manual configuration.

After an AP boots up and gets an IP address, it begins the WLC discovery process, in which it attempts to discover any available WLCs. It uses various methods to do this:

Sending broadcast discovery messages to the LAN

Contacting any WLCs it had previously joined

Contacting any WLCs it learned about via manual configuration (in the AP’s CLI)

Contacting any WLCs it learned about via DHCP option 43

Using DNS to attempt to resolve CISCO-CAPWAP-CONTROLLER.local-domain and contacting any WLCs if the resolution succeeds

After using these methods to discover WLCs, the AP will then decide to join one—the logic it uses to select a WLC isn’t important for the CCNA. In our network, there is one WLC (WLC1), and it is located in the same LAN as AP1; this means that WLC1 receives AP1’s broadcast discovery messages. Furthermore, we also configured DHCP option 43 in SW1’s DHCP pool, so AP1 also learns WLC1’s IP address when it leases an IP address from SW1.

Note Because WLC1 is able to receive AP1’s broadcast discovery messages in this case, DHCP option 43 is not necessary; I configured it just for demonstration.

Let’s change the AP’s name from the default name to AP1. To modify an AP’s settings, click the AP name to see the screen shown in figure 21.24. In addition to being able to change the AP’s name, this is where you can change the AP’s operational mode. You should recognize these modes from chapter 19: local, FlexConnect, monitor, etc.



Figure 21.24 The AP configuration screen. From here, you can change the AP’s name, configuration mode, and various other settings.

After joining with WLC1, AP1 receives its configuration information from WLC1, including the two WLANs we configured, which bands and channels it should use, its transmit power, etc. AP1 and WLC1 are now ready to accept clients! Figure 21.25 shows WLC1’s client list after connecting a client to each of the WLANs; you can view the client list by returning to the MONITOR tab and clicking on the Clients menu on the left.



Figure 21.25 WLC1’s client list, with one client connected to each WLAN

As you probably noticed when looking through these screenshots of the GUI, there are countless tabs, menus, and settings that you can configure from the GUI, most of which we skipped over. The settings we covered are the essentials that you should know for the CCNA; I recommend spending some time in the GUI familiarizing yourself with them.

Building a wireless home lab

Although Cisco Packet Tracer does offer a simulated WLC, its functionality is extremely limited. If you have the cash to spare, you can buy the same (or similar) equipment that I used off of eBay for about $100. Here is the equipment I used:

Switch—Cisco Catalyst 2960 Series Switch (any model)

WLC—Cisco 2504 Wireless Controller

AP—Cisco Aironet 3502 access point

With that said, the limited configurations supported by Packet Tracer’s simulated WLC are sufficient for you to familiarize yourself with most of what we covered in this chapter. A physical lab is nice to have but not necessary.

Summary
A WLC usually connects to the network via a Link Aggregation Group (LAG)—the industry-standard term for an EtherChannel. Cisco WLCs only support static LAGs; they cannot use the negotiation protocols PAgP or LACP.

DHCP option 42 can be used to tell DHCP clients which NTP server they should use.

DHCP option 43 can be used to tell LWAPs the IP address of their WLC.

Before you can create WLANs via the WLC GUI, you need to perform some initial configurations. You can do so with the Cisco Wizard Configuration Tool in the CLI by connecting to the WLC’s console port.

The initial configuration includes settings like the management interface; this is the interface you can connect to in order to access the WLC’s GUI.

The Virtual Gateway IP Address is used in communications between the WLC and wireless clients, such as when relaying DHCP messages. It should be unique on the network but doesn’t have to be reachable by other devices.

The Multicast IP Address is used by the WLC to send multicast messages to clients.

The Mobility/RF Group Name configures the mobility group, which is used to allow multiple WLCs to coordinate to support roaming clients, and the RF group, which is used to manage and coordinate RF settings across multiple WLCs.

If you enable DHCP bridging mode, the WLC will forward clients’ DHCP messages as is, simply translating the 802.11 frames to Ethernet frames. If you disable bridging mode, the WLC will function in proxy mode, like a DHCP relay agent.

The WLC’s country code must match the regulatory domain of the LWAPs it manages.

There are various methods to connect to and manage a WLC. You can access the CLI via the console port or over the network via Telnet/SSH. You can access the GUI over the network via HTTP/HTTPS.

The WLC can authenticate users with its own local user database or by using a RADIUS/TACACS+ AAA server.

To connect to the WLC’s GUI, open a web browser, and type the IP address of its management interface in the address bar.

From the Management tab, you can view and modify which kinds of management connections are allowed. By default, HTTP, HTTPS, and SSH connections are allowed, but Telnet connections aren’t.

To view and modify the WLC’s management user authentication methods and their order, go to the Security tab, open the Priority Order dropdown menu, and access the Management User menu.

You can configure a CPU ACL in the Security tab to filter traffic to and from the WLC itself, such as management and CAPWAP traffic.

To configure a CPU ACL, expand the Access Control Lists dropdown menu, create an ACL in the Access Controls Lists menu, and apply it in the CPU Access Control Lists menu.

A WLC port is a physical port, and a WLC interface is a logical entity in the WLC.

The console port is a standard console port like on a router or switch.

The service port is a dedicated out-of-band (OOB) management port. It doesn’t support VLAN tagging, so it must connect to an access port on the switch.

The redundancy port is used to connect two WLCs to form a redundant pair.

Distribution system (DS) ports are the standard network ports that connect to the distribution system.

If you enable link aggregation, all of the WLC’s DS ports will be included in the LAG by default. As long as there is at least one functioning physical port in the LAG, it will be operational.

The management interface is the default interface for in-band management. It maps to a management VLAN and sends and receives traffic via the DS ports.

The AP-manager interface is used by the WLC to communicate with LWAPs via CAPWAP. By default, the management interface functions as the AP-manager interface, but you can configure a separate AP-manager interface.

The redundancy management interface is used to connect to and manage the standby WLC in a redundant pair.

The service-port interface corresponds to the physical service port.

The virtual interface is used for specific purposes like DHCP relay; the Virtual Gateway IP Address is applied to this interface.

A dynamic interface is similar to an SVI on a switch. Each dynamic interface is mapped to a VLAN and corresponding WLAN.

Before creating WLANs, you must create a dynamic interface for each WLAN.

You can create dynamic interfaces from the Interfaces menu of the Controller tab.

You can create WLANs from the WLANs tab. Each WLAN has three identifiers: the SSID is the name as seen by clients. The Profile Name can be any descriptive name (or the same as the SSID), and the ID is a unique numeric identifier.

When creating a WLAN, the Security tab allows you to configure settings like WPA authentication/encryption, which are Layer 2 security settings.

You can configure the PSK as 64 hexadecimal characters or an 8- to 63-bit ASCII passphrase.

The Layer 3 tab allows you to configure web policy security features that require clients to perform additional actions/authentication before accessing the network, such as Authentication, Passthrough, Conditional Web Redirect, and Splash Page Web Redirect.

The QoS tab allows you to specify the WLAN’s QoS level. The levels are Platinum (voice), Gold (video), Silver (best effort, the default), and Bronze (background).

The Advanced tab allows you to configure various optional features. Client Load Balancing encourages clients to associate with less busy LWAPs. Client Band Select encourages clients to use the 5 GHz band instead of the 2.4 Ghz band.

FlexConnect can be enabled from the Advanced tab. FlexConnect Local Switching means the LWAP can switch client traffic between the wired and wireless networks on its own—no need to tunnel it to the WLC.

FlexConnect Local Auth allows the LWAP to authenticate clients on its own.

You can view LWAPs that the WLC controls from the Wireless tab.

After an AP boots up and gets an IP address, it brings the WLC discovery process, in which it attempts to discover WLCs before joining with one.

Discovery methods include broadcast discovery messages, previously joined WLCs, manual configuration, DHCP option 43, and DNS.

You can configure an AP’s operational mode (local, FlexConnect, monitor, etc.) by clicking on the AP name in the Wireless tab.

You can view the list of wireless clients from the Clients menu in the Monitor tab.