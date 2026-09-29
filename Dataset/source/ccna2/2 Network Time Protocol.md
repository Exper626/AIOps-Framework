2 Network Time Protocol
This chapter covers

The importance of date and time on network devices
Manually setting the date and time on Cisco routers and switches
How NTP enables devices to synchronize their clocks over a network
Configuring and securing NTP on Cisco routers and switches

When you think of the most important functions of a router or switch, keeping accurate date and time information is probably not among the first things that come to mind. However, timekeeping that is accurate and consistent across all devices is critical for a variety of functions and services in a network, from security protocols to logging. So how can we achieve accurate timekeeping on our network devices?

The answer is Network Time Protocol (NTP), the topic of this chapter. Using NTP, devices across a network can synchronize their clocks to a common time source. NTP isn’t limited to just network infrastructure devices like routers and switches; it’s used by all kinds of network-connected devices, including smartphones, PCs, and servers. In this chapter, we’ll cover CCNA exam topic 4.2: Configure and verify NTP operating in a client and server mode.

2.1 Date and time on network devices
Accurate date and time information on network devices is more important than you might expect. In this section, we’ll look at a few reasons why that is. We’ll also cover how to manually configure the date and time on Cisco IOS devices before covering NTP itself in section 2.2.

2.1.1 The importance of date and time
Devices must have accurate date and time information for several reasons. For example, many security protocols (such as Transport Layer Security—TLS) rely on time-based mechanisms to function correctly. From a CCNA perspective, however, the main reason is event logging. When events occur on a network device, the device keeps logs of what happened. Log entries can be created for countless kinds of events, but here are a few examples:

An interface going up or down
An OSPF neighbor moving to the Full state or Down state
A user logging in to the CLI of the device


Each log entry is given a timestamp, indicating when the event occurred. You can use show logging to view the log entries saved on the local device. The following example shows a couple of log entries on a Cisco router:

R1# show logging
. . .
Aug 28 16:34:07.860: %OSPF-5-ADJCHG: Process 1,        ❶
➥Nbr 10.0.0.2 on GigabitEthernet0/0 from LOADING to   ❶
➥FULL, Loading Done                                   ❶
Aug 28 16:35:07.080: %OSPF-5-ADJCHG: Process 1,        ❷
➥Nbr 10.0.0.2 on GigabitEthernet0/0 from FULL to      ❷
➥DOWN, Neighbor Down: Dead timer expired              ❷
❶ An OSPF neighbor entered the Full state.

❷ The same OSPF neighbor entered the Down state due to an expired dead timer.

NOTE We will cover logging in detail in chapter 7, which is about Syslog.

The first log message shows that, at about 16:34, R1’s OSPF relationship with neighbor 10.0.0.6 moved to the Full state. Then, 1 minute later, the neighbor relationship moved to the Down state due to an expired dead timer. One essential step in identifying the cause of such events is correlating log entries between devices. However, in this case, there is a problem. The following example shows the output of show clock, which displays the current date and time, on the two OSPF neighbors (R1 and R2):

R1# show clock
*17:10:17.146 UTC Mon Aug 28 2023      ❶

R2# show clock
*09:49:34.199 UTC Tue Aug 8 2023       ❷
❶ R1 believes it is 17:10 on August 28, 2023.

❷ R2 believes it is 9:49 on August 8, 2023.

NOTE The .146 and .199 after the hours, minutes, and seconds indicate milliseconds.

Because the clocks of the two devices are not synchronized, correlating log entries between them is much more difficult. If the problem involves more than two devices, all with clocks set to different dates and times, you’ll definitely be wishing that you had configured NTP.

2.1.2 Setting the date and time
All Cisco routers and switches have an internal software clock for keeping the time; that’s the clock that you can view with the show clock command. By adding the detail keyword to the end, you can also get information about how the device learned the current date and time, as shown in the following example:

R1# show clock detail
*08:56:18.831 UTC Mon Aug 28 2023      ❶
Time source is hardware calendar       ❷
❶ The asterisk (*) indicates that the time is not authoritative.

❷ R1 learned the date and time from its hardware calendar.

