7 Syslog
This chapter covers

Real-time logging to the console and VTY lines
Storing log messages locally and on a Syslog server
The Syslog message format
Syslog severity levels
Syslog is a standard for message logging in computers and is CCNA exam topic 4.5: Describe the use of syslog features including facilities and severity levels. Like SNMP, the topic of the previous chapter, Syslog provides mechanisms to collect information about devices and monitor network health.

Although they do have their similarities, there are significant differences between SNMP and Syslog, and for that reason, most networks make use of both protocols. SNMP is like a network health report, proactively polling devices at regular intervals to gather mostly (but not exclusively) quantitative metrics—numerical statistics like traffic rates, CPU utilization, error rates, etc. SNMP is also often used for event-based alerting using Trap and Inform messages.

Syslog, on the other hand, is like a journal that the device keeps—a logbook that records significant (and not so significant) events that occur on a device. Although there is overlap between the information both protocols gather, Syslog generally focuses on qualitative information—descriptive information that provides context or insight into what’s happening on the device; this is especially useful when you need to dive deep into troubleshooting or forensic analysis. SNMP might alert you that a router is down, but Syslog can tell you the sequence of events that led to the failure.

7.1 Viewing device logs
As you’ve practiced configuring Cisco routers and switches throughout your studies, you’ve certainly seen messages shown in the CLI like this:

Sep 18 00:54:27.832: %LINK-3-UPDOWN: Interface FastEthernet0/1, 
➥changed state to down
This is an example of a Syslog message logging a change in an interface’s state. Syslog messages can be displayed in real time to users connected to the CLI of a device. They can also be stored locally on the device or a centralized Syslog server to be viewed later. In this section, we’ll examine both aspects of Syslog.

7.1.1 Real-time logging
Cisco IOS displays Syslog messages to users connected to the CLI via the console line by default. This can be controlled with the logging console command, which is enabled by default. You can disable logging to the console line with no logging console if you wish; the device will then stop showing log messages to users connected to the console line.

Similarly, logging to the VTY lines is enabled by default; this applies to users connected to the CLI via Telnet or SSH. This is a result of the logging monitor command that is configured by default; you can disable it with no logging monitor.

However, despite the logging monitor command being enabled by default, when connected to a device’s VTY lines via Telnet or SSH, no log messages are displayed by default. This is because an additional command is required to enable VTY line logging for a particular session: terminal monitor, which is issued in privileged EXEC mode.

Note In this context, a session is an individual connection between a user’s device and a network device via Telnet or SSH.

I demonstrate this in the following example. I am connected to SW1 via SSH, but disabling GigabitEthernet0/1 shows no Syslog messages. However, after I issue the terminal monitor command, reenabling the interface results in two Syslog messages being shown:

SW1(config)# interface g0/1
SW1(config-if)# shutdown                                                            ❶
SW1(config-if)# do terminal monitor                                                 ❷
SW1(config-if)# no shutdown                                                         ❸
Sep 18 02:17:46.867: %LINK-3-UPDOWN: Interface FastEthernet0/3, changed state to up ❹ 
Sep 18 02:17:47.874: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/3, changed state to up                                                                 ❹
❶ No Syslog messages are shown after disabling G0/1.

❷ Enables real-time logging for the session

❸ Reenables the interface

❹ Syslog messages are displayed.

To view real-time Syslog messages when connected via a VTY line, you must use the terminal monitor command every time you connect to the CLI; the command only applies to one session. For example, if you disconnect and then reconnect, you must use the command again if you want to view the real-time messages. Likewise, if multiple users are connected to the VTY lines simultaneously, each user must use the command.

Figure 7.1 demonstrates these concepts. PC1’s user, connected to R1’s console line, enables R1’s G0/1 interface with no shutdown and is shown a Syslog message. PC2 and PC3 are both connected to R1 via SSH. PC2’s user has issued the terminal monitor command and therefore is shown the same log message as PC1’s user. PC3’s user has not used terminal monitor, so no Syslog message is displayed on PC3.



Figure 7.1 Syslog messages displayed when connected to the console line versus when connected to a VTY line

