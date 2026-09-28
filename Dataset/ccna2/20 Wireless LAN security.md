20 Wireless LAN security
This chapter covers

Applying the CIA triad to wireless communications
Authenticating wireless LAN clients before allowing them to communicate
Maintaining the confidentiality and integrity of communications in a wireless LAN
The WPA, WPA2, and WPA3 security certification programs
Imagine that you are in a room full of people. You have to communicate a private message to your friend on the other side of the room, but all you can do is shout at the top of your lungs. Basically, that’s how communication in a wireless LAN works. Security is a major concern in all networks, but the unbounded nature of the medium means that securing communications in wireless LANs is even more critical.

In this chapter, we will take a high-level overview of wireless LAN security concerns and solutions, covering CCNA exam topic 5.9: Describe wireless security protocols (WPA, WPA2, and WPA3). WPA stands for Wi-Fi Protected Access—a set of security certification programs developed by the Wi-Fi Alliance. To earn “Wi-Fi Certified” status, devices must comply with WPA’s standards. We will first examine the various elements of wireless LAN security and then see how they all fit together in WPA, WPA2, and WPA3.

20.1 Wireless LAN security concepts
Although wireless LANs introduce unique challenges, the fundamental security concepts we covered in chapter 11 still apply. In this section, we’ll consider how the CIA triad applies to wireless LANs and examine the security measures implemented in the original 802.11 standard (before the creation of WPA).

20.1.1 The CIA triad in wireless LANs
For review, the CIA triad describes the goals of information security and stands for

Confidentiality—Data and systems should only be accessible by authorized entities.

Integrity—Data and systems should be trustworthy. For example, data should not be altered during storage or transmission except by authorized entities.

Availability—Data and systems should be accessible and usable by authorized entities when required.

Let’s examine each of these goals in the context of wireless LANs. The unbounded nature of wireless LANs makes ensuring the CIA of communications an even greater challenge.

Confidentiality

Confidentiality in a wired LAN is largely ensured by the physical characteristics of the medium: the signals are contained within the cables, reducing (although not eliminating) the risk of unauthorized access to communications. Confidentiality is primarily a concern when communicating over public networks like the internet.

However, wireless signals can be picked up by any receiver within range of the transmitter, making it essential to protect information as it travels through the air, even within a private LAN. Figure 20.1 illustrates why encryption of wireless communications is important: a user’s unencrypted login information is overheard by an attacker.



Figure 20.1 Unencrypted communications in a wireless LAN are not secure, as wireless signals can be picked up by nearby devices, allowing malicious users to gain access to confidential information.

To maintain the confidentiality of communications in a wireless LAN, encryption of wireless signals is essential. Encrypting a message converts it into an unintelligible string of text that can only be restored by the intended recipient. Later in this chapter, we will take a look at some encryption methods used in wireless LANs.

Note Unencrypted information (that will not be encrypted) is called cleartext. Unencrypted information that will be encrypted (but has not yet been fed into the encryption algorithm) is plaintext, and encrypted information is called ciphertext.

Integrity

Even if a message is encrypted, preventing an attacker from reading its contents, that is no guarantee that the data will not be altered by a malicious user. A bit-flipping attack is an attack in which the attacker flips bits (between 0 and 1) in the ciphertext to create predictable changes in the plaintext—even without decrypting the ciphertext.

To protect the integrity of a message before sending it over the air, the sender uses a mathematical function to generate a checksum—a small block of data derived from the original message. This checksum is appended to the end of the plaintext message before encrypting and sending it.

Upon receiving the encrypted message, the receiver decrypts it and then calculates its own checksum from the decrypted message. If the newly calculated checksum matches the one sent with the message, the receiver can conclude that the message hasn’t been altered. If they don’t match, the receiver discards the message. Figure 20.2 demonstrates this process.



Figure 20.2 Appending a checksum to the end of a message before encrypting and sending it helps to protect the integrity of wireless communications.

Note It’s worth noting that checksums don’t prevent data from being tampered with; they only enable a device to identify when data has been tampered with.

