8 Trivial File Transfer Protocol and File Transfer Protocol
This chapter covers

Sending files across a network with Trivial File Transfer Protocol and File Transfer Protocol Cisco IOS file systems
Upgrading Cisco IOS software
A file serves as a digital container in a computer, designed to store a variety of data ranging from text and images to audio, video, and software applications. Files can be of any size, from a few bytes to hundreds of gigabytes or more. Transferring files from one computer to another has been one of the primary functions of networks since their beginning. Over time, this has led to the development of various protocols dedicated to facilitating file transfers over a network.

Trivial File Transfer Protocol (TFTP) and File Transfer Protocol (FTP) are two such protocols that have been widely used for this purpose and still are. While TFTP is a simple protocol that is often used to transfer small files in a controlled environment, FTP offers a robust set of features for secure and versatile file transfers. These two protocols are CCNA exam topic 4.9: Describe the capabilities and functions of TFTP/FTP in the network.

TFTP and FTP can both be used to transfer any kind of file over a network, but we’ll focus on one use case that is relevant for anyone working with Cisco routers and switches: transferring IOS files from a file server to upgrade the operating system of a device.

8.1 Trivial File Transfer Protocol
Trivial File Transfer Protocol (TFTP) is a protocol used for transferring files over a network. TFTP uses a client–server model, in which one device (i.e., a PC) acts as the client and another (i.e., a file server) acts as the server. It is “trivial” because it is a relatively simple protocol with few features; the client can transfer files to and from the server, but that’s about it.

TFTP doesn’t use any kind of authentication; a TFTP server will respond to all client requests—no username/password needed. Furthermore, TFTP communications are unencrypted, so all data is sent in plaintext. For these reasons, it would not be wise to use TFTP to send important files over a public network like the internet; TFTP does not provide sufficient security.

However, to transfer files within a controlled environment like a LAN, TFTP is often selected for its simplicity and ease of use. Figure 8.1 shows an example use case for TFTP: an admin uses HTTPS to securely download a Cisco IOS image from Cisco’s website and then uses TFTP to transfer the image to a network device. In this case, the network device (SW1) is a TFTP client, and the admin’s PC is a TFTP server.

Note An IOS image is a complete copy of the Cisco IOS software that is run on a Cisco router or switch.



Figure 8.1 Transferring an IOS image to a network device with TFTP. (1) Download the IOS image from Cisco’s website via HTTPS. (2) Transfer the image to the network device via TFTP.

Note Instead of transferring the file directly from the admin’s PC to the network device, another common setup is to store IOS images in a central file server, from which network devices can use TFTP to download the appropriate image.

8.1.1 How TFTP works
A TFTP file transfer is initiated by a client sending either a read request or a write request to a TFTP server. The purpose of a read request is to request to download a file from the server, and the purpose of a write request is to request to upload a file to the server. For this chapter, we’ll focus on read requests, but keep in mind that TFTP supports both functions.

TFTP servers listen for requests on UDP port 69 (memorize that port for the exam). Given the characteristics of TCP and UDP that we covered in chapter 22 of volume 1, this may be unexpected; when transferring files, you want to make sure that the entire file arrives intact, with all of its bytes in the correct order. TCP’s reliability and sequencing features make it the usual Layer 4 protocol of choice for transferring files.

However, I also mentioned in chapter 22 of volume 1 that UDP may be preferred when reliability is provided via other means; this is the case with TFTP. TFTP uses lock-step communication, meaning that the client and server alternately send a message and then wait for a reply. When a TFTP server transfers a file to a client, it divides the file into ordered blocks. After sending one block, the server won’t send another block until it has received an acknowledgment message from the client. Each block must be acknowledged, and messages are retransmitted if needed. Figure 8.2 demonstrates this process.



Figure 8.2 TFTP lock-step communication. The client and server alternate between sending and waiting to receive messages. The server divides the requested file into ordered blocks, and the client acknowledges receipt of each block. Lost messages result in retransmissions.

