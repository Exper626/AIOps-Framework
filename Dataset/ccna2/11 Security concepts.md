11 Security concepts
This chapter covers

Key security concepts and common attacks
User authentication via passwords and alternatives
Controlling and tracking user access with AAA
Securing a network with firewalls and IPS
The most secure network would be a closed system, like a house with no doors or windows. But just like a house with no doors or windows would be uninhabitable, a completely isolated network would be counterproductive. The entire purpose of a network is connectivity—the ability to share, communicate, and access resources both within and outside of its confines.

In the real world, networks need to interact with other networks, applications, and users. But this interconnectivity introduces vulnerabilities from a variety of angles, so security concerns must always be at the forefront of any network design. The CCNA isn’t a cybersecurity certification per se. However, just as networking is an essential skill for nearly any IT professional, the same can be said of security. A system is only as secure as its weakest link, and security is everyone’s responsibility—including those in non-IT roles. In this chapter, we’ll cover a variety of fundamental security concepts. Specifically, we will cover the following CCNA exam topics:

1.1.c Next-generation firewalls and IPS

5.1 Define key security concepts (threats, vulnerabilities, exploits, and mitigation techniques)

5.2 Describe security program elements (user awareness, training, and physical access control)

5.4 Describe security password policy elements, such as management, complexity, and password alternatives (multifactor authentication, certificates, and biometrics)

5.8 Compare authentication, authorization, and accounting concepts

11.1 Key security concepts
What exactly does it mean to say that a network and its connected devices are “secure”? That’s what we’ll explore in this section. We will first delve into the CIA triad, a foundational security framework emphasizing the concepts of confidentiality, integrity, and availability. After covering the principles of the CIA triad, we’ll define and differentiate some vital terms in security, such as vulnerabilities, exploits, and threats.

11.1.1 The CIA triad
The CIA triad (not to be confused with the US Central Intelligence Agency) describes the goals of information security in an organization and stands for

Confidentiality—Systems and data should only be accessible by authorized entities.

Integrity—Systems and data should be trustworthy. For example, data should not be altered during storage or transmission except by authorized entities.

Availability—Systems and data should be accessible and usable by authorized entities when required.

Figure 11.1 shows the three elements of the CIA triad. Note that data refers to the information that is stored, processed, or transmitted, whereas systems refers to the devices, networks, and infrastructure that facilitate the storage, processing, and transmission of this data.



Figure 11.1 The CIA triad. Confidentiality protects systems and data from unauthorized access, integrity ensures that systems and data are trustworthy, and availability ensures that systems and data remain available to authorized users.

Basically, a security program should ensure that systems and data can only be accessed by authorized users, can only be controlled or modified by authorized users, and are available to authorized users when needed. If all three of these elements are ensured, we can say that the systems and data are “secure.” As we cover various security concepts in this chapter (and the rest of this part of the book), always keep the CIA triad in mind. For example, consider how a particular attack harms the confidentiality, integrity, or availability of data and how a particular security solution protects them.

11.1.2 Vulnerabilities, exploits, and threats
No system is perfectly secure. Even a closed system with no network connection to the outside world has vulnerabilities that can be exploited. For example, a malicious user with physical access to the devices is one potential threat.

Exam Tip Exam topic 5.1 specifically mentions “threats, vulnerabilities, exploits, and mitigation techniques,” so make sure you can differentiate between these concepts.

In the previous paragraph, I used three key security terms: vulnerability, exploit, and threat. These terms are related, but each has its own distinct meaning. A vulnerability is any potential weakness that can compromise the security (CIA) of a system or data. Using a house as an analogy, a window is a vulnerability that can potentially be used by an intruder to enter the house.

An exploit is something that can potentially be used to take advantage of a vulnerability. Continuing with the house analogy, a rock that can be used to break a window is an exploit. And a threat is the real possibility of a vulnerability to be exploited; an intruder who intends to use a rock to break a window and enter your house is a threat. Depending on where you live and the likelihood of threats, you may choose to implement a measure like installing metal bars over your house’s windows. This is an example of a mitigation technique—a measure implemented to protect against threats.

Let’s turn away from the house analogy to think of a computer network. Standard network protocols like DHCP contain vulnerabilities that can be exploited using various tools (computer programs). A malicious user who intends to use such tools to harm the CIA of your network is a threat. Fortunately, there are mitigation techniques like DHCP Snooping (the topic of chapter 13) that can be implemented to protect against such threats.

11.2 Common threats
Networks and the devices connected to them face various threats. For example, standard network protocols have vulnerabilities that can be exploited unless appropriate mitigation techniques are in place. To secure a network, it’s essential to “know your enemy”—to know what kinds of threats are out there. In this section, we’ll cover a variety of threats targeting networks and the devices connected to them, as well as threats targeting the humans who use those devices.

11.2.1 Technical threats
In this section, we will cover various types of threats: denial-of-service (DoS), spoofing, reflection, man-in-the-middle, reconnaissance, malware, and password-related attacks. As we go through these threat types and examples of each, consider how they affect one or more aspects of the CIA triad: confidentiality, integrity, and availability.

Denial-of-service attacks

