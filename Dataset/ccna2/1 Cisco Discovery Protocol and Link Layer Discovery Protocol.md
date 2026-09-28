1 Cisco Discovery Protocol and Link Layer Discovery Protocol
This chapter covers

The purpose of Layer 2 discovery protocols
How neighboring Cisco devices use Cisco Discovery Protocol to share information
CDP’s industry-standard equivalent: Link Layer Discovery Protocol
In a perfect world, all networks would be perfectly documented, with up-to-date network diagrams and other documents detailing the routers, switches, firewalls, and other devices that make up the network infrastructure, how they are connected, their IP addresses, etc. In reality, that’s often not the case: people cut corners, changes go undocumented, or perhaps the network was never properly documented in the first place.

In either case, the result is often that the network documentation doesn’t accurately reflect the current state of the network; this is not an ideal state of affairs. Fortunately, Layer 2 discovery protocols—the topic of this chapter—can help you remedy this situation. Layer 2 discovery protocols, such as Cisco Discovery Protocol (CDP) and Link Layer Discovery Protocol (LLDP), enable devices to share information about themselves with their directly connected neighbors. Using this information, you can map out the network by identifying the devices in the network, their hardware models, how they are connected to each other, their IP addresses, and other information.

Layer 2 discovery protocols are CCNA exam topic 2.3: Configure and verify Layer 2 discovery protocols (Cisco Discovery Protocol and LLDP). This is one of the more straightforward CCNA exam topics. In this chapter, we will primarily examine some show commands that allow you to view the information that devices share with CDP/LLDP, as well as some basic configuration commands to enable, disable, and fine-tune the protocols.

1.1 Cisco Discovery Protocol
CDP is a Cisco-proprietary Layer 2 discovery protocol that runs on Cisco network devices such as routers and switches. CDP is enabled by default; unless you want to modify the default settings, you don’t need to do any configuration to use CDP in your network. Using CDP, devices periodically send advertisement messages out of their interfaces, informing directly connected neighbors about various aspects of the local device. They also listen for similar advertisements from those same neighbors. Figure 1.1 illustrates this: R1 and SW1 exchange CDP advertisements with each other.



Figure 1.1 Two neighboring Cisco devices share information about themselves via CDP. The shared information includes hostname, capabilities (device type), port ID, IP address, and much more.

CDP messages are sent to the multicast MAC address 0100.0ccc.cccc. However, when a switch receives a CDP message, it does not flood the message like it would with regular multicast frames; the switch receives the frame for itself. Using figure 1.1’s example, SW1 will receive R1’s CDP message and add R1 to its CDP neighbor table.

Note Most CLI examples in this chapter will be from a router’s CLI. However, CDP (and LLDP) commands and their output are identical on Cisco routers and switches.

1.1.1 Viewing CDP neighbors
When using CDP, the show command you are most likely to use is show cdp neighbors; this command lists basic information about each of the device’s CDP neighbors—devices from which it has received CDP messages. In the following example, I use the command on R1:

R1# show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge       ❶
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,    ❶
                  D - Remote, C - CVTA, M - Two-port Mac Relay                ❶
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Gig 0/0           158             R S I  WS-C2960C Gig 0/1   ❷
❶ Codes used in the Capability column

❷ SW1 is R1’s CDP neighbor.

After a legend listing the different codes that can appear in the Capability column, there is a table listing the device’s CDP neighbors—neighbors from which the device has received CDP messages. The Device ID column lists the hostname of each neighbor; in our example, R1 has one neighbor: SW1.

The Local Intrfce column lists the interface on the local device that the neighbor is connected to. The value of Gig 0/0 in this column means that SW1 is connected to R1 G0/0. Don’t confuse this with the final column, Port ID, which lists the interface of the neighboring device. The value of Gig 0/1 here means that R1 is connected to SW1 G0/1.