After either device (the client or server) sends a message, it sets a timer. If the timer expires, it retransmits its previous message. Using figure 8.2’s example, after SW1 acknowledges block 1, it sets a timer. Although the TFTP server receives SW1’s acknowledgment and sends block 2, it is lost in transit. As a result, SW1’s timer expires, and it retransmits block 1’s acknowledgment. Upon receiving the retransmitted acknowledgment for block 1, the server understands that block 2 did not make it to the client. The server then retransmits block 2.

The TFTP Transfer ID

Although TFTP servers listen for requests on UDP port 69, that only applies to the initial read or write request. After receiving the initial request, the server allocates a new port number in the ephemeral range (49152–65535) to identify that specific session; this port is called the Transfer ID (TID). For the remainder of the communication between the server and client, the server will listen on and source messages from the TID port, not port 69. However, for the CCNA exam, just remember that TFTP = UDP port 69.

To summarize, although TFTP uses UDP, which doesn’t offer sequencing and reliability features, the TFTP protocol itself uses lock-step communication to provide both sequencing and reliability. It’s not as sophisticated as TCP’s features, but it’s sufficient to allow TFTP to use the lightweight UDP as its Layer 4 protocol.

8.1.2 Transferring files with TFTP
Now that you have a basic understanding of how TFTP works, in this section let’s take a look at how to use TFTP to transfer a file from a TFTP server to a Cisco IOS device. Specifically, we will copy a Cisco IOS image to our device to upgrade the device to a newer version of IOS; we’ll cover the actual upgrade process in section 8.3.

The Cisco IOS file system

To transfer files to and from Cisco IOS devices, you need a basic understanding of the Cisco IOS file system—the hierarchical structure that IOS uses to store, manage, and organize various types of files, such as configuration files, IOS images, and log files. These files can then be easily accessed and manipulated by both applications and users.

While we commonly refer to “the IOS file system” in a general sense, it’s important to note that this term encompasses multiple file systems. These are designed to manage different physical storage locations, such as flash memory, NVRAM (non-volatile RAM), and even remote storage like TFTP or FTP servers. Each of these storage options has its own unique file system. You can view the various file systems with the show file systems command. The following example shows some partial output:

Switch# show file systems 
File Systems:
       Size(b)       Free(b)      Type  Flags  Prefixes
             -             -    opaque     rw   system:      ❶
             -             -    opaque     rw   tmpsys:
     249872384     235347968      disk     rw   crashinfo:
*   1624104960    1126379520      disk     rw   flash:       ❷
    2024710144    1911066624      disk     ro   webui:
             -             -    opaque     rw   null:
             -             -    opaque     ro   tar:
             -             -   network     rw   tftp:        ❸
       2097152       2085006     nvram     rw   nvram:       ❹
             -             -    opaque     wo   syslog:
. . .
❶ system:, where the running-config is stored, uses the opaque type.

❷ flash: uses the disk type; the asterisk indicates that this is the default file system.

❸ tftp: uses the network type.

❹ The device’s non-volatile RAM (nvram:) has its own type: nvram.

There are a few different types of file systems in that output that you should know:

Opaque—Logical file systems used for internal functions

NVRAM—Used for the device’s NVRAM (where the startup-config file is saved)

Disk—Physical storage devices (like flash memory)

Network—Used to access external file systems over a network (i.e., TFTP servers)

Let’s look at these four types and some examples of each. Opaque file systems are logical file systems used for the device’s internal functions. For example, system: is where the device’s running-config file is stored; the configuration commands in this file determine how the device actually functions. You can view the contents of a file system with the dir command, as in the following example:

Switch# dir system:
Directory of system:/
    2  -r--                0                    <no date>  default-running-config
    4  dr-x                0                    <no date>  memory
    1  -rw-             5369                    <no date>  running-config     ❶
. . .
❶ The running-config file is stored in system.

Previously, we used the show running-config command to view this file; this command is basically a shortcut, providing a simple method to view the device’s configuration without needing to know the actual location of the file. Alternatively, you can use the more command, which allows you to view the contents of a file, and then specify the system:running-config file path, as in the following example. The output is the same as show running-config:

