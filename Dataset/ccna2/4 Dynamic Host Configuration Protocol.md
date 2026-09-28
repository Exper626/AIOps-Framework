4 Dynamic Host Configuration Protocol
This chapter covers

How Dynamic Host Configuration Protocol (DHCP) automates the configuration of network hosts
Configuring Cisco IOS devices as DHCP servers and clients
Using DHCP relay to enable centralized DHCP servers
Viewing IP settings on Windows, macOS, and Linux
Dynamic Host Configuration Protocol (DHCP) is a protocol that automates the assignment of IP addresses, default gateways, and other network configuration information to hosts. But what exactly is a host? A host is any device that sends and receives packets over a network—put in other terms, any device with an IP address. Manually configuring thousands (or tens of thousands) of hosts in a large network is simply not feasible. Even in a small network—for example, a home network—automating host configuration makes using the network much simpler for end users who might not be tech savvy (or even if they are, would rather not have to manually configure all of their devices).

Hosts can also include network infrastructure devices like routers and switches—as we’ll see in the next chapter on Secure Shell (SSH), even a Layer 2 switch can have an IP address to allow remote management. However, DHCP is most often used to automate the configuration of end hosts, such as PCs, smartphones, tablets, etc., and is almost ubiquitous in modern networks. In this chapter, we will cover the following CCNA exam topics:

1.10: Verify IP parameters for Client OS (Windows, Mac OS, Linux)

4.3: Explain the role of DHCP and DNS within the network

4.6: Configure and verify DHCP client and relay

4.1 The basic functions of DHCP
For a host to communicate over a network, it needs certain settings to be configured. In most cases, the following four are the bare minimum:

IP address—Acts as the host’s identity on the network, providing an address to send and receive packets

Netmask—Allows the host to determine which IP addresses belong to its LAN and which do not

Default gateway—Enables the host to communicate with devices in different LANs

DNS server address—Translates human-readable domain names into IP addresses

While it is possible to manually configure these settings on each host, this approach is not scalable. In a large network, manually configuring all of these parameters on thousands of hosts would be both time consuming and error prone; occasional typos are inevitable, and more typing means more typos.

Furthermore, manual configuration isn’t flexible. In dynamic environments where hosts frequently move between networks—think of a smartphone or laptop—manual configuration quickly becomes impractical. DHCP, on the other hand, automates host configuration in a way that is both accurate (less error prone) and scalable.

DHCP uses a client–server model in which clients send requests to a DHCP server, which then leases an IP address to each client, along with providing other settings such as the client’s default gateway. Figure 4.1 shows a router using DHCP to lease IP addresses to clients in a LAN—in small networks, it’s common for a router to function as a DHCP server.

Note DHCP is stateful, meaning the DHCP server keeps track of the addresses it leases to clients. This is in contrast to SLAAC (as covered in chapter 21 of volume 1), which is stateless—no server keeps track of each device’s IP address.



Figure 4.1 R1, a DHCP server, leases IP addresses to clients PC1 and PC2. In addition to IP addresses, clients learn their netmask, default gateway, and DNS server addresses. R1 keeps track of leases and when they expire.

In this section, we’ll examine the DHCP leasing process step by step. Then, we’ll examine how to configure a Cisco IOS device to function as both a DHCP server and a DHCP client.

4.1.1 Leasing an IP address with DHCP
For a DHCP client to lease an IP address from a DHCP server, there is a four-step process that you can remember as DORA, for the first letter of each message type involved:

DISCOVER—Client locates DHCP servers and announces that it needs an IP address

OFFER—Server offers the client an IP address (and other settings)

REQUEST—Client accepts the offered IP address

ACK (Acknowledgment)—Server confirms and finalizes the lease

Note The four message types are actually named DHCPDISCOVER, DHCPOFFER, DHCPREQUEST, and DHCPACK in RFC 2131, which defines DHCP. I’ll keep the uppercase lettering but leave out DHCP from each message’s name.

DHCP uses UDP as its Layer 4 protocol. However, unlike most other protocols in which only the server uses a reserved port (and the client uses an ephemeral port), in DHCP both use reserved ports. DHCP servers source their messages from and listen on UDP port 67, and DHCP clients source messages from and listen on UDP port 68.

Exam Tip Memorize those ports! DHCP server = UDP 67, DHCP client = UDP 68.

Bootstrap Protocol