A denial-of-service (DoS) attack is a malicious attempt to disrupt a targeted system, service, or network and render it unusable. Referring to the CIA triad, DoS attacks affect the target’s availability. Figure 11.2 shows an example DoS attack that exploits the TCP three-way handshake by flooding a target with SYN messages; this is called a SYN flood attack.



Figure 11.2 A TCP SYN flood attack—an example of a DoS attack. (1) The target is flooded with SYN messages and (2) replies with SYN-ACK messages. (3) The half-open TCP connections prevent the target from accepting legitimate TCP connections.

After being flooded with SYN messages, the target responds to each SYN message with a SYN-ACK message and adds each connection to its TCP connection table. However, the final ACK message required to complete each TCP connection never comes, resulting in the target’s TCP connection table being full of these “half-open” connections. As a result, legitimate users are unable to access the target server; the server has reached its maximum capacity and cannot accept any more connections.

Note The attack in figure 11.2 is an example of a distributed denial-of-service (DDoS) attack. A botnet—a group of devices infected with malware—is used to attack the target in a distributed manner (instead of attacking from a single device).

Spoofing attacks

A spoofing attack is any attack that involves falsifying a device’s identity (i.e., by using a fake source IP or MAC address). Spoofing is used in a variety of attacks. For example, SYN flood attacks often involve spoofing; the attacker can spoof their source IP address so that the target’s SYN-ACK replies are not sent back to the attacker.

Another example of an attack that involves spoofing is a DHCP exhaustion attack (also known as DHCP starvation). The attacker sends countless DHCP DISCOVER messages using spoofed MAC addresses to exhaust the DHCP server’s address pool, preventing legitimate clients from receiving IP addresses. Figure 11.3 demonstrates DHCP exhaustion.



Figure 11.3 A DHCP exhaustion attack. The attacker sends countless DHCP DISCOVER messages with spoofed MAC addresses, exhausting the target DHCP server’s pool. As a result, legitimate user devices cannot receive IP addresses.

Note DHCP exhaustion is also an example of a DoS attack, making the network unusable for legitimate users because their devices cannot get IP addresses.

Reflection/amplification attacks

In a reflection attack, the attacker sends spoofed requests (using the IP address of the target) to third-party servers (called reflectors in this context). This triggers the servers to send responses to the target, overwhelming it. Reflection attacks can be particularly effective when a small request triggers large amounts of data to be sent in response; this is called an amplification attack. Figure 11.4 shows a reflection/amplification attack.



Figure 11.4 A reflection/amplification attack. The attacker sends spoofed requests to third-party servers (reflectors), triggering asymmetrically large responses that are sent to the target, overwhelming it and resulting in a denial of service.

Note The reflection/amplification attack shown in figure 11.4 is an example of both a DoS attack and a spoofing attack. NTP and DNS are two common protocols used for reflection/amplification attacks because small requests can result in large responses.

Man-in-the-middle attacks

A man-in-the-middle (MITM) attack is an attack in which an attacker secretly intercepts communications between two parties, relaying messages between them. The attacker gains access to the contents of the communications and can even alter them without the communicating parties noticing. One example is ARP poisoning (or ARP spoofing), in which an attacker sends spoofed ARP replies to make communicating hosts send their frames to the attacker instead of directly to each other. Figure 11.5 illustrates ARP poisoning.



Figure 11.5 An ARP poisoning attack. An attacker sends malicious ARP replies to modify the ARP tables of PC1 and R1, allowing it to intercept their communications.

Steps 1 and 2 of figure 11.5 show a legitimate ARP exchange between PC1 and R1. PC1 broadcasts an ARP request to learn the MAC address of 10.0.0.1 (R1), and R1 replies. Through this exchange, PC1 and R1 learn each other’s MAC address. However, in steps 3 and 4, the attacker sends malicious ARP replies to PC1 and R1, overwriting their legitimate ARP table entries with “poisoned” entries that map PC1’s and R1’s IP addresses to the attacker’s MAC address. As a result, the attacker is able to intercept frames sent between PC1 and R1; instead of sending frames to each other’s correct MAC address, PC1 and R1 will send frames to the attacker’s MAC address.

Reconnaissance attacks

A reconnaissance attack isn’t an attack in and of itself but is rather used to gather information about a target that can be used for a future attack. Reconnaissance attacks don’t necessarily use illicit techniques to gather information; a common part of reconnaissance attacks is open-source intelligence (OSINT), which involves collecting and analyzing information that is publicly available. For example, a WHOIS lookup can be used to learn the email addresses, phone numbers, physical addresses, etc. of a domain’s owners.

Note You can go to https://lookup.icann.org/lookup to perform a WHOIS lookup.

Malware

Malware, which stands for malicious software, refers to harmful programs that can “infect” a target computer and then perform malicious actions like encrypting files, enabling unauthorized access, stealing personal data, etc. Here are a few examples of malware:

Virus—A type of malware that attaches itself to a legitimate program or file. When the program or file is executed, the virus is also executed. Viruses can spread to other computers by infecting files that are shared between computers.

Worm—A type of malware that can spread without human intervention. Worms often spread across networks by exploiting vulnerabilities in software.