Availability

Attacks against the availability of a wireless LAN—denial of service (DoS) attacks—are quite simple to carry out by any malicious user with the proper tools. For example, in an RF jamming attack, the attacker uses a signal generator to flood the 802.11 frequency bands, preventing legitimate devices from communicating.

An RF jamming attack doesn’t require sophisticated hacking skills or deep knowledge of the network, making it an easy choice for a malicious user looking to disrupt the network. Furthermore, preventing such attacks can be challenging; the only solution to an RF jamming attack is to locate and disable/remove the device that is performing the attack. And the only preventative measure is physical security—ensuring that only authorized users have access to the physical premises.

Note Due to the simplicity of wireless DoS attacks, we won’t address them any further in this chapter. Instead, we’ll focus on protecting the confidentiality and integrity of wireless communications.

20.1.2 Legacy 802.11 security
The original 802.11 standard defined a security protocol called Wired Equivalent Privacy (WEP). As the name suggests, WEP promised to provide privacy to wireless communications equivalent to that of wired communications. Unfortunately, it failed to live up to that promise; various vulnerabilities were soon identified, and WEP is now obsolete—it is a legacy protocol. However, studying the basics of WEP is crucial for understanding the evolution of wireless security protocols.

WEP Open System and Shared Key Authentication

The definitions I gave for confidentiality, integrity, and availability all mention “authorized entities”—data should only be accessible to and modified by authorized entities and should remain available to those entities. To authorize an entity (a user or device), you must verify that entity’s identity—as we covered in chapter 11, the verification process is called authentication. WEP defined two methods of authentication: Open System Authentication and Shared Key Authentication.

We already saw an example of Open System Authentication in chapter 19 when covering the association process: the client device sends an authentication request, and the AP sends an authentication response. No credentials are exchanged; the AP simply approves all authentication requests unless there’s a problem with the request itself (i.e., invalid formatting)—no questions asked! This verifies that the client and AP are both valid 802.11 devices, but I think it goes without saying that this is not a secure authentication method.

Shared Key Authentication involves the configuration of a static WEP key on the AP and each client—basically, this is the Wi-Fi password. To verify that a client has the correct WEP key, the following process, illustrated in figure 20.3, is used:

The client sends an authentication request.

The AP sends an authentication response with an unencrypted challenge phrase.

The client uses the WEP key to encrypt the challenge phrase.

The client sends the ciphertext challenge phrase back to the AP.

The AP uses the WEP key to decrypt the challenge phrase.

The AP compares the original challenge phrase to the one it just decrypted.

If the decrypted text matches the original phrase, the AP sends back a response indicating successful authentication (or unsuccessful, if the text doesn’t match).



Figure 20.3 WEP Shared Key Authentication involves exchanging a challenge phrase and encrypting/decrypting it with a shared WEP key.

Note Diagrams in this chapter omit the probe request/probe response exchange (or beacon messages when using passive discovery) that we covered in chapter 19, but keep in mind that this exchange occurs before any authentication/association processes; the client must discover the AP before it can authenticate.

A static WEP key can be either 40 bits or 104 bits in length. Furthermore, the device generates a random 24-bit number called an initialization vector (IV) that is combined with the WEP key. A new IV is generated for each packet; this adds some randomness to the encryption process, making it harder for an attacker to figure out the encryption key.

Note As we covered in chapter 19, after the client successfully authenticates (via Open System or Shared Key Authentication), it can send an association request to associate with the AP and start communicating.

WEP encryption and integrity

In addition to authentication, WEP provides confidentiality via encryption. The same WEP key used in Shared Key Authentication can be used to encrypt data messages to and from wireless clients. The encryption algorithm used by WEP is Rivest Cipher 4 (RC4); RC4 is no longer considered secure, so newer security standards use different algorithms.

WEP also ensures the integrity of communications as described previously, appending a 32-bit checksum called the integrity check value (ICV). This is appended to each plaintext message before it is encrypted, allowing the receiver to verify that the message was not tampered with.

