3 Cables, connectors, and ports
This chapter covers

The specifications and standards that allow computers to communicate
The fundamentals of traffic over a network
Types of wired connections and cabling standards
The uses of unshielded twisted pair and fiber-optic connections in networks
In chapter 2, we looked at a few diagrams showing network nodes connected with cables. In this chapter, we will look at the specific kinds of cables, connectors, and ports used to make those connections. These topics are part of section 1.0, Network Fundamentals, of the CCNA exam. Specifically, we will cover aspects of exam topic 1.3, which is as follows:

1.3 Compare physical interface and cabling types

1.3.a Single-mode fiber, multimode fiber, copper
1.3.b Connections (Ethernet shared media and point-to-point)
In the past, there have been many different ways to connect devices, and there still are. However, in modern networks, Ethernet reigns supreme and is by far the most common connection type. Perhaps you have heard of Ethernet before in reference to Ethernet cables. Ethernet is not one single thing but rather a collection of standards for physical wired connections as well as rules for communicating over those connections. In this chapter, we will look at two different kinds of physical connections between devices: those using copper cables and those using fiber-optic cables.

3.1 Network standards
In modern networks, someone in an office using a Dell PC connected to a Cisco switch can communicate with another person using an Apple MacBook connected to the Wi-Fi in Starbucks. The data is sent over the internet, possibly traveling over the infrastructure of multiple Internet Service Providers (ISPs), which use entirely different hardware. How is it possible that all of these devices, made by different companies, can communicate with each other? For this modern miracle, we can thank standards: sets of technical requirements and specifications that define the rules of communication in networks.
To demonstrate why these rules of communication are important, let’s forget about computers for a second and think about direct communication between humans. If an English speaker uses English to speak to a person who only understands Japanese, there isn’t going to be any communication at all. Each language, English and Japanese, has a different set of rules about how information should be communicated between people. Unless both speaker and listener agree on the rules, communication doesn’t happen.
Even if both parties understand English, they must agree on the medium of communication. If person A writes a message on a piece of paper, but person B closes their eyes and tries to listen to the message, the result is the same as in the previous example: communication doesn’t happen. For humans to be able to communicate with each other, we must agree on both the rules of communication and the medium of communication.
The same can be said of computers. For two computers to communicate, they must adhere to the same rules of communication—for example, how to format data when sending it over the network. There must also be rules governing the medium of communication: specifications for physical cables, connectors, and ports, as well as radio waves used in wireless communications.
There are several governing bodies that define the standards used in computer networks, and I’ll be mentioning a couple of them throughout this book’s two volumes. The main one relevant to this chapter is the Institute of Electrical and Electronics Engineers (IEEE, pronounced I-triple-E). In 1983, the IEEE first defined the IEEE 802.3 standard, better known as Ethernet.
Note The IEEE also defines the IEEE 802.11 standard, better (but not officially) known as Wi-Fi. IEEE 802.11 wireless LANs are a major topic of the CCNA exam and are covered in part 4 of volume 2 of this book.
Ethernet is not a single standard but rather a family of standards that define both physical aspects of network connections as well as how data should be formatted into messages to be sent over the network.