Trojan horse—A type of malware that disguises itself as legitimate software. Trojan horses are often spread through email attachments or malicious websites.

Backdoor—A type of malware that allows unauthorized users to access an infected computer. Backdoors are often installed by Trojan horses or other types of malware.

Ransomware—A type of malware that encrypts files on an infected computer and demands payment (often in cryptocurrency) to decrypt the files. Ransomware is often spread through email attachments or malicious websites.

A common element of most types of malware is that they rely on human intervention to spread. You should always be careful about what email attachments you open and what websites you visit. If you are unsure, it is always best to err on the side of caution and not open it or visit it.

Password-related attacks

The most common form of user authentication is a username/password combination. Determining a user’s username is usually a simple task for an attacker; it’s often a publicly displayed username or the user’s email address. Therefore, we rely on the strength of the password to provide the necessary security.

Attackers have a few options to learn a user’s password. It can be as simple as guessing or making use of information learned about the target through an OSINT reconnaissance attack (such as the target’s birthday, pets’ names, etc.). Another option is a dictionary attack, in which the attacker uses a program that runs through a “dictionary”—a list of common passwords—to find the target’s password.

A third option is a brute-force attack, in which a program tries every possible combination of letters, numbers, and special characters to find the target’s password. To protect against these methods, it’s essential to use sufficiently strong passwords; the feasibility of brute-force attacks decreases with the length and complexity of the password. In section 11.3, we’ll cover some password-related best practices.

11.2.2 Social engineering
Social engineering is the act of manipulating individuals into divulging confidential information or performing specific actions, typically bypassing traditional security measures. Instead of exploiting software vulnerabilities, social engineering targets the human element of security, which is often the weakest link.

Social engineering attacks

There are various ways to target users; you’ve certainly been the target (but hopefully not the victim) of one or more of these on the internet. One example is phishing—perhaps the most widespread form of social engineering. Attackers send deceptive emails, pretending to be from a trustworthy entity, to trick recipients into clicking malicious links, downloading malware, or providing sensitive information. Your email’s spam folder is likely full of such emails. Here are some additional types of phishing:

Spear phishing—A more targeted form of phishing, often aimed at employees of a certain company

Whaling—Phishing targeted at high-profile individuals, such as the company CEO

Smishing (SMS phishing)—Phishing via SMS text messages

Vishing (voice phishing)—Phishing performed over the phone

Pretexting is another type of social engineering attack in which the attacker creates a fabricated scenario in an attempt to manipulate the target. For example, the attacker might call an employee and say “Hi, this is Jeremy from the IT department. Due to company policy, we need to reset your password. Can you go to this URL, log in, and change your password?”—this is also an example of vishing.

Tailgating (or piggybacking) is a physical method in which an attacker seeks entry into a restricted area by following someone authorized to enter. The attacker exploits the target’s courtesy or distraction—people are likely to hold the door for the attacker, even if entering a restricted area.

All of these attacks exploit various aspects of human social behavior. For example, people tend to comply with requests from figures of authority. We also tend to comply with requests from people we like. If someone does something for us, we naturally want to return the favor. And once committed to a certain choice or action, people are more likely to follow through—it’s hard to back out. Furthermore, many social engineering attacks also play on creating a sense of urgency to make targets act without thinking.

Social engineering as an exploit

Social engineering is often a precursor or facilitator to the technical threats we covered in section 11.2.1, acting as a “human exploit.” For example, an attacker might use phishing to deceive a user into downloading malware; the user is a vulnerability that the attacker exploits with social engineering to enable the malware threat.

Security program elements

Exam Tip Exam topic 5.2 mentions “security program elements (user awareness, training, and physical access control),” so remember these concepts!

To defend against social engineering, it’s essential to raise awareness and provide training so individuals can recognize and respond appropriately to deceptive tactics. The CCNA exam topics list three essential elements of a security program: user awareness, user training, and physical access control.

User awareness programs are not formal training but are designed to make employees aware of potential security threats and risks. For example, a company might send out false phishing emails to trick employees into clicking a link and signing in with their login credentials. Although the emails themselves are harmless, employees who fall for the false emails will be informed that it is part of a user awareness program and that they should be more cautious about phishing emails and other deceptive tactics. Regular reminders like this keep security at the forefront of employees’ minds, which is crucial; as I mentioned at the beginning of this chapter, security is everyone’s responsibility.

User training programs are more formal educational programs that are usually mandatory for some or all employees (depending on the topic). Examples are dedicated training sessions educating users on corporate security policies or how to avoid potential threats (such as social engineering attacks).

Physical access control protects systems and data from potential threats by only allowing authorized users into areas such as network closets or data center floors. For example, badge readers can be installed to only allow authorized users to open a door.

Unlike a traditional key, badges are flexible, and user permissions can easily be changed. For example, permissions can be removed when an employee leaves the company. However, for particularly sensitive areas, locks requiring multifactor authentication (such as a badge scan and a fingerprint scan) are preferred—more on that in the next section. Security cameras—monitoring the actions of employees and guests on the premises—are another example of physical access control.

