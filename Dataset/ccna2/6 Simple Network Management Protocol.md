6 Simple Network Management Protocol
This chapter covers

Managing network devices with Simple Network Management Protocol (SNMP)
The SNMP network management station and its managed devices
The three main versions of SNMP
Securing SNMP with passwords, user authentication, and encryption
Simple Network Management Protocol (SNMP) is, as the name states, a protocol that facilitates the management of networks—specifically, the management of the devices that make up the network. Whether it is simple is perhaps subjective; like most topics, there is plenty of complexity to be found if you dig deep enough!

SNMP allows an admin to centrally monitor the status of devices, trigger alerts for specific events, and even modify device configurations without having to log into a device’s CLI. Various types of devices can be managed using SNMP: network devices, like routers and switches; servers; user devices, like PCs and laptops; printers; and many more. For our purposes, we will focus on managing Cisco routers and switches with SNMP.

SNMP is CCNA exam topic 4.4: Explain the function of SNMP in network operations. It’s a CCNA exam topic for a good reason: SNMP is widely used in networks of all sizes to provide real-time monitoring and management capabilities that are essential to modern network operations.

6.1 SNMP operations and components
The two main components of SNMP are the network management station (NMS) and the managed devices. The NMS is a software platform designed for monitoring and managing devices using SNMP; it is usually run on an admin’s PC (in smaller networks) or a central server (in larger networks).

Each managed device organizes information about itself into a database called the Management Information Database (MIB), and these pieces of information are stored as variables. One variable in a device’s MIB could be GigabitEthernet0/1 status, and the value of that variable could be up or down. Some other variables could be the internal temperature of the device, the current CPU utilization, the state of Open Shortest Path First (OSPF) neighbors, and many more; Cisco routers and switches store thousands of these variables.

In this section, we’ll examine how devices can use SNMP to interact with the MIB of a device: how the NMS can read and modify MIBs and how the managed devices can notify the NMS of changes to their MIBs. Then, we’ll look at the components of the NMS and the managed devices in greater detail.

Note Although I will generally refer to the NMS in most examples in this chapter, it is possible for there to be multiple NMSs; this provides the benefit of redundancy.

6.1.1 SNMP operations
In this section, let’s take the example of the GigabitEthernet0/1 status variable to demonstrate SNMP’s primary operations. We’ll cover how the NMS can read and modify the variables in the MIB and how the managed devices can notify the NMS when certain events occur.

Reading the MIB

The NMS can query its managed devices to get the value of one or more variables. I use the term get because that’s the name of the SNMP message type used to do so: Get. Figure 6.1 demonstrates how an NMS queries a managed device to read the value of one of the variables in its MIB and then receives a Response message from the managed device.



Figure 6.1 An SNMP Get and Response exchange. (1) The NMS sends a Get to R1 to learn the status of R1’s G0/1 interface. (2) R1 replies, informing the NMS that G0/1 is down.

The NMS uses a Get message to query the value of one or more variables in the MIB, and the managed device then replies with a Response message, which includes the requested information. Get messages can be manually sent by an administrator as needed, but automation makes them even more powerful. Get messages can be automated from the NMS to periodically check the status of various devices within the network; this allows the NMS to actively monitor the state of the network, gather performance metrics, and collect other information.

Note There are three types of messages used to read the MIB: Get, GetNext, and GetBulk. We’ll cover the SNMP message types in greater detail in section 6.2.

Modifying the MIB

In addition to gathering information about managed devices with Get messages, the NMS can modify the values of the MIB’s variables with Set messages. Figure 6.2 demonstrates the concept: the NMS sends a Set message to R1, instructing it to change the status of one of its interfaces. R1 changes the status as instructed and sends a Response message.



Figure 6.2 An SNMP Set and Response exchange. (1) The NMS sends a Set message instructing R1 to change its G0/1 interface to Up. (2) R1 changes G0/1’s status as instructed. (3) R1 sends a Response message to the NMS.

