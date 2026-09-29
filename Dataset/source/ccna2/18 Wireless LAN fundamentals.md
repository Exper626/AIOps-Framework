18 Wireless LAN fundamentals
This chapter covers

The challenges of using air as a communication medium
The characteristics of radio frequency
Wireless LAN standards as defined by IEEE 802.11
Connecting wireless devices using different kinds of service sets
It’s time to break our communications out of their wired constraints and explore a new medium for communication: air. Just as copper twisted-pair and glass fiber-optic cables provide a medium to transmit encoded messages using electricity and light, the air all around us (or, more precisely, the space around us that happens to be filled with air) provides an alternative medium to transmit messages using electromagnetic waves.

In this chapter and the three that follow it, we will cover various aspects of wireless LANs as defined by IEEE 802.11—better known as Wi-Fi. This chapter starts by covering the foundational concepts of wireless LANs and how devices communicate with radio frequency waves. We will cover the following CCNA exam topics:

1.1 Explain the role and function of network components

1.1.d Access points

1.11 Describe wireless principles

18.1 Wireless communications
Wired LANs as defined by IEEE 802.3—better known as Ethernet—have been a major focus of both volumes of this book up to this point, and for good reason: Ethernet is the dominant technology used in modern wired network connections and is a key topic of the CCNA exam. Ethernet defines standards at Layers 1 and 2 of the TCP/IP model: physical cables, methods of encoding data signals over these cables, the Ethernet frame format, and various other functions.

Wireless LANs are defined by IEEE 802.11. Like Ethernet, 802.11 defines standards at Layers 1 and 2 of the TCP/IP model: the precise frequencies that can be used for wireless LANs, how to encode data signals in electromagnetic waves over the air, the 802.11 frame format, etc.

Note Wireless LAN is sometimes abbreviated as WLAN. Wired and wireless both start with W, so that might seem confusing, but a wired LAN is typically just called a LAN.

Figure 18.1 demonstrates the similar roles of Ethernet and 802.11: they both address how to send a message to another device connected to the same physical medium. Thanks to the modular nature of the TCP/IP model, Layers 3 and above operate identically regardless of which Layer 1/2 protocols are used.



Figure 18.1 Ethernet and 802.11 serve similar functions: how to send a message to another device over a particular physical medium. Layers 3 and above operate identically, regardless of which Layer 1/2 protocols are used.

What’s Wi-Fi?

Most people know 802.11 wireless LANs by the name Wi-Fi. However, Wi-Fi is not an official name used by the IEEE; it is a trademark of the Wi-Fi Alliance, an organization that tests and certifies equipment for 802.11 standards compliance. An organization whose products pass the testing and certification process can mark their equipment as “Wi-Fi Certified.” The goal of this process is to ensure interoperability between different vendors’ devices (although a device’s lack of Wi-Fi certification doesn’t necessarily mean that it is incompatible with other devices). For the sake of accuracy, I will avoid the name Wi-Fi unless specifically referring to the Wi-Fi Alliance’s certifications.

18.1.1 The challenges of wireless communications
Copper and fiber-optic Ethernet cables are bounded media—the signals are confined to the cables, providing a controlled pathway for data transmission. This physical boundary offers some advantages in terms of security (only the device at the other end of the cable receives the signal) and signal consistency (the signal is less susceptible to interference).

In contrast, the air used to transmit wireless signals is an unbounded medium. Unlike wired connections, wireless signals propagate freely in open space, radiating in all directions from the source. The unbounded nature of wireless communication introduces both opportunities and challenges. On one hand, it allows for greater mobility and flexibility, as devices don’t need to be physically connected with a network cable. However, it also brings various challenges. Here are some key examples:

All devices within range of a wireless device receive that device’s signals.

Wireless devices must contend for airtime.

Signal interference can be a major issue.

Wireless communications are regulated by various international and national bodies.

Wireless signal coverage area must be considered.

Let’s walk through each of these challenges. First, all devices within sufficient range of a wireless device receive that device’s signals. In fact, wireless communication is sometimes likened to wired communication via an Ethernet hub—all devices connected to a hub receive all frames from other devices connected to the hub. Figure 18.2 shows this similarity.

This means that data privacy within a wireless LAN is a greater concern than it is in a wired LAN. For this reason, communications are usually encrypted, even within a LAN; we’ll cover more about wireless LAN security in chapter 20.



Figure 18.2 Similar to how frames are flooded to all devices connected to a hub, all devices within range of a wireless device receive its signals.

Another consequence of using an unbounded medium is that devices must operate in half-duplex mode; only one device can transmit at a time, or their signals will collide. Wireless devices must contend for airtime—they compete for the chance to transmit data over a shared medium. This half-duplex nature is a significant factor in why wireless networks often do not match the speeds of wired networks using switches (which operate in full-duplex mode).