DHCP is based on an older protocol called Bootstrap Protocol (BOOTP). DHCP features many improvements over BOOTP, which is now considered obsolete. Like DHCP, BOOTP also used UDP ports 67 and 68. In fact, when specifying these port numbers in an extended ACL, the keywords in the command are bootps (BOOTP server, UDP 67) and bootpc (BOOTP client, UDP 68), even though DHCP supplanted BOOTP many years ago.

Figure 4.2 outlines the four-message DORA process. PC1 (a DHCP client) broadcasts a DISCOVER message. Then, R1 (a DHCP server) responds with an OFFER message. PC1 replies with a REQUEST message, again destined for the broadcast IP address 255.255.255.255. Finally, R1 replies with an ACK message.



Figure 4.2 Leasing an IPv4 address via DHCP (the DORA process): (1) DISCOVER from client to server, (2) OFFER from server to client, (3) REQUEST from client to server, (4) ACK from server to client.

The DHCP process begins when a client first connects to a network; for example, after a PC boots up or after it is connected to a router/switch with a cable. To communicate over the network, the client needs to know its network configuration—IP address, netmask, etc.—so it will initiate the DHCP leasing process.

A DISCOVER message is sent by the client to locate any DHCP servers on the LAN and let those servers know that the client wants an IP address. Because the client doesn’t have an IP address yet, it sources this packet from 0.0.0.0—the all-zeros IP address, which is reserved for a few uses, such as DHCP. The client also doesn’t know the IP address of any DHCP servers, so it sends the packet to 255.255.255.255—the reserved broadcast address.

Note When a host first connects to a switch port, it takes 30 seconds for the switch port to move through the Spanning Tree Protocol (STP) listening and learning states to the forwarding state; this will block the client’s DISCOVER messages, preventing it from getting an IP address via DHCP. However, you can configure PortFast to allow the switch port to skip to the forwarding state.

After receiving the DISCOVER message, the DHCP server will reply with an OFFER message, which offers an IP address to the client. This message is usually sent as a unicast packet destined for the IP address offered to the client; to offer PC1 10.0.0.6, R1 will address the OFFER message to 10.0.0.6. However, because the client technically doesn’t have an IP address configured yet, some client devices will be unable to accept unicast packets until the DHCP leasing process is complete; such clients will indicate so in the initial DISCOVER message, and the server will broadcast the OFFER message instead.

Note If there are multiple DHCP servers in the LAN, all will send OFFER messages to the client. In this case, the client will typically accept the first OFFER it receives. However, this situation is rare; usually, there will be just one server.

To accept the offered IP address, the client will send a REQUEST message, again sourced from 0.0.0.0. Although the client now knows the server’s IP address (because it received the OFFER from the server), the client broadcasts this message to all hosts in the LAN. The reason is to accommodate situations where multiple DHCP servers sent OFFERs—if a server sees that another server’s OFFER was accepted, it knows that its own OFFER was not. A server whose OFFER was not accepted will free up its offered IP address to be leased to other clients.

To confirm and finalize the lease, the server will send an ACK message. Like the OFFER message, this can be unicast or broadcast, depending on the capabilities of the client. After receiving the ACK, the lease process is complete; the client can start using the assigned IP address (and other parameters) to communicate over the network.

Note An IP address learned via DHCP is called a dynamic IP address, whereas a manually configured IP address is called a static IP address.

Lease renewal

DHCP leases are typically not permanent. Lease time can vary from a few hours (or even a few minutes) in public Wi-Fi networks to 24 hours or more for home networks. To maintain network connectivity, a client must renew its lease. To do so, the client will send a REQUEST message to the server it is leasing the address from; unlike the REQUEST in the DORA process, this is a unicast message. Typically, a client starts this renewal process when 50% of its lease time has expired. Upon receiving the REQUEST, the DHCP server responds with an ACK message, effectively renewing the lease.

4.1.2 Cisco IOS as a DHCP server
In small networks, the router usually serves as the DHCP server for hosts in its connected LANs. Home routers, for example, are typically preconfigured as DHCP servers; a user only has to connect their devices to the router to use the network—no need to understand how to configure IP addresses or even what an IP address is.

In this section, we’ll look at how to configure a Cisco IOS router as a DHCP server, including how to configure a DHCP pool—a group of IP addresses that can be leased to clients—and how to exclude particular addresses from that pool. Figure 4.3 shows the configurations we’ll cover.



Figure 4.3 Configuring a Cisco IOS router as a DHCP server, specifying a range of excluded addresses, and then creating a pool of addresses to lease to clients