Although WEP seems to have all the bases covered when it comes to wireless security—authentication, confidentiality (encryption), and integrity—it is no longer considered secure. Cryptography, and security in general, is a never-ending arms race, and attackers have known how to exploit WEP for over two decades. As threats evolve and become more sophisticated, so must security protocols.

20.2 Wireless client authentication
After WEP’s vulnerabilities were discovered, the Wi-Fi Alliance developed the Wi-Fi Protected Access (WPA) certification as an interim enhancement until the IEEE could develop a more permanent solution (the 802.11i standard, which was adopted by WPA2). WPA (and its more recent versions WPA2 and WPA3) defines two main authentication methods:

WPA-Personal—A pre-shared key (PSK) is used for authentication. This is similar to WEP Shared Key Authentication but more secure. The most recent WPA3 certification enhances this with Simultaneous Authentication of Equals (SAE).

WPA-Enterprise—Designed to provide more robust authentication in enterprise LANs, WPA-Enterprise uses 802.1X and EAP, replacing the PSK with individual user or device credentials.

20.2.1 WPA-Personal: PSK and SAE
WPA-Personal authentication, typically used in SOHO networks, involves configuring a pre-shared key (PSK)—a static 256-bit string used to generate secure encryption keys. The same PSK must be configured on all members of the BSS—the AP and its clients—and is used similarly to the key in WEP Shared Key Authentication.

A 256-bit PSK, which is 64 hexadecimal characters, would be difficult for most users to remember (or enter without typos). To simplify things, you can configure an 8- to 63-character passphrase—what most people call the “Wi-Fi password,” which is then automatically converted into a 256-bit PSK.

Figure 20.4 demonstrates how WPA-Personal authentication with a PSK works. Interestingly, this authentication occurs after the client has already associated with the AP, beginning with Open System Authentication as we covered earlier; the true authentication occurs after the association.



Figure 20.4 WPA-Personal authentication with a PSK. After the client associates with the AP, a four-way handshake is used to confirm that both have the same PSK and to generate unique encryption keys.

After the 802.11 Open System Authentication and association, a four-way handshake is used for two main purposes: to confirm that both the client and the AP have the same PSK and to generate unique encryption keys that will be used to encrypt and decrypt data sent to and from the client.

This method of authentication is used in WPA and WPA2 and provides much greater security than WEP Shared Key authentication. However, there are still vulnerabilities. For example, if an attacker manages to capture the four-way handshake, those messages contain enough information for an attacker to attempt a brute-force attack to learn the PSK.

To protect against the vulnerabilities of WPA/WPA2’s PSK authentication, WPA3 adopts a new authentication method called simultaneous authentication of equals (SAE), which is carried out before 802.11 association (which is then followed by the four-way handshake). Note that SAE still uses a PSK, but the SAE authentication process allows the client and AP to verify that they have matching PSKs without rendering the PSK vulnerable to brute-force attacks. While any password-based system can theoretically be brute-forced with enough time and computational power, the design and implementation of SAE in WPA3 make it practically infeasible. Figure 20.5 illustrates the WPA3-Personal authentication process.



Figure 20.5 WPA3-Personal authentication using SAE. SAE authentication allows the client and AP to confirm they have the same PSK and derive a key used in the four-way handshake. In the four-way handshake, they generate the encryption keys used to encrypt/decrypt data messages.

Note To the user, the experience of using WPA/WPA2/WPA3-Personal authentication is the same: the user just needs to enter an 8- to 63-character passphrase.

Although SAE makes WPA3-Personal more secure than WPA/WPA2 by protecting against brute-force attacks, it still relies on a PSK. The PSK, or the passphrase from which it is derived, could be compromised through a social engineering attack, granting an attacker access to the LAN. Outside of SOHO networks, it’s best to opt for a more secure option: WPA-Enterprise.

Exam Tip For the CCNA exam, know that WPA-Personal authentication involves configuring a shared passphrase (which generates a PSK) and that WPA3 uses SAE to protect the PSK against brute-force attacks.