While wired devices connected to a hub use Carrier-Sense Multiple Access with Collision Detection (CSMA/CD) to detect and recover from collisions, wireless devices use a similar protocol called Carrier-Sense Multiple Access with Collision Avoidance (CSMA/CA). Figure 18.3 shows a simplified version of the CSMA/CA process. After preparing a frame for transmission, the device will listen to see if the channel is free. If the channel is busy, the device will wait a random (short) period of time before checking again. The device will transmit the frame only when it senses the channel is free.



Figure 18.3 The CSMA/CA process. To avoid collisions, a device will listen to ensure the channel is free before transmitting a frame.

Note Although CSMA/CA attempts to avoid collisions, if two devices happen to transmit simultaneously, the frames can still collide, resulting in an incoherent signal. In such a case, the devices will have to retransmit their frames.

The third challenge of wireless communications is signal interference, which can significantly impact network performance. For example, wireless LANs from neighboring offices, homes, or apartments operating on the same or overlapping frequency ranges can cause interference. Interference can disrupt the clarity and integrity of the signal, leading to data transmission errors and reduced network performance in the LAN. Managing interference is a critical aspect of wireless network design, requiring careful channel selection.

Note It’s not only other 802.11 networks that can cause interference; other devices like microwave ovens, cordless phones, and Bluetooth devices operating in the same frequency range can disrupt wireless LAN communications.

Another challenge stems from the complex landscape of national and international regulations. Each country has its own regulatory body, such as the US Federal Communications Commission (FCC), that governs the use of radio frequencies and sets standards for wireless communication. These regulations are necessary to manage the electromagnetic spectrum and prevent interference between different types of services, such as cellular signals, satellite communications, and wireless LANs.

Although international bodies like the International Telecommunications Union (ITU) work to coordinate the allocation of the radio frequency spectrum across countries to ensure consistent use, there are still differences between countries, and adhering to these regulations is a legal necessity. For this reason, wireless networking equipment used in one country might be legally prohibited in another.

The final challenge we’ll consider is the signal coverage area of a wireless LAN. Similar to how cable length must be considered in wired LANs, coverage area is an essential consideration in wireless LANs. As wireless signals propagate through space, they lose strength; this is called free-space path loss (FSPL). In addition to FSPL, signals can be influenced by a variety of factors; these include reflection off surfaces, diffraction around obstacles, scattering due to irregularities in the medium, and others.

How far do wireless signals travel?

The real question here is “How far can a wireless signal travel and maintain enough strength for the receiver to effectively distinguish the signal from background noise and decode the information?” Indoors, this is typically up to 150 feet (46 meters). Outdoors, it can extend beyond 300 feet (91 meters), but these distances vary greatly depending on factors like the signal’s frequency, transmitter power, antenna type, and environmental conditions such as physical obstructions.

18.1.2 Wave behaviors
The electromagnetic waves that are used to encode wireless signals are influenced by the media they pass through and objects they encounter. In this section, we’ll examine five phenomena that must be considered in a wireless LAN design, as shown in figure 18.4.



Figure 18.4 Phenomena affecting the behavior of electromagnetic waves include absorption by a medium, reflection off surfaces, refraction (bending) as waves pass through a medium, diffraction around obstacles, and scattering from irregularities.

Absorption occurs when a wave passes through a medium and is converted into heat, weakening the signal. For example, a wireless signal passing through a wall can cause significant attenuation, particularly if the wall is made of a dense material. This can prevent devices on the other side of the wall from receiving a coherent signal.

Note Attenuation is the weakening of a signal.

Reflection happens when a wave bounces off a surface rather than passing through it; this is the same phenomenon as light reflecting off a mirror. Metal surfaces are common culprits, as they are highly reflective of radio waves. Reflection is the reason wireless reception is usually poor in elevators; the signal bounces off the metal, and very little penetrates into the elevator.

Refraction occurs when a wave passes from one medium to another one with a different density, altering the wave’s speed and causing it to bend. A common everyday occurrence of refraction is the apparent shift in the position of an object in water when viewed from above; this is due to the light waves bending as they move from water to air.

Diffraction is the bending and spreading of waves around the edges of an obstacle, such as a wall. This enables wireless communication even when there isn’t a clear line of sight between the transmitter and receiver. In urban environments, diffraction often allows signals to reach street level and indoor areas that are not in direct view of the cell tower or wireless access point.

The final phenomenon is scattering, which occurs when a wave encounters a surface or medium with irregularities that cause the wave to spread out erratically. Common causes of scattering are dust, smog, water vapor, and textured surfaces. Scattering can cause signal attenuation as it disperses the signal’s energy in various directions.

When designing a wireless LAN, it’s essential to account for the various wave behaviors that affect wireless signals. Absorption by walls, reflection from surfaces, refraction through different media, diffraction around obstacles, and scattering due to irregularities all play a role in shaping the coverage and reliability of a wireless network.