Configuring the DHCP pool

The first command we will cover is ip dhcp excluded-address low-ip high-ip, which specifies a range of IP addresses that will not be leased to clients. This command is optional, but it’s common to reserve some IP addresses for hosts whose IP addresses you plan to statically assign. For example, a server’s IP address should be manually configured in most cases rather than leased via DHCP—the server’s IP address should remain constant so clients can easily connect to it. In the following example, I reserve the first few addresses from the 10.0.0.0/24 subnet:

R1(config)# ip dhcp excluded-address 10.0.0.2 10.0.0.5       ❶
❶ Exclude four addresses: 10.0.0.2 to 10.0.0.5

Note There is no need to exclude the network address (10.0.0.0), the broadcast address (10.0.0.255), or any IP addresses configured on the router itself (10.0.0.1)—the router knows not to lease them to clients.

The next step is to create a DHCP pool for the 10.0.0.0/24 subnet—the range of IP addresses that will be leased to hosts. The following example shows how to create a DHCP pool and specifies a range of IP addresses and various other parameters:

R1(config)# ip dhcp pool POOL1                   ❶
R1(dhcp-config)# network 10.0.0.0 /24            ❷
R1(dhcp-config)# default-router 10.0.0.1         ❸
R1(dhcp-config)# dns-server 10.0.0.1 8.8.8.8     ❹
R1(dhcp-config)# domain-name jeremysitlab.com    ❺
R1(dhcp-config)# lease 0 5 30                    ❻
❶ Creates the DHCP pool

❷ Specifies the range of leasable addresses

❸ Specifies the default gateway

❹ Specifies DNS server(s)

❺ Specifies the clients’ domain name

❻ Specifies a lease time of 0 days, 5 hours, and 30 minutes

The command to create a DHCP pool is ip dhcp pool name. That brings you to DHCP config mode, where you can configure the various parameters that will be leased to clients, including the range of IP addresses.

The network network-address {netmask | /prefix-length} command configures the range of IP addresses to lease to clients. Note that you can either specify a netmask (i.e., 255.255.255.0) or a prefix length (i.e. /24). In the example, I configured network 10.0.0.0 /24, specifying that clients should be leased addresses from the 10.0.0.0/24 range—network 10.0.0.0 255.255.255.0 would have the same effect.

As mentioned previously, the router won’t lease the network address or broadcast address to clients, nor will it assign the router’s own address or any addresses in an excluded range (10.0.0.2–10.0.0.5), even if they fit within the range specified in this command (10.0.0.0/24).

Exam Tip Although the network command is configured in DHCP config mode, the ip dhcp excluded-address command is configured in global config mode. Don’t mix those up!

I then used the default-router ip-address command, which specifies the default gateway clients should use. In this case, I specified 10.0.0.1—R1’s own IP address—as the default gateway. Note that although the more common term is default gateway (gateway is an old term for a router), this command is default-router.

The next command is dns-server ip-address, which allows you to specify the DNS server(s) that clients should send DNS queries to. You can specify up to eight DNS servers with this command, with a space between each. In the example, I specified two with dns-server 10.0.0.1 8.8.8.8—R1 itself and Google’s public DNS server.

Those first three commands—network, default-router, and dns-server—are the essentials you should specify when configuring a DHCP pool. With those parameters, hosts will be able to communicate with local and remote destinations and will be able to resolve domain names to IP addresses. However, there are many more settings that you can configure, and in the example I used two more: domain-name and lease.

The domain-name domain-name command tells the clients their domain name. For example, PC1 will know its full domain name is pc1.jeremysitlab.com. This makes it easier for computers in the same domain to communicate using just hostnames instead of FQDNs. When you ping another computer from PC1, you can simply type ping pc2; PC1 will automatically add the domain name, making it pc2.jeremysitlab.com.

The final command we’ll look at is lease days hours minutes, which allows you to specify the duration of leases. The default is 24 hours, but in the example, I used lease 0 5 30 to specify a lease time of 5 hours and 30 minutes. The default of 24 hours is usually fine, but you might want to reduce it for networks that have lots of clients coming and going (i.e., public Wi-Fi networks) to ensure that addresses remain available for new clients, instead of being reserved for clients that have long left the network.

Note You can also configure lease infinite to specify an unlimited lease duration.

R1 is now a DHCP server! In the following example, I use show ip dhcp binding on R1 to confirm that PC1 and PC2 have successfully leased IP addresses from R1:

R1# show ip dhcp binding 
Bindings from all pools not associated with VRF:
IP address   Client-ID/           Lease expiration        Type
             Hardware address/
             User name
10.0.0.6     0152.5400.172f.da    Sep 06 2023 01:50 PM    Automatic     ❶
10.0.0.7     0152.5400.1792.08    Sep 06 2023 01:51 PM    Automatic     ❷
❶ PC1 leased 10.0.0.6 from R1.

❷ PC2 leased 10.0.0.7 from R1.

Note In section 4.3, we will look at how to verify the IP settings directly on clients, specifically on Windows, macOS, and Linux devices.

In some cases, you may need to manually clear some or all of the addresses in the server’s binding table—for example, to free up addresses bound to clients that have already left the network or when testing DHCP in a lab environment. You can clear the DHCP binding table with clear ip dhcp binding {* | ip-address}; specifying * clears all bindings, and specifying ip-address clears only the specified binding.

The DHCP client ID

The Client-ID/Hardware address/User name column in the output of show ip dhcp binding can be a bit confusing. In DHCP, it’s important that each client has a unique identifier so the server can differentiate between clients. The client typically indicates its client ID in its DISCOVER message (and every message thereafter).

Although the formatting in the previous output makes the client IDs look like MAC addresses with two extra hexadecimal digits at the end (da and 08), they are actually MAC addresses with two extra hexadecimal digits at the beginning. Both PC1 and PC2 use a client ID format consisting of the prefix 01, which indicates the interface hardware type (Ethernet), plus the interface’s MAC address. For example, PC1’s MAC address is 5254.0017.2fda, but when the prefix 01 is added, IOS formats the client ID as 0152.5400.172f.da.

Don’t expect all client IDs to look like this—there are other formats that you might encounter. The details of the client ID and its possible formats are beyond the scope of the CCNA exam, but I remember being curious about the meaning of this column when I first saw the output of show ip binding, and I’m guessing that you might have been curious too.

Address conflicts

Before a DHCP server leases an IP address to a client, it should check to make sure that the address is unique—that another device isn’t already configured with that IP address. Although the DHCP server should keep track of which IP addresses have been leased, it’s possible that another device has been manually configured with an IP address that is in the server’s range of leasable addresses; you might have forgotten to exclude that IP address with the ip dhcp excluded-address command. This is called an address conflict. Figure 4.4 outlines how a router detects address conflicts.



Figure 4.4 R1 detects an address conflict. (1) PC3 sends a DISCOVER message, and R1 selects 10.0.0.8 to lease to PC3. (2) Before sending an OFFER, R1 pings 10.0.0.8 to verify it’s not in use. (3) SRV1’s IP address is 10.0.0.8, so it replies to R1. (4) R1 marks 10.0.0.8 as conflicted.

Cisco IOS DHCP servers send pings to detect address conflicts—addresses in the DHCP pool that are already in use by another host. After the server receives a DISCOVER message from a client, it will decide which address to lease to the client. However, before sending the OFFER message, the server will ping the IP address it intends to lease to the client; if there is no reply, the address is unique. However, if there is a reply, it means the address is not unique; another host is already using it. You should then see a message like this:

%DHCPD-4-PING_CONFLICT: DHCP address conflict:  server pinged 10.0.0.8.
The address is marked as a conflict and is removed from the DHCP pool. The server will then select a different IP address to lease to the client and use the same process to determine whether that address is unique. You can confirm IP address conflicts with the show ip dhcp conflict command, as in the following example:

R1# show ip dhcp conflict 
IP address        Detection method   Detection time          VRF
10.0.0.8          Ping               Sep 06 2023 08:40 AM   
R1 won’t assign 10.0.0.8 to any clients until the conflict is resolved—for example, by changing SRV1’s IP address. After resolving the conflict, you must also clear it from the conflict table. You can use clear ip dhcp conflict ip-address to clear the specific conflict from the table or clear ip dhcp conflict * to clear all conflicts.

4.1.3 Cisco IOS as a DHCP client
Network infrastructure devices like routers and switches typically use static (manually configured) IP addresses instead of dynamic IP addresses learned via DHCP. One reason is to simplify device management; if devices’ IP addresses remain constant, it’s easier to identify and connect to each device for remote management. Changing a router’s IP addresses could also affect other routers’ routes; next-hop IP addresses might need to change. For those and other reasons, you should usually manually configure the IP addresses of network devices.