Switch# more system:running-config
!
! Last configuration change at 09:30:41 JST Thu Sep 21 2023
!
version 16.6
. . .
The NVRAM file system type is only used for one file system: nvram:. Although it stores other files, this file system is best known for storing the startup-config file that the device loads when booting up. In the following example, I use dir nvram: to confirm the contents of the file system, and then more nvram:startup-config to view the startup-config file; this is equivalent to using the show startup-config command:

Switch# dir nvram:
Directory of nvram:/
 2049  -rw-        5449               <no date>  startup-config     ❶
 2050  ----        3573               <no date>  private-config
. . .
Switch# more nvram:startup-config                                    ❷
!
! Last configuration change at 14:43:55 JST Sat Sep 16 2023 by jeremy
! NVRAM config last updated at 14:43:55 JST Sat Sep 16 2023 by jeremy
!
version 16.6
. . .
❶ The startup-config file is stored in nvram:.

❷ Views the contents of nvram:startup-config

The Disk file system type is used for physical storage devices. One example is flash:, which is the default file system—the primary location where the operating system looks for files during various operations unless another file system is specified. This is the location we’ll copy files to with TFTP. If a USB flash drive is inserted, it typically uses the Disk file system type as well.

The Network file system type is used to access remote file systems over a network, such as TFTP servers; the tftp: file system is an example. Likewise, there is also an ftp: file system. When specifying a network file system in a command, you also have to specify the IP address of the target host—these file systems don’t reside on the local device.

Transferring files with the copy command

To transfer files to and from a TFTP server, use the copy source destination command—this creates a copy of the specified source file at the specified destination. My Cisco Catalyst 2960 switch in my home network is not running Cisco’s recommended software version, so in this section, let’s transfer a newer IOS image from a TFTP server (my PC) to my switch (SW1), and then we’ll do the upgrade itself in section 8.3. The following example shows the contents of the flash: file system on my switch:

SW1# show flash:
Directory of flash:/
   3  -rwx       10152  Mar 30 2011 10:28:53 +09:00  vlan.dat
   4  -rwx        2974  Sep 20 2023 15:32:05 +09:00  config.text
   5  -rwx        3096  Sep 20 2023 15:32:06 +09:00  multiple-fs
   6  -rwx    15208832  Sep 20 2023 13:46:38 +09:00 
➥c2960c405-universalk9-mz.150-2.SE5.bin                                 ❶
 610  -rwx        5058  Sep 20 2023 15:32:06 +09:00  private-config.text
❶ The IOS image that my switch currently uses

I have downloaded a newer IOS image from software.cisco.com and set up my PC as a TFTP server. Figure 8.3 shows how my switch will copy the new image from my PC.



Figure 8.3 Copying an IOS image from a TFTP server to a Cisco switch. (1) Copy the file with the copy tftp: flash: command. (2) The switch sends a read request for the file. (3) The file is transferred to the switch. (4) The file has been copied.

Note You need a valid service contract with Cisco to download and use IOS software; this isn’t something you need to worry about for the CCNA exam.

In the following example, I use the copy tftp: flash: command on my switch, telling it that I would like to copy a file from a TFTP server to the flash: file system:

SW1# copy tftp: flash:
Address or name of remote host []? 192.168.1.224                            ❶
Source filename []? C2960c405-universalk9-mz.152-7.E7.bin                   ❷
Destination filename [c2960c405-universalk9-mz.152-7.E7.bin]?               ❸
Accessing tftp://192.168.1.224/c2960c405-universalk9-mz.152-7.E7.bin...
Loading c2960c405-universalk9-mz.152-7.E7.bin from 192.168.1.224 (via Vlan1): !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[OK – 18179072 bytes]                                                       ❹
18179072 bytes copied in 200.831 secs (90519 bytes/sec)                     ❹
❶ Specifies the IP address of the TFTP server

❷ Specifies the name of the file on the TFTP server

❸ Specifies the name to save the file as on the local device

❹ The file was successfully copied

Note Setting up a TFTP server is beyond the scope of the CCNA exam.

After issuing the copy tftp: flash: command, I am shown a series of prompts. The first prompt asks for the IP address (or name, if DNS is available) of the TFTP server; I specify my PC’s IP address of 192.168.1.224. I am then prompted for the source filename—the name of the file that I want to copy from the TFTP server. I specify c2960c405-universalk9-mz.152-7.E7.bin—the IOS image I want to copy to my switch.