The command to stop displaying messages for a particular session is a bit different than you’re used to; it is not no terminal monitor but rather terminal no monitor. You might choose to use this command if the device is generating a significant number of messages, making it difficult to work in the CLI.

Exam Tip Remember the difference between real-time logging to the console and VTY lines. Although logging is enabled for both by default (due to the default logging console and logging monitor commands), users connected via the VTY lines must also use terminal monitor to enable VTY line logging for each session.

7.1.2 The logging synchronous command
As you’ve practiced configuring Cisco routers and switches, you’ve probably had the frustrating experience of a Syslog message being displayed as you are typing a command, resulting in something like the following example:

SW1# show ru                                 ❶
Sep 18 06:32:10.228: %LINK-5-CHANGED: Interface GigabitEthernet0/1, changed state to upnning-config                                ❷
❶ The command is cut off.

❷ The rest of the command is displayed after the Syslog message.

By default, if a Syslog message is displayed as you are typing a command, the command is cut off, and any additional characters you type are displayed on the same line as the Syslog message. If you hit Enter at this point, the command will execute correctly; using the previous example, the command would be executed as show running-config.

However, this default behavior doesn’t lead to a very good user experience; it can be especially distracting and confusing when using long and complex commands. One solution is to use the Ctrl-l keyboard shortcut, which reprints the command you are currently typing on a new line. However, a better solution is the logging synchronous command.

With logging synchronous configured on the console and VTY lines, the command you are typing will be automatically reprinted on a new line if it gets cut off by a Syslog message. I demonstrate this in the following example:

SW1(config)# line vty 0 15                                         ❶
SW1(config-line)# logging synchronous                              ❶
SW1(config-line)# end
SW1# show ru                                                       ❷
Sep 18 09:32:59.035: %SYS-5-CONFIG_I: Configured from console by jeremy on vty0 (192.168.1.224)                                                         ❷
SW1# show running-config                                            ❸
❶ Enables synchronous logging on the VTY lines

❷ The command I am typing is cut off by a Syslog message.

❸ The command is automatically reprinted on a new line, and I finish typing it.

This command is a major quality-of-life improvement when working in the CLI, and I highly recommend configuring it on the console and VTY lines of your devices; this is one command that I wish was enabled by default!

7.1.3 Storing logs
Real-time logging to the console and VTY lines is useful for alerting you to events as you configure devices, but Syslog’s ability to provide a historical view is even more valuable. This allows you to review events that occurred and their causes after the fact. To enable this, Cisco IOS provides two main ways to store Syslog messages: the device’s memory and an external Syslog server.

The logging buffer

By default, Cisco IOS devices store Syslog messages in RAM; this is called the logging buffer. You can control this with the logging buffered [bytes] command, which is enabled by default. The optional bytes argument allows you to specify how much memory to allocate to the buffer.

The size of the buffer

The default size of the buffer depends on the device. For example, my Catalyst 2960 switch’s buffer is 4,096 bytes in size by default—enough for about 35–40 log messages, depending on each message’s length. At the default size, the buffer fills up rather quickly. After it fills up, messages are added to and removed from the buffer in a first in, first out (FIFO) manner.

A Catalyst 9300 switch—a newer and much more powerful model (that I can’t afford to buy for my home lab)—uses a default size of 102,400 bytes (102.4 kilobytes). Whatever the model, the default settings are fairly conservative. In most cases, there will be enough room to expand the buffer to store more messages. However, before increasing the size of the buffer, use show memory to view the device’s current memory usage and ensure that the device has sufficient memory.

To view the logs stored in the buffer, use the show logging command. This command also displays information about the device’s Syslog settings in general, as shown in the following example. The output of this command is quite large (especially with a large buffer), so I will leave out some output and show only the two most recent log messages:

SW1# show logging
. . .
    Console logging: level debugging, 5014 messages     ❶
➥logged, xml disabled, filtering disabled              ❶
    Monitor logging: level debugging, 1080 messages     ❶
➥logged, xml disabled, filtering disabled              ❶
    Buffer logging:  level debugging, 4500 messages     ❶
