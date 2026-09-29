8 Router and switch interfaces
This chapter covers

How to configure interfaces and verify their status
Interface speed and duplex settings
Using autonegotiation to automatically determine an interface’s speed and duplex
Errors that can occur when sending and receiving messages over a network
In chapter 7, we looked at how to configure IP addresses on and enable router interfaces. In this chapter, we will dig deeper into the topic of interfaces and how they operate. Whereas the previous chapter covered how to configure IP addresses on interfaces (a Layer 3 concept), this chapter will focus primarily on Layer 1 concepts, such as how to configure the speed at which an interface can send and receive data. Specifically, we will cover the following CCNA exam topics:

1.3.b Connections (Ethernet shared media and point-to-point)
1.4 Identify interface and cable issues (collisions, errors, mismatch duplex, and/or speed)
In previous chapters, I have used the terms port and interface. The exact definitions of these terms depend on who you ask; some say a port is a Layer 2 entity that forwards frames within a LAN (switches have ports), and an interface is a Layer 3 entity that forwards packets between LANs (routers have interfaces). Another definition is that a port is the physical connector on a device that you plug a cable into, and an interface is the representation of that port within the software (hence, most Cisco IOS commands use the term interface rather than port).
In reality, these terms are often used interchangeably—even Cisco’s documentation isn’t consistent regarding these terms. In this book, I will generally use the term port to refer to a physical connector on a device and interface when talking about configurations, except in situations where one term is generally accepted as the standard over the other (in which case I will point that out).

8.1 Configuring interfaces
In this section, we will look at how to configure three aspects of an interface: description, speed, and duplex. Figure 8.1 shows how to configure these settings on Cisco routers and switches running Cisco IOS.
Figure 8.1 Interface configurations on R1 and SW1: (1) configuring R1’s G0/1 interface with an IP address, description, and manual speed and duplex settings; (2) configuring SW1’s G0/1 interface with a description, and manual speed and duplex settings; (3) configuring SW1’s connections to end-user devices (PCs) using autonegotiation; (4) disabling SW1’s unused interfaces.
Before we examine the configurations in figure 8.1 in detail, there are a couple of things worth mentioning that illustrate some differences between routers and switches. First, notice that I configured an IP address on R1’s G0/1 interface but not on SW1’s interfaces; this is because switch interfaces don’t need IP addresses to perform their role of forwarding frames within a LAN. Switches are not Layer 3 aware; they only use Layer 2 information (MAC addresses) to decide how to forward frames.
The second point is that I used no shutdown on R1’s G0/1 interface to enable it but not on SW1’s G0/1, F0/1, or F0/2 interfaces. That is because, unlike router interfaces, which are disabled by default, switch interfaces are enabled by default.
Exam Tip In figure 8.1, I used shutdown to disable SW1’s unused ports. This is considered a security best practice.

Switch interfaces are enabled by default to allow switches to operate in a plug-and-play manner; this means that to use the switch, you simply need to connect devices to it—no configuration is required. However, although a switch does not require configuration to perform its most basic function of forwarding frames, most enterprise networks will require configurations on switches to use more advanced features (which we will cover in both volumes of this book).
Note A switch that is designed to be used in a plug-and-play manner is called an unmanaged switch. Unmanaged switches are inexpensive and are sometimes used in very small networks. The CCNA focuses on managed switches, which allow you to configure more advanced features.

8.1.1 Interface descriptions
An interface description is a simple string of text that you can configure to describe or name an interface. A common use is to indicate what device is connected to the interface. The command to configure an interface’s description is description description, where description is a string of text such as “connected to R1’s G0/1 interface.” The following example shows how I configured the descriptions of SW1’s F0/1 and F0/2 interfaces. F0/1 and F0/2 are connected to end-user devices (PCs), so I configured their descriptions as ## end users ##:

SW1# configure terminal
SW1(config)# interface range f0/1-2            ❶
SW1(config-if)# description ## end users ##    ❷
❶ Configures F0/1 and F0/2 simultaneously

