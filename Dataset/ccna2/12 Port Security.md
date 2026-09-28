12 Port Security
This chapter covers

How Port Security protects against DHCP exhaustion and MAC flooding attacks
Configuring Port Security on Cisco switches
Fine-tuning Port Security configurations
Connections to an external network, such as the public internet, are obvious security concerns. However, internal network threats should not be overlooked. It could be a malware-infected device—an external threat from the internet that has taken hold in the internal network. Or it could be a malicious user; no one wants to view their own coworkers with suspicion, but ignoring such possibilities is asking for trouble.

Given these concerns, securing the points where users connect to the network—switches—is paramount. In this and the following two chapters, we will cover CCNA exam topic 5.7: Configure and verify Layer 2 security features. These include DHCP Snooping, Dynamic ARP Inspection, and Port Security—all of these are security features on switches. This chapter focuses on Port Security, which provides granular control over which devices a switch allows to communicate over the network.

12.1 Port Security basics
Port Security is a feature of Cisco switches that adds a layer of security to a switch’s MAC address-learning process. Specifically, Port Security allows you to set a limit on the number of unique MAC addresses that can be learned on each port, and it defines actions to be taken if that limit is exceeded.

By default, the number of MAC addresses that a switch can learn on a port is limited only by the maximum size of the switch’s MAC address table—typically in the range of a few thousand to tens of thousands of MAC addresses. However, this default behavior is a vulnerability that can potentially be exploited. In this section, we’ll look at a couple of attacks that exploit this behavior and see how to configure Port Security to mitigate those threats.

12.1.1 DHCP exhaustion and MAC flooding attacks
In chapter 11, we briefly looked at a DHCP exhaustion attack as an example of a spoofing attack. In a DHCP exhaustion attack, the attacker sends countless DHCP DISCOVER messages with spoofed MAC addresses to exhaust a DHCP server’s pool of available addresses, preventing legitimate user devices from getting IP addresses.

Another type of attack that involves spoofed MAC addresses is a MAC flooding attack, which attempts to fill up a switch’s MAC address table with spoofed addresses. With a full MAC address table, the switch is unable to learn the legitimate MAC addresses of hosts in the LAN. To understand the effect of this, recall how a switch forwards and floods frames.

When a switch receives a unicast frame (a frame destined for a single host’s MAC address), the switch will look for a matching entry in its MAC address table. If it finds a matching entry, it will forward the frame out of the port specified in the entry. However, if the switch doesn’t find a matching entry, the switch will flood the frame out of all ports (in the same VLAN) except the port the frame was received on.

If the switch can’t learn a host’s MAC address because the switch’s MAC address table is full, the result is that the switch will always flood frames that are destined for that host. Figure 12.1 demonstrates this. In step 1, the attacker floods thousands of frames with spoofed MAC addresses, resulting in SW1’s MAC address table becoming full in step 2. The result is that SW1 can’t learn PC1’s and R1’s MAC addresses, so it floods all frames sent between them, allowing the attacker to receive copies of those frames. With regard to the CIA triad, this harms the confidentiality of communications between PC1 and R1.



Figure 12.1 A MAC flooding attack. The attacker fills up SW1’s MAC address table with spoofed MAC addresses, preventing SW1 from learning PC1’s and R1’s MAC addresses. As a result, SW1 floods all frames sent between PC1 and R1.

Note Although DHCP exhaustion and MAC flooding are separate attacks with different goals, MAC flooding is often a side effect of DHCP exhaustion; the thousands of spoofed DHCP DISCOVER messages can result in MAC flooding.

Port Security can mitigate against both of these attack types by limiting the number of MAC addresses a switch can learn on a port and taking action if that number is exceeded. In the next section, we’ll look at how to configure basic Port Security on a Cisco switch.

Tradeoffs: Security vs. flexibility

When setting up network features like Port Security, you’re often faced with a balancing act between two elements, both of which are important. One is security—protecting the network from threats that can harm one or more aspects of the CIA triad. The other element is operational flexibility. Strict security policies can be a hindrance in dynamic environments, especially when manual intervention to adjust security settings is not readily available.

Striking the right balance is essential. While it is tempting to lock down your network with the strictest security measures, it’s also important to consider the impact on day-to-day operations. In this chapter, we’ll cover various ways to configure and fine-tune Port Security, some leaning toward the security side of the spectrum, and others more toward flexibility. Each network has unique needs and constraints. Therefore, when asked which setting is appropriate, the answer often is “It depends.”