SNMP Set messages allow you to configure the devices in your network centrally from the NMS without logging in to the CLI of each device. For example, if a new DNS server has been added to the network, the NMS can use Set messages to add the new DNS server to each router’s configuration; this is simpler than logging in to each router and manually configuring it with the ip name-server command.

Other uses for Set messages

The example of changing R1 G0/1’s status to Up is equivalent to configuring no shutdown on the interface. However, Set messages can be used for more than configuration changes. For example, you can initiate a system reboot or shutdown via a Set message. You can also use Set messages to make devices back up their configuration files to a central file server. This is more efficient than doing so manually via each device’s CLI, one by one.

Notifying the NMS

The final SNMP operation is notifying the NMS. Managed devices can be configured to send notifications to the NMS when specific events occur. Figure 6.3 shows an example: R1’s G0/1 interface goes down (perhaps due to a hardware malfunction or a cut cable), and R1 sends a Trap message to the NMS. Whereas Get messages are used to periodically retrieve information from managed devices, Trap messages allow managed devices to immediately notify the NMS when an event occurs, unsolicited by the NMS.



Figure 6.3 Notifying the NMS with a Trap message. (1) R1 G0/1 goes down. (2) R1 notifies the NMS of the event with a Trap message. (3) The NMS notifies an admin via an email or SMS text message.

Figure 6.3 also shows the NMS alerting an admin of the event with an email or SMS text message; this isn’t a feature of the SNMP protocol itself but can be implemented in most SNMP applications. Such alerts are very helpful in enabling the admin to respond quickly to serious events that occur on the network.

6.1.2 SNMP components
We’ve looked at the two main components of SNMP: the NMS and the managed devices. Each device that uses SNMP, whether it’s an NMS or a managed device, runs SNMP software that can be called the device’s SNMP entity. Each device’s SNMP entity consists of a couple of components, as shown in figure 6.4.



Figure 6.4 The components of the NMS’s and managed devices’ SNMP entities. The NMS’s SNMP entity consists of the SNMP manager and SNMP application(s). The managed devices’ SNMP entities consist of the SNMP agent and the MIB.

The SNMP entity on the NMS consists of an SNMP manager and an SNMP application, and the SNMP entity on each managed device consists of an SNMP agent and an MIB. In this section, we’ll examine each of these components.

Exam Tip Make sure you can identify which components reside on the NMS and which reside on the managed devices.

SNMP managers and agents

The SNMP manager and SNMP agent serve as the interface between the NMS and a managed device. The SNMP manager runs on the NMS and interacts with the SNMP agent that runs on each managed device.

The SNMP manager running on the NMS sends messages (i.e., Get, Set) to the SNMP agent running on each of its managed devices; the agent listens for these messages on UDP port 161 and then responds accordingly (i.e., with the requested information about the device the agent is running on). Similarly, the SNMP agent running on each managed device sends messages (i.e., Response, Trap) to the SNMP manager on the NMS; the manager listens on UDP port 162.

Exam Tip Memorize those port numbers! SNMP managers listen on UDP port 162, and SNMP agents listen on UDP port 161.

SNMP applications

An SNMP application is a piece of software that allows a human to interact with SNMP, usually through a graphical user interface (GUI). Through the application, an admin can control how they want to use SNMP to monitor and manage their network devices. Figure 6.5 shows a screenshot from PRTG Network Monitor, a network-monitoring tool that uses SNMP (although it is not exclusively an SNMP application).



Figure 6.5 The GUI of PRTG Network Monitor, an SNMP application

I have configured PRTG to send SNMP Get messages periodically (every 60 seconds) to the devices in my home network to monitor things like the rate of traffic sent and received by their interfaces, CPU and memory utilization, power supply health, internal temperature, and others. Using PRTG, I can check the current value of each monitored variable and view graphs that display historical data—for example, to view the traffic rate on my router’s internet connection for the past day, month, or year.