Exam Tip For the CCNA exam, you are not expected to be able to design a wireless LAN that accounts for these various factors. However, you should have a basic understanding of each.

18.2 Radio frequency
To send a wireless signal, a device applies an alternating electric current to an antenna, which in turn produces fluctuating electromagnetic fields that radiate out as waves; these are called electromagnetic waves. Two key measurements of an electromagnetic wave are its amplitude and frequency.

18.2.1 Amplitude and frequency
Amplitude and frequency are two fundamental characteristics of electromagnetic waves. Amplitude measures the maximum strength of the electric and magnetic fields of a wave and is associated with how much energy the wave carries; basically, higher amplitude means a stronger signal. If the amplitude of a signal is too low, the receiver won’t be able to distinguish a coherent message from the signal. Figure 18.5 shows two waves with different amplitudes: the wave represented by the solid line has a higher amplitude than the dotted one.



Figure 18.5 Waves with higher amplitude carry stronger signals, indicated by greater electric and magnetic field strengths.

Note Figure 18.5 only shows the electric field of each wave, but each has an equivalent magnetic field (hence the name electromagnetic wave) that oscillates perpendicular to the electric field.

Frequency measures how quickly the strength of the wave’s electric and magnetic fields oscillates and is measured in hertz (Hz)—the number of oscillations per second. Like bits and bytes, hertz are typically measured in thousands, millions, billions, and trillions (or even greater):

kHz (kilohertz)—1000 cycles per second

MHz (megahertz)—1,000,000 cycles per second

GHz (gigahertz)—1,000,000,000 cycles per second

THz (terahertz)—1,000,000,000,000 cycles per second

Figure 18.6 shows two waves with different frequencies: the wave represented by the dotted line has a higher frequency than the solid one. Notice that, despite having different frequencies, the waves have identical amplitudes.



Figure 18.6 Waves with higher frequency oscillate at a greater rate. Frequency is measured in hertz (Hz), which is the number of oscillations per second.

A related concept is period, which is the amount of time it takes for one full oscillation. Figure 18.7 shows a wave with a frequency of 4 Hz and, therefore, a period of 0.25 seconds—each oscillation takes 0.25 seconds.



Figure 18.7 A wave with a frequency of 4 Hz. This means it completes four full oscillations every second, resulting in a period of 0.25 seconds per oscillation.

In the context of radio waves, frequency determines a wave’s position within the electromagnetic spectrum and has a major effect on how the signal behaves as it propagates through the air and other media. In wireless LANs, higher frequencies can typically support higher data transfer rates and are less crowded with other wireless devices. However, they are also more susceptible to absorption by obstacles. On the other hand, lower frequencies penetrate better through obstacles and can, therefore, cover larger distances. However, lower frequencies typically support lower transfer rates and are more crowded with other wireless devices. In the next section, we’ll examine the concepts of the electromagnetic spectrum, radio frequency’s position in the spectrum, and the different bands and channels used by 802.11 wireless LANs.

18.2.2 RF bands and channels
The electromagnetic spectrum is the entire range of electromagnetic radiation, such as AM and FM radio, ultraviolet light, X-rays, and gamma rays. Figure 18.8 shows the electromagnetic spectrum and radio frequency’s position within it.



Figure 18.8 The electromagnetic spectrum and examples of different wave types. Radio frequency is from around 20 kHz to around 300 GHz.

Note Figure 18.8 is designed to show a general progression from lower to higher frequencies across the electromagnetic spectrum. The placement of each example doesn’t represent its precise frequency value.

Radio frequency (RF) is a segment of the electromagnetic spectrum generally defined as ranging from around 20 kHz to around 300 GHz. RF is used for a variety of purposes, from AM and FM radio to microwaves and radar. However, most relevant to this chapter are 802.11 wireless LANs. Three bands within the RF range are used for wireless LANs: the 2.4 GHz band, the 5 GHz band, and the newer 6 GHz band, introduced to wireless LANs in 2020.

Note A band is a specific range of frequencies, such as the AM radio band, FM radio band, and the 802.11 wireless LAN bands.

The 2.4 GHz band

The 2.4 GHz band spans from 2.4 to 2.495 GHz and is widely used for wireless communications due to its lower frequency, which enables better penetration through obstacles compared to the 5 GHz and 6 GHz bands. However, this band is also used for other technologies, such as Bluetooth, microwave ovens, cordless telephones, and many others. This means that it can sometimes be crowded, leading to congestion and interference.

The 2.4 GHz band is divided into 14 individual channels. Like a band, a channel is a specific range of frequencies—you can think of a channel as a smaller division of a band. For wireless communication to occur, both the transmitting and receiving devices must be tuned to the same channel, enabling them to “speak” and “listen” on the same frequency range.