3.2 Binary: Bits and bytes
Terms like bit, byte, megabit, megabyte, etc. might be familiar to you, even if you’re not entirely sure what they mean (I certainly wasn’t before I started studying networking). You might even use the terms yourself, referring to a gigabit internet connection or a file that is X gigabytes in size. Depending on your age, you might even reminisce about your 56k (kilobit) internet connection.
To understand what these terms mean, we must define the term bit. A bit is the most basic unit of information used by computers. The word bit is simply a blend of the words binary digit. Binary is a number system that expresses all values using only two digits: 0 and 1. A byte, on the other hand, is simply a unit of 8 bits. Eight bits are equal to 1 byte.
Binary is the language of computers. They compute in binary, and they communicate in binary. Everything you see on a computer screen or hear from a computer speaker is a series of 0s and 1s interpreted by a computer and presented to you in a human-understandable format. That includes applications, photos, videos, songs, this book if you’re reading it in an electronic format, and everything else a computer does.
The CCNA, as a networking certification, is all about how computers communicate; that’s what networking is. When two computers connected by a cable communicate with each other, they are sending each other long (very long, by human standards) series of bits (0s and 1s) over that cable. In modern networks, they often send these bits at the rate of billions (with a “b”) per second. Exactly how these 0s and 1s are conveyed depends on the medium. For example, 0s and 1s can be communicated over copper wiring by modifying the voltage of an electric signal between the two devices. Voltage “x” represents a value of 0, and Voltage “y” represents a value of 1. Figure 3.1 illustrates this concept; as the router sends 1 byte of data to the switch via the cable connecting them, changes in the voltage of the signal are used to communicate values of 0 and 1.
Exam Tip Understanding the binary number system is very important for the CCNA exam. In future chapters of this volume, we will cover how to count in binary and how to convert between binary and other number systems like decimal and hexadecimal.

Figure 3.1 A router sends 1 byte of data to a switch. Changes in the voltage of the electric signal indicate values of 0 or 1.

We measure the speeds of network connections by how many bits can be transmitted per second over the connection. However, due to the incredible speeds of computer networks, we express these rates using larger units like kilobits, megabits, and gigabits. The following are some common units of measuring bits:
1 kilobit (kb) = 1,000 (thousand) bits
1 megabit (Mb) = 1,000,000 (million) bits (1,000 kilobits)
1 gigabit (Gb) = 1,000,000,000 (billion) bits (1,000 megabits)
1 terabit (Tb) = 1,000,000,000,000 (trillion) bits (1,000 gigabits)

Network speeds are then stated as X bits per second (bps)—for example, 56 kilobits per second (56 kbps), 100 megabits per second (100 Mbps), 10 gigabits per second (10 Gbps), 1 terabit per second (1 Tbps), etc.
1,000 or 1,024 bits?
There is some confusion over whether 1 kilobit is 1,000 bits or 1,024 bits, 1 megabit is 1,000 kilobits or 1,024 kilobits, etc. The definitions listed previously are correct, and they are the terms you should know for the CCNA. The 1,024 values are a result of the binary (base-2) number system; 210 is equal to 1,024. The correct terms for the base-2 values are
1 kibibit (1,024 bits)
1 mebibit (1,024 kibibits)
1 gibibit (1,024 mebibits)
1 tebibit (1,024 gibibits)
3.3 Copper UTP connections
The CCNA requires you to know about two kinds of wired connections: those using copper cables and those using fiber-optic cables. First, we will look at copper cables. This is the kind of network cable most often called an Ethernet cable, although the Ethernet standard makes use of both copper and fiber-optic cable types. Before we examine a copper Ethernet cable itself, let’s look at the connector at the end of the cable as well as the port it connects to on a network device, both of which are pictured in figure 3.2.

Figure 3.2 Two 8P8C ports on a Cisco switch (left) and an 8P8C connector on a copper UTP network cable (right)
Figure 3.2 shows the 8 position 8 contact (8P8C) connector of an Ethernet cable on the right. The name refers to the fact that there are eight pins on the connector: one for each of the eight wires inside of the cable. These connectors allow the cable to connect to ports like the ones shown on the left of figure 3.2. Another name for this kind of connector is RJ45 (RJ stands for Registered Jack); strictly speaking, this name is not correct, but it is commonly used when referring to Ethernet cables.
The type of cables used for these connections are called unshielded twisted pair (UTP) cables. There are also shielded twisted pair (STP) cables, but they are less common, so I will refer to them as UTP throughout this book. Each UTP cable contains eight individual wires inside, twisted together to make four pairs. Let’s examine the meaning of UTP:
Unshielded—The wires do not have a metallic shield around them. This shield can reduce electromagnetic interference (EMI) but is not present in UTP cables.
Twisted pair—The eight wires in the cable are twisted together to form four pairs of two wires each. The twisting of the wires reduces EMI between the wires of each pair.