➥logged, xml disabled, filtering disabled              ❶
. . .
    Trap logging: level informational, 18 message lines logged
        Logging Source-Interface:       VRF Name:
Log Buffer (4096 bytes):                                ❷
. . .
Sep 18 10:35:06.528: %SEC_LOGIN-5-LOGIN_SUCCESS: Login 
➥Success [user: jeremy] [Source: 192.168.1.224] 
➥[localport: 22] at 19:35:06 JST Mon Sep 18 2023    
Sep 18 10:35:14.539: %SYS-5-CONFIG_I: Configured from   ❸
➥console by jeremy on vty0 (192.168.1.224)             ❸
❶ Console, monitor (VTY line), and buffer logging are enabled by default.

❷ The logging buffer is 4,096 bytes in size.

❸ The most recent messages are shown at the bottom of the output.

As the top section of the output shows, console, monitor (VTY line), and buffer logging are all enabled by default, thanks to the logging console, logging monitor, and logging buffered commands that are part of the device’s default configuration. If you use no logging console to disable console logging, for example, the output will state Console logging: disabled.

While troubleshooting problems on a device (or multiple devices), you will likely use show logging quite often. One point to remember is that the most recent logs are displayed at the bottom of the output; if there are quite a few messages stored in the buffer, you may have to press the spacebar quite a few times to get to the most recent messages.

Note You can also hold down the spacebar to quickly scroll to the bottom of a command with a lot of output, instead of repeatedly pressing the spacebar.

Logging to a Syslog server

In addition to locally saving log messages, you can configure the device to send them to a central Syslog server. This can be very useful, especially in large networks with many devices; storing logs in a central location simplifies the process of viewing and correlating those logs, eliminating the need to log in to each device one by one.

Logging to a Syslog server is governed by the logging trap command (not to be confused with the SNMP Trap message type). Like the other commands we’ve covered, this is enabled by default. However, for a device to actually send Syslog messages to a server, you need to tell the device which server to send the messages to. You can configure this with the logging [host] ip-address command; the device will then send Syslog messages to UDP port 514 on the specified server, in addition to the other destinations (console line, VTY lines, and buffer).

Exam Tip Although standard Syslog uses UDP port 514, there is a secure, encrypted version of Syslog called Syslog over TLS (Transport Layer Security) that uses TCP (not UDP!) port 6514. Although you don’t have to know the details of Syslog over TLS for the exam, be aware that Syslog can use both UDP 514 and TCP 6514.

Note that the host keyword in this command is optional; logging ip-address and logging host ip-address both have the same effect. However, regardless of which command you configure, it will be saved in the running-config as logging host ip-address.

Figure 7.2 visually demonstrates a network device logging events to the four destinations we have covered: real-time logging to the console line (PC1) and VTY lines (PC2) and log storage via the logging buffer (in R1’s RAM) and a Syslog server (SRV1).



Figure 7.2 R1 logs events to four different destinations: the console line, the VTY lines, the logging buffer, and a Syslog server.

7.2 The Syslog message format
Syslog messages in Cisco IOS use a consistent format, as shown in figure 7.3.



Figure 7.3 Syslog message format. The sequence number and time stamp components are optional.

Let’s use the following Syslog message as an example to examine each component:

000065: Sep 19 01:01:01.133: %LINK-3-UPDOWN: Interface FastEthernet0/1,
changed state to down
The first two fields are a sequence number (000065), indicating the order of log messages, followed by a timestamp (Sep 19 01:01:01.133), indicating the time each message was generated. These two fields are optional. For example, in the Syslog messages we have looked at previously, there is no sequence number. We will examine these two components more in section 7.2.1.

The first mandatory component is the facility—a value that indicates the source of the message within the device. In other words, it specifies the service, application, or other component that generated the message. In the example, the facility is LINK, indicating that the message was generated by one of the device’s links—this usually indicates an interface’s status changing to up or down.

Exam Tip There are various facilities, but there’s no need to memorize them for the CCNA exam. Just be sure that you can identify the facility within a Syslog message.