Keep this tradeoff in mind as you read this chapter (and the following two, which cover other switch security features). However, the CCNA exam itself focuses mainly on implementation. Questions of network design and security policy are usually left for those in senior roles with the experience necessary to make those high-impact decisions.

12.1.2 Basic Port Security configuration
Port Security, at its most basic, can be configured with a single command in interface config mode: switchport port-security. Figure 12.2 shows how to configure Port Security and how it can prevent a MAC flooding attack. Once SW1 detects multiple unique MAC addresses on its F0/1 port, the port transitions to an error-disabled state. This action effectively blocks all incoming and outgoing frames on that port.



Figure 12.2 Using Port Security, SW1 error-disables F0/1 when it detects more than one unique MAC address on the port, preventing a MAC flooding attack.

If you try to enable Port Security on a switch port with the default settings, the command will be rejected. As shown in the following example, the switch won’t allow Port Security on a dynamic port (one that uses DTP—it hasn’t been explicitly set to access or trunk mode):

SW1(config)# interface range f0/1-2
SW1(config-if-range)# switchport port-security       ❶
Command rejected: FastEthernet0/1 is a dynamic port. ❷
❶ Enables Port Security

❷ The command is rejected.

To bypass this, specify the mode (access or trunk) before enabling Port Security:

SW1(config-if-range)# switchport mode access   ❶
SW1(config-if-range)# switchport port-security ❷
❶ Configures F0/1 and F0/2 as access ports

❷ Enables Port Security

This time, the command succeeded without any error messages. To confirm the Port Security settings of a port, use the show port-security interface interface command. In the following example, I confirm F0/1’s settings:

SW1# show port-security interface f0/1
Port Security              : Enabled           ❶
Port Status                : Secure-up         ❶
Violation Mode             : Shutdown
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 1                 ❷
Total MAC Addresses        : 1                 ❸
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 0
Last Source Address:Vlan   : 3c57.311a.a480:1  ❹
Security Violation Count   : 0
❶ Port Security is enabled, and F0/1 is up.

❷ A maximum of one MAC address is allowed on the port.

❸ One MAC address has been learned on the port.

❹ F0/1’s most recently learned MAC address

From that output, you can learn that

Port Security is active and F0/1 is up.

Only one MAC address is allowed on F0/1, and it has learned one MAC address.

The most recently learned MAC address on F0/1 is 3c57.311a.a480.

Note A MAC address learned on a port security–enabled port is called a secure MAC address.

Now let’s see what happens when the attacker attempts a MAC flooding attack, sending frames with spoofed MAC addresses to SW1. The following output shows what happens when SW1 receives a frame with a different MAC address:

%PM-4-ERR_DISABLE: psecure-violation error detected on Fa0/1, 
➥putting Fa0/1 in err-disable state
%PORT_SECURITY-2-PSECURE_VIOLATION: Security violation occurred, 
➥caused by MAC address 00e0.4c68.92ff on port FastEthernet0/1.
As soon as SW1 receives the spoofed frame, a couple of Syslog messages are shown, indicating that a Port Security violation occurred on F0/1. Because SW1 had already learned one MAC address on F0/1, the second MAC address exceeded the limit and triggered the violation. Figure 12.3 demonstrates how the violation was triggered.



Figure 12.3 Port Security allows SW1 to learn only one MAC address on F0/1. Frames 1 and 2 are from the same MAC address, so they are forwarded normally. Frame 3 makes F0/1 exceed the maximum MAC count, triggering a violation.

The following output of show port-security interface shows the results of the violation. SW1 disabled F0/1:

SW1# show port-security interface f0/1
Port Security              : Enabled
Port Status                : Secure-shutdown    ❶
Violation Mode             : Shutdown
. . .
Maximum MAC Addresses      : 1
Total MAC Addresses        : 0                  ❷
. . .
Last Source Address:Vlan   : 00e0.4c68.92ff:1   ❸
Security Violation Count   : 1                  ❹
❶ F0/1 has been shut down (err-disabled) by Port Security.

❷ The total MAC addresses counter has been reset.

❸ The last MAC address learned on the port—the MAC address that caused the violation.

❹ The violation count has increased to 1.

This time, F0/1’s status is Secure-shutdown, meaning that it has been disabled by Port Security. Note that the Total MAC Addresses count is now 0; when a port is disabled, all dynamically learned MAC addresses on the port are forgotten, including secure MAC addresses.