Note TFTP does not allow you to view the files on the TFTP server; you must know the name of the file you want to download in advance.

The final prompt is for the destination filename—the name that the file will be saved as on the local device (my switch). By default, the destination filename will be the same as the source filename (as indicated by the value in square brackets); simply pressing Enter at this prompt accepts the default. You can optionally specify a different name, but IOS image names include information about the image type and IOS version, so they’re best left as is.

Note To skip the prompts for the TFTP server’s address etc., you can specify them in the command itself. The syntax is copy tftp://server-ip/src-filename flash:/dst-filename.

The new IOS image has now been transferred to my switch. The following example shows the new image, as well as the image the switch is currently using, in flash::

SW1# show flash:
Directory of flash:/
   2  -rwx    18179072  Sep 21 2023 10:40:22 +09:00 
➥c2960c405-universalk9-mz.152-7.E7.bin               ❶
. . .
   6  -rwx    15208832  Sep 20 2023 13:46:38 +09:00 
➥c2960c405-universalk9-mz.150-2.SE5.bin              ❷
. . .
❶ The newly copied image

❷ The currently used image

8.2 File Transfer Protocol
Of the two protocols we are covering in this chapter, FTP is the older one, first standardized in 1971. However, FTP is more robust, providing a variety of features that TFTP does not. For example, FTP requires authentication with a username/password, providing greater security than TFTP. However, FTP does not encrypt data; files are transferred as plaintext. For even more security, you can use an encrypted protocol like FTP Secure (FTPS). However, for the purpose of the CCNA exam, we will focus on FTP itself, not its related encrypted protocols.

Encrypted file transfers

Ideally, file transfers should be encrypted for maximum security, especially over a public network like the internet. Here are a couple of options:

File Transfer Protocol Secure (FTPS) uses Transport Layer Security (TLS) to secure FTP communications between the server and client.

SSH File Transfer Protocol (SFTP) is an extension of SSH that enables it to perform encrypted file transfers. Despite the name, this protocol isn’t actually related to FTP.

8.2.1 How FTP works
Unlike TFTP, FTP uses TCP as its Layer 4 protocol. This means that, whereas a TFTP exchange begins with the client immediately sending a request to the server, an FTP exchange must begin by establishing a TCP connection—the TCP three-way handshake. However, transferring files with FTP requires two TCP connections, not one. Figure 8.4 outlines the process.



Figure 8.4 An FTP exchange involves two TCP connections: an FTP control connection, and an FTP data connection.

Step 1 in figure 8.4 shows the initial TCP connection establishment. This is a standard TCP three-way handshake: SYN (client to server), SYN-ACK (server to client), and ACK (client to server). Once this three-way handshake is done, the client and server have established the FTP control connection—step 2 in figure 8.4. Through this connection, the server will first authenticate the client by checking its username and password. If the authentication succeeds, the client can then send FTP commands to the server; it is through these commands that the client can tell the server what it wants to do.

Exam Tip FTP servers listen for control connections on TCP port 21; memorize that port!

Unlike TFTP, in which a client can only copy files to or from the server, FTP has a variety of commands to support functions like listing the available files and directories, navigating through directories, renaming and deleting files, and various others. In our example, SW1 needs to download a file from the server. SW1 will send a RETR (retrieve) command to get a copy of a specific file; this is equivalent to a TFTP read request.

However, the actual data exchange does not take place over the FTP control connection. Instead, a second TCP connection is established—step 3 in figure 8.4. This second three-way handshake establishes the FTP data connection, which is step 4 in figure 8.4. It is over this connection that the server transfers the file to the client. One advantage of having separate control and data connections is that FTP can support multiple data transfers simultaneously; with a single control connection, the client can establish multiple data connections with the server.

Exam Tip TCP port 20 is reserved for FTP data connections, but modern FTP servers often use an ephemeral port instead—the port that will be used for the data connection is conveyed through the control connection. However, for the CCNA exam, memorize these ports: FTP control = TCP 21, FTP data = TCP 20.

FTP active and passive modes