However, one common use case for configuring a router as a DHCP client is for a connection to an Internet Service Provider (ISP). An ISP-connected interface can be configured as a DHCP client, allowing the router to learn its IP address from the ISP and automatically install a default route with the ISP’s router as the next hop. Figure 4.5 shows how to configure a Cisco router’s interface as a DHCP client.



Figure 4.5 R1 is a DHCP client of the ISP. (1) Configure G0/1 to learn its IP address via DHCP. (2) DORA exchange between R1 and the ISP router. (3) R1 configures the learned IP on G0/1, and adds a default route via the ISP router.

Configuring a Cisco IOS device as a DHCP client is simple: just use the ip address dhcp command on the appropriate interface. In the following example, I configure R1’s G0/1 interface as a DHCP client and then confirm that it has learned both an IP address and a default route via DHCP:

R1(config)# interface g0/1
R1(config-if)# ip address dhcp                                  ❶
R1(config-if)# no shutdown                                      ❶
*Dec 28 05:11:37.351: %LINK-3-UPDOWN: Interface GigabitEthernet0/1, 
➥changed state to up
*Dec 28 05:11:38.351: %LINEPROTO-5-UPDOWN: Line protocol on Interface
➥GigabitEthernet0/1, changed state to up
*Dec 28 05:11:45.611: %DHCP-6-ADDRESS_ASSIGN:                   ❷
➥Interface GigabitEthernet0/1 assigned DHCP address            ❷
➥192.168.255.50, mask 255.255.255.0, hostname R1               ❷
R1(config-if)# do show ip interface g0/1                        ❸
GigabitEthernet0/2 is up, line protocol is up
  Internet address is 192.168.255.191/24
  Broadcast address is 255.255.255.255
  Address determined by DHCP                                    ❹
. . .
R1(config-if)# do show ip route
. . .
Gateway of last resort is 203.0.113.1 to network 0.0.0.0        ❺
S*    0.0.0.0/0 [1/0] via 203.0.113.1                           ❺
. . .
❶ Configures R1 G0/1 as a DHCP client and enables it

❷ A log message indicates that G0/1 was assigned an IP address via DHCP.

❸ Confirms G0/1’s IP settings

❹ R1 learns its IP address via DHCP.

❺ R1 learns a default route with the ISP’s router as the next hop.

Notice that the code S is shown next to the default route. Normally, this code indicates a route that was manually configured with the ip route command. However, this code is a bit misleading in this case; this route was learned dynamically via DHCP, not statically configured. This can be considered a quirk of Cisco IOS; DHCP-learned routes use the code S instead of their own unique code (like OSPF’s O or EIGRP’s D).

4.2 DHCP relay
Although a Cisco router can act as a DHCP server for clients in its connected LANs, networks above a certain size will likely use a centralized approach; instead of having each LAN’s router function as a DHCP server, a centralized DHCP server is used. A centralized DHCP server simplifies the management of DHCP pools, helps maintain a consistent set of DHCP policies and configurations, and reduces the total number of DHCP servers required. Furthermore, dedicated DHCP servers, which are designed specifically for DHCP services, typically provide more advanced features that are not supported by Cisco IOS.

However, there is a problem: DHCP relies on broadcast messages, which only remain within the local subnet—routers don’t forward broadcast messages to other networks. So, how can a client’s DISCOVER and REQUEST messages reach a centralized DHCP server that is not in its local subnet?

The answer is DHCP relay, in which a router acting as a DHCP relay agent forwards DHCP clients’ broadcast DISCOVER and REQUEST messages as unicast packets to a remote DHCP server. Figure 4.6 demonstrates the concept and also shows how to configure a Cisco router as a DHCP relay agent.



Figure 4.6 The ip helper-address command makes R1 a DHCP relay agent, forwarding clients’ DHCP messages to the specified server.

To configure a Cisco router as a DHCP relay agent, use the ip helper-address server-ip command on the interface connected to the clients. This is very important! The command must be configured on the correct interface; the interface that will actually receive the clients’ broadcast messages. Using figure 4.6’s example, when PC1 broadcasts a DISCOVER message, R1 will receive it on its G0/0 interface, so the ip helper-address command must be configured on that interface.

Note A helper address is an IP address of a server that the router can relay clients’ broadcast messages to. Although most frequently used in the context of DHCP relay, the concept is not exclusive to DHCP—other protocols can use a helper address, too.