Some devices, like R1 in the example, also have a battery-powered hardware clock called the calendar that keeps the time even if the device is shut off. When R1 booted up, its software clock learned the time from the hardware calendar. However, note the asterisk (*) before the time in the previous example, which means that the time is not authoritative—not considered to be accurate; this will disappear after setting the time.

Setting the clock and calendar

The command to set the software clock is clock set hh:mm:ss month day year. Note that this command is executed from privileged EXEC mode, not global config mode. In the following example, I set R1’s software clock:

R1# clock set 18:30:00 August 28 2023
R1# show clock detail
18:30:03.553 UTC Mon Aug 28 2023       ❶
Time source is user configuration      ❷
❶ The asterisk has disappeared from the output.

❷ The time source has changed to “user configuration.”

NOTE The order of the month and day in the clock set command can be reversed—August 28 and 28 August are both valid.

The hardware calendar can also be viewed and set separately with the show calendar and calendar set commands. In the following example, I set R1’s calendar:

R1# calendar set 18:35:00 August 28 2023
R1# show calendar
18:35:02 UTC Mon Aug 28 2023
However, an easier way to ensure that the software clock and the hardware calendar have the same date and time is to use one of the following commands in privileged EXEC mode:

Sync the calendar to the clock’s time—clock update-calendar.

Sync the clock to the calendar’s time—clock read-calendar.

Note that both commands perform a one-time synchronization; they don’t ensure that the clock and calendar remain in sync (unless you use the command again).

Configuring the time zone

The default time zone on Cisco devices is Coordinated Universal Time (UTC)—you may have noticed the UTC output in previous examples. Actually, UTC is not strictly considered a time zone but rather a time standard—the difference doesn’t matter for our purposes.

The command to change the time zone of the device is clock timezone name hours-offset minutes-offset. Note that this command, unlike the previous commands, is configured in global config mode. The hours-offset and minutes-offset arguments refer to the offset relative to UTC. For example, my time zone (Japan Standard Time) is UTC+9—9 hours and 0 minutes ahead of UTC. I configure that in the following example:

R1(config)# clock timezone JST 9 0      ❶
R1(config)# do show clock
03:50:09.104 JST Tue Aug 29 2023        ❷
❶ The JST time zone is 9 hours and 0 minutes ahead of UTC.

❷ The time zone has changed to JST.

NOTE Changing the time zone will adjust the clock forward or backward according to the specified offsets. If you previously configured the time in UTC, you may have to reconfigure it in the new time zone.

Configuring daylight saving time/summer time

Some countries adjust their clocks forward 1 hour in the spring; this is called daylight saving time (DST) or summer time, depending on the country. They then adjust their clocks back in the fall. In a country that observes DST, you should configure your network devices to adjust their clocks to match.

The command to configure DST is clock summer-time name recurring start-date-time end-date-time in global config mode. Figure 2.1 shows the specifics of the syntax, using the time zone of my hometown (Toronto) as an example (my current home of Japan doesn’t observe DST). Toronto’s time zone is called Eastern Daylight Time (EDT) while DST is in effect, and it begins at 02:00 on the second Sunday of March and ends at 02:00 on the first Sunday of November.



Figure 2.1 The syntax of the clock summer-time command. The example specifies that EDT begins at 02:00 on the second Sunday of March and ends at 02:00 on the first Sunday of November.

2.2 How NTP works
When it comes to ensuring that all devices in a network operate with synchronized, accurate date and time, manual configuration simply doesn’t cut it. Even if you configure the date and time on all devices, their clocks will drift over time, resulting in inaccurate and inconsistent time. NTP is a much more scalable solution that allows devices to automatically sync their clocks over a network.

The devices you use in your daily life, such as a PC or smartphone, are almost certainly NTP clients. Windows PCs, for example, sync their time with Microsoft’s NTP servers by default. Using NTP, NTP clients (i.e., Windows PCs) learn the time from NTP servers (i.e., Microsoft’s NTP servers) by sending NTP requests to UDP port 123—memorize that port!

NOTE NTP allows accuracy of time within 1 millisecond if the NTP server is in the same LAN as the client or within about 10–100 milliseconds if connecting to the server over a WAN or the internet.