3.3.1 IEEE 802.3 standards (copper)
The IEEE defines various standards for Ethernet connections that support different speeds, cable types (copper or fiber-optic), and distances. Each standard is referred to by a few different names:

One name is derived from the maximum supported transmission speed.
The name of the IEEE task group that defined the standard is also used to refer to the standard itself. These names begin with IEEE 802.3, followed by a letter.
The third name is an informal name given by the IEEE that indicates both the speed and cable type (standards for copper cabling end with T).
IEEE working groups and task groups
The IEEE assigns working groups to develop specific technologies. The two main working groups relevant to the CCNA are 802.3 (tasked with developing the Ethernet standard for wired networks) and 802.11 (wireless LANs, also known as Wi-Fi).
Within each working group, task groups are assigned to revise and continue developing upon the original standards. Each time a task group is formed, it is assigned a letter in serial order (i.e., 802.3a to 802.3z). Once all of the letters are used, an additional letter is added (i.e., 802.3aa to 802.3az). At the time of writing, 802.3dk is in development.

Table 3.1 lists some examples of Ethernet standards using copper cabling. Take note of the three names for each standard, as listed previously.
Table 3.1 A handful of Ethernet standards

| Speed    | Speed-derived name | IEEE task group | Informal name | Maximum cable length |
| -------- | ------------------ | --------------- | ------------- | -------------------- |
| 10 Mbps  | Ethernet           | IEEE 802.3i     | 10BASE-T      | 100 m                |
| 100 Mbps | Fast Ethernet      | IEEE 802.3u     | 100BASE-T     | 100 m                |
| 1 Gbps   | Gigabit Ethernet   | IEEE 802.3ab    | 1000BASE-T    | 100 m                |
| 10 Gbps  | 10 Gig Ethernet    | IEEE 802.3an    | 10GBASE-T     | 100 m                |

Exam Tip For the purpose of the CCNA exam, there is no need to memorize the IEEE task group names associated with each standard. You should be aware of the speed-derived and informal names, however.
Each of these standards supports a maximum cable length of 100 meters. Attempts to use UTP cables longer than the listed maximum can result in signal attenuation and decreased performance. Maximum cable length can be a problem for copper UTP connections. As you’ll see in section 3.4, increased maximum cable length is a major advantage of fiber-optic cables over copper UTP cables.
Note The cables used in the aforementioned Ethernet standards are not actually defined by the IEEE but rather by two other organizations: the Electronic Industries Alliance (EIA) and the Telecommunications Industry Association (TIA). So the name “Ethernet cable” isn’t very accurate because the cables, although used by Ethernet, are not defined by IEEE 802.3.
The standards for these cables are given names like Category 5, which is often shortened to Cat 5. Table 3.2 lists some cable standards that can be used with the aforementioned Ethernet standards.
Table 3.2 Common UTP cable standards


| Speed    | Ethernet informal name | Cable name |
| -------- | ---------------------- | ---------- |
| 10 Mbps  | 10BASE-T               | Cat 3      |
| 100 Mbps | 100BASE-T              | Cat 5      |
| 1 Gbps   | 1000BASE-T             | Cat 5e     |
| 10 Gbps  | 10GBASE-T              | Cat 6a     |