The third column is Holdtme, which states the current holdtime—how long until R1 will remove SW1’s entry from the neighbor table. The default timer is 180 seconds; each time the device receives a CDP advertisement from the neighbor, this time is reset to 180 and starts counting down. The value of 158 in this column means that 22 seconds have elapsed since R1 received a CDP message from SW1. If this counts down to 0, R1 will remove SW1’s entry from the CDP neighbor table. We’ll cover this timer more in the next section.

The fourth column is Capability, which identifies the type of device. S means Switch, as indicated in the Capability Codes at the top of the output; SW1 is a switch. However, it also has the R code (for Router), because it has some Layer 3 capabilities, and I (for IGMP), meaning it supports the Internet Group Management Protocol—a topic beyond the scope of the CCNA exam.

The next column is Platform, which indicates the hardware model of the neighbor. WS-C2960C is a model in the Catalyst 2960 series of switches, which is no longer being manufactured (but is a great option if you want a switch for a home lab at a low price).

Exam Tip Make sure you’re comfortable reading the output of show cdp neighbors. Particularly, remember that Local Intrfce is the port of this device (R1), and Port ID is the port of the neighbor device (SW1).

However, the output of show cdp neighbors lists only a fraction of the information learned from the neighbor. To view even more information about each neighbor, you can use show cdp neighbors detail. In the following example, I show the output of the command and highlight the same information we saw previously in show cdp neighbors. Take a look through the rest of the output to get an idea of what information is conveyed, but focus on the main information shown at the top of the output:

R1# show cdp neighbors detail
-------------------------
Device ID: SW1                                    ❶
Entry address(es): 
Platform: cisco WS-C2960C-8PC-L,                  ❷
➥Capabilities: Router Switch IGMP                ❷
Interface: GigabitEthernet0/0,                    ❸
➥Port ID (outgoing port): GigabitEthernet0/1     ❸
Holdtime : 170 sec                                ❹
 
Version :
Cisco IOS Software, C2960C Software (C2960c405-UNIVERSALK9-M), 
➥Version 15.0(2)SE5, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2013 by Cisco Systems, Inc.
Compiled Fri 25-Oct-13 14:35 by prod_rel_team
 
advertisement version: 2
VTP Management Domain: ''
Native VLAN: 1
Duplex: full
                           
Total cdp entries displayed : 1
❶ The neighbor’s hostname

❷ The neighbor’s hardware model and capabilities

❸ Interface lists the local device’s (R1’s) port, and Port ID lists neighbor’s (SW1’s) port.

❹ The current holdtime; 10 seconds have elapsed since R1 received an advertisement from SW1.

Note You can use the show cdp entry name command (i.e., show cdp entry SW1) to view the same information as show cdp neighbors detail for only the specified neighbor; this is helpful when the device has multiple neighbors.

1.1.2 Mapping a network with CDP
As an exercise in reading the CDP neighbor table, let’s practice mapping a network using CDP. This is not just an arbitrary exercise—you may have to do this in the real world at some point. Imagine that you have entered a networking role at an organization with less-than-ideal documentation. Although you don’t have physical access to the devices, you have remote access to the CLI of several devices via Secure Shell—the topic of chapter 5. However, you don’t have access to an up-to-date network diagram. Your task is to fix that, and CDP is a great tool for doing so.

The following five examples show the output of show cdp neighbors on five devices. Grab a pen or pencil, and try to draw out the network using the information in the Local Intrfce and Port ID columns of this output:

R1# show cdp neighbors
. . .
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Gig 0/2           163             R S I            Gig 0/1
SW2              Gig 0/1           151             R S I            Gig 0/2
R2               Gig 0/0           132              R B             Gig 0/1

R2# show cdp neighbors
. . .
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW3              Gig 0/0           160             R S I            Gig 0/1
R1               Gig 0/1           150              R B             Gig 0/0

SW1# show cdp neighbors
. . .
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW2              Gig 0/2           168             R S I            Gig 0/1
R1               Gig 0/1           178              R B             Gig 0/2

SW2# show cdp neighbors
. . .
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Gig 0/1           124             R S I            Gig 0/2
R1               Gig 0/2           157              R B             Gig 0/1