Exam Tip You are not expected to know or be able to set up any particular SNMP application for the CCNA. Just understand its role as SNMP’s human interface.

The SNMP MIB

The Management Information Base (MIB) is the database in which each managed device organizes information about itself; as we covered before, this information is stored as a series of variables. Directly interacting with the MIB is the agent’s job; for example, when the agent receives a Get message from the manager, the agent will look up the requested variables, retrieve their values, and send them to the manager in a Response message.

Each variable is given an object identifier (OID) that uniquely identifies it. For example, 1.3.6.1.2.1.2.2.1.8 is the OID for interface operational status; the manager can query this OID to learn the status of a particular interface. OIDs are hierarchically organized into a tree-like structure similar to the DNS hierarchy; each number in the OID represents a different level or branch in the tree. Figure 6.6 demonstrates this tree-like structure.



Figure 6.6 A small segment of the SNMP OID hierarchy. 1.3.6.1.2.1.2.2.1.8 is the OID of the ifOperStatus variable.

OIDs can be complex and lengthy, making them difficult to remember or work with directly. To simplify this, SNMP applications like PRTG translate these OIDs into user-friendly, descriptive names. So, while the SNMP manager might send a Get for an OID like 1.3.6.1.4.1.9.9.109.1.1.1.1.4, the SNMP application’s interface will display this as something more understandable, such as “CPU Utilization.” This way, the application removes the need for the user to deal with the intricate details of OIDs.

Note You can explore different OIDs at https://oidref.com/. For example, https://oidref.com/1.3.6.1.2.1.2.2.1.8 and https://oidref.com/1.3.6.1.4.1.9.9.109.1.1.1.1.4 are the two example OIDs mentioned in this section.

Vendor-specific OIDs

Vendors can define their own OIDs, and in some cases, the NMS might not be aware of them by default. However, vendors (i.e., Cisco) often provide MIB files for download that define the specific OIDs used by their devices. You can import these MIB files into the NMS to allow it to properly interpret those OIDs when receiving them in Traps and other messages.

6.2 SNMP messages
Now that we’ve covered the basics of SNMP—what it does and its components—let’s dig into some more details. In addition to the messages we’ve covered so far, SNMP includes a few more message types that the NMS and managed devices can exchange with each other. We’ve already covered four different SNMP message types: Get, Response, Set, and Trap—one message from each class of SNMP message. Table 6.1 lists the four SNMP message classes and the messages included in each category.

Table 6.1 SNMP message types

| Message class | Description                                                        | Message types         |
|---------------|--------------------------------------------------------------------|-----------------------|
| Read          | Sent by the NMS to retrieve information from its managed devices   | Get, GetNext, GetBulk |
| Write         | Sent by the NMS to modify the values of one or more OIDs           | Set                   |
| Notification  | Sent by the managed devices to alert the NMS of a particular event | Trap, Inform          |
| Response      | Sent in response to a previous message                             | Response              |



6.2.1 The Read message class
Messages in the Read class are sent by the NMS to retrieve information from its managed devices—to ask for the values of one or more OIDs. The Read class includes three message types: Get, GetNext, and GetBulk. The Get message is the simplest of the three; in a Get message, the NMS specifies one or more OIDs, and the managed device responds with the values associated with those OIDs.

GetNext is used to discover unknown OIDs. When an NMS sends a GetNext request, the managed device returns the next OID in the tree and its value. For example, consider the following three OIDs:

1.3.6.1.2.1.1.1

1.3.6.1.2.1.1.2

1.3.6.1.2.1.1.3

If a managed device sends a GetNext request asking for the OID immediately following 1.3.6.1.2.1.1.1, it would receive the value associated with OID 1.3.6.1.2.1.1.2. This allows the NMS to discover the available information without having to know each specific OID in advance, also called “walking the tree.”