❷ Applies a description to both interfaces

Note The two hash symbols (##) at the beginning and end of the description are not necessary. I use them in my interface descriptions to help them stand out when viewing them in the CLI.
Notice that I used the interface range f0/1-2 command to configure SW1’s F0/1 and F0/2 interfaces at the same time; interface range can be a big timesaver when configuring multiple interfaces! The command to configure a range of interfaces is interface range type slot/port-port. Let me explain each of those arguments in the command:
type means Ethernet, FastEthernet, GigabitEthernet, etc.
slot is the first number in the interface name.
port is the second number in the interface name.
Note Another example from figure 8.1 is interface range f0/3-8, g0/2. This configures F0/3, F0/4, F0/5, F0/6, F0/7, F0/8, and G0/2. To include interfaces of a different type in the same interface range command, you must separate the interface names with a comma.
Interface descriptions are optional, but I highly recommend configuring them; interface descriptions that are consistently configured and updated as needed make it much easier to identify the purpose of each interface when viewing the configurations at a later date.
To view interface descriptions on a router or switch, you can use the show interfaces description command. The following example shows the output of that command after configuring SW1’s interface descriptions (some output is omitted for the sake of space). Note that the command also lists the Layer 1 status (Status) and Layer 2 status (Protocol) of each interface:

SW1# show interfaces description                          ❶
Interface   Status         Protocol   Description
Fa0/1       up             up         ## end users ##     ❷
Fa0/2       up             up         ## end users ##     ❷
Fa0/3       down           down       ## not in use ##    ❷
. . .    
Gi0/1       up             up         ## to R1 ##         ❷
Gi0/2       down           down       ## not in use ##    ❷
❶ Views a list of interfaces and their descriptions

❷ Interface status and descriptions are shown.

Another command that can be used to view interface descriptions is show interfaces status. However, this command only works on switches, not on routers. We will use this command in the next few sections as well, as it also shows information about the interface speed and duplex. The following example shows the output of this command (the descriptions are displayed in the Name column):

SW1# show interfaces status
Port      Name               Status       Vlan       Duplex  Speed Type
Fa0/1     ## end users ##    connected    1          a-full  a-100 10/100BaseTX
Fa0/2     ## end users ##    connected    1          a-full  a-100 10/100BaseTX
Fa0/3     ## not in use ##   notconnect   1            auto   auto 10/100BaseTX
. . .
Gi0/1     ## to R1 ##        connected    1          a-full a-1000 10/100/1000BaseTX
Gi0/2     ## not in use ##   notconnect   1            auto   auto 10/100/1000BaseTX
8.1.2 Interface speed
An interface’s speed is the maximum rate at which it can send and receive traffic, measured in bits per second. Most interfaces support multiple speeds—for example, most FastEthernet interfaces support speeds of both 10 and 100 Mbps—in which case they can be called 10/100 interfaces. Likewise, most GigabitEthernet interfaces support speeds of 10, 100, and 1,000 Mbps (1 Gbps) and are therefore called 10/100/1000 interfaces. Ideally, an interface will operate at its maximum speed, but if connected to a device that only supports slower speeds, it’s important that an interface can match the speed of the other device.

The speed at which an interface operates can be manually configured or automatically determined by the device using a process called autonegotiation, in which the connected devices communicate with each other to determine at what speed they should operate. Cisco IOS devices use autonegotiation by default, and in most cases, you can leave autonegotiation enabled. However, there are cases where you should manually configure an interface’s speed, such as when the neighboring device does not use autonegotiation. The command to manually configure an interface’s speed is speed {speed | auto}, where speed is specified in megabits per second.
Note When writing the syntax of a command, options in curly braces are a mandatory choice. In the speed command, you must either specify the speed value or use auto to enable autonegotiation.
In the following example, I use context-sensitive help to show the available options when configuring the speed of SW1’s G0/1 interface: 10, 100, 1000, and auto. I then manually configure the speed at 1 Gbps (1,000 Mbps) and use show running-config interface g0/1 to verify the interface’s configuration:

SW1(config)# interface g0/1
SW1(config-if)# speed ?
  10    Force 10 Mbps operation                           ❶
  100   Force 100 Mbps operation                          ❶
  1000  Force 1000 Mbps operation                         ❶
  auto  Enable AUTO speed configuration    
SW1(config-if)# speed 1000                                ❷
SW1(config-if)# do show running-config interface g0/1     ❸
. . .
interface GigabitEthernet0/1    
 description ## to R1 ##    
 speed 1000    
End
❶ The available keywords for the speed command

❷ Manually configures a speed of 1,000 Mbps

❸ Views G0/1’s settings in the running-config

Note You can use the show running-config interface interface-name command to view the active configurations for a specific interface. To view the active configurations for all interfaces, use show running-config | section interface.

In the next example, I configure speed auto on SW1’s F0/1 and F0/2 interfaces and then view F0/1’s configuration. However, speed auto is not shown because it is the default setting. To avoid clutter in a device’s configuration files, many default settings are hidden:

SW1(config)# interface range f0/1-2                       ❶
SW1(config-if)# speed auto                                ❶
SW1(config-if)# do show running-config interface f0/1     ❷
. . .
interface FastEthernet0/1                                 ❷
 description ## end users ##                              ❷
End
❶ Configures speed autonegotiation on F0/1 and F0/2

❷ Speed auto is not shown because it is the default setting.

Note In figure 8.1 and the previous example, I configured speed auto, but because that is the default setting, it is not actually necessary to issue that command.

8.1.3 Interface duplex
An interface’s duplex setting refers to whether it is able to send and receive data at the same time or not. There are two types of duplex:
Half duplex—The interface can send and receive data but not at the same time.
Full duplex—The interface can send and receive data at the same time.
Note The opposite of duplex is simplex, which is one-way communication. The communication from a keyboard to a computer is an example of simplex communication; the keyboard sends data to the computer, but the computer does not send data to the keyboard.
An example of half-duplex communication is an IEEE 802.11 wireless LAN (Wi-Fi). Because devices connected to a wireless LAN share the same physical medium (radio frequency), devices must wait their turn to communicate; they cannot send and receive data at the same time. We will focus on wireless LANs in part 4 of volume 2 of this book, but for now we will focus on wired LANs using Ethernet.
An example of full-duplex communication is a wired Ethernet LAN using a switch (or switches). Devices connected to a switch are able to send and receive traffic at the same time, which allows much greater performance compared to half duplex. However, devices connected to a wired LAN weren’t always able to operate in full duplex. Before switches, devices called hubs were used to connect devices in a LAN, and devices connected to a hub had to operate in half-duplex mode (these days, hubs are almost never used).

Ethernet hubs
To understand duplex, let’s examine one of the precursors to the Ethernet switch: the Ethernet hub. The basic role of a hub is the same as a switch: to connect hosts in a LAN. Switches use Layer 2 information (MAC addresses) to forward frames to the appropriate destination (or flood them as necessary). Hubs, on the other hand, aren’t Layer 2 aware; when bits of data are received on one port, they simply repeat those bits out of all other ports. This means that all devices in the LAN receive every frame sent in the LAN; each device then examines the destination MAC address of the frame to determine whether it should keep or discard the frame. Hubs are considered Layer 1 devices; they receive and repeat electrical signals but don’t examine those signals to make forwarding decisions.
A major downside of hubs is that they do not have memory to store frames before flooding them. Therefore, if two devices connected to a hub attempt to send frames at the same time, the hub will attempt to flood both frames at the same time, resulting in a garbled mess rather than two coherent messages; this is called a collision, and all devices connected to a hub are said to be in the same collision domain. Only one device in a collision domain can send traffic at a time without causing collisions. Thus, devices connected to a hub must operate in half duplex, not full duplex.

Collision domains
A collision occurs when two messages are sent simultaneously over a shared medium and then collide, resulting in an incoherent signal—like if two people talk at the same time, making you unable to understand either of them. A collision domain is a network segment in which simultaneous transmission will result in collisions. As mentioned previously, all hosts connected to a hub are in the same collision domain; this means that only one can transmit at a time. While one host is transmitting, the others can only receive data—they have to wait their turn to transmit. Figure 8.2 shows what happens when two hosts connected to a hub attempt to transmit at the same time.
Figure 8.2 Four PCs are connected to a hub, and two attempt to transmit at the same time, resulting in collisions. All four PCs are in the same collision domain. (1) PC2 sends a frame addressed to PC1’s MAC address, and PC4 sends a frame addressed to PC3’s MAC address. (2) The hub attempts to flood both frames at the same time, resulting in collisions. Neither PC1 nor PC3 receive their respective frames intact.
Unlike hosts connected to a hub, each host connected to a switch is in its own collision domain; switches are able to store frames in memory and forward (or flood) them one after the other, avoiding collisions. This means that hosts connected to a switch can operate in full-duplex mode; all devices in the LAN can send and receive traffic at the same time, with no worry of messages colliding.
Note Exam topic 1.3.b states, “Connections (Ethernet shared media and point-to-point).” All devices connected to a hub are connected to a shared medium; each device has to share the medium and wait its turn to transmit. Connections to a switch are considered Ethernet point-to-point connections—connections between only two devices: the switch and its connected device. Devices connected to a switch do not have to share the medium—they do not have to wait their turn to transmit.
Collisions should not occur in a switched LAN; if collisions occur, it is an indicator of a problem in the network (we will cover some possible problems in section 8.3). Figure 8.3 shows how a switch is able to flood frames one after the other without causing collisions.
Figure 8.3 Four PCs are connected to a switch, each in its own collision domain. (1) PC2 and PC4 each send a broadcast frame at the same time. (2) The switch floods the frames, but it does not flood PC2’s frame to PC1 or PC3; it buffers the frame in memory. (3) The switch floods PC2’s frame to PC1 and PC3 after it has finished flooding PC4’s frame.
Carrier-sense multiple access with collision detection
To facilitate communications over a shared medium (a LAN using a hub), devices use a method called carrier-sense multiple access with collision detection (CSMA/CD). Let’s examine each part of that title:
Carrier-sense means that devices will attempt to sense whether the medium is in use (by “listening” for electrical signals) before transmitting a message.
Multiple access means that a shared medium is used (i.e., accessed by multiple devices).
Collision detection means that if a collision occurs, devices connected to the medium will detect it (and send a signal to notify other devices of the collision).
CSMA/CD helps devices connected to a hub avoid collisions and deal with collisions when they inevitably happen; interfaces operating in half-duplex mode must use CSMA/CD. The CSMA/CD process is as follows:
Before sending a frame, devices wait until they detect that other devices are not sending.
When a collision occurs, devices that detect the collision will send a jamming signal to inform the other devices of the collision.
Each device then waits a random period of time before sending frames again.
The process repeats.
Exam Tip Hubs are rarely used in modern networks, having been almost entirely replaced by switches. However, collisions, collision domains, and CSMA/CD are foundational networking concepts that may appear on the CCNA exam.
Configuring an interface duplex
Like an interface’s speed, its duplex can also be manually configured or automatically determined using autonegotiation. The command to configure an interface’s duplex is duplex {auto | full | half}, and the default setting is auto (which uses autonegotiation). Let’s configure SW1’s interface duplex settings, as in the example in figure 8.1. In the following example, I first confirm the current status with show interfaces status:

SW1# show interfaces status
Port      Name             Status      Vlan  Duplex  Speed Type
Fa0/1     ## end users ##  connected   1     a-full  a-100 10/100BaseTX       ❶
Fa0/2     ## end users ##  connected   1     a-full  a-100 10/100BaseTX       ❶
Fa0/3     ## not in use ## notconnect  1     auto    auto 10/100BaseTX
. . .
Gi0/1     ## to R1 ##      connected   1     a-full   1000 10/100/1000BaseTX  ❶
Gi0/2     ## not in use ## notconnect  1     auto    auto 10/100/1000BaseTX
❶ The prefix a- indicates autonegotiation.

Note that the current duplex state for SW1’s active interfaces (F0/1, F0/2, and G0/1) is a-full. This means that they are operating in full duplex, which was decided using autonegotiation. Interfaces that are not active (i.e., not connected to another device) are auto, meaning autonegotiation is enabled, but SW1 hasn’t decided if those interfaces will operate in half or full duplex (because they aren’t connected to another device yet).
Note In the Speed column of the previous example, F0/1 and F0/2 show a-100, meaning autonegotiation was used to decide on a speed of 100 Mbps. G0/1 simply displays 1000, because I manually configured a speed of 1,000 Mbps.
Next, let’s configure the duplex of SW1’s interfaces according to figure 8.1. In the following example, I do so and then confirm with show interfaces status:

SW1# configure terminal
SW1(config)# interface g0/1                                                ❶
SW1(config-if)# duplex full                                                ❶
SW1(config-if)# interface range f0/1-2                                     ❷
SW1(config-if)# duplex auto                                                ❷
SW1(config-if)# do show interfaces status
Port      Name             Status     Vlan  Duplex  Speed Type
Fa0/1     ## end users ##  connected  1     a-full  a-100 10/100BaseTX     ❸
Fa0/2     ## end users ##  connected  1     a-full  a-100 10/100BaseTX     ❸
Fa0/3     ## not in use ## notconnect 1     auto   auto 10/100BaseTX
. . .
Gi0/1     ## to R1 ##      connected  1     full   1000 10/100/1000BaseTX  ❹
Gi0/2     ## not in use ## notconnect 1     auto   auto 10/100/1000BaseTX
❶ Manually configures G0/1’s duplex

❷ Uses duplex autonegotiation (default) on F0/1 and F0/2

❸ F0/1 and F0/2 use speed and duplex autonegotiation (the default settings).

❹ G0/1’s duplex and speed are manually set to full/1000.

Notice that G0/1’s duplex has changed from a-full to full; this means the interface was manually configured to operate in full duplex. The output for F0/1 and F0/2, however, does not change. As with speed auto, duplex auto is the default setting, so it is not necessary to issue the command to enable autonegotiation—I include it in the example to demonstrate that.
Note Although duplex is an important concept to understand, in modern wired networks, you can expect all devices to operate in full duplex; there’s no reason to use half duplex. However, wireless LANs operate in half duplex, so we will return to the topic of half duplex when we cover wireless LANs in part 4 of volume 2 of this book.

8.2 Autonegotiation
In section 8.1, we learned that autonegotiation can be used to automatically determine the speed and duplex at which an interface operates without manual configuration. In most cases, you can leave autonegotiation enabled without any issues, although some engineers prefer to manually configure speed and duplex for connections between network infrastructure devices (such as between routers and switches). The reason for this is that manually configuring the speed and duplex settings means that there is one less thing to potentially not work properly (autonegotiation) and cause problems. However, manual configuration does include the potential for human error, and it is extremely rare for autonegotiation to malfunction, so this is not a hard-and-fast rule.
In either case, it is best to leave autonegotiation enabled for connections to end devices such as PCs. Different end devices might support different speeds, and manually configuring speed settings for each PC (or other end device) in a network is often not feasible.
In the autonegotiation process, each device advertises its capabilities to its neighbor, and the two agree upon the best operational mode supported by both neighbors. Table 8.1 lists some operational modes in order of priority—greater speeds are prioritized over lesser speeds, and full duplex is prioritized over half duplex (as you would probably expect).

Table 8.1 Operational modes

| Priority | Operational mode      |
| -------- | --------------------- |
| 1        | 10 Gbps, full duplex  |
| 2        | 1 Gbps, full duplex   |
| 3        | 100 Mbps, full duplex |
| 4        | 100 Mbps, half duplex |
| 5        | 10 Mbps, full duplex  |
| 6        | 10 Mbps, half duplex  |

Note Table 8.1 only includes full duplex for 10 and 1 Gbps. 1 Gbps/half duplex is possible, but devices that support it are very rare; you can’t configure that combination on a Cisco device, for example. Speeds of 10 Gbps or greater do not support half duplex, only full duplex.
Figure 8.4 shows an example of autonegotiation between a router and a switch. After each device advertises its capabilities, it chooses the best mode shared by both devices (100 Mbps, full duplex).

Figure 8.4 A router and a switch advertise their speed and duplex capabilities to each other. The best option supported by both R1 and SW1 is 100 Mbps/full duplex, as highlighted in bold. Although R1 G0/1 is capable of 1 Gbps/full duplex, it will operate at 100 Mbps/full duplex to match SW1 F0/1.
Figure 8.4 demonstrates what happens when both devices are using autonegotiation, but what if speed and duplex are manually configured on one end of the connection and autonegotiation is used on the other end? In such a situation, the device with autonegotiation enabled will behave as follows:
Speed—Tries to sense the speed at which the other device is operating. If that fails, uses the slowest supported speed (i.e., 10 Mbps on a 10/100/1000 interface).
Duplex—If the speed is 10 or 100 Mbps, uses half duplex. If the speed is 1,000 Mbps or greater, uses full duplex.
These behaviors can result in some problems, and figure 8.5 demonstrates one of those problems. R1 G0/1 is using autonegotiation, but SW1 F0/1’s speed and duplex are manually configured. R1 is able to sense the speed at which SW1 F0/1 is operating (100 Mbps) and match its speed. However, following the previously stated rules, R1 G0/1 operates in half duplex, not full duplex. This creates a duplex mismatch. If R1 fails to sense SW1’s operating speed, R1 G0/1 will operate at 10 Mbps, resulting in a speed mismatch. We will cover speed and duplex mismatches in section 8.3.
Figure 8.5 A router and switch are connected, but only the router is using autonegotiation. R1 senses SW1’s speed (100 Mbps) and matches its speed to SW1. However, because R1 G0/1 is operating at 100 Mbps, it operates in half duplex. This creates a duplex mismatch between R1 G0/1 (half duplex) and SW1 F0/1 (full duplex).
Exam Tip An autonegotiation-enabled device’s behavior when connected to a device with manually configured speed and duplex settings is a potential exam question. Be aware of how the autonegotiation-enabled device will select its operational speed and duplex, as well as the possible negative results (speed or duplex mismatch).

8.3 Interface errors
Cisco IOS devices maintain various counters to keep track of errors encountered when sending or receiving messages (such as when messages collide). When a device encounters errors while sending or receiving messages on an interface, it increments the relevant counter(s). You can view these counters in the output of show interfaces, as shown in the following example:

SW1# show interfaces f0/1                                       ❶
. . .
     164850273 packets input, 138587749740 bytes, 0 no buffer   ❷
     Received 606 broadcasts (0 multicasts)                     ❷
     0 runts, 0 giants, 0 throttles                             ❷
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored       ❷
     0 watchdog, 0 multicast, 0 pause input                     ❷
     0 input packets with dribble condition detected            ❷
     165209751 packets output, 180164587250 bytes, 0 underruns  ❷
     0 output errors, 0 collisions, 0 interface resets          ❷
     0 unknown protocol drops                                   ❷
     0 babbles, 0 late collision, 0 deferred                    ❷
     0 lost carrier, 0 no carrier, 0 pause output               ❷
     0 output buffer failures, 0 output buffers swapped out     ❷
❶ Views detailed information about F0/1

❷ Various errors and statistics are listed at the bottom of the output.

I have highlighted some errors in the output that you should be able to identify for the CCNA. Let’s take a look at what each error type means:
Runts are frames received that are smaller than the minimum frame size, which is 64 bytes. When a device wants to send a frame smaller than 64 bytes, it is supposed to add padding (bytes of all 0s) to the end of the message to make it 64 bytes in size. Runts can be caused by collisions.
Giants are frames received with a payload greater than the interface’s MTU (maximum transmission unit), which is typically 1,500 bytes. Giants are usually a sign of a misconfiguration; devices in the network are not using consistent MTU values.
Input errors is a counter that includes all errors for received frames.
CRC (Cyclic Redundancy Check) counts frames that failed the FCS (Frame Check Sequence) check in the Ethernet trailer. This could be the result of electromagnetic interference (EMI) causing data corruption.
Output errors is a counter that includes all errors for transmitted frames.
Collisions is a counter for all collisions that happen when the device is transmitting a frame. If the device is connected to a hub, collisions are expected. In a switched LAN, this counter should remain at 0.
Late collision is a counter for collisions that happen after the 64th byte of the frame has been transmitted. This counter is significant because, due to the timing of CSMA/CD, collisions should only occur within the first 64 bytes of a frame’s transmission. If a collision occurs after that, it often indicates that one of the devices is not using CSMA/CD to check the medium before transmitting (probably due to a duplex mismatch).
As indicated in their descriptions, some of these errors are expected as a result of collisions and are therefore normal occurrences in LANs using hubs. Others are a sign of a problem in the network, such as a misconfiguration or hardware malfunction. In addition to these errors, for the CCNA exam, you must also be familiar with speed mismatches and duplex mismatches and the consequences of each.

8.3.1 Speed mismatches
Speed mismatches—when two connected interfaces attempt to communicate at different speeds—are a fairly simple problem. They are almost always caused by a misconfiguration (e.g., one interface configured with speed 100 and the other configured with speed 1000). The result of a speed mismatch is that both interfaces will be in a down/down state (referring to the Status and Protocol columns in the output of show ip interface brief). The two devices will not be able to communicate with each other. Figure 8.6 demonstrates this.



Figure 8.6 A speed mismatch between a router and a switch. Because of the speed mismatch, their interfaces are in a down/down state; R1 and SW1 cannot communicate.

The following examples show the output of show ip interface brief for both R1 and SW1 after configuring mismatching speeds on each:

R1# show ip interface brief
Interface           IP-Address   OK? Method Status   Protocol
GigabitEthernet0/1  192.168.1.1  YES NVRAM  down     down       ❶
. . .     
  
SW1# show ip interface brief
Interface           IP-Address   OK? Method Status    Protocol
FastEthernet0/1     Unassigned   YES NVRAM  down      down      ❶
. . .  
❶ A speed mismatch results in both interfaces being down/down.

Speed mismatches are a risk when manually configuring interface speeds; there is always a chance for human error. However, if you’re careful, they shouldn’t occur.
Exam Tip For the CCNA exam, remember the result of a speed mismatch: both interfaces will be in a down/down state. The interfaces will not be operational.

8.3.2 Duplex mismatches
Duplex mismatches—when two connected interfaces are operating at different duplex settings—can be a bit harder to identify than speed mismatches. Even with a duplex mismatch, both interfaces will be operational—they will be in an up/up state and able to forward network traffic. A duplex mismatch can occur when each end of the connection is configured with a different duplex setting (duplex full and duplex half) or when one end is using autonegotiation and the other isn’t (as we saw in figure 8.5).
The effect of a duplex mismatch is that the performance of the link will be greatly reduced; the device operating in half duplex will have to wait for the other device to stop transmitting before it can transmit any data. If the full-duplex device transmits a frame while the half-duplex device is also transmitting a frame, the half-duplex device will interpret that as a collision (although a collision hasn’t actually occurred). In the output of show interfaces, you can expect to see incrementing collisions and late collision counters on the half-duplex device.
When the half-duplex device thinks it has detected a collision, it will send a jamming signal (as part of the CSMA/CD process), destroying any frames currently being sent by either device. When the full-duplex device receives these destroyed (corrupted) frames, it will usually increase the Runts and/or CRC counters on the interface that received them.
Note Two devices connected with UTP or fiber Ethernet cables can both send and receive traffic at the same time without collisions occurring. If there is a duplex mismatch, the half-duplex device may detect false collisions when the full-duplex device transmits, but a collision hasn’t actually physically occurred. Actual collisions should only occur in a wired LAN when connecting multiple hosts with a hub, which is extremely rare in modern networks.

Summary
Router interfaces are disabled by default (they have the shutdown command applied), but switch interfaces are enabled by default.
It is considered best practice to disable unused switch ports with shutdown.
An interface description is a string of text used to describe an interface. It is optional (but recommended) and can be configured with the description description command in interface configuration mode.
You can use the interface range command to configure multiple interfaces at once.
You can use show interfaces description to view a list of interfaces along with their status and description.
You can use show interfaces status (on switches only) to view a list of interfaces and other information, like their description, status, duplex, and speed.
An interface’s speed is the maximum rate at which it can send and receive traffic. Most interfaces support multiple speeds, such as 10/100 or 10/100/1000.
An interface’s speed can be configured with speed {speed | auto}, where speed is specified in Mbps. The default setting is speed auto, which uses autonegotiation to determine the interface’s operating speed.
You can use show running-config interface interface-name to view the active configurations for a specific interface or show running-config | section interface to view the active configurations for all interfaces.
To avoid clutter, default configurations often do not appear in the running-config (or startup-config). For example, the speed auto command is not shown.
An interface’s duplex setting determines whether it is able to send and receive data at the same time. An interface operating in half duplex can send and receive data but not at the same time. An interface operating in full duplex can send and receive data at the same time.
The opposite of duplex is simplex, which is one-way communication.
Wireless LANs operate in half duplex. Wired LANs using switches operate in full duplex, but wired LANs using hubs operate in half duplex.
Hubs are Layer 1 devices that simply repeat signals received on an interface out of all other interfaces; all devices in the LAN receive every frame sent in the LAN. They are legacy hardware, rarely (if ever) used in modern networks.
Hubs do not have memory to store frames before flooding them. If a hub receives two frames at once, it will attempt to flood both at once, resulting in a collision.
A collision domain is a network segment in which simultaneous transmissions will result in collisions. Only one host in a collision domain can transmit at a time.
All hosts connected to a hub are in the same collision domain, but all hosts connected to a switch are in their own collision domain (and therefore don’t have to worry about collisions).
Devices operating in half duplex use carrier-sense multiple access with collision detection (CSMA/CD) to detect and deal with collisions.
An interface’s duplex can be configured with duplex {auto | full | half}. The default is duplex auto.
Autonegotiation allows devices to automatically determine what speed and duplex settings an interface should use. The two devices advertise their capabilities to each other and select the best mode supported by both devices.
If only one device is using autonegotiation, it will try to sense the speed of the other device. If that fails, it will use the slowest supported speed. If the speed is 10 or 100 Mbps, it will use half duplex. If the speed is 1000 Mbps or greater, it will use full duplex.
Cisco IOS uses various counters to keep track of errors encountered when sending and receiving messages. They can be viewed in the output of show interfaces. Some examples are runts, giants, CRC, collisions, and late collisions.
A speed mismatch occurs when two connected interfaces attempt to communicate at different speeds. This will result in both interfaces being down/down; the interfaces will not be operational.
Speed mismatches are usually caused by a misconfiguration.
A duplex mismatch occurs when two connected interfaces operate at different duplex settings: half and full. The interfaces will be operational, but performance will be greatly reduced.
Duplex mismatches can be caused by one side being configured as full duplex and the other as half duplex. They can also be caused by one side using autonegotiation and the other not.