20.2.2 WPA-Enterprise: 802.1X/EAP/RADIUS
Instead of using a PSK that is shared among all devices in the LAN, the WPA-Enterprise authentication mode verifies each individual user’s or device’s credentials through the IEEE 802.1X standard, which uses the Extensible Authentication Protocol (EAP) framework. We briefly covered 802.1X and EAP in chapter 11 in the context of port-based network access control (PNAC) for wired hosts connected to switch ports.

WPA-Enterprise uses the same concept, but instead of controlling access to individual switch ports, it controls access to the wireless LAN. To authenticate with WPA-Enterprise, the client first uses Open System Authentication and then associates with the AP. At this point, even though the client is associated with the AP, it cannot communicate over the network; it must authenticate with 802.1X/EAP.

EAP defines various authentication methods and message formats. However, EAP itself doesn’t define how those messages should be transported over a network; that’s 802.1X’s role. 802.1X defines how to encapsulate EAP messages over Ethernet or 802.11 LANs, called EAP over LANs (EAPoL). Figure 20.6 shows the 802.1X/EAP “protocol stack”—the set of protocols it uses to enable authentication via EAP.



Figure 20.6 The 802.1X/EAP protocol stack. 802.1X defines EAPoL, which allows EAP messages to be transported over Ethernet or 802.11 LANs.

Note The Authentication Layer on top of EAP refers to the various EAP methods that EAP defines. We’ll briefly cover a few of them in this section.

EAPoL is designed to transport EAP messages within a LAN between the 802.1X supplicant (client device) and the authenticator (the AP). For review, here are the three devices’ roles in 802.1X:

Supplicant—The client device that wants to connect to the network

Authenticator—The network device that the client connects to (the AP)

Authentication server (AS)—The server that verifies the supplicant’s credentials (usually a RADIUS server)

Note In a split-MAC architecture, the WLC functions as the authenticator instead of the AP; the AP tunnels clients’ EAP messages to the WLC using CAPWAP.

To relay the supplicant’s EAP messages to the AS, the authenticator uses RADIUS. Figure 20.7 illustrates this process: EAPoL carries EAP messages between the supplicant and the authenticator, and RADIUS carries the EAP messages between the authenticator and the AS.



Figure 20.7 EAPoL is used to transport EAP messages between the supplicant and authenticator, and RADIUS between the authenticator and AS.

Note Although previous authentication examples showed a standalone AP, WPA-Enterprise is more common in enterprise networks that would likely use a split-MAC architecture (with a WLC)—not autonomous APs.

EAP isn’t a single authentication method. As the name suggests, EAP is extensible, acting as a framework that defines various authentication methods called EAP methods. The CCNA exam doesn’t expect you to know these EAP methods in detail, but here are a few examples:

LEAP (Lightweight EAP)—Developed by Cisco to address WEP’s vulnerabilities. The client authenticates with a username/password combination, and then the supplicant and AS exchange challenge phrases, providing mutual authentication. LEAP uses WEP encryption and is no longer considered secure.

EAP-FAST (EAP-Flexible Authentication via Secure Tunneling)—Developed by Cisco to replace LEAP. It establishes a Transport Layer Security (TLS) tunnel using a Protected Access Credential (PAC)—a shared secret—to authenticate the supplicant and AS. Within this tunnel, user credentials are exchanged for authentication.

PEAP (Protected EAP)—The AS has a digital certificate that the supplicant uses to authenticate the AS and establish a TLS tunnel. In the tunnel, user credentials are provided for authentication.

EAP-TLS (EAP-Transport Layer Security)—The AS and supplicant each have a digital certificate that they use to authenticate each other. EAP-TLS is considered the most secure, but managing certificates on all client devices can be burdensome.

Regardless of which EAP method is used, the same four-way handshake that we outlined in the WPA-Personal section is always used after authentication to generate the encryption keys used to encrypt/decrypt data messages. This handshake is done between the supplicant and authenticator (the client and the AP/WLC).