Although the FTP client initiates the control connection (by sending the first TCP SYN to port 21 on the FTP server), the data connection can be initiated by either the client or the server. In the original FTP standard, it was the server that initiated the data connection; this is called active mode (the server is the “active” one).

However, active mode caused problems as firewalls and Network Address Translation (NAT—next chapter’s topic) became common, as they could block the incoming data connection from the server to the client. This led to the development of passive mode, in which the client initiates the data connection (the server is “passive”), solving the problems with active mode. A Cisco IOS device will use passive mode by default when acting as an FTP client; it does this by sending a PASV command to the server.

8.2.2 Transferring files with FTP
Transferring files with FTP is largely the same as with TFTP but with the addition of username/password authentication. For this section, we will once again look at how to transfer an IOS image from an FTP server (my PC) to a Cisco IOS device (a switch in my home network)—I erased the one we transferred previously with TFTP (the command to do so is delete file). In the following example, I use show flash: to confirm the contents of my switch’s flash drive:

SW1# show flash:
Directory of flash:/
   3  -rwx       10152  Mar 30 2011 10:28:53 +09:00  vlan.dat
   4  -rwx        2974  Sep 20 2023 15:32:05 +09:00  config.text
   5  -rwx        3096  Sep 20 2023 15:32:06 +09:00  multiple-fs
   6  -rwx    15208832  Sep 20 2023 13:46:38 +09:00
   ➥c2960c405-universalk9-mz.150-2.SE5.bin                              ❶
 610  -rwx        5058  Sep 20 2023 15:32:06 +09:00  private-config.text
❶ The IOS image that my switch currently uses

To transfer a file with FTP, we can use the same command as with TFTP: copy source destination, using ftp: instead of tftp: for the source argument. However, as the following example shows, this doesn’t work initially:

SW1# copy ftp: flash:                    
Address or name of remote host []? 192.168.1.224
Source filename []? c2960c405-universalk9-mz.152-7.E7.bin
Destination filename [c2960c405-universalk9-mz.152-7.E7.bin]?
Accessing ftp://192.168.1.224/c2960c405-universalk9-mz.152-7.E7.bin...
%Error opening ftp://192.168.1.224/c2960c405-
➥universalk9-mz.152-7.E7.bin (Incorrect Login/Password)     ❶
❶ The connection fails due to incorrect credentials.

FTP requires username/password authentication, so we first have to configure an FTP username and password on SW1 with the ip ftp username username and ip ftp password password commands; of course, these must match a user account on the FTP server. In the following example, I use these commands on SW1:

SW1(config)# ip ftp username jeremy
SW1(config)# ip ftp password password123
Note This probably goes without saying, but you should never use a password like “password123.” We will cover password best practices in chapter 11.

With these credentials configured, SW1 is able to authenticate to the server and retrieve the file, as shown in the following example:

SW1# copy ftp: flash:
Address or name of remote host [192.168.1.224]? 
Source filename []? c2960c405-universalk9-mz.152-7.E7.bin
Destination filename [c2960c405-universalk9-mz.152-7.E7.bin]?
Accessing ftp://192.168.1.224/c2960c405-universalk9-mz.152-7.E7.bin...
Loading c2960c405-universalk9-mz.152-7.E7.bin
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[OK - 18179072/4096 bytes]
18179072 bytes copied in 157.933 secs (115106 bytes/sec)
The credentials specified in the ip ftp username and ip ftp password commands are the device’s default FTP credentials—the credentials that will be used if none are specified in the command. To specify the credentials in the command, the syntax is copy ftp://username:password@server-ip flash:; for example, copy ftp://jeremy:password123@192.168.1.224 flash:.

After the file transfer is complete, I once again use show flash: to confirm that the new IOS image is in SW1’s flash drive. In the next section, we’ll configure SW1 to load that new image instead of its current one after its next reboot:

SW1# show flash:
Directory of flash:/
   2  -rwx    18179072  Sep 21 2023 21:18:13 +09:00 
➥c2960c405-universalk9-mz.152-7.E7.bin               ❶
. . .
   6  -rwx    15208832  Sep 20 2023 13:46:38 +09:00 
➥c2960c405-universalk9-mz.150-2.SE5.bin              ❷
. . .
❶ The newly copied image