The GetBulk message type, which was introduced in SNMPv2, provides the NMS with an efficient way to retrieve lots of information from a managed device without specifying each individual OID. Instead, GetBulk allows the NMS to specify an entire range of OIDs. This message type also allows the NMS to “walk the tree” like GetNext, but in a more efficient manner; whereas GetNext requests OIDs one at a time, GetBulk can request many at once.

6.2.2 The Write message class
The Write message class, containing only the Set message type that we looked at earlier, allows the NMS to modify the value associated with a specified OID. In section 6.1.1, I gave the example of modifying an interface’s status, equivalent to issuing the shutdown or no shutdown commands in the CLI. A few other examples of OIDs you might use Set messages to change are the device’s hostname, ACLs, IP addresses, and various other device configurations.

However, it’s worth noting that some OIDs are read-only—their values can’t be modified with Set messages. Some types of OIDs that would likely be read-only are OIDs related to system information (i.e., temperature, system health), resource utilization (i.e., CPU, memory), and interface statistics (i.e., current traffic rate). The NMS might send Get messages to retrieve the values associated with these OIDs, but modifying them with Set messages doesn’t make much sense—telling a device “your internal temperature is X degrees” won’t actually change the temperature!

6.2.3 The Notification message class
Next is the Notification message class, which includes two message types: Trap and Inform. Figure 6.7 demonstrates the difference between these two message types.



Figure 6.7 The two notification messages: Trap and Inform. Whereas Traps are unacknowledged, the NMS acknowledges each Inform with a Response message.

Traps are simple. When a particular event occurs (i.e., when the device’s internal temperature passes X degrees or when an interface goes down), the managed device will send a Trap to the NMS; the NMS is thus considered notified of the event, regardless of whether it actually received the Trap or not. If the NMS successfully receives the Trap, it can then display an alert in the SNMP application, notify an admin, or perhaps just add the Trap to its logs. However, it does not respond to the managed device that sent the Trap.

Informs, introduced in SNMPv2, serve the same purpose as Traps: informing the NMS of a particular event. However, whereas Traps are unacknowledged by the NMS, Informs are acknowledged with a Response message. This provides a more reliable method of notifying the NMS; if the managed device doesn’t receive a Response after sending an Inform, it will retransmit the Inform to ensure that the NMS receives it. For this reason, Informs should be preferred over Traps when using SNMPv2 or SNMPv3—if an event is worth notifying the NMS about, it’s worth ensuring that the NMS actually received the notification.

Exam Tip Traps are unacknowledged notifications, and Informs are acknowledged notifications. Remember this difference between the two! Note that you can configure network devices to send Traps, Informs, or both.

6.2.4 The Response message class
The final message class is Response, which consists of a single message type, also called Response; we’ve already looked at Response messages multiple times in this chapter. Response messages are used by both the NMS and its managed devices:

Managed devices send Responses to reply to Get, GetNext, GetBulk, and Set.

The NMS sends Responses to reply to Informs.

Although all of these examples use the Response message type, the exact contents of the message depend on the type of message it is in response to. For example, a Response message sent in response to a Get message includes the requested OIDs and their values. A Response message sent in response to an Inform message, on the other hand, confirms that the NMS received the managed device’s Inform message.

6.3 SNMP versions and security
Three major versions of SNMP have been widely implemented: SNMPv1, SNMPv2c, and SNMPv3. Table 6.2 summarizes the three versions of SNMP.

Table 6.2 SNMP versions

| Version | Message types                                    | Authentication                                  | Encryption |
|---------|--------------------------------------------------|-------------------------------------------------|------------|
| SNMPv1  | Get, GetNext, Set, Trap, Response                | Community strings                               | No         |
| SNMPv2c | Get, GetNext, Set, Trap, Response, GetBulk, Inform | Community strings                             | No         |
| SNMPv3  | Get, GetNext, Set, Trap, Response, GetBulk, Inform | Hash-based authentication with username/password | Yes      |