However, the output still shows the MAC address that was most recently seen on that port in the Last Source Address:Vlan row. This is the spoofed MAC address that triggered the Port Security violation. In the bottom row of the output, you can see the Security Violation Count. Each time the port is disabled by Port Security, this count will increment by 1.

We have thwarted the attacker! By using Port Security to make SW1 disable a port if too many unique MAC addresses are learned on the port, we prevented the attacker from filling SW1’s MAC address table up with spoofed MAC addresses. In this example, Port Security prevented an attack, but it could also interfere with legitimate communications. Port Security simply limits the number of MAC addresses allowed on a specific port but doesn’t inherently differentiate between a spoofed frame and a legitimate one.

For example, some devices may legitimately send frames from multiple MAC addresses—one example is a device running virtual machines (which we’ll cover in chapter 17). In such a scenario, the default Port Security settings would result in the port being disabled, despite the frames being legitimate. Later in this section, we’ll see how to adjust the number of allowed MAC addresses to accommodate scenarios where a switch needs to learn multiple MAC addresses on a port.

Reenabling an error-disabled port

This isn’t the first time we’ve seen error-disabled ports in either volume of this book. The first time was in chapter 14 of volume 1, Spanning Tree Protocol (STP), when we covered BPDU Guard—a feature that error-disables a port if it receives STP Bridge Protocol Data Units (BPDUs). And in chapter 10, we covered Power Policing, which disables a port if a PoE-powered device draws too much power.

Just like in those previous examples, you can reenable an error-disabled port by first disabling the port with shutdown and then reenabling it with no shutdown. In the following example, I do that on F0/1:

SW1(config)# interface f0/1
SW1(config-if)# shutdown                               ❶
SW1(config-if)# no shutdown                            ❷
%PM-4-ERR_DISABLE: psecure-violation error detected    ❸
➥on Fa0/1, putting Fa0/1 in err-disable state         ❸
%PORT_SECURITY-2-PSECURE_VIOLATION: Security violation ❸
➥occurred, caused by MAC address 3c57.311a.a481 on    ❸
➥port FastEthernet0/1.                                ❸
❶ Shuts down F0/1

❷ Reenables F0/1

❸ F0/1 is error-disabled by Port Security again.

After reenabling F0/1, it was almost immediately disabled by Port Security again. The lesson here is that you should always address the underlying issue causing the error-disabled state before reenabling the port. In this case, the attacker that triggered the violation was still connected to F0/1.

In addition to manually reenabling error-disabled ports, there is a feature called ErrDisable Recovery that does it automatically. ErrDisable Recovery is disabled by default, but can be enabled on a per-cause (also called per-reason) basis. Cause refers to the event that caused the port to be error-disabled (BPDU Guard, Power Policing, Port Security, etc.). You can use show errdisable recovery to verify the status of ErrDisable Recovery:

SW1# show errdisable recovery 
ErrDisable Reason            Timer Status
-----------------            --------------
. . .
bpduguard                    Disabled                 ❶
. . .
inline-power                 Disabled                 ❷
. . .
psecure-violation            Disabled                 ❸
. . .
Timer interval: 300 seconds                           ❹
Interfaces that will be enabled at the next timeout:  ❺
❶ ErrDisable Recovery is disabled for ports disabled by BPDU Guard.

❷ ErrDisable Recovery is disabled for ports disabled by Power Policing.

❸ ErrDisable Recovery is disabled for ports disabled by Port Security.

❹ The default timer is 300 seconds (5 minutes).

❺ No interfaces will be automatically reenabled.

ErrDisable Recovery works by automatically reenabling an error-disabled port after a preset duration; the default timer is 300 seconds. To enable ErrDisable Recovery for ports disabled by a particular cause, use the errdisable recovery cause cause command in global config mode. The keywords for the causes we have covered so far in these volumes are:

bpduguard (BPDU Guard)

inline-power (Power Policing)

psecure-violation (Port Security)

Note You can modify the ErrDisable Recovery timer with errdisable recovery interval seconds in global config mode.

In the following example, I enable ErrDisable Recovery for ports disabled by Port Security and then confirm. Note that F0/1 now appears at the bottom of the output, indicating that it will be automatically reenabled when the timer counts down to 0:

SW1(config)# errdisable recovery cause psecure-violation ❶
SW1(config)# do show errdisable recovery    
ErrDisable Reason            Timer Status
-----------------            --------------
. . .
psecure-violation            Enabled                     ❷
. . .
Timer interval: 300 seconds     
Interfaces that will be enabled at the next timeout:
Interface       Errdisable reason       Time left(sec)
---------       -----------------       --------------
Fa0/1          psecure-violation          295            ❸
❶ Enables ErrDisable Recovery for ports disabled by Port Security

❷ ErrDisable Recovery is enabled for ports disabled by Port Security.

❸ F0/1 will be reenabled after the timer counts down to 0.

ErrDisable Recovery is a convenient feature for reenabling error-disabled ports, but keep in mind that you still need to solve the problem that caused the port to be error-disabled in the first place. If not, the port will be disabled again after recovering.

Increasing the maximum MAC addresses

By default, a Port Security–enabled port can only receive frames from one unique MAC address—anything more will trigger a violation. However, there are some scenarios that require a switch port to learn multiple MAC addresses on a single port. Figure 12.4 shows two examples: a port connected to another switch (F0/2) and a port connected to an IP phone and PC (F0/3).



Figure 12.4 Allowing multiple MAC addresses on Port Security–enabled ports

Note Figure 12.4 omits the switchport mode configurations, but remember that Port Security can only be enabled on manually configured access or trunk ports.

SW1 F0/2 is connected to another switch with its own connected hosts. As those hosts communicate over the network, SW1 will learn their MAC addresses on its F0/2 port; the Port Security default of a single MAC address isn’t enough in this situation. I used switchport port-security maximum 8 to allow SW1 to learn up to eight unique MAC addresses on F0/2, but the appropriate number depends on how many hosts are connected to the other switch.

SW1 F0/3 is connected to an IP phone and a PC, each with its own MAC address. SW1 needs to be able to receive frames from both devices, so the Port Security default of one MAC address doesn’t work here either. I used switchport port-security maximum 2 to increase the maximum number of MAC addresses to two. Let’s confirm these settings on SW1 with a new command, show port-security:

SW1# show port-security    
Secure Port  MaxSecureAddr  CurrentAddr  SecurityViolation  Security Action
                (Count)       (Count)          (Count)
---------------------------------------------------------------------------
      Fa0/1              1            1                  0         Shutdown  ❶
      Fa0/2              8            5                  0         Shutdown  ❷
      Fa0/3              2            2                  0         Shutdown  ❸
---------------------------------------------------------------------------
. . .
❶ F0/1 allows a maximum of 1 MAC address and has learned 1.

❷ F0/2 allows a maximum of 8 MAC addresses and has learned 5.

❸ F0/3 allows a maximum of 2 MAC addresses and has learned 2.

Configuring static secure MAC addresses

The examples we have looked at so far are dynamic secure MAC addresses—secure MAC addresses that are dynamically learned. But Port Security allows you to control not only how many MAC addresses are allowed on a port, but also exactly which MAC addresses are allowed. You can do this by manually configuring static secure MAC addresses.

You might want to configure static secure MAC addresses to control exactly which devices can connect to which ports. For example, figure 12.5 adds a server to the previous topology. The server is connected to SW1’s F0/4 port, and no other devices are allowed to connect to that port.



Figure 12.5 Configuring static secure MAC addresses. There can be a mix of static and dynamic secure MAC addresses on a port, as in F0/5’s case.

Figure 12.5 also shows an IP phone and a PC connected to SW1’s F0/5 port. To accommodate both devices, I raise the maximum number of MAC addresses to two. However, I only statically configure the phone’s MAC address, allowing the PC’s MAC address to be learned dynamically. Port Security supports this kind of flexibility; on the same port, there can be a mix of static and dynamic secure MAC addresses.

Note Dynamic and static secure MAC addresses both count toward the maximum. If the maximum is two addresses, and you configure one static secure MAC address, that means that only one dynamic MAC address can be learned on the port.

The command to configure a static secure MAC address is switchport port-security mac-address mac-address. If you issue the command as is, the static secure MAC address will be configured in the access VLAN of the port. However, to configure a static secure MAC address in the voice VLAN—the MAC address of an IP phone—add the vlan voice keywords to the end of the command.

Like any other MAC addresses learned by a switch, secure MAC addresses appear in the switch’s MAC address table, which you can view with show mac address-table. However, to view only secure MAC addresses, you can add the secure keyword, as in the following example:

SW1# show mac address-table secure
          Mac Address Table
-------------------------------------------
Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
. . .
   1    0200.0011.1234    STATIC      Fa0/4    ❶
   1    00e0.423c.f021    STATIC      Fa0/5    ❶
   2    0200.0022.3456    STATIC      Fa0/5    ❶
❶ All secure MAC addresses appear as STATIC in the MAC address table.

That output shows one confusing fact about secure MAC addresses in the MAC address table: they are all listed as STATIC, regardless of whether they were dynamically learned or statically configured. Instead, a better option to view secure MAC addresses is show port-security address. This command lists static secure MAC addresses as SecureConfigured and dynamic secure MAC addresses as SecureDynamic:

SW1# show port-security address 
               Secure Mac Address Table
-----------------------------------------------------------------------------
Vlan    Mac Address       Type                          Ports   Remaining Age
. . .
   1    0200.0011.1234    SecureConfigured              Fa0/4        -
   1    00e0.423c.f021    SecureDynamic                 Fa0/5        -
   2    0200.0022.3456    SecureConfigured              Fa0/5        -
. . .
12.2 Port Security configuration options
In the previous section, we covered the basics of Port Security configuration: enabling Port Security, reenabling error-disabled ports, modifying the maximum number of MAC addresses that a port can learn, and configuring static secure MAC addresses. However, Port Security includes some other configuration options that allow you to fine-tune how it operates, and we’ll cover those in this section.

12.2.1 Port Security violation modes
By default, a Port Security enabled port will be error-disabled if a violation occurs. This is because of the default violation mode: shutdown. However, there are two other violation modes that can be configured on a per-port basis: restrict mode and protect mode. Table 12.1 summarizes each violation mode.

Table 12.1 Port Security violation modes

|                                   | Shutdown | Restrict | Protect |
|-----------------------------------|----------|----------|---------|
| Discards violating frames?        | Yes      | Yes      | Yes     |
| Error-disables port?              | Yes      | No       | No      |
| Increments violation counter?     | Yes      | Yes      | No      |
| Generates Syslog/SNMP messages?   | Yes      | Yes      | No      |


To configure the violation modes, you can use the switchport port-security violation mode command. In the following example, I configure the restrict mode on F0/2 and the protect mode on F0/3:

SW1(config)# interface f0/2   
SW1(config-if)# switchport port-security violation restrict                 ❶
SW1(config-if)# interface f0/3
SW1(config-if)# switchport port-security violation protect                  ❷
SW1(config-if)# do show port-security
Secure Port  MaxSecureAddr  CurrentAddr  SecurityViolation  Security Action
                (Count)       (Count)          (Count)
---------------------------------------------------------------------------
      Fa0/1      1             1            0               Shutdown        ❸
      Fa0/2      8             5            0               Restrict        ❸
      Fa0/3      2             2            0               Protect         ❸
. . .
❶ Configures the restrict violation mode

❷ Configures the protect violation mode

❸ The violation modes are listed under the Security Action column.

With the default shutdown violation mode enabled, the switch error-disables the port if a violation occurs, effectively shutting down the port. In some cases, this reaction might be a bit extreme; the entire port becomes nonoperational. For example, if the port connects to a server providing an essential service, disabling the entire port might not be the ideal choice, despite it being the most secure option. Once again, always keep these tradeoffs in mind.

The restrict violation mode is less extreme. Instead of error-disabling the port, it only discards frames that violate the MAC address limit—the port remains up. Figure 12.6 shows how it works. The port in this example can learn a maximum of one MAC address. The first and third frames, which have source MAC addresses matching the port’s secure MAC address, are forwarded. The second frame, which has a MAC address that doesn’t match the secure MAC address, is discarded (but the port is not error-disabled).



Figure 12.6 The restrict violation mode. Only frames that violate the Port Security rules are discarded. Frames that don’t violate the rules are forwarded as normal.

The third mode, protect, operates similarly to the restrict mode. A port with protect mode enabled will not be error-disabled if a violation occurs; the port will only discard violating frames, as we saw in figure 12.6. The difference between these two modes is that protect mode silently discards violating frames, but restrict mode increments the violation counter for each violating frame and also generates Syslog messages and SNMP Traps/Informs to notify you of the violation.

Note The shutdown mode also increments the violation counter and generates notification messages, but only when the first violating frame is received. After the port has been error-disabled, all frames are simply ignored.