❷ The currently used image

8.3 Upgrading Cisco IOS
After transferring a new IOS image to a device, configuring the device to use that new image requires just one configuration command, followed by a system reboot. Regardless of whether you use TFTP, FTP, or another method to transfer the new image to the device, the upgrade process is identical. However, before we do that, let’s pause to consider the purpose of upgrading to a new version of IOS in the first place. Here are a few reasons:

Security—New releases often include fixes for security vulnerabilities that have been discovered in previous releases. By keeping your devices up to date, you can protect your network from known security threats.

Bug fixes—New releases often include bug fixes for issues such as memory leaks, crashes, and performance problems that can negatively affect your network.

New features and functionality—New releases often include new features and functionality not present in previous versions, offering more configuration options and networking solutions.

Cisco support—Cisco routinely ends support for older versions, making it challenging to get technical assistance for any issues that may occur.

Security is undoubtedly the most important reason to upgrade to a new version of Cisco IOS. The version of IOS currently running on my switch has 48 security advisories associated with it, 4 of which are marked as “critical”—this would not be acceptable in an enterprise network. To check the current version of IOS running on a device, use the show version command, as in the following example:

SW1# show version 
Cisco IOS Software, C2960C Software (C2960c405-
➥UNIVERSALK9-M), Version 15.0(2)SE5, RELEASE SOFTWARE (fc1)     ❶
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2013 by Cisco Systems, Inc.
. . .
❶ The current version is 15.0(2)SE5.

Note To check the latest and recommended versions of IOS available for a particular device, go to software.cisco.com (a Cisco account is required) and search for the device model. From there, you will also be able to find links to release notes, security advisories, etc.

To make the device boot with a different image, use the boot system image-path command in global config mode. I do so in the following example and confirm before and after with the show boot command, which lists various boot settings:

SW1(config)# do show boot                                            ❶
BOOT path-list      : flash:/c2960c405-universalk9-mz.150-2.SE5.bin  ❷
Config file         : flash:/config.text
. . .
SW1(config)# boot system flash:/c2960c405-universalk9-mz.152-7.E7.bin ❸ 
SW1(config)# do show boot
BOOT path-list      : flash:/c2960c405-universalk9-mz.152-7.E7.bin   ❹
Config file         : flash:/config.text
. . .
❶ Confirms SW1’s boot settings

❷ SW1 is configured to boot with the 150-2.SE5.bin image.

❸ Configures SW1 to boot with the new image

❹ SW1 will boot with the 152-7.E7.bin image next time.

The second show boot command indicates that SW1 will load the new image the next time it boots, so now we just have to save the configuration (very important!) and reboot the device with the reload command, as in the following example:

SW1# write memory                 ❶
Building configuration...
[OK]
SW1# reload                       ❷
Proceed with reload? [confirm]    ❸
❶ Saves SW1’s configuration

❷ Reloads SW1

❸ Press Enter to confirm.

Note Make sure to save the configuration with write, write memory, or copy running-config startup-config before rebooting, or the boot system command will not take effect upon reboot.

If you are connected to the device remotely via Telnet or SSH, you will lose connectivity while the device reboots—you won’t be able to see the CLI. However, if you are connected via the console port, the device will display its boot sequence in real time. You’ll be able to observe the device as it goes through its POST (Power-On Self-Test), loads the specified IOS image, and finally brings you back to the CLI once it has successfully rebooted. This can be particularly useful for troubleshooting issues or verifying that the device is booting correctly. In the following example, I use the show version command once again to verify that SW1 is using the new image:

SW1# show version 
Cisco IOS Software, C2960C Software (C2960c405-
➥UNIVERSALK9-M), Version 15.2(7)E7, RELEASE SOFTWARE (fc10)     ❶
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2022 by Cisco Systems, Inc.
. . .
❶ SW1 is now using version 15.2(7)E7.

After the upgrade is complete, you can delete the old IOS image with the delete command, for example, delete flash:/c2960c405-universalk9-mz.150-2.SE5.bin. However, it’s important to verify that the device is functioning properly and there are no network issues before doing so; if any issues arise, you may have to “roll back” to the previous IOS version.