Exam Tip For the CCNA exam, you should understand the basics of 802.1X (supplicant, authenticator, AS), EAP, and RADIUS: EAPoL carries EAP messages between the supplicant and authenticator, and RADIUS carries EAP messages between the authenticator and AS.

20.3 Wireless encryption and integrity
WEP defined confidentiality (encryption) and integrity measures that promised to offer privacy equivalent to that of wired LANs. As we already covered, that turned out not to be the case; WEP has various vulnerabilities and should not be used anymore. In this section, we’ll examine the encryption and integrity protocols that replaced WEP and were adopted by the Wi-Fi Alliance’s WPA, WPA2, and WPA3 certifications.

20.3.1 Temporal Key Integrity Protocol
After WEP’s vulnerabilities were discovered, a more secure solution was urgently needed. However, there was a major problem: existing hardware was built to use WEP. To address this issue before new protocols and hardware were developed, Temporal Key Integrity Protocol (TKIP) was created as an enhancement to WEP. TKIP was included in the Wi-Fi Alliance’s first WPA certification.

WEP’s fundamental flaw was the fact that it used static encryption keys; all clients used the same encryption key, and it remained unchanged unless an admin manually configured a new passphrase. TKIP solved this by using a process called per-packet key mixing, generating a unique encryption key for each packet. This makes it much more difficult for an attacker to decipher the PSK through a brute-force attack. TKIP also added a few more security improvements, such as the following:

TKIP’s data integrity checksum, called a message integrity check (MIC), is stronger than WEP’s ICV.

TKIP adds a sequence number to each frame to mitigate against replay attacks.

Note A replay attack is when an attacker captures valid messages and retransmits them later. For example, an attacker can gain unauthorized access to a system by replaying a user’s valid authentication messages.

20.3.2 Counter Mode with Cipher Block Chaining Message Authentication Code Protocol
Although TKIP served as a stopgap to protect against WEP’s vulnerabilities, the IEEE 802.11i standard, which formed the basis of WPA2, brought in more advanced security protocols that are still in use in many wireless LANs today. 802.11i/WPA2 uses Counter Mode with Cipher Block Chaining Message Authentication Code Protocol (CCMP) to provide message encryption and integrity. That’s quite a long name—let’s examine it.

Whereas WEP and TKIP use the RC4 encryption algorithm, CCMP uses Advanced Encryption Standard (AES), a more robust algorithm that provides much more secure encryption. Specifically, CCMP uses AES counter mode encryption, hence the “Counter Mode” in CCMP’s name. The details of counter mode aren’t necessary for the CCNA exam, but in essence, it involves encrypting a counter value that increments for each block of encrypted data, ensuring that each block of data is encrypted with a unique key.

The second part of the name refers to Cipher Block Chaining Message Authentication Code (CBC-MAC); CCMP’s CBC-MAC provides a more robust data integrity checksum than TKIP’s MIC.

20.3.3 Galois/Counter Mode Protocol
The latest security certification from the Wi-Fi Alliance is WPA3, and it uses Galois/Counter Mode Protocol (GCMP) for data encryption and integrity. GCMP can be considered an improved version of CCMP, offering improved security as well as greater efficiency—this efficiency is necessary for encryption to keep up with the faster data rates of the latest 802.11 standards.

Like CCMP, GCMP uses AES counter mode encryption. However, it supports greater AES key lengths (128 or 256 bits) than CCMP (128 bits), providing stronger encryption. For its data integrity checksum, GCMP uses Galois Message Authentication Code (GMAC)—once again, this provides more secure data integrity than the protocols used in earlier standards.

Note Galois is pronounced “gal-wah”—the name of a French mathematician.

20.4 Wi-Fi Protected Access
We’ve covered a lot of different protocols for providing authentication, encryption, and integrity to wireless LANs, referencing the WPA generation that supports each. Table 20.1 summarizes these protocols, including WEP for reference as well.

Exam Tip CCNA exam topic 5.9 states that you must be able to “describe wireless security protocols (WPA, WPA2, and WPA3).” In this section, we’ll summarize which standards are supported by which WPA certifications; make sure you know them!

Table 20.1 WPA security protocols