Protect mode is generally not recommended. If a Port Security violation occurs, it’s better to receive a notification (i.e., SNMP Trap) so you can take any necessary action, such as disconnecting the device that triggered the violation. The choice between shutdown mode and restrict mode depends on how drastic an action you want the switch to take when a violation occurs. Shutdown mode is more secure because it prevents all traffic from being sent or received by the port if a violation occurs, but restrict mode is less disruptive to legitimate network traffic.

12.2.2 Secure MAC address aging
We covered the topic of MAC aging in chapter 6 of volume 1. To recap, dynamic MAC addresses are automatically removed (or “aged out”) from the MAC address table using a 5-minute timer. This timer resets whenever a frame from the corresponding MAC address is received. But if a frame from that MAC address isn’t received for 5 minutes (allowing the timer to count down to 0), the entry is aged out of the table. This ensures that the switch’s MAC address table remains up to date and doesn’t fill up with stale entries for devices that are no longer connected to the LAN.

Note Static MAC addresses, which are manually configured, don’t age out.

However, dynamic secure MAC addresses behave differently. Unlike their regular counterparts, they don’t age out by default. The following output shows the default settings for secure MAC address aging:

SW1# show port-security interface f0/1
. . .
Aging Time                 : 0 mins    ❶
Aging Type                 : Absolute  ❷
SecureStatic Address Aging : Disabled  ❸
. . .
❶ The default aging time is 0 minutes, meaning that secure MAC addresses don’t age out.

❷ The default aging type is Absolute.

❸ Aging of static secure MAC addresses is disabled by default.

Enabling secure MAC address aging

By default, a secure MAC address remains in the table indefinitely as long as the port it was learned on stays up. Once the port has learned its maximum number of secure MAC addresses, no more MAC addresses will be allowed on that port. You can change this behavior by enabling secure MAC address aging on a per-port basis with the switchport port-security aging time minutes command. In the following example, I configure an aging time of 5 minutes on SW1 F0/1:

SW1(config)# interface f0/1
SW1(config-if)# switchport port-security aging time 5 ❶
SW1(config-if)# do show port-security interface f0/1
. . .
Aging Time                 : 5 mins                   ❷
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
. . .
❶ Enables secure MAC address aging on F0/1 with a 5-minute timer

❷ The aging time is now 5 minutes.

With this configuration, secure MAC addresses learned on F0/1 will be removed from the table after 5 minutes, making the port available for learning a new secure MAC address. This means that the port isn’t indefinitely “locked” to a specific MAC address, creating a balance between maintaining network security and allowing for dynamic changes in the network environment.

Secure MAC address aging types

Even with aging enabled, the aging behavior of secure MAC addresses is still different from that of regular MAC addresses—those learned on ports without Port Security. That’s because of the default aging type, which determines how secure MAC addresses age out.

As the previous example shows, the default aging type is absolute. This means that after a secure MAC address is learned, the aging timer starts, and the MAC address will be removed after the timer expires, even if the switch continues receiving frames from the same MAC address. In other words, the timer doesn’t reset upon receiving new frames from the same MAC address. However, you can switch to a different aging type—inactivity—to change this behavior on a per-port basis. Here’s how:

SW1(config)# interface f0/1
SW1(config-if)# switchport port-security aging type inactivity ❶
SW1(config-if)# do show port-security interface f0/1
. . .
Aging Time                 : 5 mins
Aging Type                 : Inactivity                        ❷
SecureStatic Address Aging : Disabled
. . .
❶ Enables the inactivity aging type

❷ The aging type is now inactivity.

In inactivity mode, the aging timer will reset if a frame from the secure MAC address is received, similar to regular dynamic MAC addresses. Figure 12.7 demonstrates the difference between the absolute and inactivity aging types.



Figure 12.7 Absolute vs. inactivity aging types. With absolute aging enabled, the aging timer does not reset upon receiving new frames from the same MAC. With inactivity aging enabled, the aging timer resets each time a new frame is received.

The absolute aging type forces the switch to regularly relearn its secure MAC addresses. The inactivity aging type, on the other hand, allows the switch to keep secure MAC addresses in its MAC address table as long as it regularly receives frames from those addresses.

Static secure MAC address aging

As mentioned in a previous note, static MAC addresses, which are manually configured (with the mac address-table static command), do not age out. Just as they are manually configured, they must be manually removed. The same is true of static secure MAC addresses by default.