NTP uses a hierarchical model. At the top are reference clocks—usually these are very accurate timekeeping devices such as atomic clocks or GPS clocks. The “distance” of an NTP server from a reference clock is called stratum—a server with a lower stratum value is closer to a reference clock, and NTP clients will prefer it over a higher-stratum server. “Closer” doesn’t mean physically closer in this case but closer in the NTP hierarchy.

Figure 2.2 demonstrates the NTP hierarchy. Reference clocks are stratum 0 in the NTP hierarchy, and NTP servers that learn the time directly from a reference clock are stratum 1. Then NTP servers that learn the time from stratum 1 servers are stratum 2, servers that learn the time from stratum 2 servers are stratum 3, etc.



Figure 2.2 The NTP hierarchy. Reference clocks (stratum 0) are high-precision timekeeping devices such as atomic clocks. Stratum 1 NTP servers connect directly and sync to reference clocks. Stratum 2 NTP servers sync to stratum 1 NTP servers. Servers can peer with devices at the same stratum.

NOTE The upper stratum limit is 15. A stratum of 16 indicates a time source that is not considered reliable; devices will not sync to a stratum 16 time source.

Figure 2.2 also demonstrates a few important points about NTP. First, a device can be both an NTP server and an NTP client at the same time. For example, the stratum 2 servers are clients of the stratum 1 servers but are also capable of providing the time for their own clients (such as stratum 3 NTP servers or end devices like PCs). However, note that stratum 1 servers are not NTP clients of the reference clocks; instead, they directly connect to and sync with these highly accurate time sources via specialized hardware and protocols rather than by using NTP.

NOTE An NTP server that gets its time directly from a reference clock is also called a primary server. An NTP server that gets its time from another NTP server is called a secondary server; a secondary server is both an NTP client and an NTP server.

Second, a device can be a client of multiple NTP servers—actually, this is recommended. In addition to the redundancy and fault tolerance benefits of having multiple time sources (if one server goes down, the client can still learn the time from another server), the clients use algorithms to analyze and consider the time reports of each server, discard outliers, and select the best time source.

Third, two NTP servers can form a peer relationship that allows them to exchange time information with each other; these are represented by the bidirectional horizontal arrows. Unlike the typical client–server relationship where the client syncs its time solely based on the time provided by the server, peering allows for a bidirectional exchange between the two peers.

Like a client that learns the time from multiple servers, peering provides similar benefits. Each peer can use the other’s time data as an additional reference point, improving the overall accuracy of timekeeping. Furthermore, peering provides an additional layer of redundancy and fault tolerance; if one peer loses connectivity with its servers, it can still sync to its peer.

2.3 Configuring NTP
Cisco routers and switches can function as NTP clients, NTP servers, and NTP peers. In this section, we’ll examine how to configure all three of these modes in Cisco IOS, as well as how to secure NTP by configuring authentication.

2.3.1 NTP client mode
You can configure a Cisco IOS device to become a client of an NTP server with the command ntp server ip-address [prefer]. In figure 2.3, I configure a Cisco router as an NTP client of two servers: Google’s and Microsoft’s.



Figure 2.3 Configuring R1 as an NTP client of two NTP servers: Google’s (216.239.35.0) and Microsoft’s (20.43.94.199). The optional prefer keyword tells the router to favor Google’s server when deciding which server to sync to.

By adding the optional prefer keyword to the end of the command, you can tell the device to favor the specified server when deciding which server to sync to. Note that this doesn’t guarantee that the client will select that server; other factors, like the server’s stratum, are still taken into account (a lower stratum value is typically preferred). In the following example, I configure R1 as a client of Google’s and Microsoft’s NTP servers and then confirm with show ntp associations and show clock detail:

R1(config)# ntp server 216.239.35.0 prefer                                    ❶
R1(config)# ntp server 20.43.94.199                                           ❶
R1(config)# do show ntp associations
  address       ref clock    st  when  poll reach  delay  offset  disp
*~216.239.35.0  .GOOG.       1   24    64   377 4  0.726  22.840  6.929       ❷
+~20.43.94.199  25.66.230.3  3   25    64   377    9.032  24.786  6.720       ❸
 * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured
R1(config)# do show clock detail
13:44:32.959 JST Tue Aug 29 2023
Time source is NTP                                                            ❹
❶ Configures R1 as an NTP client of two servers, marking one as preferred (optional)

❷ Google’s server is marked as sys.peer.

❸ Microsoft’s server is marked as candidate.

❹ R1’s time source is now NTP.

NOTE NTP synchronization can be quite slow, sometimes taking up to 15–20 minutes, depending on a variety of factors. One tip to speed up the process is to manually configure the correct time before configuring NTP.

After configuring R1’s two NTP servers, both appear in the output of show ntp associations. The * next to the Google server, sys.peer, indicates that this is the NTP server R1 is currently synced to. The + next to the Microsoft server, candidate, indicates that R1 considers the server as a reliable time source, but it is not currently being used; this is because R1 has selected Google’s server instead.

Various columns are shown in the output, but you only need to know the first three: address, ref clock, and st. The address column is self-explanatory; it’s the NTP server’s IP address. ref clock shows the server’s time source. The Google server lists .GOOG.—Google’s own reference clock. The Microsoft server lists 25.66.230.3—another NTP server. So, whereas the Google NTP server in this example gets its time directly from a reference clock (and is, therefore, a primary server), the Microsoft server gets its time from another NTP server (and is, therefore, a secondary server).

The different time sources are reflected in the next column, st; this indicates the NTP stratum of the server. Because Google’s server gets its time directly from a reference clock (stratum 0), its stratum is 1. Microsoft’s server is stratum 3, meaning that it gets its time from a stratum 2 NTP server.

Another useful NTP verification command is show ntp status. This command shows a lot of output; for the CCNA, just focus on the top line. In the following example, I use the command on R1. Notice that because R1 is synced to a stratum 1 NTP server, it is now at stratum 2 in the NTP hierarchy:

R1(config)# do show ntp status
Clock is synchronized, stratum 2, reference is 216.239.35.0        ❶
nominal freq is 1000.0003 Hz, actual freq is 1000.0003 Hz, precision is 2**16
ntp uptime is 7500 (1/100 of seconds), resolution is 1000
reference time is E897F742.5E14162D (13:49:06.367 JST Tue Aug 29 2023)
. . .
❶ R1 is synced to a stratum 1 server and is, therefore, stratum 2.

NOTE NTP syncs only the software clock by default, not the hardware calendar. You can use ntp update-calendar in global config mode to make NTP periodically update the calendar to ensure that it is accurate.

2.3.2 NTP server mode
A Cisco router that is an NTP client doesn’t need any additional configuration to become an NTP server. Now that R1 is a client of the Google and Microsoft NTP servers, other devices can use R1 as their NTP server. Figure 2.4 demonstrates this: R1 gets its time from two NTP servers and provides the time for clients of its own.



Figure 2.4 R1, a client of two NTP servers, is an NTP server for clients of its own.

EXAM TIP Remember that although the ntp server command makes the device an NTP client, it also makes it an NTP server; this is sometimes called client/server mode. Later in this section, we’ll cover how to make the device an NTP server without it being an NTP client.

One recommended practice when using a Cisco router as an NTP server is to configure a loopback interface on the router and configure clients to use the IP address of the loopback interface as their NTP server. We covered loopback interfaces in chapter 18 of volume 1; their benefit is that they provide a stable, reliable interface that isn’t dependent on the status of any particular physical port. Figure 2.5 shows how you can configure this.



Figure 2.5 Using a loopback interface to provide a reliable NTP server address. The ntp source command specifies that R1 should source NTP messages from its Loopback0 interface.

Configuring the IP address of R1’s Loopback0 interface (172.16.1.1) as the NTP server of R2 and R3 causes them to send their NTP requests to that address. If one of R1’s G0/0 or G0/1 ports goes down, R2 and R3 will still be able to sync their clocks to R1 via the loopback interface. The ntp source loopback0 command then makes R1 use the IP address of the Loopback0 interface as the source of its NTP messages—this is optional but recommended. In the following example, I configure NTP on R2 and confirm its status. Note that R2, a client of a stratum 2 server (R1), is now at stratum 3 of the NTP hierarchy:

R2(config)# ntp server 172.16.1.1
R2(config)# do show ntp associations
  address      ref clock      st  when  poll reach  delay  offset   disp
*~172.16.1.1   216.239.35.0   2   15    64   1      1.494  0.695    187.55     ❶
 * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured
R(config)# do show ntp status
Clock is synchronized, stratum 3, reference is 172.16.1.1                      ❷
. . .
❶ R2 is synced to R1.

❷ R2 is now a stratum 3 NTP server.

Although a Cisco router is automatically able to function as an NTP server if it’s a client of another NTP server, you can also use the ntp master command to make the router a primary NTP server with its own internal clock acting as the reference clock—the source of time that the router (and its NTP clients) sync to. This allows the device to act as an NTP server even if it’s not an NTP client of another server.

However, while the ntp master command allows the router to function as an NTP server, it’s not meant to replace the ntp server command. Instead, the two commands should be used together. The ntp server command should be the first choice for time synchronization because it links your device to external NTP servers that get their time from highly accurate reference clocks. But what happens if those external servers become unavailable?

In the example network we’ve been using in this chapter, R1 is an NTP client of two external NTP servers, and R2 and R3 are clients of R1. However, if R1 loses connectivity to both external NTP servers, R1 will no longer be able to provide time to R2 and R3. The ntp master command allows R1 to use its own clock as a backup time source in case it loses connectivity to its servers; it can then provide that time to its clients R2 and R3. Although R1’s internal clock isn’t as accurate as an atomic clock, at least the time will be consistent across the devices in the network—this is better than having no time synchronization at all. In the following example, I use the command on R1 and confirm:

R1(config)# ntp master                                                      ❶
R1(config)# do show ntp associations
  address       ref clock  st  when   poll reach  delay   offset  disp
*~216.239.35.0  .GOOG.     1   22     64   1      43.221  -1.699  437.57
 ~127.127.1.1   .LOCL.     7   15     16   1      0.000   0.000   7937.5    ❷
+~20.43.94.199  25.66.230.5      3     22  64     1  9.397   1.251 437.54
 * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured
❶ Configures R1 to use its own clock as an NTP time source

❷ 127.127.1.1 is added as a time source with stratum 7.

Let’s examine a few important points about that output. First, notice that the address column lists 127.127.1.1—an address in the reserved loopback address range (127.0.0.0/8) that represents the local device; R1 is listing itself as a time source. Then the ref clock column lists .LOCL.—the clock of the local device.

The final point worth covering is 127.127.1.1’s stratum of 7. This means that R1, when using 127.127.1.1 (its local clock) as a time source, will be a stratum 8 NTP server. This is the default value when using the ntp master command and reflects the fact that R1’s internal clock is not a true reference clock like an atomic clock, which would have a stratum of 0. The stratum value of the local clock is purposefully made higher by default so that R1 views it as a less desirable time source than external NTP servers (such as Google’s, which gets its time from a real reference clock). However, you can optionally specify a stratum value at the end of the command. I do that in the following example and confirm:

R1(config)# ntp master 5                                                    ❶
R1(config)# do show ntp associations
  address       ref clock  st   when  poll reach  delay   offset  disp
*~216.239.35.0  .GOOG.     1    45    64   37     40.890  20.622  2.240
 ~127.127.1.1   .LOCL.     4    3     16   1      0.000   0.000   7937.5    ❷
+~20.43.94.199    25.66.230.5   3     169  512     7  8.585  15.092  4.220
❶ Specifies a stratum of 5

❷ The stratum of the local clock is 4.

The output may be a bit different than expected; even though I specified a stratum of 5 in the ntp master command, the stratum of 127.127.1.1 in the output is 4. That’s because the stratum you specify in the command is not the stratum of 127.127.1.1 (the local clock) but rather the stratum of the device when it is synced to that clock. The command ntp master 5 means that R1, when synced to the local clock, will be at stratum 5 of the NTP hierarchy. However, in this case R1 is still synced to the Google server; it will only use its local clock as a backup.