11.3 Passwords and alternatives
Passwords—secret strings of characters—are an essential tool for user authentication; only the legitimate user(s) of an account should know the password. In this section, we will cover some best practices related to passwords (including some Cisco IOS-specific best practices), as well as some alternatives that can provide more robust means of authentication.

Exam Tip These topics are exam topic 5.4: Describe security password policy elements, such as management, complexity, and password alternatives (multifactor authentication, certificates, and biometrics).

11.3.1 Password-related best practices
When using a password as a means of user authentication, it’s important that the password is strong, meaning that it’s resilient to the password-related attacks we covered in section 11.2. Here are a few best practices regarding passwords:

Length—Use at least 15 characters (although length recommendations vary).

Complexity—Include upper- and lowercase letters, numbers, and special symbols (#, @, !, ?, etc.).

Unique—Don’t use the same password for multiple accounts.

Hard to guess—Don’t use common words or personal information about you that is publicly available (that an OSINT reconnaissance attack could reveal).

It is often recommended that users be required to change their passwords regularly. However, there is a growing trend against this for a few reasons. First, there is no particular benefit to changing a password that hasn’t been compromised (if the current password is already strong). Second, requiring users to regularly change passwords tends to lead to weaker passwords; users will often reuse passwords from other accounts. Instead, it’s recommended to change passwords only in certain circumstances, such as after a data breach (in which case the password may have been compromised) or if you discover malware on your device.

Password managers

A password manager is a software tool that users can use to store and manage passwords. One popular example is Bitwarden, but most modern web browsers have their own built-in password managers too. These days, using a password manager is generally considered a best practice for a variety of reasons. Here are a few:

Length and complexity—Users can generate and store long, complex, and unique passwords for each account, without having to remember each password.

Auto-fill—The password manager can automatically fill in usernames/passwords without requiring any keystrokes from the user. This can prevent passwords from being learned by keylogger malware that reads and logs keystrokes.

Encrypted storage—Password managers encrypt stored passwords, so even if a device is compromised, the passwords in the manager are protected.

Password managers also often support multifactor authentication for additional security—more on that in section 11.3.2.

Cisco IOS password hashing

It’s crucial that a password remains secret; if it loses its secrecy, it no longer serves as a valid means of authenticating a user’s identity. To that end, it’s crucial to protect passwords “at rest”; do not store passwords as cleartext (unencrypted text). Instead, passwords should be stored as hashes. A hash function converts an input (a password, in this case) into a fixed-length string—a hash—that cannot be reverted to the original input. Hash functions are one-way (irreversible).

In this section, we will cover some best practices regarding the storage of passwords on Cisco IOS devices. We will focus on the enable password and enable secret commands, but the same concepts apply to the passwords of user accounts created with the username command.

For review, you can use enable password password to configure an enable password that is stored in cleartext; Cisco calls this a type 0 password—not acceptable from a security standpoint. You can use the service password-encryption command to make the device encrypt the enable password (and other passwords) with a weak form of reversible encryption; Cisco calls this a type 7 password. Type 7 passwords are also unacceptable, as they can easily be decrypted with free online tools.

Note Hashing and encryption are often confused. Whereas hashing is irreversible, encryption is reversible.

Instead of enable password, you should always use the enable secret command, which stores the configured password as a secure hash using one of multiple supported hashing algorithms; the algorithms supported depend on the device model and IOS version. If you simply configure enable secret password, without specifying the hash algorithm, the device will use its default hash algorithm, which for many years was MD5 (type 5) but is now scrypt (type 9) in modern devices.

To configure the enable secret and hash it with a particular algorithm, use the enable algorithm-type algorithm secret password command. Here are a few options that can be used for the algorithm argument:

md5 (type 5)

sha256 (type 8)

scrypt (type 9)

Note The US National Security Agency (NSA) has released a set of recommendations regarding Cisco IOS passwords and how to configure them. You can read it at https://mng.bz/9dyl. The NSA recommends type 8, but type 9 (Cisco’s recommendation) is also considered very strong.

The enable secret will be saved in the running-config file as enable secret type hash, with the algorithm type being indicated by its number. The following example demonstrates this; note how the enable secret appears differently in the running-config than the command used to configure it:

SW1(config)# enable algorithm-type scrypt secret CiscoCCNA                    ❶
SW1(config)# do show running-config | include enable
enable secret 9 $9$h.p1X8KVxbaILq$pNEykQjoAJbKCYfmBL9Hq8yPU/EqDGpoBkCIZ.s9GJA ❷
❶ Configures an enable secret and hashes it with the scrypt algorithm

❷ The enable secret is saved as a hash, with the algorithm type indicated before the hash.

Then, if you want to configure the same enable secret on another device, you can simply copy and paste the command as it appears in the running-config; the enable secret type hash command allows you to configure an already-hashed enable secret without having to retype the cleartext password.

Note The equivalent commands for configuring a user account are username username algorithm-type algorithm secret password to create a user account and hash its password with the specified algorithm, and username username secret type hash to create a user account with an already-hashed password.

11.3.2 Multifactor authentication
No matter how strong a password is, it remains a potential vulnerability. If a malicious actor learns an account’s password, they can access the account. Instead of simple username/password authentication, multifactor authentication is becoming increasingly prevalent as a more secure option.

Multifactor authentication (MFA) is the process of verifying a user’s identity by requiring multiple forms of authentication before granting access—usually two, in which case it can also be called two-factor authentication (2FA). The goal is to enhance security by ensuring that even if one authentication factor is compromised (i.e., an attacker learns your password), unauthorized access is still prevented by the need for additional factors. The “factors” of MFA are usually categorized into three main types:

Knowledge—Something you know

Passwords or PINs

Security questions and answers

Possession—Something you have

An ID badge

A smartphone receiving SMS codes or push notifications

An app like Google Authenticator that generates one-time codes. To obtain the code, you need access to the specific device where the app is installed.

Inherence—Something you are

Biometrics such as a facial, palm, fingerprint, or retinal scan

To truly be considered MFA, factors from different categories must be used. Requiring a password and a PIN is not considered true MFA because both are something you know. An example of true MFA is requiring a user to touch their badge to a badge reader (something you have) and scan their fingerprint (something you are) to enter a restricted area. Another example is logging in with a username/password and receiving an SMS code on your phone; the username/password combination is something you know, and the SMS code, although a password-like code, is dependent on something you have—your smartphone.

11.3.3 Digital certificates
Digital certificates are a key form of authentication, predominantly used by websites. Most modern websites use digital certificates to prove their identity—to prove that the website you are visiting is who it says it is and not a fake website designed to imitate a legitimate website.

When you connect to a website, your browser will check the site’s digital certificate, verifying its authenticity with a trusted Certificate Authority (CA)—an organization that issues and verifies digital certificates. You can think of CAs as the “passport offices” for digital certificates. If everything checks out, your connection proceeds securely using HyperText Transfer Protocol Secure (HTTPS)—the encrypted and secure version of HTTP. If not, you’ll typically receive a warning alerting you to potential risks. In Google Chrome, a website with a valid digital certificate will display a padlock next to the URL (see figure 11.6).



Figure 11.6 Digital certificates are used to verify the authenticity of websites. In Chrome, a padlock next to the URL indicates a secure connection via HTTPS. Clicking on it shows more details, such as information about the certificate.

Digital certificates are an essential part of the modern internet. They help to ensure that users are able to connect to websites securely and that they are not being redirected to fake websites and also play an essential role in enabling secure, encrypted communications via HTTPS.

11.4 User access control with AAA
Authentication, authorization, and accounting (AAA, pronounced “triple-A”) is a framework for controlling user access in a network. AAA divides user access control into three components: verifying users’ identities (authentication), granting appropriate access (authorization), and recording user activities (accounting). In this section, we’ll cover these three components of AAA and two network protocols that use this framework.

Exam Tip AAA is CCNA exam topic 5.8: Compare authentication, authorization, and accounting concepts. Make sure you know the differences between them!

11.4.1 AAA components
The AAA framework consists of three components: authentication, authorization, and accounting. Let’s break down these three components:

Authentication—This is the process of verifying the identity of a user or system. It answers the question “Who are you?” Ideally, this is performed using MFA.

Authorization—Once authenticated, the next step is to grant the user or device appropriate access. Authorization answers the question “What are you allowed to do?” This could include which files the user is allowed to read or modify, which services the user can access, which Cisco IOS commands they can use, etc.

Accounting—This is the process of keeping track of user activities. Accounting answers the question “What did you do?” Every action a user takes can be logged, from opening or editing a file to making configuration changes to a device. This is crucial for audits, troubleshooting, and understanding user behavior.

By integrating these three components, AAA ensures controlled, secure, and transparent user access to networks and the resources they make available.

11.4.2 AAA protocols
Implementing AAA in a network involves a centralized AAA server that controls user authentication, authorization, and accounting. From this server, you can control user accounts and credentials, what each user is authorized to do, and keep account of each user’s activities. Cisco’s AAA server solution is called Identity Services Engine (ISE).

AAA is typically implemented using one of two protocols: Remote Authentication Dial-In User Service (RADIUS) or Terminal Access Controller Access-Control System Plus (TACACS+)—I’m not sure if there’s a connection between AAA protocols and overly wordy names. Cisco network devices (and ISE) support both protocols. RADIUS and TACACS+ both serve the purpose of providing AAA functionality to control user access, but there are differences between them. Table 11.1 compares RADIUS and TACACS+.

Table 11.1 RADIUS and TACACS+

| RADIUS                                              | TACACS+                                  |
|-----------------------------------------------------|------------------------------------------|
| Open standard                                       | Created by Cisco but now open standard   |
| Combines authentication and authorization into a single operation | Keeps all three AAA components separate |
| UDP ports 1812 and 1813                             | TCP port 49                              |
| Encrypts passwords only                             | Encrypts all communications              |
| Typically used for network access                   | Typically used for device administration |

Both protocols are open standards that have been implemented by various vendors, although TACACS+ was originally developed by Cisco. Let’s take a look at some of the differences between the two as listed in table 11.1.

One major difference is that whereas TACACS+ keeps all three AAA components separate, RADIUS combines authentication and authorization into a single operation (called the Access Request). Because TACACS+ keeps all three components as separate operations, it often provides more granular control. Figure 11.7 demonstrates this difference between RADIUS and TACACS+. A user connects to the CLI of a router, and the router uses RADIUS (left) and TACACS+ (right) to control the user’s access to the router.



Figure 11.7 A simplified look at RADIUS and TACACS+ communications. Whereas RADIUS combines authentication and authorization into a single operation, TACACS+ keeps them separate.

RADIUS and TACACS+ also differ in the Layer 4 protocols they use. RADIUS uses UDP, and the RADIUS server listens on ports 1812 (for authentication/authorization) and 1813 (for accounting). TACACS+, on the other hand, uses TCP as its Layer 4 protocol, and the TACACS+ server listens on TCP port 49 for all messages.

Whereas TACACS+ encrypts the contents of all messages between the client and server, RADIUS only encrypts the password in the Access Request message. The rest of the Access Request message’s content, and the contents of other RADIUS messages, are sent in cleartext.

Although the more robust features of TACACS+ may make it seem the superior choice for an AAA protocol, both are used in different scenarios. TACACS+ is typically used to control device administration, such as an admin configuring a router or switch. TACACS+ provides granular control over which commands a user can use; this can be configured on a per-user or per-group basis (with users assigned to different groups).

RADIUS, on the other hand, is typically used to control network access. This is largely due to the simplicity and efficiency of RADIUS compared to TACACS+, especially when such granular control is not necessary. In the next section, we’ll take a look at 802.1X, an example of how RADIUS can be used to control network access.

Exam Tip The details of RADIUS and TACACS+ are beyond the scope of the CCNA exam, but I recommend knowing their basic characteristics. Refer to table 11.1 for a summary.

11.4.3 IEEE 802.1X
802.1X (usually pronounced “dot one X”) is a standard created by the IEEE for port-based network access control (PNAC). Basically, it’s a way to secure each port on a switch, allowing only authorized devices to connect to the network. Without 802.1X, a device connected to a switch port can immediately send a DHCP request, lease an IP address, and begin communicating over the network; 802.1X changes that.

When a device first connects to a port secured by 802.1X, the port remains locked until the user successfully authenticates. The only traffic that is allowed is 802.1X authentication traffic, as shown in figure 11.8.



Figure 11.8 An 802.1X-secured port only allows 802.1X traffic until the user has authenticated.

The 802.1X authentication process involves three devices, as shown in figure 11.9:

Supplicant—The client device that wants to connect to the network

Authenticator—The network device that the supplicant connects to

Authentication server—The server that verifies the supplicant’s credentials (usually a RADIUS server)



Figure 11.9 802.1X port-based network access control. The authenticator (SW1) only allows the supplicant (PC1) to access the network after PC1 authenticates with the authentication server (SRV1).

802.1X uses a framework called Extensible Authentication Protocol (EAP) for the authentication process, which defines various authentication methods and message formats. However, RADIUS is usually employed as the protocol for checking the credentials provided by the supplicant. We will take a closer look at 802.1X and EAP’s various authentication methods in chapter 20; 802.1X, paired with RADIUS, is used for both wired and wireless access control.

11.5 Firewalls and IPS
The CCNA exam focuses primarily on configuring Cisco routers and switches. However, the type of network device most synonymous with network security is the firewall. Although firewall configuration is beyond the scope of the CCNA exam, you are expected to have a basic understanding of how firewalls work.

Exam Tip These topics are CCNA exam topic 1.1.c: Next-generation firewalls and IPS.

11.5.1 Stateful packet filtering
Routers and switches both have various security features. For example, routers can use ACLs to control which types of traffic are permitted and denied. In fact, ACLs applied to a router’s interfaces are a form of stateless firewall. They examine each packet on a per-packet basis and decide to permit or deny it, without considering other context, such as the packet’s relation to other packets (i.e., whether this packet is a reply to a previously permitted packet).

Most modern firewalls are stateful firewalls; they don’t just consider individual packets with no other context but also each packet’s relationship to other packets. For example, a stateful firewall might block all internet traffic from entering the internal network—generally a good idea, given the public nature of the internet. However, if a host in the internal network initiates communication with a host on the internet (i.e., google.com’s web server), the firewall will allow the reply traffic from the internet host.

Figure 11.10 demonstrates stateful packet filtering as done by a firewall and also introduces the concept of zones. In addition to considering information like source/destination ports and IP addresses, firewalls consider how packets move between these zones when determining whether to permit or deny them.

If a host in the Inside zone initiates communication with a host in the Outside zone, the firewall will permit the reply traffic. However, if a host in the Outside zone attempts to initiate communication with a host in the Inside zone, the firewall will block it. Stateless firewalls (like ACLs on a router) are not able to consider the context of packets like this; each packet is considered independently.



Figure 11.10 Simple firewall rules. Hosts in the Inside zone can initiate communications with hosts in the Outside zone, but hosts in the Outside zone cannot initiate communications with hosts in the Inside zone.

Note Figure 11.10 doesn’t show a router. Most firewalls have their own routing capabilities. Depending on the size and requirements of the network, the firewall’s routing capabilities may be sufficient, or you may need a separate router.

Figure 11.10 shows two zones, but firewalls can have many different zones, with different policies controlling communication between hosts in each zone. For example, it’s common to have a zone called the demilitarized zone (DMZ). Servers that need to be reachable from the public internet are placed here so that they can be accessed without compromising the security of hosts in the Inside zone, as shown in figure 11.11.



Figure 11.11 Servers that need to accept connections from the internet can be placed in the DMZ without compromising the security of hosts in the Inside zone.

11.5.2 Next-generation firewalls
Next-generation firewall (NGFW) is a bit of marketing lingo that has become the standard terminology for a type of firewall that goes beyond the functionalities of traditional firewalls. While the core remains stateful packet filtering, an NGFW incorporates several advanced security features.

One of those advanced features is Application Visibility and Control (AVC). AVC means that the firewall can not only identify traffic based on information like source and destination addresses and ports but can also examine the actual contents of packets to identify the application (similar to NBAR, as we covered in chapter 10).

Cisco NGFWs can also integrate with their anti-malware offering, Advanced Malware Protection (AMP). This allows the firewall to inspect files to identify and protect against all types of malware, such as those we covered in section 11.2.

Another common feature of an NGFW is Intrusion Prevention System (IPS) functionality. Historically, an IPS was a separate hardware device. However, in modern networks, the IPS feature is typically integrated within an NGFW. This integration simplifies and streamlines the implementation and management of the IPS.

An IPS inspects network traffic for malicious or suspicious activities. Once detected, the IPS takes predefined actions, such as blocking the traffic. Instead of operating based on user-configured rules, an IPS downloads attack “signatures”—identifiable patterns of data that can be used to detect malicious activity—from the vendor (i.e., Cisco). An IPS is also capable of building a picture of typical network activity and looking for anomalies that don’t match up with that baseline. The following are some threats that an IPS can protect against:

DoS and DDoS

Malware such as viruses, worms, Trojan horses, and ransomware

Reconnaissance attacks

SQL injections

Cisco calls their IPS offering a next-generation IPS (NGIPS). In addition to traditional IPS functionality (i.e., signature-based threat detection), Cisco’s NGIPS includes features such as

Contextual awareness—The NGIPS gathers contextual information about the applications, device types, operating systems, users, etc. The NGIPS uses these details to better understand the actual activity on the network.

Talos integration—Talos is a security research company that’s a part of Cisco. The threat intelligence gathered by Talos includes attack signatures and known bad actors (known malicious IP addresses, websites, etc.).

Application Visibility and Control (AVC)—Like Cisco’s NGFW, the NGIPS can also examine the contents of packets to identify the application.

Exam Tip Listing the various features of Cisco’s security products can sound like a marketing pitch. You don’t have to be able to list all of these features for the CCNA exam. Just understand that an NGFW includes additional features like IPS and anti-malware functionality on top of stateful packet filtering.

Exam scenarios

Here are a couple of questions that illustrate how your understanding of these security concepts might be tested on the CCNA exam:

1. (multiple-choice, single-answer)

Which of the following commands can be used to configure an enable secret that has been pre-hashed with the scrypt algorithm?

A. enable algorithm-type scrypt secret hash

B. enable algorithm-type 8 secret hash

C. enable secret 9 hash

D. enable secret 5 hash

The key to answering this question is knowing the difference between configuring and hashing the enable secret with enable algorithm-type algorithm secret password and configuring an already-hashed enable secret with enable secret type hash. This question is asking for the latter, so C) is the correct answer. D) is incorrect because it specifies type 5, which is MD5 (not scrypt).