The next component is the severity, which is a numerical value indicating how urgent or critical the message is—a lower value is more severe. In our example, the severity is 3; we’ll cover severity levels in detail in section 7.2.2.

Next is the mnemonic—a short text string that provides a more specific descriptor of the event that triggered the Syslog message. The mnemonic acts as a code that briefly identifies the reason or area within the facility that generated the message. In our example, the mnemonic is UPDOWN, indicating that the message was generated by an interface state changing to up or down.

The final part is the description, which provides a more detailed explanation of the event that triggered the message. In our example, the facility LINK and the mnemonic UPDOWN indicate that the message relates to a link’s status changing to up or down, and the description Interface FastEthernet0/1, changed state to down gives us the details of what really happened.

7.2.1 Sequence numbers and timestamps
The first two components of a Syslog message—the sequence number and timestamp—are optional. Whether they are present or absent by default can vary depending on the device; in many cases, sequence numbers are not included by default, but timestamps are.

You can enable sequence numbers with the service sequence-numbers command in global config mode. After issuing this command, sequence numbers will be added to any future Syslog messages generated by the device (but not past messages).

Timestamps can be controlled with the service timestamps log command in global config mode. However, this command includes various keywords that allow you to control how timestamps are displayed. The following are two options:

service timestamps log datetime

service timestamps log uptime

With the datetime option configured, Syslog messages will be timestamped with the date and time when the event occurred. With the uptime option, however, Syslog messages will be timestamped with the uptime of the device (the amount of time since the device booted up) when the event occurred. datetime is generally the more useful option of the two, enabling you to identify exactly when events occurred and correlate logs across different devices.

Note You can check a device’s current uptime in the output of show version. For example: SW1 uptime is 15 hours, 14 minutes.

The datetime keyword has some further options that you can configure. For example, with service timestamps log datetime localtime, you can configure the device to timestamp Syslog messages in the local time zone. By default, Syslog messages are timestamped in UTC. In an international network with devices in multiple time zones, this default behavior is generally preferred; it makes correlating logs between devices in different time zones easier. However, you may prefer to have messages timestamped with the local time; the localtime option allows you to do this.

You can also add milliseconds to the timestamps with the service timestamps log datetime msec command; the format of the timestamps will be hh:mm:ss.msec. All of the timestamps shown in this chapter have included milliseconds, but they are optional. If you don’t include the msec option in the command, they will not be displayed.

Note You can combine the localtime and msec options if you want; service timestamps log datetime localtime msec will timestamp Syslog messages using the local time and will also include milliseconds.

7.2.2 Syslog severity levels
Syslog messages are categorized by their severity—how urgent or critical the logged event is. There are eight severity levels, and a lower value indicates a more severe event. In addition to a numerical value, each severity level also has a keyword that you can use when configuring severity levels in Cisco IOS. Figure 7.4 outlines the eight Syslog severity levels. Note that some of the keywords are different from those in the Syslog standard (RFC 5424). For the CCNA exam, remembering the keywords as used in Cisco IOS is more useful.



Figure 7.4 The eight Syslog severity levels. Lower levels are more severe.

Exam Tip Make sure you can identify the severity levels and their keywords for the CCNA exam. You can use a mnemonic such as “Every Awesome Cisco Engineer Will Need Ice Cream Daily,” using the first letter of each level’s keyword.

The first two severity levels (0–1) are reserved for particularly serious events—system crashes, critical hardware failures, and other events that demand immediate attention. The next three severity levels (2–4), described by RFC 5424 as critical, error, and warning conditions, respectively, are used for events that should be addressed but do not necessarily require immediate action. An example is an interface unexpectedly going down, which IOS categorizes at severity level 3 (LINK-3-UPDOWN).

The next two levels (5–6) are usually used for routine operational status messages or notifications of minor changes that don’t typically affect performance or security. For example, a user logging into the CLI is categorized at severity level 5 (SEC_LOGIN-5-LOGIN_SUCCESS), and so is an interface being manually disabled with the shutdown command (LINK-5-CHANGED).