NOTE In addition to providing a backup time source, you can use ntp master to make a Cisco IOS device an NTP server when no external server is available, such as in an isolated network without internet access. This is called server mode, as opposed to the client/server mode we configured with the ntp server command. Just keep in mind that the device’s local clock is not a truly accurate time source—it doesn’t keep time accurately like an atomic clock.

Symmetric active mode

Although not covered in the CCNA exam topics list, in addition to client and server, there is a third mode called symmetric active mode; this is the NTP peering I mentioned in section 2.2. To configure NTP peers in symmetric active mode, use the ntp peer ip-address command on each device, specifying the other device’s IP address. Unlike a client–server relationship, each peer acts as a time source for the other. To summarize, here are the three commands/modes we covered:

ntp server—client/server mode—The device becomes a client of an NTP server and a server for other clients.

ntp master—server mode—The device becomes a primary NTP server, using its local clock as a reference clock.

ntp peer—symmetric active mode—The two devices become NTP peers, each using the other as a time source.

2.3.3 NTP authentication
Public NTP servers like Google’s and Microsoft’s are open; any client is free to sync their time to those servers, and there are no security checks on the part of either the clients or the servers. However, in more secure environments with private NTP servers, that approach may not be acceptable.

For example, a malicious server could exploit NTP to provide incorrect time data, which could disrupt the operation of time-sensitive applications and protocols. In such an environment, we should ensure that our client devices don’t sync to unauthorized NTP servers. In this section, we’ll look at how to protect our NTP clients with authentication.

Authentication is the process of verifying someone’s—or something’s—identity. In the context of NTP, that means verifying that a server really is the server that it claims to be—not an attacker using a spoofed (falsified) IP address. Figure 2.6 shows how to configure NTP authentication between an NTP server (R1) and client (R2).



Figure 2.6 Configuring NTP authentication between a server and client. This ensures that R2 will only sync its time to R1 and not to a malicious NTP server.

Let’s walk through the configuration of both devices. In the following example, I configure the server, R1:

R1(config)# ntp master                                     ❶
R1(config)# ntp authentication-key 42 md5 AcingTheCCNA!    ❷
R1(config)# ntp trusted-key 42                             ❸
❶ Makes R1 an NTP server

❷ Configures an NTP authentication key

❸ Specifies the key as trusted

After using ntp master to make R1 an NTP server, the first step to configuring authentication is to create an authentication key (password) with the ntp authentication-key key-number md5 key command. The key-number argument is simply a numerical identifier for the key; the key argument is the key itself—the actual password.

NOTE Newer versions of IOS support hashing protocols beyond md5, which is no longer considered secure. You can use the IOS context-sensitive help feature (the question mark: ntp authentication-key key-number ?) to view the available protocols on the device you are configuring.

However, creating an authentication key alone is not enough; you then have to use the ntp trusted-key key-number command to specify that the key is a trusted key. Without this command, the key cannot be used.

In the following example, I configure the client, R2:

R2(config)# ntp authentication-key 42 md5 AcingTheCCNA!     ❶
R2(config)# ntp trusted-key 42                              ❷
R2(config)# ntp server 10.0.0.1 key 42                      ❸
❶ Configures an NTP authentication key

❷ Specifies the key as truste

❸ Authenticates R1 using key 42

First, I create the same authentication key as on R1 and also specify it as a trusted key. Here’s an important point: both the key number (42) and the key itself (AcingTheCCNA!) have to match; it’s not enough for just the key itself to match. Then, in the final command, I configure R2 as a client of R1 (10.0.0.1), specifying that R2 should authenticate R1 using key 42. The command syntax is ntp server ip-address key key-number.

The result of this configuration is that R2 will include key 42 in its NTP messages to R1, and R1 will include the same key in its NTP messages to R2. Because the key number and the key itself match, R2 will accept R1’s time and sync to it; if either parameter does not match, R2 will refuse to sync to R1.

NOTE You can use a nearly identical configuration to authenticate NTP peers: just replace ntp server ip-address key key-number with ntp peer ip-address key key-number. Make sure to configure it on both peers!

The ntp authenticate command