SW3# show cdp neighbors
. . .
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
R2               Gig 0/1           157              R B             Gig 0/0
Figure 1.2 shows the network diagram. Don’t worry if the arrangement of the devices in the network you drew is different (i.e., R1 on the right instead of the left); it’s how the devices are connected that matters.



Figure 1.2 The network mapped out using show cdp neighbors

1.1.3 Configuring and verifying CDP
As mentioned previously, CDP is enabled by default. You can confirm that CDP is enabled on the device with show cdp. If it is enabled, you will see output like in the following example:

R1# show cdp
Global CDP information:
Sending CDP packets every 60 seconds        ❶
Sending a holdtime value of 180 seconds     ❷
Sending CDPv2 advertisements is enabled     ❸
❶ The advertisement timer is 1 minute.

❷ The default holdtime is 3 minutes.

❸ CDPv2 is enabled by default.

In addition to confirming that CDP is enabled on the device, the output gives us three pieces of information. The line Sending CDP packets every 60 seconds shows the CDP advertisement timer—how often the device sends CDP messages out of each interface—which is 60 seconds by default.

The second line, Sending a holdtime value of 180 seconds, indicates the holdtime, which is 180 seconds by default. The CDP holdtime determines how long the neighbor will keep this device (R1) in its CDP neighbor table after ceasing to receive CDP messages from this device. A value of 180 seconds means that R1 is telling SW1, “If you don’t get a CDP message from me for 3 minutes, remove me from your neighbor table.”

The final line, Sending CDPv2 advertisements is enabled, indicates that R1 is sending CDP version 2 messages. The differences between CDPv1 and CDPv2 are outside of the scope of the CCNA exam, and unless the neighboring device is very old and only supports version 1, you can leave version 2 enabled. Although there is usually no reason to change the advertisement timer, holdtime, and version, in the following example, I demonstrate the commands to modify them:

R1(config)# cdp timer 30                       ❶
R1(config)# cdp holdtime 120                   ❷
R1(config)# no cdp advertise-v2                ❸
R1(config)# do show cdp
Global CDP information:
Sending CDP packets every 30 seconds           ❹
Sending a holdtime value of 120 seconds        ❹
Sending CDPv2 advertisements is not enabled    ❹
❶ Changes the advertisement timer to 30 seconds

❷ Changes the holdtime to 120 seconds

❸ Disables CDPv2

❹ The three settings have changed from their defaults.

If you wish to disable CDP on the device, you can do so with the no cdp run command in global config mode. In the following example, I use the command on R1; notice how the output of show cdp changes:

R1(config)# no cdp run       ❶
R1(config)# do show cdp    
% CDP is not enabled         ❷
❶ Disables CDP globally on the device

❷ CDP is no longer running.

Note You can use cdp run to reenable CDP after disabling it.

no cdp run disables CDP globally—on the entire device. However, you can also disable CDP on a per-interface basis with the no cdp enable command. This prevents the specific interface both from sending CDP advertisements and from processing CDP advertisements it receives—it will discard them. In the following example, I reenable CDP on R1, use no cdp enable on one of R1’s interfaces, and confirm with a new command:

R1(config)# cdp run
R1(config)# interface g0/0                               ❶
R1(config-if)# no cdp enable                             ❶
R1(config-if)# do show cdp interface g0/0                ❷
 CDP is not enabled on interface GigabitEthernet0/0      ❸
❶ Disables CDP on R1 G0/0

❷ Confirms CDP’s status on G0/0

❸ CDP is disabled on G0/0.

To reenable CDP on the interface, use cdp enable. I do so in the following example and then confirm with show cdp interface g0/0 once again; notice how the output of the command changes:

R1(config-if)# cdp enable                   ❶
R1(config-if)# do show cdp interface g0/0
  Encapsulation ARPA                        ❷
  Sending CDP packets every 30 seconds      ❷
  Holdtime is 120 seconds                   ❷