The final severity level (7) is unique; it is reserved for messages that are generated as a result of the debug command, which allows you to track events in detail as they occur. We will cover the debug command in the next section.

You can control the types of events logged to each destination—the console, VTY lines, buffer, and Syslog server—based on their severity levels. For example, to avoid filling up the device’s logging buffer, you may want to only store logs for more severe events in the buffer.

Let’s first look at the default logging configurations for these different destinations. The logging console, logging monitor, logging buffered, and logging trap commands on their own—which are part of the device’s default configuration—enable logging to each destination with the default severity levels. To check these defaults, use show logging:

SW1(config)# logging console                                      ❶
SW1(config)# logging monitor                                      ❶
SW1(config)# logging buffered                                     ❶
SW1(config)# logging trap                                         ❶
SW1(config)# do show logging
. . .
    Console logging: level debugging, 5014 messages               ❷
➥logged, xml disabled, filtering disabled                        ❷
    Monitor logging: level debugging, 1080 messages               ❷
➥logged, xml disabled, filtering disabled                        ❷
    Buffer logging:  level debugging, 4500 messages               ❷
➥logged, xml disabled, filtering disabled                        ❷
. . .
    Trap logging: level informational, 18 message lines logged    ❸
. . .
❶ These commands are already enabled by default.

❷ logging console, logging monitor, and logging buffered enable logging at the debugging level by default.

❸ logging trap enables logging at the informational level by default.

Logging to the console, monitor, and buffer is enabled at level 7 (debugging) by default. This means that events with that severity level or numerically lower (more severe) will be logged; because level 7 is the numerically highest, all events will be logged to the console, monitor, and buffer by default (severity levels 0–7).

However, trap logging (to a Syslog server) is enabled at severity level 6 (informational) by default; this means that events of severity level 6 or lower will be logged to the Syslog server. Level 7 events will not be logged to the server. This choice of default settings minimizes unnecessary network traffic to the Syslog server.

To modify which severity levels are logged to each destination, you can add the optional level argument to the end of each command. Note that for this argument, you can specify either the numerical value or the keyword. For example, logging console 4 and logging console warnings both enable console logging for severity levels 4 and lower (0–4). Table 7.1 summarizes the commands we’ve covered, adding the optional severity argument.

Table 7.1 Syslog config ration commands

| Destination          | Commands                                                                                    |
|----------------------|---------------------------------------------------------------------------------------------|
| Console line         | `Device(config)# logging console [ severity ]`                                              |
| VTY lines (monitor)  | `Device(config)# logging monitor [ severity ]` <br> `Device# terminal monitor`              |
| Logging buffer       | `Device(config)# logging buffered [ bytes ] [ severity ]`                                   |
| Syslog server (trap) | `Device(config)# logging trap [ severity ]` <br> `Device(config)# logging [ host ] ip-address` |



Exam Tip Remember that specifying a certain severity level enables logging for events at that level and all numerically lower (more severe) levels.

7.2.3 The debug command
The debug command allows you to view detailed real-time information about various operations on a Cisco IOS device, including data about network activity, internal processes, and other specific events. You can use this command to troubleshoot difficult problems or learn more about how the device is functioning.

This command includes countless keywords that allow you to specify what kind of information you want to see. For example, debug spanning-tree events can be used to display real-time messages about STP-related events, such as changes in port roles and states. The following example shows some output generated by that command:

SW1# debug spanning-tree events
Spanning Tree event debugging is on
Sep 19 05:38:17.003: STP: VLAN0010 new root port Gi0/1, cost 8
Sep 19 05:38:17.003: STP: VLAN0010 Gi0/1 -> listening
Sep 19 05:38:32.003: STP: VLAN0010 Gi0/1 -> learning
Sep 19 05:38:47.003: STP[10]: Generating TC trap for port GigabitEthernet0/1
Sep 19 05:38:47.004: STP: VLAN0010 sent Topology Change Notice on Gi0/1
Sep 19 05:38:47.005: STP: VLAN0010 Gi0/1 -> forwarding
Note Debug output does not follow the same format as regular Syslog messages.