Each channel has a defined center frequency and a standard width of 20 MHz, although older standards use 22 MHz. Wireless devices communicate using these channels, so careful channel selection is critical to minimize interference. Figure 18.9 shows the 14 channels of the 2.4 GHz band (you don’t have to memorize the center frequency values).



Figure 18.9 Channels in the 2.4 GHz band. There are 14 channels in total. Because many channels in the 2.4 GHz band overlap, channels 1, 6, and 11 should be used to avoid interference.

Note Not all channels in the 2.4 GHz band can be used in all countries. For example, only channels 1 to 11 are commonly allowed in the United States/Canada, while most countries allow 1 to 13. Channel 14 is allowed in Japan, but only when using an older 802.11 standard.

As figure 18.9 shows, there is significant overlap between the 2.4 GHz channels. In a wireless LAN that needs multiple APs for full coverage, it’s important to use non-overlapping channels to avoid interference. If adjacent access points use the same channel, devices not only have to contend for airtime with other devices using the same access point but with devices using neighboring access points too. Channels 1, 6, and 11 are recommended, as highlighted in figure 18.9. However, in countries that allow up to channel 13, a layout using channels 1, 5, 9, and 13 is also possible. Figure 18.10 shows both layouts.



Figure 18.10 Non-overlapping channel layout options in the 2.4 GHz band. Each hexagon represents a wireless access point’s coverage area.

Exam Tip The key takeaways for the CCNA exam are that the 2.4 GHz band uses overlapping channels and that you should use a 1–6–11 layout to avoid interference (1–5–9–13 is also possible in most countries outside of the U.S./Canada).

The 5 GHz band

The 5 GHz band, ranging from approximately 5.150 to 5.895 GHz (depending on the country), is the second frequency band widely used for wireless LANs. Compared to the 2.4 GHz band, the 5 GHz is generally less crowded and not as prone to interference from common household devices.

However, signals in the 5 GHz band don’t penetrate walls and other barriers as well as the 2.4 GHz band. This can be both a benefit and a drawback. On the upside, it means that 5 GHz signals from neighboring rooms and buildings are less likely to cause interference. On the downside, this can limit the coverage area of 5 GHz signals.

Unlike the 2.4 GHz band, channels in the 5 GHz band are non-overlapping when using the standard 20 MHz width, which simplifies the channel selection process when setting up multiple wireless access points. These channels can be combined to form wider channels of 40, 80, or 160 MHz, supporting higher data transfer rates (although resulting in fewer available channels). Figure 18.11 shows the various 5 GHz channels, demonstrating how they can be combined to make wider channels. The number written in each channel is the channel number that identifies it. I include them only for reference; you don’t have to memorize them.



Figure 18.11 Channels in the 5 GHz band. Twenty MHz channels can be combined into wider channels of 40, 80, or 160 MHz to support greater data transfer rates.

Note The available channels in the 5 GHz band can vary greatly depending on the country, so the channels shown in figure 18.11 do not apply everywhere.

The 6 GHz band

The 6 GHz band is the newest addition to the 802.11 wireless LAN frequency bands, ranging from 5.925 GHz to 7.125 GHz (notably, its low and high ends are both beyond the 6 GHz range). This band provides even more non-overlapping channels than the 5 GHz band. The standard channel width is 20 GHz, but channels can be combined to form wider channels of 40, 80, 160, or even 320 MHz, enhancing data transfer rates. Figure 18.12 shows the different channels in the 6 GHz band.



Figure 18.12 Channels in the 6 GHz band. 20 MHz channels can be combined into wider channels of 40, 80, 160, or 320 MHz to support greater data transfer rates. Note that there is some overlap between 320 MHz channels.

The 6 GHz band was adopted in 2020 in the 802.11ax standard, better known as Wi-Fi 6E, and also the new 802.11be (Wi-Fi 7) standard. Due to its relatively recent adoption, the 6 GHz band isn’t as widely used as the 2.4 and 5 GHz bands. However, it’s expected to alleviate the congestion found in the other bands and provide even greater data transfer rates.

18.2.3 IEEE 802.11 standards
Just as there are various 802.3 Ethernet standards designed to accommodate different network environments and objectives, with new ones continually in development to meet evolving demands (such as higher speeds), the same can be said of the 802.11 family of standards. Table 18.1 lists the major generations of 802.11 wireless LAN standards, starting from the original 802.11 standard, which was released in 1997.

Table 18.1 IEEE 802.11 wireless LAN standards

| 802.11 standard | Wi-Fi generation | Maximum rate (Mbps) | RF band (GHz) |
|-----------------|------------------|---------------------|---------------|
| 802.11          | -                | 1-2                 | 2.4           |
| 802.11b         | -                | 1-11                | 2.4           |
| 802.11a         | -                | 6-54                | 5             |
| 802.11g         | -                | 6-54                | 2.4           |
| 802.11n         | Wi-Fi 4          | 72-600              | 2.4/5         |
| 802.11ac        | Wi-Fi 5          | 433-6933            | 5             |
| 802.11ax        | Wi-Fi 6          | 574-9608            | 2.4/5         |
|                 | Wi-Fi 6E         |                     | 6             |
| 802.11be        | Wi-Fi 7          | 1376-46120          | 2.4/5/6       |