3.3.2 Straight-through and crossover cables
Although these days all UTP cables used for network communications have four pairs of wires (eight wires), not all of the Ethernet standards use all four pairs of wires:
10BASE-T uses two pairs (four wires).
100BASE-T uses two pairs (four wires).
1000BASE-T uses four pairs (eight wires).
10GBASE-T uses four pairs (eight wires).
Each wire inside of the cable is connected to one of the eight pins of the 8P8C connector. For devices to communicate over these wire pairs, each wire pair forms an electrical circuit between the two connected devices. In 10BASE-T and 100BASE-T connections, it is very important to use the proper cable to ensure that the wires connect the pins on one end of the connection to the correct pins on the other end of the connection. To facilitate that, there are two kinds of cables we can use: straight-through and crossover. These cable types differ in which pins on one end of the cable connect to which pins on the other end of the cable.
Straight-through cables
10BASE-T and 100BASE-T use two wire pairs, one for each direction of communication. The two wire pairs are
The pair connected to pins 1 and 2
The pair connected to pins 3 and 6 (yes, it’s 3 and 6, not 3 and 4)
This is shown in figure 3.3, in which a PC and a switch are connected via a UTP cable. Pins 1 and 2 on the PC connect to pins 1 and 2 on the switch. Likewise, pins 3 and 6 on the PC connect to pins 3 and 6 on the switch.

Figure 3.3 A PC and a switch connected via a straight-through cable
When devices are connected with a straight-through cable, a pin pair on one connector connects to the same pin pair on the other connector. This works well when connecting a PC to a switch. As shown in figure 3.3, PCs use the 1–2 pin pair to transmit data (this is often shortened to Tx), and switches use the 1–2 pin pair to receive data (often shortened to Rx). Likewise, switches use the 3–6 pin pair to transmit data, and PCs use the 3–6 pin pair to receive data.
However, what would happen if two switches were connected? Or two PCs? Or two routers? In these cases, using a straight-through cable would cause problems, as shown in figure 3.4.

Figure 3.4 Two routers connected via a straight-through cable. Because both routers transmit data using the same pin pair, communication fails.
When two devices that transmit using the same pin pair are connected with a straight-through cable, they will not be able to communicate. The Tx pins of one device are connected to the Tx pins of the other device. For devices like this to communicate, they need a cable that is wired differently: a crossover cable.

Crossover cables
A crossover cable connects opposite pin pairs; pins 1 and 2 on one end of the cable connect to pins 3 and 6 on the other end. This allows devices that transmit data on the same pin pair to communicate with each other. As figure 3.5 shows, devices that transmit using the same pin pair can communicate with each other when connected with a crossover cable.

Figure 3.5 Two routers connected via a crossover cable. The Tx pin pair of one router connects to the Rx pin pair of the other router.
Table 3.3 lists some common network device types and which pins they use to transmit and receive data. To put it simply, switches transmit on pins 3 and 6 and receive on pins 1 and 2. All other devices are the opposite.
Table 3.3 Common device types and their Tx/Rx pin pairs


| Device type | Transmit (Tx) pins | Receive (Rx) pins |
| ----------- | ------------------ | ----------------- |
| Router      | 1 and 2            | 3 and 6           |
| Firewall    | 1 and 2            | 3 and 6           |
| PC/Server   | 1 and 2            | 3 and 6           |
| Switch      | 3 and 6            | 1 and 2           |


Note Although 10BASE-T and 100BASE-T only use two wire pairs, there are still four wire pairs inside of the cable. The remaining two wire pairs are unused.
Auto MDI-X
Now that we’ve covered straight-through and crossover cables, I would like to share some good news: on modern networking equipment, we don’t have to worry about using the correct cable type. That’s because of a feature called Auto Medium-Dependent Interface Crossover (Auto MDI-X). Auto MDI-X allows a device to change which pins it will use to transmit and receive data depending on the device they are connected to. You should know about straight-through and crossover cables as a potential exam question, but in the field, you probably won’t have to think about whether a cable is straight-through or crossover.