2. (drag-and-drop)

Drag each authentication method on the left to the appropriate factor type on the right.

(A) Entering a username and password

Something you know

(B) Scanning your fingerprint

Something you have

(C) Entering a one-time password generated by a phone app

Something you are

(D) Automated voice recognition

(E) Answering a security question

(F) Scanning an ID badge

Here are the correct answers:

Something you know: (A) and (E)

Something you have: (C) and (F)

Something you are: (B) and (D)

MFA is widely employed in modern systems to make the authentication process more secure. For the CCNA exam, make sure that you can identify which authentication methods fall into each category: knowledge (something you know), possession (something you have), and inherence (something you are).

Summary
The CIA triad describes the goals of information security: confidentiality (prevent unauthorized access), integrity (prevent unauthorized alteration), and availability (ensure resources are accessible by authorized entities when required).

Attacks target one or more components of the CIA triad.

A vulnerability is any potential weakness that can compromise the CIA of a system or data.

An exploit is something that can potentially be used to take advantage of a vulnerability.

A threat is the real possibility of a vulnerability to be exploited, such as an attacker who wants to exploit the vulnerability.

A mitigation technique is a measure implemented to protect against threats.

A denial-of-service (DoS) attack is a malicious attempt to disrupt a targeted system, service, or network and render it unusable. An example is a SYN flood attack, in which an attacker floods the target with TCP SYN messages.