IOS upgrade best practices

You should not carelessly upgrade a device to a newer IOS version. Here are a few best practices to ensure a successful upgrade:

Back up your configuration before upgrading. This will allow you to restore it if something goes wrong.

Read the release notes for the new IOS version carefully and ensure you understand the changes.

Test the new IOS version in a lab before deploying it in a live network to identify any potential problems.

Have a plan in place for rolling back to the previous IOS version if necessary.

Summary

A file is a digital container for data such as text, images, audio, video, and software.

Transferring files between computers is one of the primary functions of networks.

Trivial File Transfer Protocol (TFTP) is a protocol used for transferring files over a network. It is relatively simple, allowing a client to transfer files to and from a server without additional features.

TFTP doesn’t use authentication and encryption, so it is recommended that you only use it to transfer files within a controlled environment like a LAN.

A TFTP file transfer is initiated by a client sending either a read request to download a file from a server or a write request to upload a file to a server.

TFTP servers listen for requests on UDP port 69. Although UDP doesn’t provide the reliability and sequencing features desirable when transferring protocols, the TFTP protocol itself provides these features.

TFTP uses lock-step communication, in which the client and server alternately send a message and then wait for a reply. Files are divided into ordered blocks, and each block must be acknowledged by the receiver before the next one is sent.

If a device doesn’t receive a reply to one of its messages after a certain period of time, it will retransmit the message.

Cisco IOS uses a variety of file systems to store, manage, and organize files. Use show file systems to view them.

The opaque file system type indicates logical file systems used for internal functions. For example, the system: file system that stores the running-config.

The disk type is used for physical storage devices, like the flash file system, which is the default file system.

The network type is used to access external file systems over a network, for example, the tftp: file system is used to access remote TFTP servers.

The nvram type is used for the device’s NVRAM, where the startup-config is stored.

Use the dir command to view the contents of a particular file system. To view the flash: file system, you can also use show flash:.

Use the more command to view the contents of a particular file.

To transfer files to and from a TFTP server, use copy source destination, which creates a copy of the specified source file at the specified destination.

You can specify the full file path of the source and/or destination in the copy command: copy tftp://server-ip/src-filename flash:/dst-filename.

File Transfer Protocol (FTP) serves the same purpose as TFTP but is more robust, providing a variety of features that TFTP does not.

FTP requires username/password authentication. However, it does not encrypt data; files are transferred as plaintext.

Protocols like File Transfer Protocol Secure (FTPS) and SSH File Transfer Protocol (SFTP) can be used for encrypted file transfers.

FTP uses TCP as its Layer 4 protocol. FTP exchanges require two TCP connections: one for the FTP control connection and one for the FTP data connection.

Using the FTP control connection, the server authenticates the client, and the client sends FTP commands to the server. For example, the RETR (retrieve) command is used to retrieve a copy of a specific file on the server, like a TFTP read request.

FTP servers listen for FTP control connections on TCP port 21.

The client and server establish a separate FTP data connection for the actual file exchange. TCP port 20 is reserved for FTP data connections, but modern FTP servers often use an ephemeral port instead. For the CCNA, remember TCP port 20.

Transferring files from an FTP server requires a username and password. Use ip ftp username username and ip ftp password password to configure a Cisco IOS device’s default FTP username and password.

Alternatively, you can specify a username and password in the copy command. The syntax is copy ftp://username:password@server-ip flash:.

Regardless of whether you use TFTP, FTP, or another method to transfer a new IOS image to a device, the upgrade process is identical.

There are various reasons to upgrade a device’s IOS software. A few main reasons are security, bug fixes, new features and functionality, and Cisco support.

Security is the most important reason to upgrade to a new version of IOS. If a particular version has known security vulnerabilities, running it is a risk.

Use show version to confirm the current version of IOS running on a device.

Use show boot to view the device’s boot settings, such as which IOS image it will load the next time it boots up.

Use boot system image-path to specify the IOS image the device should load the next time it boots up. Remember to save the configuration.

Use reload to reboot the device. If connected via Telnet or SSH, you will lose connectivity during reboot. If connected via the console port, you’ll be able to observe the device as it boots up.