Figure 3.6 demonstrates this concept. The two routers are connected via a straight-through cable. Routers typically transmit data on the 1–2 pair and receive data on the 3–6 pair, but thanks to Auto MDI-X, the router on the right reverses that; it transmits data on the 3–6 pair and receives data on the 1–2 pair.
Figure 3.6 Two routers connected via a straight-through cable. The router on the right uses Auto MDI-X to adjust which pins it uses to transmit and receive data.
1000BASE-T and 10GBASE-T
1000BASE-T and 10GBASE-T take advantage of all eight wires in a cable, so a total of four wire pairs are used. The same 1–2 and 3–6 pin/wire pairs are used as in 10BASE-T and 100BASE-T. The remaining two pairs are the pair in positions 4 and 5 and the pair in positions 7 and 8. This is shown in figure 3.7.

Figure 3.7 Pin and wire pairs used on 1000BASE-T and 10GBASE-T connections. All eight wires of the cable are used.
Additionally, instead of a device using each pair of wires exclusively for transmitting or receiving data, each wire pair can be used for both purposes simultaneously.
If a crossover cable is used, the 1–2 and 3–6 pairs are crossed over as in 10BASE-T and 100BASE-T, and the new 4–5 and 7–8 are crossed over as well. However, thanks to Auto MDI-X, we no longer have to worry about selecting the proper cable type.

3.4 Fiber-optic connections
Copper UTP connections are still the most common type of connection within a LAN. Both the cables and the switch ports themselves are fairly inexpensive, and they are supported by nearly all modern devices that connect to a network. However, there is a major limitation that can make copper connections unfeasible in some cases: the maximum cable length of 100 meters. For connections between devices on the same floor of a building, 100 meters is usually more than enough, but for some connections between devices on separate floors, it might not suffice. And certainly, for connections between buildings and WAN connections, the next type of cabling is preferred: fiber-optic cabling.

Fiber-optic cables, instead of transmitting electrical signals along a copper wire, transmit light signals along a glass fiber. The glass fiber used is more flexible than you might think of when you imagine glass, but still, fiber-optic cables must be handled with care; a sharp bend in the cable can damage the glass fiber, rendering the cable unusable. Even if the glass fiber doesn’t snap, bending the cable can cause light to leak out of the cable, resulting in a weakening of the signal.

3.4.1 The anatomy of a fiber-optic cable
A typical fiber-optic connection does not use a single cable but rather two: one for transmitting data and one for receiving data. These cables connect to a Small Form-Factor Pluggable (SFP) transceiver that is inserted into an SFP port on the device. SFP transceivers are modular and must be purchased separately from the device itself (and you’d probably be surprised at how much those little things cost).
Figure 3.8 shows a Cisco switch with a couple of SFP transceivers: one inserted into an SFP port and one on top of the switch. Notice that two cables connect to the SFP transceiver, not one. When connecting two devices with fiber-optic cables, it’s important to connect the cables correctly: one device’s transmitter must connect to the other device’s receiver; otherwise, communication is not going to happen (similar to correctly selecting straight-through/crossover cables when connecting devices that don’t support Auto MDI-X).
Figure 3.8 A Cisco switch with an SFP transceiver inserted into one of its SFP ports. An additional SFP is placed on top of the switch.
As shown in figure 3.9, there are a few layers to a fiber-optic cable. An outer jacket (4) and buffer (3) serve to protect and contain the inner components. A layer of reflective cladding (2) helps carry the light signal along the glass core (1). The core is a very thin glass fiber, although the thickness of the core depends on the type of cable.

Figure 3.9 The typical structure of a fiber-optic cable. An outer jacket (4) and buffer (3) serve to protect and contain the inner components. A layer of reflective cladding (2) helps carry the light signal along the glass core (1).
All types of fiber-optic cabling can carry a signal farther than copper cabling, but even within the category of fiber-optic cabling, the maximum supported length can vary greatly. There are two main types of fiber-optic cabling: multimode fiber (MMF) and single-mode fiber (SMF). Figure 3.10 shows how light travels along MMF and SMF cables.