SNMPv1 was originally defined in three RFCs in 1990: RFCs 1155, 1156, and 1157. It included five message types: Get, GetNext, Set, Trap, and Response—no GetBulk or Inform messages yet. SNMPv1 included very basic security in the form of community strings—essentially passwords used to authenticate SNMP operations between an NMS and its managed devices.

SNMPv2 was later introduced, adding two new message types: GetBulk and Inform. However, the standard did not include the community string feature, instead introducing a different system of security. However, industry demand for backward compatibility and the simplicity of community strings led to SNMPv2c, also called community-based SNMPv2, which uses the same community string system (the “c” in SNMPv2c stands for community-based).

SNMPv3 did not add new message types but greatly improved SNMP’s security by adding improved authentication and encryption. Security is a major concern when using SNMP because an attacker can use SNMP both to gather information about the devices in your network and also to make changes to them with Set messages. In the rest of this section, let’s dig into SNMPv1’s and SNMPv2c’s community-based security, and SNMPv3’s improved security features.

6.3.1 SNMPv1 and SNMPv2c security
SNMPv1 and SNMPv2c use a community-based security model. An SNMP community is a group of SNMP managers and agents that share common authentication parameters—a password called a community string. SNMPv1 and v2c define two different community types: read-only (RO) and read-write (RW). Figure 6.8 demonstrates the difference between them.



Figure 6.8 The difference between read-only (RO) and read-write (RW) community strings. NMS1 provides the RO string, so its Get (1) succeeds, but its Set (2) fails. NMS2 provides the RW string, so its Get (3) and Set (4) both succeed.

An NMS that provides the RO community string in its messages can only read information from the managed device; it can send Get, GetNext, and GetBulk requests, but it can’t modify the managed device with Set messages. In figure 6.8, NMS1 provides the RO community string in its requests to R1. As a result, its Get message succeeds, but R1 rejects NMS1’s Set message.

An NMS that provides the RW community string is capable of both reading information from (i.e., with Get) and writing to (with Set) the managed device. In figure 6.8, NMS2’s Get and Set requests both succeed because NMS2 provides the RW string.

CCNA exam topic 4.4 states that you must be able to “explain the function of SNMP in network operations”; it doesn’t mention SNMP configuration. However, examining a few basic SNMP configuration commands can help you grasp the concepts. The following example shows how I configured the two community strings on R1:

R1(config)# snmp-server community password123 RO      ❶
R1(config)# snmp-server community password456 RW      ❷
❶ Configures a read-only community string

❷ Configures a read-write community string

These commands alone are sufficient to enable R1 to respond to SNMP Get (including GetNext/GetBulk) and Set messages. R1 will respond to Get messages that specify either the RO community string (password123) or the RW community string (password456). R1 will also respond to Set messages, but only those that specify the RW community string.

Note You can also specify an ACL for each community string: snmp-server community community-string {RO | RW} [acl]. The device will only respond to messages specifying that community string if the NMS is permitted by the ACL.

To enable R1 to send Traps to an NMS, we need a couple more commands: one to enable traps (snmp-server enable traps), and one to specify the IP address of an NMS (snmp-server host ip-address [version 2c] community-string). I configure both commands in the following example:

R1(config)# snmp-server enable traps                                ❶
R1(config)# snmp-server host 192.168.1.10 version 2c password789    ❷
❶ Enables all Traps

❷ Specifies an NMS to send SNMPv2c Traps to with the specified community string

The first command, snmp-server enable traps, enables all Trap messages. Alternatively, you can limit traps to specific events; one example is snmp-server enable traps cpu, which only sends CPU-related traps (i.e., CPU utilization alerts). There are many different options; if you have access to the CLI of a Cisco device, check some of them out with the IOS context-sensitive help feature (the question mark “?”).