|                              | WEP                      | WPA          | WPA2         | WPA3         |
|------------------------------|--------------------------|--------------|--------------|--------------|
| Release Year                 | 1997                     | 2003         | 2004         | 2018         |
| Authentication (WPA-Personal)    | Open System, Shared key  | PSK          | PSK          | SAE          |
| Authentication (WPA-Enterprise)  | N/A                      | 802.1X/EAP   | 802.1X/EAP   | 802.1X/EAP   |
| Encryption                   | RC4                      | RC4 (TKIP)   | AES (CCMP)   | AES (GCMP)   |
| Integrity                    | ICV                      | MIC (TKIP)   | CBC-MAC (CCMP) | GMAC (GCMP) |

It’s worth noting that table 20.1 isn’t complete; it only lists the strongest encryption protocol supported by each WPA certification. For example, WPA2 includes optional support for TKIP to accommodate older client devices that don’t support CCMP. Similarly, WPA3 doesn’t just support GCMP; it supports CCMP as well. However, for the CCNA exam, I recommend learning the protocols as listed in table 20.1; further details can be left for future studies.

As of 2020, a device must support WPA3 to earn “Wi-Fi Certified” status. WPA2 is still commonly used in enterprise and SOHO wireless LANs, but the move to WPA3 is underway, and WPA3 support is now commonplace for new hardware. In addition to the superior protocols we already covered, WPA3 has some other security benefits:

Protected Management Frames (PMF)—PMF ensures the authenticity and integrity of 802.11 management frames (i.e., authentication and association messages), preventing certain types of spoofing attacks. PMF was supported in WPA2 but is mandatory in WPA3.

Forward Secrecy (FS)—FS, also known as Perfect Forward Secrecy (PFS), ensures that the security of encrypted data remains intact even if the PSK is compromised in the future; a compromised PSK cannot be used to decrypt past communications. This is because the encryption keys used for each session are unique and not solely derived from the PSK.

Summary
Although wireless LANs introduce unique challenges, fundamental security concepts like the CIA triad still apply.

Confidentiality in a wired LAN is largely ensured by the medium: the signals are contained within the cables. However, wireless signals can be picked up by any receiver within range of the transmitter, making encryption essential.

Unencrypted information (that will not be encrypted) is called cleartext. Unencrypted information that will be encrypted (but has not yet been fed into the encryption algorithm) is plaintext, and encrypted information is called ciphertext.

To protect the integrity of a message before sending it over the air, the sender uses a mathematical function to generate a checksum—a small block of data derived from the original message, allowing the receiver to check whether it was altered.

Attacks against the availability of a wireless LAN are simple to carry out by any malicious user with the proper tools. An example is an RF jamming attack, in which the attacker uses a signal generator to flood the 802.11 frequency bands.

The only solution to an RF jamming attack is to locate and disable/remove the source of the attack, and the only preventative measure is physical security.

The original 802.11 standard defined a security protocol called Wired Equivalent Privacy (WEP). WEP is now obsolete; it is no longer secure.

WEP defined two methods of authentication: Open System and Shared Key.

In WEP Open System Authentication, the client device sends an authentication request, and the AP sends an authentication response; no questions asked.

WEP Shared Key Authentication involves the configuration of a static WEP key on the AP and each client—the Wi-Fi password.

To verify that each client has the correct WEP key, the AP sends an unencrypted challenge phrase that the client encrypts with the WEP key and sends back to the AP. The AP then decrypts the challenge phrase and ensures it matches the original.

In addition to authentication, WEP provides confidentiality with encryption. The same WEP key used in Shared Key Authentication can be used to encrypt messages to and from wireless clients. The encryption algorithm is Rivest Cipher 4 (RC4).

WEP ensures the integrity of communications using a checksum called the integrity check value (ICV).

After WEP’s vulnerabilities were discovered, the Wi-Fi Alliance developed the Wi-Fi Protected Access (WPA) certification as an interim enhancement until the IEEE could develop a more permanent solution (802.11i, which was adopted by WPA2).