❶ Reenables CDP on R1 G0/0

❷ Information about G0/0’s Layer-2 encapsulation and CDP timers is displayed.

Note If CDP is disabled globally, CDP won’t be active on any interfaces, regardless of the status of the [no] cdp enable command.

Why disable CDP?

CDP is quite a useful protocol, so why would you want to disable it globally or on individual interfaces? One reason is that CDP shares a lot of information about the local device, which can be a security concern. A malicious user could, for example, learn the software version of the device, search for known security vulnerabilities of that particular version, and launch targeted attacks to exploit those vulnerabilities. Therefore, it may be advisable to disable CDP either globally (with no cdp run) or on specific interfaces (with no cdp enable) where it is not strictly necessary for network operations.

One final CDP show command that can be helpful is show cdp traffic, which displays statistics about how many CDP messages the device has sent and received. The following example shows the output of the command on R1:

R1# show cdp traffic 
CDP counters :
        Total packets output: 319, Input: 246                    ❶
        Hdr syntax: 0, Chksum error: 0, Encaps failed: 0
        No memory: 0, Invalid packet: 0, 
        CDP version 1 advertisements output: 164, Input: 4       ❷
        CDP version 2 advertisements output: 155, Input: 242     ❸
❶ The total number of CDP messages sent/received

❷ The number of CDPv1 messages sent/received

❸ The number of CDPv2 messages sent/received

In sections 1.1.1 and 1.1.2, we’ve covered plenty of CDP configuration and verification commands. Table 1.1 summarizes the verification (show) commands we covered; make sure you’re familiar with how to read the output of these commands.

Table 1.1 CDP show commands



| Command                            | Information displayed                                                                   |
|------------------------------------|-----------------------------------------------------------------------------------------|
| `show cdp neighbors`               | CDP neighbors and basic information about each                                          |
| `show cdp neighbors detail`        | More detailed information about CDP neighbors                                           |
| `show cdp entry name`              | The same information as `show cdp neighbors detail` but for the specified neighbor only |
| `show cdp`                         | Basic information about CDP (timers, version)                                           |
| `show cdp interface [ interface ]` | Information about CDP-enabled interfaces                                                |
| `show cdp traffic`                 | The number of CDP messages sent/received                                                |


Table 1.2 summarizes the configuration commands. In general, CDP is a fairly hands-off protocol; you can leave it at the default settings in most cases. However, I recommend being familiar with the configuration commands we covered for the CCNA exam.

Table 1.2 CDP configuration commands


Command                              Description
-------                              -----------
R1(config)# cdp timer seconds       Configures the CDP advertisement timer
R1(config)# cdp holdtime seconds    Configures the CDP holdtime
R1(config)# [no] cdp advertise-v2  Enables/disables CDP version 2 advertisements
R1(config)# [no] cdp run           Enables/disables CDP globally
R1(config-if)# [no] cdp enable     Enables/disables CDP on a specific interface



1.2 Link Layer Discovery Protocol

The Link Layer Discovery Protocol (LLDP) was developed by the IEEE as a vendor-neutral equivalent to CDP (and other vendor-proprietary Layer 2 discovery protocols). Defined in IEEE 802.1AB, LLDP serves a similar purpose as CDP, but as an industry standard, it can be freely implemented by any vendor. This includes Cisco; Cisco routers and switches support both CDP and LLDP. Figure 1.3 shows a Cisco router and switch sharing information about themselves using LLDP.

Whereas CDP messages are sent to the multicast MAC address 0100.0ccc.cccc, LLDP messages are sent to the multicast MAC address 0180.c200.000e. However, like a CDP message, when a switch receives an LLDP message, it does not flood the message; the switch receives the frame for itself.



Figure 1.3 Two neighboring Cisco devices share information about each other via LLDP. The shared information is similar to that shared via CDP.

CDP or LLDP?