Note Starting from the 802.11n standard, each new generation has been marketed as Wi-Fi X, with 802.11n as Wi-Fi 4. Although not official names, 802.11, 802.11b, 802.11a, and 802.11g are sometimes retroactively called Wi-Fi 0, 1, 2, and 3, respectively.

The maximum transfer rates listed in table 18.1 are theoretical maximums under ideal conditions and don’t necessarily reflect the performance that can actually be achieved. Due to the complexities of wireless communications and the various external factors that can have an effect, in real-world applications, actual transfer rates will be lower.

Exam Tip For the CCNA exam, I particularly recommend memorizing which standards use which RF bands. For most CCNA exam domains, you don’t have to memorize IEEE standard names, but this is an exception.

Exam scenario

Here’s an example of how the CCNA exam might test your knowledge of the 802.11 standards. As in this example, CCNA exam questions that require you to select multiple answers will state so explicitly (select two, select three, etc.).

Q: In which of the following 802.11 standards is careful channel selection necessary to avoid interference among neighboring APs? (select two)

A. 802.11a

B. 802.11b

C. 802.11g

D. 802.11ac

To correctly answer this question, you need to know two things: which frequency band requires careful channel selection to avoid interference and which 802.11 standards use that band. The 2.4 GHz band consists of channels with significant overlap, so the 1-6-11 or 1-5-9-13 channel patterns should be used to avoid interference among neighboring APs. Of the four options in the question, the two standards that use the 2.4 GHz band are 802.11b and 802.11g, so the correct answers are B and C.

18.3 Service sets
Now that we’ve covered the basics of electromagnetic waves, RF frequency bands, and 802.11 standards, let’s consider how wireless devices can use these tools to communicate. In the 802.11 standards, a service set is a group of devices that operate on the same wireless LAN, sharing the same service set identifier (SSID)—a human-readable label that identifies the service set. There are four main types of service sets:

Independent basic service set (IBSS)—A peer-to-peer network where devices communicate directly (without an access point)

Basic service set (BSS)—Devices connect through a single access point, forming the basic building block of a wireless LAN

Extended service set (ESS)—Multiple linked BSSs, providing seamless connectivity across a broader area

Mesh basic service set (MBSS)—A network of interconnected APs providing flexible coverage

Note When you use 802.11 (Wi-Fi) to connect to a wireless network from your smartphone or laptop, the network name you select is that network’s SSID.

18.3.1 Independent basic service set
An independent basic service set (IBSS), also called an ad hoc wireless network, consists of wireless devices (laptops, smartphones, etc.) communicating directly with each other. Figure 18.13 shows a simple IBSS with an SSID of “Jeremy’s IBSS” that consists of a smartphone and two laptops.



Figure 18.13 An IBSS of three devices. The devices can communicate directly with each other and share resources.

An IBSS is useful for quick, temporary communication setups. For example, an IBSS can be used for file sharing or gaming (although LAN parties are largely a thing of the past). However, an IBSS doesn’t scale beyond a few devices. In most wireless LANs, you will want to employ some network infrastructure: wireless access points.

18.3.2 Basic service set
A basic service set (BSS) forms the fundamental building block of an 802.11 wireless LAN. In a BSS, wireless clients connect to a wireless access point (abbreviated as WAP or AP), which coordinates the communication between the devices and serves as the gateway to other network resources, such as a wired LAN or the internet.

Note A client is any device that connects to a wireless LAN via an AP. 802.11 standards use the term station to refer to any wireless-capable device (including clients and APs), but it’s a more technical term that isn’t common in everyday usage. Cisco products call them clients, so that’s the term I’d expect on exam questions.

Figure 18.14 shows a BSS consisting of an AP and three clients, all communicating using channel 1 of the 2.4 GHz band. The clients connected to AP1 cannot send frames directly to each other (even if they are in range of each other’s signals); they must send their frames to AP1, which will relay the frames to their destination.

Note The area around an AP where clients can successfully communicate with it—the AP’s coverage area—is called a basic service area (BSA) or cell.

The SSID of the BSS, Jeremy’s Wi-Fi, is a human-readable name that serves as the network’s identifier for users. SSIDs do not need to be unique. Instead, a basic service set identifier (BSSID) serves to uniquely identify the BSS. While multiple BSSs may use the same SSID to create an extended service set (ESS) for wider coverage, each BSS will have a unique BSSID; we’ll cover ESSs in the next section.



Figure 18.14 A BSS consisting of an AP and three clients. Clients cannot send frames directly to each other; they must communicate via the AP.