A distributed denial-of-service (DDoS) attack is a DoS attack performed from a group of devices infected with malware, called a botnet.

A spoofing attack is any attack that involves falsifying a device’s identity, such as by using a fake source IP or MAC address.

An example of a spoofing attack is a DHCP exhaustion (or DHCP starvation) attack, in which the attacker sends countless DHCP DISCOVER messages to exhaust a DHCP server’s address pool.

In a reflection attack, the attacker sends spoofed requests (using the IP address of the target) to third-party servers (called reflectors). This triggers the servers to send responses to the target. The goal result is a DoS.

Reflection attacks can be particularly effective when small requests trigger asymmetrically large responses. This is called an amplification attack. NTP and DNS are commonly used for reflection/amplification attacks.

A man-in-the-middle (MITM) attack is an attack in which an attacker secretly intercepts communications between two parties, gaining access to their contents and even altering them without the two parties noticing.

ARP poisoning (or ARP spoofing), in which an attacker sends spoofed ARP replies, is an example of an MITM attack.

A reconnaissance attack is used to gather information about a target that can be used for a future attack. Reconnaissance attacks often employ open-source intelligence (OSINT), which involves gathering publicly available information.

Malware (malicious software) refers to harmful programs that can infect a target computer and then perform malicious actions. Common types of malware include viruses, worms, Trojan horses, backdoors, and ransomware.