However, this behavior can be changed on a per-port basis with the switchport port-security aging static command in interface config mode. In the following example, I enable static secure MAC address aging on SW1 F0/1, configure a static secure MAC address, and then verify that it is removed from the configuration after 5 minutes:

SW1(config)# interface f0/1
SW1(config-if)# switchport port-security aging static               ❶
SW1(config-if)# switchport port-security mac-address aaaa.bbbb.cccc ❷
SW1(config-if)# do show running-config
. . .
interface FastEthernet0/1
 switchport mode access
 switchport port-security mac-address aaaa.bbbb.cccc                ❸
 switchport port-security aging time 5
 switchport port-security aging type inactivity
 switchport port-security aging static                              ❹
 switchport port-security
. . .
SW1(config-if)# do show running-config                              ❺
. . .
interface FastEthernet0/1
 switchport mode access
 switchport port-security aging time 5
 switchport port-security aging type inactivity 
 switchport port-security aging static
 switchport port-security
. . .
❶ Enables static secure MAC address aging

❷ Configures a static secure MAC address

❸ The static secure MAC address appears in the running-config.

❹ Static secure MAC address aging is enabled.

❺ After 5 minutes of inactivity, the static secure MAC address is removed from the configuration.

Enabling static secure MAC address aging is rare. Generally, if you manually configure a static secure MAC address, you don’t want it to be automatically removed. However, static aging could be used to configure a static secure MAC address for a limited time without needing to manually remove the address afterward. The aging type has a major effect on how this works: do you want the static address to be removed after a certain period of time or only after the device stops communicating?

12.2.3 Sticky secure MAC addresses
We’ve discussed two types of secure MAC addresses in this chapter:

Dynamic—These are learned dynamically when the switch receives frames and are stored only in the MAC address table. They are removed if the port goes down.

Static—These are manually configured and stored in both the MAC address table and the running-config. They remain even if the port goes down.

Dynamic addresses offer a hands-off approach, requiring no manual configuration. Static addresses provide more control, allowing you to specify exactly which addresses are allowed on a port.

However, there is a third option that offers a middle ground: sticky secure MAC addresses. These addresses are

Dynamically Learned—Like dynamic addresses

Stored in the running-config—Like static addresses, they are stored in the running-config and retained even if the port goes down.

Note Sticky secure MAC addresses cannot be aged out.

Sticky secure MAC addresses can be useful in situations where you want to combine the flexibility of dynamic secure MAC addresses with the persistence of static secure MAC addresses. For example, perhaps the security policy states that only the intended devices can access certain ports; you should not be able to disconnect one device from a port and connect with another. Sticky MAC address learning can facilitate that without requiring the manual configuration of each MAC address on each port, automating the process and reducing administrative overhead.

To enable sticky secure MAC address learning, use the switchport port-security mac-address sticky command in interface config mode. This command turns all current and future dynamically learned secure MAC addresses on the port into sticky addresses, automatically adding them to the running-config. I demonstrate the command in the following example:

SW1(config)# interface f0/1
SW1(config-if)# switchport port-security mac-address sticky ❶
SW1(config-if)# do show running-config
. . .
interface FastEthernet0/1
 switchport mode access
 switchport port-security mac-address sticky
 switchport port-security mac-address sticky 00e0.4c68.92ff ❷
 switchport port-security
❶ Enables sticky secure MAC address learning

❷ A sticky secure MAC address was added to the running-config.

Note Disabling sticky learning with no switchport port-security mac-address sticky converts all sticky addresses on the port back to dynamic.

Figure 12.8 demonstrates secure MAC address persistence. When a port that has learned dynamic secure MAC addresses goes down, those addresses are forgotten. When the port comes back up, it is free to learn a new dynamic secure MAC address (or addresses, depending on the limit). Static and sticky secure MAC addresses, on the other hand, are retained in the running-config, persisting even when their associated port goes down.



Figure 12.8 Secure MAC address persistence. Dynamic addresses are forgotten when the port goes down, but static and sticky addresses persist.

Summary
Port Security adds a layer of security to a switch’s MAC address-learning process by setting a limit on the number of unique MAC addresses that can be learned on each port and defining an action to be taken if that limit is exceeded.

By default, the number of MAC addresses that can be learned on a port is limited only by the maximum size of the switch’s MAC address table.