With the command configured, R1 acts as a middleman between PC1 (a DHCP client) and SRV1 (a DHCP server). R1 receives PC1’s broadcast DISCOVER and REQUEST messages and forwards them as unicast packets to SRV1. Likewise, R1 receives SRV1’s OFFER and ACK messages and forwards them to PC1. In the following example, I use the ip helper-address command on R1 G0/0, and confirm with show ip interface:

R1(config)# interface g0/0
R1(config-if)# ip helper-address 10.2.2.10       ❶
R1(config-if)# do show ip interface g0/0
GigabitEthernet0/0 is up, line protocol is up
  Internet address is 10.0.0.1/24
  Broadcast address is 255.255.255.255
  Address determined by non-volatile memory
  MTU is 1500 bytes
  Helper address is 10.2.2.10                    ❷
. . .
❶ Configures R1 G0/0 as a DHCP relay agent

❷ SRV1’s IP address is a helper address.

4.3 Client OS IP settings
Although the CCNA exam is focused on Cisco IOS (as you’ve probably noticed), Cisco expects you to be able to verify the IP settings of client devices using the Windows, macOS, and Linux operating systems (OSs).

Note Linux is technically not an OS, but a family of OSs based on the Linux kernel (a program at the core of the OS); each Linux-based OS is called a Linux distribution.

From a practical perspective, this is something you might do as part of the troubleshooting process if a client is unable to communicate over the network. In this section, we’ll look at some commands on each OS that allow you to verify clients’ IP settings.

4.3.1 IP settings in Windows
Windows offers two CLI applications that you can use to interact with it: Command Prompt and PowerShell. Command Prompt is nice and simple, whereas PowerShell includes more advanced functionality; the commands we will cover here work in both programs. The most basic command that you can use to verify IP settings on a Windows PC is ipconfig, as shown in the following example:

C:\Users\jmcdo> ipconfig
. . .
Ethernet adapter Ethernet1:
   Connection-specific DNS Suffix  . : jeremysitlab.com     ❶
   IPv4 Address. . . . . . . . . . . : 192.168.1.224        ❷
   Subnet Mask . . . . . . . . . . . : 255.255.255.0        ❷
   Default Gateway . . . . . . . . . : 192.168.1.1          ❸
❶ My PC’s DNS suffix (domain name)

❷ My PC’s IP address and netmask (subnet mask)

❸ My PC’s default gateway (my router’s IP address)

However, ipconfig only shows the most basic information about the device’s configuration. For more information, use ipconfig /all, as in the following example:

C:\Users\jmcdo> ipconfig /all
. . .
Ethernet adapter Ethernet1:
   Connection-specific DNS Suffix  . : jeremysitlab.com
   Description . . . . . . . . . . . : Intel(R) Ethernet Controller (3) I225-V
   Physical Address. . . . . . . . . : D8-BB-C1-CC-FF-76                        ❶
   DHCP Enabled. . . . . . . . . . . : Yes                                      ❷
   Autoconfiguration Enabled . . . . : Yes
   IPv4 Address. . . . . . . . . . . : 192.168.1.224(Preferred)                 ❸
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Lease Obtained. . . . . . . . . . : Thursday, September 7, 2023 9:29:52 AM
   Lease Expires . . . . . . . . . . : Thursday, September 7, 2023 3:29:51 PM
   Default Gateway . . . . . . . . . : 192.168.1.1                              ❹
   DHCP Server . . . . . . . . . . . : 192.168.1.1                              ❹
   DNS Servers . . . . . . . . . . . : 192.168.1.1                              ❹
   NetBIOS over Tcpip. . . . . . . . : Enabled
❶ My PC’s MAC address

❷ DHCP is enabled on my PC’s interface.

❸ (Preferred) means my PC requested this IP address (because it used it previously).

❹ My PC’s default gateway, DHCP server, and DNS server are all my router.

You might be surprised that Windows PCs build their own routing table. Although they don’t route packets from other hosts, they can use the routing table to ensure that they send their own packets to the correct next hop. You can view the routing table with netstat -rn, as in the following example:

C:\Users\jmcdo> netstat -rn
. . .
IPv4 Route Table
===========================================================================
Active Routes:
Network Destination    Netmask          Gateway      Interface      Metric
        0.0.0.0        0.0.0.0          192.168.1.1  192.168.1.224  25     ❶