The second command, snmp-server host 192.168.1.10 version 2c password789, tells R1 to send Traps to the specified NMS (192.168.1.10) using SNMPv2c and the specified community string (password789). Notice that I specified a different community string here than those I configured previously.

The RO and RW community strings I configured earlier determine how the device reacts to Get, GetNext, GetBulk, and Set messages from an NMS. However, the community string in the snmp-server host command determines the community string the device will send in its Trap (and Inform) messages to the NMS; it doesn’t have to match the community string specified in the snmp-server community command. You can then configure the NMS to only accept Traps/Informs that include the correct community string.

6.3.2 SNMPv3 security
Although community strings, in combination with ACLs, provide some degree of security, remember that community strings are sent in plaintext; they are not encrypted. This is not acceptable in modern networks; any attacker who gets a copy of the SNMP communications will know the community strings. SNMPv3 improves SNMP’s security in four main ways:

User-based—Instead of community strings, which are tied to each device, SNMPv3 grants access based on users. For example: “User A can access information X on the managed devices,” “User B can access information Y,” etc.

Message integrity—SNMPv3 performs checks to ensure that messages weren’t altered by an attacker before reaching their destination.

Authentication—Username/password authentication that can be secured with hashing algorithms (like those used by the enable secret command), preventing hackers from reading the passwords.

Encryption—SNMPv3 message contents can be encrypted so that only the intended recipient can read them.

All of these features are great for improving SNMP’s security, but SNMPv3 offers some flexibility: authentication and encryption are optional. Although most networks should ideally use both for maximum security, SNMPv3 offers three security levels:

NoAuthNoPriv—No authentication and no encryption

AuthNoPriv—Authentication, but no encryption

AuthPriv—Both authentication and encryption

SNMPv3’s security features make its configuration a bit more complicated than SNMPv1/SNMPv2c. For example, here’s how to configure a device to respond to SNMPv3 Get messages:

R1(config)# snmp-server group GROUP1 v3 priv                                      ❶
R1(config)# snmp-server user USER1 GROUP1 v3 auth sha AuthPW priv aes 256 PrivPW  ❷
❶ Creates a group with AuthPriv security

❷ Creates a user account (USER1) in the GROUP 1 group

Instead of simply specifying one or more community strings, you must specify a group that specifies the security level to be used (priv configures the AuthPriv security level) and then assigns one or more users to that group. Figure 6.9 clarifies the syntax of the snmp-server user command.



Figure 6.9 The syntax of the snmp-server user command. This command configures user USER1 in group GROUP1, the SHA authentication algorithm with password AuthPW, and the AES-256 encryption algorithm with password PrivPW.

After creating one or more groups and assigning users to each group, you can then enable Traps with snmp-server enable traps (like in SNMPv1 and v2c), and specify an NMS with snmp-server host.

Exam Tip Don’t expect CCNA exam questions about the specifics of configuring SNMPv1/v2c and SNMPv3. It’s sufficient to understand SNMPv1/v2c’s community-based security model and SNMPv3’s user-based security and additional security improvements (integrity, hash-based authentication, and encryption).

Summary
Simple Network Management Protocol (SNMP) facilitates the management of devices, such as routers and switches, over a network.

The two main components of SNMP are the network management station (NMS) and the managed devices. The NMS is a software platform designed for monitoring and managing devices using SNMP.

Managed devices organize information about themselves into a database called the Management Information Base (MIB). The pieces of information are stored as variables, such as “interface status,” “CPU utilization,” etc.

SNMP operations can be divided into reading the MIB, modifying the MIB, and notifying the NMS.

The NMS can query a managed device to get the value of one or more variables in the managed device’s MIB. Get messages are used for this purpose.

The NMS can modify the value of the MIB’s variables with Set messages.

In addition to configuration changes, Set messages can also serve other purposes, such as initiating system reboots and backing up device configuration files.

Managed devices can notify the NMS when specific events occur, such as an interface going down, using Trap messages.