The debug command is extremely useful for troubleshooting difficult problems, allowing you to get a detailed look at how the device is functioning. Furthermore, it is a great tool for learning. For example, when studying OSPF neighbor relationships, you can use debug ip ospf adj to see how the routers transition through the OSPF neighbor states.

Note Debug messages are processed by the device’s CPU, and debugging can be quite resource intensive. It is recommended that you be very careful about using this command on a live network to avoid overwhelming the device.

Feel free to experiment with the debug command in a lab, but it is beyond the scope of the CCNA exam. You just need to understand its relationship to the Syslog severity levels: debugging-level events will not be logged unless severity level 7 (debugging) is enabled.

Summary
Syslog is a standard for message logging in computers, providing mechanisms to collect information about devices and monitor their health.

Whereas SNMP provides regular polling of quantitative metrics and event-based alerting, Syslog functions like a logbook that records significant (and not so significant) events that occur on a device.

Syslog messages can be displayed in real time to users connected to the CLI of a device and stored locally or on a centralized Syslog server for later review.

Real-time logging to the console line is controlled with the logging console command, which is enabled by default.

Real-time logging to the VTY lines is controlled with the logging monitor command, which is also enabled by default.

A user connected to a VTY line must issue the terminal monitor command in privileged EXEC mode to view real-time messages for that session. The command only applies for the individual session.

The logging synchronous command can be configured in line config mode to make the device automatically reprint the command you are typing on a new line if it gets cut off by a Syslog message.

Cisco devices can store Syslog messages in the logging buffer in RAM. Use show logging to view the messages stored in the logging buffer.

Logging to the buffer is controlled with the logging buffered [bytes] command, which is enabled by default. The optional bytes argument lets you specify the size of the logging buffer.

You can configure a device to send Syslog messages to a central Syslog server. This is especially useful in large networks with many devices to facilitate viewing and correlating their logs.

Logging to a Syslog server is controlled with the logging trap command, which is enabled by default. However, you also must specify the IP address of the Syslog server with logging [host] ip-address.

Standard Syslog uses UDP port 514. However, the more secure version, Syslog over TLS, uses TCP port 6514.

The Syslog message format is seq:timestamp: %facility-severity-mnemonic: description.

The first part is a sequence number that identifies the order of messages, followed by a timestamp that indicates when the message was generated. These two components are optional.

The facility indicates the source of the message within the device—the service, application, or other component that generated the message.

The severity is a numerical value indicating how urgent or critical the message is.

The mnemonic is a short text string that provides a descriptor of the event that triggered the Syslog message.

The description is a more detailed description of the event.

You can control whether sequence numbers are added to Syslog messages with the service sequence-numbers command in global config mode.

You can configure timestamps with service timestamps log [datetime | uptime]. The datetime keyword timestamps log messages with the date and time of the event. The uptime keyword timestamps log messages with the device’s uptime when the event occurred.

The datetime keyword has further options like localtime, which timestamps logs in the device’s local time zone (instead of the default UTC), and msec, which adds milliseconds to the timestamps.

Syslog messages are categorized by their severity—how urgent or critical the logged event is. A lower numerical value is more severe. The eight severity levels and their keywords in IOS are

    0—emergencies
    1—alerts
    2—critical
    3—errors
    4—warnings
    5—notifications
    6—informational
    7—debugging

Console, monitor, and buffer logging are enabled at level 7 (debugging) by default. This means that all events of severity level or numerically lower (all events) will be logged.

Trap logging (to a Syslog server) is enabled at severity level 6 (informational) by default. This means that events of severity level 6 or lower will be logged.

You can control the severity levels that are logged to each destination (console, monitor, buffer, trap) by adding the optional severity argument to each command. You can either specify the severity level’s keyword or numerical value.

For example, logging console 4 and logging console warnings both enable console logging for severity levels 4 and lower (0–4).

The debug command allows you to view detailed real-time information about various operations on a Cisco IOS device, including data about network activity, internal processes, and other specific events.

Debugging-level events will not be logged unless severity level 7 is enabled.