Cisco devices support both CDP and LLDP, so why would you choose one over the other? The main difference is that CDP is Cisco proprietary, whereas LLDP is vendor neutral. If your network uses only Cisco devices, the default CDP is fine. If your network uses a mix of vendors, you should enable LLDP. Note that a device can run both CDP and LLDP at the same time, although it is a bit redundant; they share mostly identical information.

1.2.1 Configuring and verifying LLDP
Although Cisco network devices support LLDP, it is not enabled by default. For that reason, let’s first look at how to configure LLDP before analyzing the information that devices share via LLDP. In the following example, I use show lldp to confirm that LLDP is disabled on R1, enable LLDP with lldp run, and then confirm that it is enabled:

R1# show lldp
% LLDP is not enabled                                     ❶
R1# configure terminal
R1(config)# lldp run                                      ❷
R1(config)# do show lldp
Global LLDP Information:
    Status: ACTIVE                                        ❸
    LLDP advertisements are sent every 30 seconds         ❹
    LLDP hold time advertised is 120 seconds              ❹
    LLDP interface reinitialisation delay is 2 seconds    ❹
❶ LLDP is disabled by default.
❷ Enables LLDP globally
❸ LLDP is enabled.
❹ The default timers

After enabling LLDP, show lldp displays similar information about LLDP as show cdp does about CDP. The default LLDP advertisement timer is 30 seconds—half that of CDP. The default holdtime is also shorter: 120 seconds. As with CDP, this is the holdtime that the local device is telling neighbors to use; R1 is telling its neighbor SW1, “If you don’t get an LLDP message from me for 2 minutes, remove me from your neighbor table.” The commands to modify these timers are similar to CDP’s—just replace cdp with lldp: lldp timer seconds and lldp holdtime seconds.

LLDP has one additional timer shown in the previous output: the reinitialization delay, which is 2 seconds by default. This means that after LLDP is activated on an interface, the device will wait 2 seconds before starting to send LLDP messages. This is beneficial in situations where an interface is bouncing (alternating) between up and down states due to an unstable connection or other problem. This delay provides time for the port to stabilize before sending LLDP messages. You can configure this timer with lldp reinit seconds, but in most cases, the default is fine.

Like CDP, you can also enable/disable LLDP on a per-interface basis. However, there is a major difference: whereas CDP uses only one command ([no] cdp enable), LLDP uses two commands: [no] lldp transmit and [no] lldp receive. This allows you to control the transmission and reception of LLDP messages separately. For example, an interface with transmission enabled but reception disabled will send LLDP messages but will discard any LLDP messages it receives. Likewise, an interface with transmission disabled but reception enabled will not send LLDP messages but will process any LLDP messages it receives and update the LLDP neighbor table as appropriate.

Note Disabling only one of either LLDP transmission or reception is rare. One possible use case is that you may want to leave reception enabled to learn about connected devices but disable transmission for security purposes.

LLDP’s equivalent to show cdp interface is show lldp interface. In the following example, I use the command to view the status of R1 G0/0. If LLDP is globally enabled, LLDP transmission and reception will be enabled on all interfaces by default. If needed, you can then disable them on an interface with no lldp transmit and/or no lldp receive:

R1# show lldp interface g0/0
GigabitEthernet0/0:
    Tx: enabled                    ❶
    Rx: enabled                    ❶
    Tx state: IDLE                 ❷
    Rx state: WAIT FOR FRAME       ❸
❶ Tx (transmission) and Rx (reception) are enabled.

❷ G0/0 is not currently transmitting an LLDP message.

❸ G0/0 is actively listening for LLDP messages.

Note As shown in the previous example, Tx is often used as a shorthand for transmission, and Rx is often used as a shorthand for reception.

The final LLDP verification command we’ll look at in this section is show lldp traffic, which is equivalent to show cdp traffic. It can be handy when troubleshooting to verify whether the device is actually sending and receiving LLDP messages. The following example shows the output of this command:

R1# show lldp traffic
LLDP traffic statistics:
    Total frames out: 1239           ❶
    Total entries aged: 0
    Total frames in: 413             ❷
    Total frames received in error: 0
    Total frames discarded: 0
    Total TLVs discarded: 0
    Total TLVs unrecognized: 0
❶ The number of LLDP messages sent

❷ The number of LLDP messages received

1.2.2 Viewing LLDP neighbors
Now that we’ve enabled LLDP and checked out some of its settings, here’s the most important part: the LLDP neighbor table. The commands are the same as in CDP, replacing cdp with lldp. The following example shows the output of show lldp neighbors on R1:

R1# show lldp neighbors
Capability codes:
    (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device     ❶
    (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other        ❶
Device ID        Local Intf     Hold-time  Capability      Port ID
SW1              Gi0/0          102        B,R             Gi0/1       ❷
Total entries displayed: 1
❶ Codes used in the Capability column

❷ SW1 is R1’s LLDP neighbor.

The top of the output shows a legend of the different codes that can be used in the Capability column. The codes B,R in SW1’s entry indicate that it has both routing and switching capabilities—B for Bridge is equivalent to CDP’s S for Switch. The Local Intf and Port ID columns are the same as in show cdp neighbors; this output means that R1’s G0/0 interface is connected to SW1’s G0/1.

You can view more detailed information about all LLDP neighbors with show lldp neighbors detail. The following example shows the output of that command on R1, highlighting the same information we saw in the previous example. This command shows plenty of additional information, not all of it relevant to the CCNA exam; just make sure you can identify the highlighted information:

R1# show lldp neighbors detail
------------------------------------------------
Local Intf: Gi0/0                                 ❶
Chassis id: 0cf5.a452.b100
Port id: Gi0/1                                    ❷
Port Description: GigabitEthernet0/1
System Name: SW1                                  ❸
 
System Description: 
Cisco IOS Software, C2960C Software (C2960c405-UNIVERSALK9-M), 
➥Version 15.0(2)SE5, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2013 by Cisco Systems, Inc.
Compiled Fri 25-Oct-13 14:35 by prod_rel_team
 
Time remaining: 118 seconds                       ❹
System Capabilities: B,R                          ❺
Enabled Capabilities: B,R                         ❺
Management Addresses - not advertised
Auto Negotiation - not supported
Physical media capabilities - not advertised
Media Attachment Unit type - not advertised
Vlan ID: 1
Total entries displayed: 1
❶ The interface of the local device (R1)

❷ The interface of the neighbor (SW1)

❸ The neighbor’s hostname

❹ The current holdtime

❺ The neighbor’s capabilities

Note You can use the show lldp entry name command (i.e., show lldp entry SW1) to view the same information as show lldp neighbors detail for only the specified neighbor.

Table 1.3 summarizes the LLDP show commands we covered in this section. Make sure you can interpret the output of these commands for the CCNA exam.

Table 1.3 LLDP show commands


| Command                             | Information displayed                                                                    |
|-------------------------------------|------------------------------------------------------------------------------------------|
| `show lldp neighbors`               | LLDP neighbors and basic information about each                                          |
| `show lldp neighbors detail`        | More detailed information about LLDP neighbors                                           |
| `show lldp entry name`              | The same information as `show lldp neighbors detail` but for the specified neighbor only |
| `show lldp`                         | Basic information about LLDP (status, timers)                                            |
| `show lldp interface [ interface ]` | Information about LLDP-enabled interfaces                                                |
| `show lldp traffic`                 | The number of LLDP messages sent/received                                                |


Table 1.4 summarizes the LLDP configuration commands we covered. In most cases, enabling LLDP with lldp run is sufficient, but there are cases in which you might want to fine-tune LLDP with the other commands.

Table 1.4 LLDP configuration commands

| Command                              | Description                                        |
|--------------------------------------|----------------------------------------------------|
| `R1(config)# lldp timer seconds`     | Configures the LLDP advertisement timer            |
| `R1(config)# lldp holdtime seconds`  | Configures the LLDP holdtime                       |
| `R1(config)# lldp reinit seconds`    | Configures the LLDP reinitialization timer         |
| `R1(config)# [no] lldp run`          | Enables/disables LLDP globally                     |
| `R1(config-if)# [no] lldp transmit`  | Enables/disables LLDP Tx on a specific interface   |
| `R1(config-if)# [no] lldp receive`   | Enables/disables LLDP Rx on a specific interface   |


Summary

Layer 2 discovery protocols such as Cisco Discovery Protocol (CDP) and Link Layer Discovery Protocol (LLDP) allow devices to share information about themselves with their directly connected neighbors.
The shared information includes hostnames, capabilities (device type), port ID, IP address, and much more.
CDP is Cisco proprietary and runs on Cisco network devices such as routers and switches. It is enabled by default.
CDP-enabled devices periodically send CDP advertisement messages out of their interfaces and listen for CDP advertisements from neighboring devices.
CDP messages are sent to multicast MAC address 0100.0ccc.cccc but are not flooded by switches.
Use show cdp neighbors to view information about CDP neighbors, such as which neighbor is connected to which interface.
Use show cdp neighbors detail to view more detailed information.
Use show cdp entry name to view the same information as show cdp neighbors detail but for just a single neighbor.
Use show cdp to view basic information about CDP such as the advertisement timer, the holdtime, and the advertisement version.
The advertisement timer determines how often the device sends CDP advertisement messages. The default is 60 seconds. Use cdp timer seconds to modify it.
The holdtime tells the neighbor how long to keep this device in its neighbor table after ceasing to receive CDP messages from this device. The default is 180 seconds. Use cdp holdtime seconds to modify it.
There are two versions of CDP: CDPv1 and CDPv2. Modern Cisco devices send CDPv2 advertisements by default, but you can use no cdp advertise-v2 to enable CDPv1 advertisements (e.g., if the device is connected to a very old device).
You can globally disable CDP with no cdp run and use cdp run to reenable it.
You can use [no] cdp enable in interface config mode to enable/disable CDP on individual interfaces. It is enabled on all interfaces by default.
Use show cdp interface [interface] to view the status of CDP on each interface.
Use show cdp traffic to view statistics about CDP messages sent/received.
Link Layer Discovery Protocol (LLDP) is an industry-standard (IEEE 802.1AB) Layer 2 discovery protocol that can be implemented by any vendor, including Cisco.
CDP and LLDP are very similar, as are their commands. In most cases, you can just replace cdp with lldp to get the equivalent command.
LLDP messages are sent to multicast MAC address 0180.c200.000e. Like CDP messages, they are not flooded by switches.
Cisco routers and switches support both CDP and LLDP, but LLDP is disabled by default. You can enable it globally with lldp run.
Use show lldp to view basic LLDP information such as the advertisement timer, holdtime, and reinitialization delay.
The default LLDP advertisement timer is 30 seconds, the default holdtime is 120 seconds, and the reinitialization timer is 2 seconds. You can modify them with lldp timer seconds, lldp holdtime seconds, and lldp reinit seconds.
The LLDP advertisement timer and holdtime function the same as CDP’s timers. The reinitialization timer determines how long an interface will wait to send LLDP messages after LLDP is activated on it (i.e., after the interface is enabled).
LLDP can be enabled/disabled on a per-interface basis. [no] lldp transmit enables/disables LLDP transmission (Tx) on an interface, and [no] lldp receive enables/disables LLDP reception (Rx).
If LLDP is globally enabled, it is enabled on each interface by default. You can then use no lldp transmit and/or no lldp receive to disable Tx and/or Rx.
Use show lldp interface [interface] to view the LLDP status of interfaces.
Use show lldp traffic to view statistics about LLDP messages sent/received.
Use show lldp neighbors to view a list of the device’s LLDP neighbors, such as which interface each neighbor is connected to.
Use show lldp neighbors detail to view more detailed information.
Use show lldp entry name to view the same information as show lldp neighbors detail but for a single neighbor (instead of all neighbors).