. . .
        192.168.1.0    255.255.255.0    On-link      192.168.1.224   281   ❷
        192.168.1.224  255.255.255.255  On-link      192.168.1.224   281   ❷
. . .
❶ A default route to my router

❷ Routes to my PC’s connected subnet and its own IP address

Note netstat on its own shows active TCP connections. -r tells it to show the routing table, and -n tells it to display numerical addresses (otherwise, it will attempt reverse DNS lookups to translate the IP addresses to domain names). You can combine -r and -n into -rn, as I did in this example.

4.3.2 IP settings in macOS
In macOS, you can access the device’s CLI with the Terminal application. The macOS equivalent of Windows’ ipconfig is ifconfig, and it displays similar information. In the following example, I use the command on my MacBook:

jeremy@Jeremys-MacBook-Air ~ % ifconfig
. . .
en5: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
options=6467<RXCSUM,TXCSUM,VLAN_MTU,TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,
ZEROINVERT_CSUM>
    ether 00:e0:4c:68:92:ff                                                ❶
    inet6 fe80::1838:d69d:2d7d:7ecf%en5 prefixlen 64 secured scopeid 0x18 
    inet 192.168.1.225 netmask 0xffffff00 broadcast 192.168.1.255          ❷
    nd6 options=201<PERFORMNUD,DAD>
    media: autoselect (100baseTX <full-duplex>)
    status: active
❶ My MacBook’s MAC address

❷ My MacBook’s IP address, netmask, and subnet broadcast address

Note macOS displays the netmask in hexadecimal: 0xffffff00 is equivalent to 255.255.255.0.

macOS devices also build a routing table, like Windows devices. To view it, the command is the same as in Windows (netstat -rn), although the output is slightly different. I use that command in the following example to view my MacBook’s default gateway:

jeremy@Jeremys-MacBook-Air ~ % netstat -rn
Routing tables
Internet:
Destination        Gateway            Flags           Netif Expire
default            192.168.1.1        UGScg             en5          ❶
. . .    
❶ My MacBook’s default gateway is 192.168.1.1 (my router).

4.3.3 IP settings in Linux
Because Linux isn’t a single OS but rather a variety of OSs built on top of the Linux kernel, there is some variation in how to view the IP settings. Some Linux distributions still support an old set of commands called net-tools by default, which include ifconfig (to view interface information) and route (to view the routing table). The following example shows the output of those commands on a Linux host named linuxpc:

jeremy@linuxpc ~ $ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.226  netmask 255.255.255.0  broadcast 192.168.1.255    ❶
        inet6 fe80::5054:ff:fe17:7862  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:17:78:62  txqueuelen 1000  (Ethernet)                  ❷
. . .
jeremy@linuxpc ~ $ route
Kernel IP routing table
Destination   Gateway       Genmask        Flags  MSS  Window irtt Iface
0.0.0.0       192.168.1.1   0.0.0.0        UG     0    0      0    eth0       ❸
192.168.1.0   0.0.0.0       255.255.255.0  U      0    0      0    eth0       ❹
. . .
❶ linuxpc’s IP address is 192.168.1.226/24.

❷ linuxpc’s MAC address is 52:54:00:17:78:62.

❸ A default route

❹ A route to linuxpc’s connected LAN

Note netstat -rn works in Linux, too.

Other distributions have removed default support for net-tools, instead using a set of commands called iproute2. In the following example, I use iproute2’s equivalents to ifconfig and route: ip addr and ip route:

jeremy@linuxpc ~ $ ip addr
. . .
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
    link/ether 52:54:00:17:78:62 brd ff:ff:ff:ff:ff:ff                  ❶
    inet 192.168.1.226/24 brd 192.168.1.255 scope global dynamic eth0   ❷  
       valid_lft 86042sec preferred_lft 86042sec
. . .
jeremy@linuxpc ~ $ ip route
default via 192.168.1.1 dev eth0 proto dhcp src                         ❸
➥192.168.1.226 metric 1024                                             ❸
192.168.1.0/24 dev eth0 proto kernel scope link src                     ❸
➥192.168.1.226                                                         ❸
. . .
❶ linuxpc’s MAC address (and broadcast MAC address)

❷ linuxpc’s IP address, broadcast address, and other information

❸ A default route and a route to linuxpc’s connected LAN

Exam Tip Lots of additional information is shown in the output of the commands we covered. If you can identify the parameters we covered here (IP address, netmask, MAC address, etc.) in the output of each command, you should be ready to answer questions about this topic on the CCNA exam.