Figure 3.10 Light travels down an MMF cable at multiple angles (modes), whereas light travels down SMF cables at a single angle.
MMF cables have a wider core than single-mode fiber cables. They are used in combination with LED transmitters that send light down the cable at multiple angles (modes), reflecting off of the cladding. MMF cables typically support maximum distances of several hundreds of meters.
SMF cables use a very narrow core in combination with laser transmitters that send light down the cable at a single angle. These laser transmitters are typically more expensive than the LED transmitters used by MMF cables. However, SMF cables also support much greater maximum distances: up to tens of kilometers.

3.4.2 UTP vs. fiber
Fiber-optic connections support much greater distances than copper UTP cables but at increased cost (largely due to expensive SFP transceivers). Both connection types are in common use in modern networks. UTP connections are most common for connections from switches to end hosts. In an office setting, there are generally switches on each floor, and the 100-meter maximum cable length is usually sufficient for end hosts to reach a switch on their floor. On the other hand, fiber-optic connections are more common for connections between network infrastructure—for example, connecting switches and routers that are located on separate floors or in separate buildings.
However, fiber cabling has a couple more advantages over copper UTP: one is that copper UTP cables are vulnerable to EMI. This is generally not a concern, but in environments with lots of electrical equipment, EMI can negatively affect the signals traveling along a UTP cable. A second disadvantage is that copper UTP cables can emit (leak) their signal outside of the cable. This leaked signal is quite weak, but it’s possible that it can be detected and read, posing a security risk.
The most common considerations for whether to use copper UTP or fiber cabling are maximum distance, cost, and which connection type is supported by the devices to be connected. Most client devices (such as PCs) do not have SFP ports that can be used for fiber-optic connections, so a UTP connection is the only choice.

Summary
Standards provide agreed-upon sets of rules for communication over networks.
Ethernet is a family of standards defined by the Institute of Electrical and Electronics Engineers (IEEE) 802.3 working group. It defines standards for communication over physical wired connections.
Computers compute and communicate using binary: 0s and 1s. Each binary digit is called a bit, and a group of 8 bits is called a byte.
Network speeds are measured in bits per second using units like kilobit (1,000 bits), megabit (1,000 kilobits), gigabit (1,000 megabits), and terabit (1,000 gigabits).
The most common connection type in Ethernet LANs uses copper unshielded twisted pair (UTP) cables. Unshielded means the wires in the cable do not have a metallic shield around them to protect against electromagnetic interference (EMI). Twisted pair means the eight wires in the cable are twisted together to form four pairs of two wires. The twisting of the wires reduces EMI between the wires of each pair.
UTP cables use 8 position 8 contact (8P8C) connectors, also known as Registered Jack-45 (RJ45).
10BASE-T and 100BASE-T connections use two of the four wire/pin pairs in a UTP cable, and 1000BASE-T and 10GBASE-T connections use all four pairs. All connection types support a maximum cable length of 100 meters.
In 10BASE-T and 100BASE-T connections, different device types send and receive data using different pins of the connector; however, Auto MDI-X allows devices to automatically adjust which pins to use for which purpose.
Fiber-optic cables send light signals down a glass fiber core and support much greater maximum distances than UTP cables.
Single-mode fiber (SMF) cables support greater maximum distances (tens of kilometers) than multimode fiber (MMF) cables (hundreds of meters), but the laser-based small form factor pluggable (SFP) transceivers used by SMF connections are more expensive than the LED-based transceivers used by MMF connections.
Fiber-optic connections are more expensive than copper UTP connections, largely due to the cost of the SFP transceivers.
UTP connections are more common between end hosts and switches because of their lower cost and because the 100-meter maximum cable length is usually sufficient. Additionally, most client devices (such as PCs) only support UTP connections.
Fiber-optic connections are more common between network infrastructure devices because of the increased maximum cable length. Network devices often connect to other network devices on different floors and in different buildings.