Note The BSSID is the MAC address of the AP’s radio. MAC addresses are uniquely assigned to the device by the manufacturer; no two devices will have the same MAC.

Multiple BSSs

A single AP is capable of providing more than one BSS. For example, an enterprise may create a BSS for staff and a BSS for guests, applying different security policies to each. However, all of the AP’s BSSs must use the same channel—the channel its radio is tuned to. For this reason, creating multiple BSSs won’t help to alleviate a congested wireless LAN; all of the AP’s clients, regardless of BSS, share the same channel.

Figure 18.15 shows an AP providing two BSSs. Note that, despite both BSSs sharing the same radio, each has a unique BSSID; this is usually accomplished by incrementing the radio’s MAC address by 1 for each new BSS.



Figure 18.15 An AP providing two BSSs for clients. Both use the same channel. Each BSS requires a unique BSSID. Hosts can only communicate within their BSS.

Note Many modern APs have multiple radios, allowing them to provide BSSs in different channels (typically one in each of the 2.4 and 5 GHz bands).

Distribution system

Most wireless LANs aren’t standalone networks. Rather, wireless LANs are a way for wireless clients to connect to the wired network infrastructure, enabling wireless clients to communicate with hosts in other BSSs, hosts in the wired LAN, in remote sites via the WAN, over the internet, etc. 802.11 calls the wired network infrastructure the distribution system (DS). Although the previous diagrams omitted the DS, a wireless LAN without a DS is rare. Without a DS, an AP’s wireless clients can only communicate among themselves; they have no gateway to other networks.

In addition to its wireless radio, each AP has an Ethernet port through which it can connect to the DS (usually via a switch). The AP serves as a bridge connecting the two mediums: it translates 802.11 frames from wireless clients to Ethernet frames to be sent over the wired LAN, and vice versa. Figure 18.16 shows an AP connected to a DS (represented by a single switch). The AP maps each wireless SSID to a VLAN on the wired Ethernet network.



Figure 18.16 The DS connects each BSS to the rest of the network, enabling wireless clients to communicate with hosts outside of their BSSs.

18.3.3 Extended service set
In a SOHO network, a single AP (typically a component of a wireless router) is usually sufficient. However, in most enterprise sites (i.e., an office), the range of a single AP isn’t enough to provide signal coverage for the entire site. To expand a wireless LAN beyond the range of a single AP, we use an extended service set (ESS).

An ESS links multiple BSSs through a DS. Each BSS in an ESS is identified by its own BSSID (the MAC address of the AP), but all operate using the same SSID. Figure 18.17 shows an ESS consisting of three BSSs.



Figure 18.17 An ESS consisting of three BSSs. Each BSS shares the same SSID, but has a unique BSSID. A client can roam seamlessly between BSSs.

Note Notice that each BSS uses a different non-overlapping channel to avoid interference—specifically, the 1–6–11 pattern we covered previously.

To the user, the ESS appears as a single wireless network. Using figure 18.17’s example, once a user connects to Jeremy’s Wi-Fi, they can move freely throughout the office space without needing to manually reconnect to the network. As the user moves away from the current AP and its signal weakens, the client device will automatically decide to switch to a new AP with a stronger signal, joining its BSS instead of the previous one. This process of passing between BSSs in an ESS is called roaming.

Note To provide a seamless roaming experience without temporary loss of connectivity, each AP’s cell should overlap by about 10% to 15% (some recommend 20%).

18.3.4 Mesh basic service set
In most cases, each AP has its own wired connection to the DS. But in environments where it is impractical or too costly to run an Ethernet cable to each AP, a mesh basic service set (MBSS) provides a flexible solution. An MBSS connects multiple APs wirelessly, forming a mesh of APs that can relay data between wireless clients and the DS without each AP requiring a wired connection to the DS. Figure 18.18 illustrates an MBSS.



Figure 18.18 An MBSS is a mesh of wireless connections between two types of APs, RAPs and MAPs, that allows them to relay data to and from wireless clients.

Note In an MBSS, an AP connected to the DS is a root access point (RAP), and an AP not connected to the DS is a mesh access point (MAP).

Ideally, each AP in an MBSS should have two radios tuned to two different channels: one dedicated to providing a BSS to serve wireless clients and one dedicated to relaying frames between wireless clients and the DS over the mesh. A single-radio AP can participate in an MBSS but with greatly reduced performance; its single radio has to perform both jobs.

18.4 Additional AP operational modes
APs can operate in various specialized roles outside of simply providing a BSS for wireless clients. An AP participating in an MBSS is an example; in addition to providing a BSS for wireless clients, the AP forms a mesh with other APs to relay frames between them. In this section, we’ll look at three more specialized AP operational modes: repeater, workgroup bridge, and outdoor bridge.