Summary
For a host to communicate over a network, it typically needs an IP address, a netmask, a default gateway, and a DNS server.

Manually configuring each host with those parameters in a large network isn’t feasible and isn’t desirable even in small networks. Dynamic Host Configuration Protocol (DHCP) automates the configuration of these parameters on hosts.

DHCP uses a client–server model in which clients send requests to a DHCP server, which leases an IP address to each client. DHCP is stateful, meaning the server keeps track of the addresses it leases to clients.

DHCP servers source messages from and listen on UDP port 67, and DHCP clients source messages from and listen on UDP port 68.

The DHCP leasing process consists of four steps, usually called DORA: DISCOVER, OFFER, REQUEST, and ACK (Acknowledge).

The DISCOVER message is sent by the client to locate any DHCP servers and announce that the client needs an IP address. It is sourced from 0.0.0.0 and broadcast to 255.255.255.255.

The OFFER message is sent by the server to offer an IP address (and other configurations) to the client. It is either addressed to the offered IP address (unicast) or broadcast to 255.255.255.255.

If multiple DHCP servers send OFFER messages, the client typically accepts the first.

The REQUEST message is sent by the client to accept the server’s OFFER. It is sourced from 0.0.0.0 and broadcast to 255.255.255.255.

The ACK message is sent by the server to confirm and finalize the lease. After receiving this message, the client can use the leased parameters to communicate over the network.

An IP address learned via DHCP is called a dynamic IP address, whereas a manually configured IP address is called a static IP address.

In small networks, the router usually serves as the DHCP server.

Use ip dhcp excluded-address low-ip high-ip in global config mode to configure a range of IP addresses that will not be leased to clients. There is no need to exclude the network address, broadcast address, or the router’s own address.

Use ip dhcp pool name to create a DHCP pool—a set of addresses and other configuration parameters to be leased to clients.

Use network network-address {netmask | /prefix-length} to configure the range of addresses to be leased to clients.

Use default-router ip-address to configure clients’ default gateway.

Use dns-server ip-address to configure up to eight DNS servers (with a space between each) that clients should send DNS queries to.

Use domain-name domain-name to specify clients’ domain name.

Use lease {days hours minutes | infinite} to configure the duration of leases. The default lease period is 24 hours.

Use show ip dhcp binding to see active DHCP leases.

Use clear ip dhcp binding {* | ip-address} to either clear all bindings (*) or the specified binding (ip-address).

After receiving a DISCOVER message and selecting an IP address to lease to a client, a Cisco IOS DHCP server will ping the selected address to detect address conflicts—addresses in the DHCP pool that are already in use by another host.

If the server’s ping receives a reply, the address is marked as a conflict and is removed from the pool—it won’t be assigned to another host until the conflict is resolved and it is cleared with clear ip dhcp conflict {* | ip-address}.

Use show ip dhcp conflict to view address conflicts.

Network infrastructure devices typically use static IP addresses, but it’s common for a router’s ISP-connected interface to use DHCP to receive a dynamic IP address and default route from the ISP.

Use ip address dhcp to configure a router’s interface as a DHCP client.

Use show ip interface interface to confirm that the interface’s IP address was learned via DHCP, and show ip route to confirm that the router has learned a default route.

Instead of each LAN’s router functioning as a DHCP server, in larger networks, it’s more common to use a dedicated and centralized DHCP server. This simplifies management and reduces the number of DHCP servers required.

A DHCP relay agent is able to forward DHCP clients’ broadcast DISCOVER and REQUEST messages to a remote DHCP server.

Use ip helper-address server-ip on a router’s interface to configure it as a DHCP relay agent. Make sure to configure it on the interface that will receive the clients’ broadcast messages—the interface connected to the clients.

Use show ip interface interface-name to confirm that a helper address has been configured on the interface.

Use ipconfig in the Windows CLI to view basic IP settings (domain name, IP address/netmask, default gateway) and ipconfig /all to view more detailed information.

Use netstat -rn to view the routing table in Windows, macOS, and Linux.

Use ifconfig in macOS to view IP settings similar to ipconfig.

Because a variety of distributions are built on top of the Linux kernel, there is some variation in how to view the IP settings.

Some Linux distributions still support an old set of commands called net-tools by default, which include ifconfig (to view interface information) and route (to view the routing table).

Other distributions use a set of commands called iproute2, which include ip addr (equivalent to ifconfig) and ip route (equivalent to route).