A few different attacks can be used to learn a target’s password. A dictionary attack uses a program that runs through a list of common passwords. A brute-force attack tries every possible combination of letters, numbers, and special characters.

Social engineering is the act of manipulating individuals into divulging confidential information or performing specific actions.

Common social engineering attacks include phishing, spear phishing, whaling, smishing, vishing, pretexting, and tailgating/piggybacking.

To defend against social engineering attacks, it’s essential to raise awareness and provide training so individuals can recognize them and respond appropriately.

User awareness programs are not formal training but are designed to make employees aware of potential security threats (i.e., false phishing emails).

User training programs are more formal educational programs that educate users on corporate security policies, how to avoid potential threats, etc.

Physical access control protects systems and data from potential threats by only allowing authorized users into restricted areas (i.e., with badge readers).

Passwords are an essential authentication tool. A password should be of sufficient length (15+ characters) and complexity (upper- and lowercase letters, numbers, and symbols), and be unique (only used for one account) and hard to guess.

A password manager is software that stores and manages passwords. It allows users to store strong passwords without having to remember each one. It can also protect against keylogger malware by auto-filling in passwords.

Cisco IOS passwords should be stored as secure hashes. Use enable algorithm-type algorithm secret password to configure an enable secret with a specific hashing algorithm.

Type 5 (md5) was the default hash algorithm for many years, but modern Cisco devices use type 9 (scrypt). The NSA recommends type 8 (sha256).