This default behavior makes the switch vulnerable to attacks such as DHCP exhaustion or MAC flooding, which attempts to fill up a target switch’s MAC address table with spoofed MAC addresses.

If a switch’s MAC address table is full, it can’t learn any more MAC addresses. If it can’t learn a host’s MAC address, the switch will flood frames destined for that host.

Port Security can be enabled on a port with switchport port-security.

Port Security cannot be enabled on a dynamic port—a port that uses DTP. The port must be configured in access or trunk mode.

Use show port-security interface interface to confirm the Port Security settings of a port.

A MAC address learned on a Port Security–enabled port is called a secure MAC address.

By default, a Port Security–enabled port can only learn one MAC address. If a frame from another MAC address is received on the port, a Port Security violation occurs. The default action when a violation occurs is to error-disable the port.

When a port goes down, all dynamically learned MAC addresses on the port are forgotten (cleared from the MAC address table), including secure MAC addresses.

An error-disabled port can be manually reenabled with shutdown followed by no shutdown.

You can use ErrDisable Recovery to automatically reenable error-disabled ports.

Use show errdisable recovery to check the status of ErrDisable Recovery.

ErrDisable Recovery automatically reenables an error-disabled port after a preset duration; the default timer is 300 seconds.

ErrDisable Recovery is disabled by default, but can be enabled on a per-cause basis with errdisable recovery cause cause in global config mode.

You can modify the ErrDisable Recovery timer with errdisable recovery interval seconds in global config mode.

Use switchport port-security maximum maximum to increase the maximum number of MAC addresses allowed on a port before a violation is triggered. For example, this is necessary on a port connected to an IP phone and a PC.

Use show port-security to view information about all Port Security–enabled ports, such as the maximum number of MAC addresses allowed on each port.

Dynamically learned secure MAC addresses are dynamic secure MAC addresses.

Statically configured secure MAC addresses are static secure MAC addresses.

Use switchport port-security mac-address mac-address to configure a static secure MAC address on a port. Add the vlan voice keywords if necessary to specify that the MAC address is in the port’s voice VLAN.

There can be a mix of static and dynamic secure MAC addresses on a port.

Use show mac address-table secure to view secure MAC addresses in the MAC address table. Secure MAC addresses have the STATIC type.

You can also use show port-security address to view secure MAC addresses.

There are three Port Security violation modes that determine how a port reacts to a Port Security violation: shutdown, restrict, and protect.

Use switchport port-security violation mode to configure each port’s violation mode.

The default violation mode is shutdown, which error-disables the port.

The restrict violation mode doesn’t error-disable the port if a violation occurs; it only discards frames that violate the MAC address limit. If the port’s maximum is one MAC address, frames from its learned secure MAC address are allowed, but frames from other MAC addresses are discarded.

The protect violation mode operates similarly to the restrict mode. It only discards violating frames; it doesn’t error-disable the port if a violation occurs.

The difference between the restrict and protect modes is that restrict increments the violation counter for each violating frame. Furthermore, restrict mode generates Syslog/SNMP messages, whereas protect silently discards violating frames without incrementing the counter or generating any messages.

Secure MAC addresses have an aging time of 0 by default, meaning they don’t age out.

Use switchport port-security aging time minutes to configure the aging time of secure MAC addresses.

The default secure MAC address aging type is absolute. This means that after a secure MAC address is learned, the aging timer starts, and the MAC address will be removed after the timer expires, even if the switch continues receiving frames.

The second aging type is inactivity. With this mode configured, the aging timer will be refreshed each time the switch receives a frame from the corresponding MAC address. This is similar to the behavior of regular dynamic MAC addresses.

Use switchport port-security aging type type to modify the aging type on a per-port basis.

Regular static MAC addresses do not age out of the MAC address table; they must be manually removed. The same is true of secure static MAC addresses by default.

Aging of secure static MAC addresses can be enabled on a per-port basis with switchport port-security aging static.

Sticky secure MAC addresses offer a middle ground between dynamic and static secure MAC addresses. They are dynamically learned but are automatically inserted into the running-config and retained even if the port goes down.

Sticky secure MAC addresses cannot be aged out.

Use switchport port-security mac-address sticky to enable sticky address learning on a per-port basis. If you enable it, all current and future dynamically learned secure MAC addresses on the port will become sticky.

If you disable sticky learning on a port, all sticky addresses on the port will be converted back to dynamic addresses.