18.4.1 Repeater
A repeater is an AP used to extend the range of a wireless network. An AP configured as a repeater takes the signal from a main AP and retransmits it to areas outside of the main AP’s cell range. This mode is particularly useful in large homes or offices where the coverage of a single AP might not be sufficient. Figure 18.19 shows an AP in repeater mode (AP2) extending AP1’s cell.

Repeater APs might remind you of an MBSS. While both repeater APs and APs in an MBSS extend wireless coverage, they serve different network topologies and function differently. A repeater AP is typically a standalone device that extends the range of a single AP without the need for additional configuration or infrastructure. In contrast, a mesh AP is part of a larger mesh network where each AP intelligently routes traffic through the best path within a web of interconnected APs.



Figure 18.19 AP2, in repeater mode, extends AP1’s cell by repeating (retransmitting) wireless signals it receives.

Note A repeater AP can significantly reduce the performance of a wireless LAN. By retransmitting the main AP’s signal, the repeater occupies additional airtime for each packet, reducing the network’s overall data throughput—the rate at which data can be transferred over the network.

18.4.2 Workgroup bridge
Not all devices have wireless capabilities. If such a device needs to connect to the network, but running a cable to the nearest switch is not feasible, an AP operating as a workgroup bridge (WGB) can be used to connect the wired device to a wireless LAN. The wired device connects to the WGB via an Ethernet cable, and the WGB functions as a client of a main AP on behalf of the wired device, effectively allowing it to participate in the wireless LAN despite having no wireless capabilities. Figure 18.20 shows how it works.



Figure 18.20 AP2, in WGB mode, functions as a client of AP1 to provide network access to PC1, which does not have wireless capabilities.

Note A WGB can support multiple wired devices—not just one. However, if the main AP (AP1 in figure 18.20) is not a Cisco AP, the WGB will have to operate in Universal WGB (uWGB) mode, which only supports a single wired device.

18.4.3 Outdoor bridge
Laying cabling between buildings across a campus or city can be quite expensive. An alternative is to connect remote sites wirelessly with APs operating as outdoor bridges. Outdoor bridges connect separate LANs over long distances, and are ideal for campus or metropolitan settings, connecting buildings without the need for physical cabling. Figure 18.21 demonstrates a point-to-point outdoor bridge setup connecting two sites. However, a point-to-multipoint setup, in which multiple sites connect to a central site, is also possible.



Figure 18.21 APs functioning as outdoor bridges can connect LANs wirelessly over long distances.

Note Outdoor bridges use directional antennas to focus the wireless signal, allowing the signal’s strength to be maintained over longer distances than normally possible.

Outdoor bridges can be established over many kilometers. However, the maximum distance varies greatly depending on the hardware and various external conditions; for example, clear line of sight between the two APs is essential.

Summary
Wireless LANs (sometimes abbreviated as WLANs) are defined by the IEEE 802.11 family of standards. It defines standards at Layers 1 and 2 of the TCP/IP model.

Copper and fiber-optic cables are bounded media; the signals are confined to the cables, providing a controlled pathway for data transmission.

The air used to transmit wireless signals is an unbounded medium; the signals propagate freely in open space, radiating in all directions from the source.

All devices in range of a wireless device can receive its signals, making security a major concern.

Wireless devices must contend for airtime. If two devices transmit at the same time, a collision occurs. Wireless devices use Carrier-Sense Multiple Access with Collision Avoidance (CSMA/CA) to avoid collisions.

Wireless signals are vulnerable to interference, for example, from neighboring wireless LANs, microwave ovens, cordless phones, and Bluetooth devices.

The complexity of national and international regulations means that the same devices can’t always be used in different countries.

Coverage area is an essential consideration in wireless LANs. As wireless signals propagate through space, they lose strength; this is called free-space path loss (FSPL). Devices will be unable to receive the signal if it is too weak.

Electromagnetic waves are influenced by the media they pass through and the objects they encounter.

Absorption occurs when a wave passes through a medium and is converted into heat, resulting in signal attenuation (weakening).

Reflection happens when a wave bounces off a surface.

Refraction occurs when a wave passes from one medium to another with a different density, altering the wave’s speed and causing it to bend.

Diffraction is the bending and spreading of waves around the edges of an obstacle.

Scattering occurs when a wave encounters a surface or medium with irregularities that causes the wave to spread out erratically.

To send a wireless signal, a device applies an alternating electric current to an antenna, which in turn produces fluctuating electromagnetic fields that radiate out as waves; these are called electromagnetic waves.

Amplitude is the maximum strength of the electric and magnetic fields of a wave and is associated with how much energy the wave carries; higher amplitude means a stronger signal.

Frequency measures how often the strength of the wave’s electric and magnetic fields oscillates and is measured in hertz (Hz)—oscillations per second.