Each device that uses SNMP runs SNMP software that can be called the SNMP entity.

The SNMP entity of the NMS consists of the SNMP manager and SNMP application.

The SNMP entity of a managed device consists of the SNMP agent and MIB.

The manager and agent serve as the interface between the NMS and a managed device, the manager running on the NMS and the agent on the managed device.

The manager sends messages (i.e., Get, Set) to the agent, which listens on UDP port 161. The agent sends messages (i.e., Response, Trap) to the manager, which listens on UDP port 162.

An SNMP application is a piece of software that allows a human to interact with SNMP, usually through a graphical user interface (GUI). Through the application, an admin can control how they want to use SNMP to monitor and manage the network.

Each variable in the MIB is given an object identifier (OID) that uniquely identifies it. OIDs are hierarchically organized into a tree-like structure, similar to the DNS hierarchy. Each number in the OID represents a different level or branch in the tree.

OIDs can be complex and lengthy (i.e., 1.3.6.1.4.1.9.9.109.1.1.1.1.4), making them difficult to remember or work with directly. SNMP applications typically translate these OIDs into user-friendly, descriptive names like CPU Utilization.

Vendors can define their own OIDs to use on their devices. You may need to download an MIB file from the vendor and import it into the NMS to allow it to properly interpret the vendor-specific OIDs.

SNMP messages can be divided into four classes: Read (Get, GetNext, Bulk), Write (Set), Notification (Trap, Inform), and Response (Response).

Get messages retrieve the values associated with one or more OIDs.

GetNext messages retrieve the value of the next OID in the MIB—the OID after the one specified in the message. This allows the NMS to discover the available OIDs.

GetBulk messages provide an efficient way to retrieve lots of information without specifying each individual OID. GetBulk allows the NMS to specify a range of OIDs.

Set messages are used to modify the values associated with one or more OIDs.

Trap messages notify the NMS of a particular event, but the NMS does not send a Response back to the managed device. If the Trap is lost, it is not retransmitted.

Inform messages serve the same purpose as Traps, but the NMS acknowledges receipt of each Inform by sending a Response message to the managed device. If the Inform message is lost, the managed device will retransmit it, making Informs more reliable than Traps.

Response messages are sent by both the NMS (in response to Inform messages) and managed devices (in response to Get, GetNext, GetBulk, and Set messages).

There are three main SNMP versions: SNMPv1, SNMPv2c, and SNMPv3.

SNMPv1 uses five messages: Get, GetNext, Set, Trap, and Response.

SNMPv2c and SNMPv3 add GetBulk and Inform messages to SNMPv1’s five messages.

SNMPv1 and SNMPv2c use a community-based security model. An SNMP community is a group of SNMP managers and agents that share common authentication parameters—a password called a community string.

There are two community types: read-only (RO) and read-write (RW).

An NMS that provides the RO community string in its messages can only read information from the managed device (Get, GetNext, GetBulk). It cannot use Set.

An NMS that provides the RW community string in its messages can both read information from (i.e., Get) and write information to (Set) the managed device.

Use snmp-server community community-string {RO | RW} [acl] to configure RO and RW community strings on a Cisco IOS device. This enables it to respond to SNMP messages that include the appropriate community string.

Use snmp-server enable traps to enable all Trap messages.

Use snmp-server host ip-address [version 2c] community-string to specify an NMS to send Traps/Informs to. The community-string in this command will be sent with all Traps/Informs, and the NMS can use it to authenticate the device.

SNMPv3 greatly improves SNMP’s security with a user-based security system, message integrity checks, hash-based authentication, and encryption.

Authentication and encryption are highly recommended but optional. The three security levels are NoAuthNoPriv (no authentication and no encryption), AuthNoPriv (authentication, but no encryption), and AuthPriv (authentication and encryption).

SNMP’s user-based system requires you to create groups with snmp-server group, and then assign one or more users to each group with snmp-server user.