WPA, WPA2, and WPA3 define two main authentication methods: WPA-Personal (primarily for SOHO networks) and WPA-Enterprise (for larger businesses).

WPA-Personal involves configuring a pre-shared key (PSK)—a static 256-bit string that is used to generate secure encryption keys. The same PSK must be configured on the AP and its clients.

To simplify the experience, you can configure an 8- to 63-character passphrase—what most people call the “Wi-Fi password”—which is then automatically converted into a 256-bit PSK.

WPA-Personal authentication involves the client and AP performing a four-way handshake to verify the PSK and generate encryption keys. This occurs after the client has performed Open System Authentication and is associated with the AP.

WPA/WPA2’s PSK authentication is vulnerable to brute-force attacks if an attacker captures the four-way handshake. To protect against this, WPA3 adopts a new method called simultaneous authentication of equals (SAE).

SAE is carried out before 802.11 association, which is then followed by the same four-way handshake. It still uses a PSK, but in a way that protects against brute-force attacks.

WPA3 with SAE still relies on a PSK—a single passphrase that can be compromised through a social engineering attack. Outside of SOHO networks, it’s best to opt for a more secure option: WPA-Enterprise.

WPA-Enterprise authenticates each individual user’s or device’s credentials through 802.1X and EAP. The client first uses Open System Authentication and associates with the AP and then authenticates with 802.1X/EAP.

802.1X defines port-based network access control (PNAC), controlling whether a host is allowed to communicate via a switch port (or a wireless LAN, in this case).

EAP defines various authentication methods (EAP methods) and message formats, and 802.1X defines how to encapsulate EAP messages over Ethernet or 802.11 LANS, called EAP over LANs (EAPoL).

802.1X defines three device roles: supplicant (the device that wants to connect to the network), authenticator (the network devices that the client connects to), and authentication server/AS (the server that verifies the supplicant’s credentials).

EAPoL transports EAP messages within a LAN between the supplicant (the client device) and the authenticator (the AP or the WLC in a split-MAC architecture).

RADIUS is typically used to transport EAP messages between the authenticator and the AS, which is usually a RADIUS server.

EAP isn’t a single authentication method; it is extensible and defines various EAP methods. Some examples are LEAP (Lightweight EAP), EAP-FAST (EAP-Flexible Authentication via Secure Tunneling), PEAP (Protected EAP), and EAP-TLS (EAP-Transport Layer Security).

Regardless of which EAP method is used, the same four-way handshake is always used after authentication to generate encryption keys.

After WEP’s vulnerabilities were discovered, Temporal Key Integrity Protocol (TKIP) was created as an enhancement that worked on hardware developed for WEP. TKIP was included in the Wi-Fi Alliance’s first WPA certification.

TKIP uses per-packet key mixing to generate a unique encryption key for each packet, making the PSK less vulnerable to brute-force attacks.

TKIP’s data integrity checksum, called a message integrity check (MIC), is stronger than WEP’s ICV.

TKIP adds a sequence number to each frame to mitigate against replay attacks.

IEEE 802.11i, which formed the basis of WPA2, brought in more advanced security protocols that are still in use in many wireless LANs.

WPA2 uses Counter Mode with Cipher Block Chaining Message Authentication Code Protocol (CCMP) to provide data encryption and integrity.

CCMP uses Advanced Encryption Standard (AES) in counter mode as its encryption algorithm, which is stronger than WEP/TKIP’s RC4 algorithm.

CCMP uses Cipher Block Chaining Message Authentication Code (CBC-MAC) to provide a more robust data integrity checksum than TKIP’s MIC.

WPA3 uses Galois/Counter Mode Protocol (GCMP) for data encryption and integrity. GCMP is more secure and more efficient than CCMP, which is necessary for encryption to keep up with the faster data rates of the latest 802.11 standards.

Like CCMP, GCMP uses AES counter mode encryption, although it supports greater key lengths (128 bits or 256 bits) than CCMP (128 bits).

GCMP uses Galois Message Authentication Code (GMAC) for its data integrity checksum.