1 kHz (kilohertz) = 1000 Hz, 1 MHz (megahertz) = 1,000,000 Hz, 1 GHz (gigahertz) = 1,000,000,000 Hz, 1 THz (terahertz) = 1,000,000,000,000 Hz.

Period is the amount of time it takes for one full oscillation. If the frequency is 4 Hz (four oscillations per second), the period is 0.25 seconds.

In wireless LANs, higher frequencies can typically support higher data transfer rates and are less crowded with other wireless devices, but are more susceptible to absorption by obstacles (i.e. walls). Lower frequencies typically support lower data transfer rates and are more crowded, but penetrate better through obstacles.

The electromagnetic spectrum is the entire range of electromagnetic radiation.

Radio frequency (RF) is a segment of the electromagnetic spectrum defined as ranging from around 20 kHz to around 300 GHz. Wireless LANs use three RF bands: the 2.4 GHz band, the 5 GHz band, and the 6 GHz band.

The 2.4 GHz band spans from 2.4 to 2.4835 GHz and is divided into 14 channels with a standard width of 20 MHz. Not all channels can be used in all countries.

There is significant overlap among the 2.4 GHz channels, so adjacent APs should use non-overlapping channels (1–6–11 or 1–5–9–13) to avoid interference.

The 5 GHz band ranges from approximately 5.150 to 5.895 GHz (depending on the country). Channels in this band are non-overlapping when using the standard 20 MHz width, simplifying the channel selection process.

Channels can be combined to form wider channels of 40, 80, or 160 MHz, supporting higher data transfer rates (although resulting in fewer channels).

The 6 GHz band is the newest addition to the 802.11 frequency bands, ranging from 5.925 GHz to 7.125 GHz, providing even more non-overlapping channels.

The standard channel width is 20 MHz, but channels can be combined to form wider 40, 80, 160, or 320 MHz channels.

New 802.11 standards are constantly in development to meet evolving demands.

The major generations of 802.11 standards and the RF bands they use are 802.11 (2.4 GHz), 802.11b (2.4 GHz), 802.11a (5 GHz), 802.11g (2.4 GHz), 802.11n (Wi-Fi 4, 2.4/5 GHz), 802.11ac (Wi-Fi 5, 5 GHz), 802.11ax (Wi-Fi 6, 2.4/5 GHz and Wi-Fi 6E, 6 GHz), and 802.11be (Wi-Fi 7, 2.4/5/6 GHz).

A service set is a group of devices that operate on the same wireless LAN and share the same service set identifier (SSID)—a human-readable label for the service set.

An independent basic service set (IBSS), also called an ad hoc wireless network, consists of wireless clients communicating directly with each other. An IBSS is useful for quick, temporary setups, but doesn’t scale beyond a few clients.

A wireless client is any device that connects to a wireless LAN.

In a basic service set (BSS), clients connect to a wireless access point (WAP or AP), which coordinates the communication between wireless clients and serves as the gateway to other network resources, such as a wired LAN or the internet.

Clients in a BSS must communicate via the AP, not directly with each other.

An AP’s coverage area is called a basic service area (BSA) or cell.

A BSS’s SSID does not have to be unique. Instead, a basic service set identifier (BSSID) serves to uniquely identify the BSS. The BSSID is usually the MAC address of the AP’s radio.

A single AP can provide more than one BSS. However, if the AP only has a single radio, all BSSs must share the same channel.

Most wireless LANs serve as a way for wireless clients to connect to the wired network infrastructure (an Ethernet LAN). 802.11 calls the wired network infrastructure the distribution system (DS).

The AP maps each wireless SSID to a VLAN on the wired Ethernet LAN, serving as a bridge connecting the two mediums.

An extended service set (ESS) links multiple BSSs through a DS, expanding the coverage area. Each BSS shares an SSID, but has a unique BSSID.

In an ESS, each AP’s cell should overlap by about 10%–15% to allow clients to seamlessly roam among the BSSs without losing connectivity. Neighboring BSSs should use non-overlapping channels.

A mesh basic service set (MBSS) connects multiple APs wirelessly, forming a mesh of APs that can relay data between wireless clients and the DS without each AP requiring a wired connection to the DS.

In an MBSS, an AP connected to the DS is a root access point (RAP), and an AP not connected to the DS is a mesh access point (MAP).

A repeater is an AP used to extend the range of a wireless network. An AP configured as a repeater takes the signal from a main AP and retransmits it to areas outside of the main AP’s coverage area.

An AP functioning as a workgroup bridge (WGB) allows a wired device without wireless capabilities to communicate over a wireless LAN.

The wired device connects to the WGB via an Ethernet cable, and the WGB functions as a client of a main AP on behalf of the wired device.

APs operating as outdoor bridges can be used to connect geographically separated LANs wirelessly without the need for physical cabling.

Outdoor bridges use directional antennas to focus the wireless signal, allowing the signal’s strength to be maintained over longer distances than normally possible.