Multifactor authentication (MFA), or two-factor authentication (2FA), is the process of authenticating a user with multiple forms (factors) of authentication.

There are three main categories of factors: knowledge (something you know), possession (something you have), and inherence (something you are). MFA must use factors from different categories.

A digital certificate is a form of authentication predominantly used by websites. Digital certificates are issued and verified by a Certificate Authority (CA).

AAA is a framework for controlling user access in a network. AAA divides access control into authentication (verifying users’ identities), authorization (granting appropriate access), and accounting (recording user activities).

Cisco’s AAA server solution is Identity Services Engine (ISE).

Remote Authentication Dial-In User Service (RADIUS) and Terminal Access Controller Access-Control System Plus (TACACS+) are the main AAA protocols.

RADIUS combines authentication and authorization into a single operation (Access Request), but TACACS+ keeps all three separate.

RADIUS uses UDP ports 1812 and 1813, and TACACS+ uses TCP port 49.

RADIUS encrypts only passwords, but TACACS+ encrypts the entire contents of all messages.

RADIUS is typically used for network access (i.e., clients connecting to a wired or wireless LAN), and TACACS+ is typically used for device administration.

802.1X is a standard for port-based network access control (PNAC). Instead of a device being immediately allowed to access the network after connecting to a switch port, the device must authenticate first.

802.1X defines three components: the supplicant (the client device that wants to connect), the authenticator (the network device that the client connects to), and the authentication server (the server that verifies the supplicant’s credentials).

802.1X uses a framework called Extensible Authentication Protocol, which defines authentication methods and message formats. RADIUS is usually employed for checking the supplicant’s credentials.

ACLs applied to a router’s interfaces are a form of stateless firewall, meaning they examine each packet independently of context (like its relation to other packets).

Modern firewalls are stateful firewalls, meaning they can consider the packet’s relationship to other packets. For example, traffic from the internet to the internal network might be blocked except if it’s in reply to a host in the internal network.

Firewalls use the concept of zones to differentiate between areas of the network, such as Inside, Outside, and the demilitarized zone (DMZ). Policies can be configured to control how traffic is allowed to flow between zones.

A next-generation firewall (NGFW) incorporates several advanced security features beyond stateful packet filtering, such as Application Visibility and Control (AVC), Advanced Malware Protection (AMP), and Intrusion Prevention System (IPS).

Historically, an IPS was a separate hardware device, but it is typically integrated within an NGFW in modern networks.

An IPS inspects network traffic for malicious or suspicious activities using attack signatures that it downloads from the vendor (as opposed to configured policies). An IPS can protect against DoS/DDoS attacks, malware, and much more.