You’ll often see the ntp authenticate command included on both the client and the server in NTP authentication configuration examples—this is usually a mistake. Although it’s fine to include this command (it doesn’t do any harm), it’s not necessary when you configure the ntp server ip-address key key-number command on the client.

The ntp authenticate command is necessary to authenticate servers or peers when using the ntp passive, ntp broadcast client, or ntp multicast client commands on the client—all beyond the scope of the CCNA exam. For all of the scenarios presented in this chapter, the ntp authenticate command is not necessary to achieve authentication.

Summary

Keeping an accurate date and time is very important for network infrastructure devices and network-connected devices. For example, many security protocols rely on time-based mechanisms.

Correlating logs between devices is often an essential step in troubleshooting issues, and accurate timestamps facilitate that process.

A device keeps its time using a software clock. You can view it with show clock. Adding the detail keyword shows additional information about the time source.

Some devices also have a hardware clock called the calendar. You can view its time with show calendar.

You can set the software clock with clock set hh:mm:ss month day year.

You can set the hardware calendar with calendar set hh:mm:ss month day year.

The clock update-calendar command syncs the calendar to the clock’s time, and the clock read-calendar syncs the clock to the calendar’s time.

The default time zone is Coordinated Universal Time (UTC). You can change that with clock timezone name hours-offset minutes-offset in global config mode.

You can configure daylight saving time (DST) with clock summer-time name recurring start-date-time end-date-time in global config mode.

Maintaining accurate date and time information is not feasible with manual configuration. Network Time Protocol (NTP) is the solution, allowing devices to automatically sync their time over a network.

NTP clients send NTP requests to UDP port 123 on NTP servers.

NTP uses a hierarchical model. At the top are reference clocks—usually very accurate timekeeping devices such as atomic clocks or GPS clocks.

The “distance” of an NTP server from a reference clock is called its stratum.

An NTP server that learns the time directly from a reference clock is stratum 1—this type of server is called a primary server.

Stratum 2 servers learn the time from stratum 1 servers, stratum 3 servers learn the time from stratum 2 servers, etc. These are called secondary servers—they are NTP clients and NTP servers at the same time.

A device can be a client of multiple NTP servers. This provides improved redundancy and fault tolerance and improves the accuracy of the client’s timekeeping.

Two NTP servers can form a peer relationship that allows them to exchange time information with each other. This provides similar benefits to a client learning the time from multiple servers.

You can configure a Cisco IOS device to be a client of an NTP server with ntp server ip-address [prefer]. The prefer keyword is optional but increases the likelihood that the client will sync its time to the specified server.

The ntp server command puts the device in client/server mode. The device becomes an NTP client of the specified server but can also function as an NTP server for clients of its own.

Use show ntp associations to view information about each of the device’s NTP time sources. Use show ntp status to view information about the device’s NTP status, such as its stratum in the NTP hierarchy.

When a Cisco IOS device is functioning as an NTP server, it is recommended that you configure a loopback interface and specify that address as the client’s NTP server. This provides a stable interface that isn’t dependent on a physical port.

You can use ntp source interface to specify which interface NTP messages should be sourced from.

Use the ntp master [stratum] command to make the device function like an NTP primary server, using its own software clock as a reference clock. This is called server mode, as opposed to client/server mode.

The ntp master command makes the device a stratum 8 NTP server by default, but you can optionally specify the stratum argument to change this behavior.

You can configure symmetric active mode with the ntp peer ip-address command. Configure it on both devices to make them NTP peers.

You can configure NTP authentication to ensure clients only sync to authorized servers. Authentication is the process of verifying someone’s/something’s identity.

On both the client and server, use ntp authentication-key key-number md5 key to create an authentication key. Both the key-number and key arguments must match between the client and server.

On both the client and server, use ntp trusted-key key-number to specify that the key is a trusted key; without this step, the key can’t be used.

On the client, add key key-number to the standard ntp server ip-address command to specify that the server should be authenticated with the key. The complete syntax is ntp server ip-address key key-number.

You can configure authentication between NTP peers by following the same steps, replacing ntp server ip-address key key-number with ntp peer ip-address key key-number. Make sure to configure it on both peers.