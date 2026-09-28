22 Network automation
This chapter covers

Network automation and its benefits
The three logical planes of networking functions
Software-defined networking architecture and solutions
Cisco DNA Center-enabled network management
Enterprise networks can potentially have hundreds, or even thousands, of routers, switches, firewalls, and other network infrastructure devices. In the past, deploying, managing, and maintaining such large networks was very labor intensive, requiring manual configuration of each individual device. However, modern enterprises are increasingly adopting automation to streamline the deployment, management, and maintenance of their networks.

In this chapter, we will take a high-level look at the topic of network automation as a whole and the advantages it offers, allowing networks to scale to meet the needs of modern organizations. We will then move on to look at software-defined networking (SDN), an approach to networking that centralizes network intelligence in one or more controllers, facilitating the management and operation of the entire network with a programmatic approach. We will cover the following CCNA exam topics:

1.1.e Controllers

6.1 Explain how automation impacts network management

6.2 Compare traditional networks with controller-based networking

6.3 Describe controller-based and software-defined architectures (overlay, underlay, and fabric)

6.3.a Separation of control plane and data plane

6.3.b North-bound and South-bound APIs

6.4 Explain AI (generative and predictive) and machine learning in network operations

22.1 The benefits of network automation
What does it mean to automate a network? The term network automation doesn’t refer to any particular tool or technology but rather a broad category of techniques and methods used to automate network-related tasks. At its core, network automation involves the use of software to create processes that perform various network tasks without the need for manual intervention. This can range from simple scripts for routine tasks to more complex automation platforms that manage multiple interdependent configurations across a variety of devices.

To understand the benefits of network automation, consider this situation. Your company has added a new server that functions as a Syslog server and SNMP manager, gathering logging and status updates from devices in the network. As a junior network engineer, it’s your job to add the necessary configurations to each device. That involves connecting to each device one by one using SSH and making the following configurations:

R1# configure terminal
R1(config)# logging host 192.0.2.1                                 ❶
R1(config)# snmp-server host 192.0.2.1 version 2c ComMun1tyS7R1ng! ❷
R1(config)# end
R1# copy running-config startup-config                             ❸
❶ Configures the new Syslog server

❷ Configures the new SNMP manager

❸ Saves the configuration changes

Adding two new commands to and saving a device’s configuration isn’t such a cumbersome task, and a manual approach is fine if the network has only a few devices. But what if the network consists of thousands of routers and switches? Manually configuring each device one by one would not only take a long time, but it would likely result in mistakes: mistyped IP addresses on some devices, unsaved configurations on others—human error is inevitable. Figure 22.1 shows a better approach: using a Python script, you can reliably and accurately push the necessary configurations to each device in a fraction of the time.



Figure 22.1 Pushing configurations to devices with a Python script. Automating repetitive tasks provides greater accuracy and efficiency.

Writing and interpreting scripts in Python (or any other language) isn’t part of the CCNA exam, but for reference, the following example shows how you could accomplish this using Python. Using a library (basically, a set of tools) called Netmiko, I wrote a script to log in to a series of devices and apply the specified commands to each:

from netmiko import ConnectHandler                            ❶
 
devices = [                                                   ❷
    {"device_type": "cisco_ios", "host": "R1",                ❷
➥"username": "admin", "password": "pW12!"},                  ❷
    {"device_type": "cisco_ios", "host": "R2",                ❷
➥"username": "admin", "password": "pW12!"}                   ❷
]                                                             ❷
 
commands = [                                                  ❸
    "logging host 192.0.2.1",                                 ❸
    "snmp-server host 192.0.2.1 version 2c ComMun1tyS7R1ng!"  ❸
]                                                             ❸
 
for device in devices:                                        ❹
    print(f"Connecting to {device['host']}...")               ❹
    try:                                                      ❹
        with ConnectHandler(**device) as net_connect:         ❹
            output = net_connect.send_config_set(commands)    ❹
            print(output)                                     ❹
            net_connect.save_config()                         ❹
    except Exception as e:                                    ❺
        print(f"Failed to connect to {device['host']}: {e}")  ❺
 
print("Configuration complete.")                              ❻
❶ Imports the ConnectHandler class from the netmiko library

❷ Lists the devices to be configured (only two shown for brevity)

❸ Specifies the configuration commands

❹ Connects to each device, issues the commands, and saves the configuration

❺ Displays an error message for each failed connection

❻ Displays a message when the configurations are complete

As long as the script has been properly written, you can trust it to quickly and reliably make the specified configuration changes—no typos or other mistakes. Automation ensures that configuration changes are made accurately and in a fraction of the time required for manual configuration. By improving the efficiency of network operations, the opex (operating expenses—ongoing costs) of the network are reduced; fewer hours are required for each task.

Note Although automation can reduce opex, it doesn’t reduce capex (capital expenses—upfront costs). For example, automation doesn’t reduce the amount of hardware a network requires.

Automating configuration changes with Python scripts is just one example of network automation, but the scope of network automation extends beyond just scripting. Network automation encompasses a range of tools and methodologies aimed at making network design, deployment, and management more efficient, reliable, and scalable. In the next section, we’ll cover software-defined networking (SDN), a framework that enables and enhances network automation.

22.2 Software-defined networking
Software-defined networking (SDN) is a paradigm shift in the way networks are designed, managed, and operated. At its core, SDN is a type of network architecture that separates the network “brains”—the intelligent decision-making processes that determine how the network operates—from the “brawn”—the actual forwarding of messages across the network. In this section, we’ll clarify how these different elements work in traditional network architectures and then examine how SDN decouples these processes, centralizing network intelligence in controllers that facilitate the programmatic control of the network.

Note SDN is an example of controller-based networking. We looked at another example when covering wireless LANs: split-MAC architecture with a WLC.

22.2.1 The logical planes of network devices
A router routes packets and a switch switches frames, but that’s not all they do. Although the main purpose of these networking devices is forwarding messages across the network, they have various other functions and responsibilities that contribute to their main purpose. For example, here are some other things that routers do:

Use a routing protocol like OSPF to share routing information with other routers and build a routing table

Use ARP to build an ARP table, mapping IP addresses to MAC addresses

Use Syslog to keep logs of events

Use NTP to sync its time to a trusted NTP server

Function as an SSH server, allowing users to connect to and configure it via the CLI

There are many other examples. Think back to the various topics we’ve covered in this book, and I’m sure you’ll be able to list some more. All of these functions can be divided into three logical planes:

The Data Plane—Functions that are responsible for the actual forwarding of packets based on predetermined rules, handling the physical transmission of data across the network.

The Control Plane—Functions that control how the Data Plane operates, such as the processes that build a router’s ARP and routing tables.

The Management Plane—Functions related to configuring, managing, and monitoring devices.

Figure 22.2 illustrates these planes on three routers.



Figure 22.2 The three logical planes. The Data Plane involves forwarding messages, the Control Plane controls how the Data Plane functions, and the Management Plane includes all configuration/management tasks.

The Data Plane

The Data Plane includes all functions directly related to forwarding messages over the network: receiving a message on one interface, performing any necessary processing, and then forwarding it out of another interface. For example, on a switch, the Data Plane includes functions such as

Forwarding and flooding frames according to their destination MAC address and the switch’s MAC address table

Permitting or denying frames according to security features like Port Security, DHCP Snooping, or DAI

Tagging frames with 802.1Q before forwarding them over a trunk link

Figure 22.3 lists some equivalent Data Plane functions relevant to routers.



Figure 22.3 Data Plane functions on routers. All tasks directly involved in forwarding packets are part of the Data Plane.

Note The Data Plane is also called the Forwarding Plane because it is concerned with forwarding messages over the network.

The Data Plane functions according to a set of predetermined rules or instructions. For example, a router’s routing table can be thought of as a set of instructions: to forward a packet toward destination X, encapsulate it in a frame destined for next hop Y, and forward it out of interface Z. Establishing those rules and instructions is the responsibility of the next logical plane: the Control Plane.

The Control Plane

The Control Plane, as the name suggests, “controls” the Data Plane. Functions in the Control Plane are not directly involved in the process of forwarding messages but instead perform necessary overhead work to enable the Data Plane’s operations:

OSPF itself isn’t involved in the process of forwarding packets, but it allows the router to build its routing table, which is necessary for forwarding packets.

STP itself isn’t involved in the process of forwarding frames, but it informs the switch about which ports should and shouldn’t be used to forward frames.

ARP messages don’t contain user data but are used to build an ARP table, which is used in the process of forwarding data packets.

A switch’s MAC address-learning process (examining frames’ source MAC addresses) is separate from the frame-forwarding process but is necessary to build the switch’s MAC address table and enable frame forwarding.

To put it simply, Control Plane functions influence (but aren’t directly involved in) the message-forwarding process, whether it is routing packets at Layer 3 or switching frames at Layer 2. Figure 22.4 demonstrates how routers use OSPF and ARP in the Control Plane to facilitate the Data Plane’s packet-forwarding capabilities.



Figure 22.4 Control Plane functions influence (but aren’t directly involved in) the message-forwarding process.

Whereas the Data Plane is the “brawn” of the network—the set of processes that actually move messages across the network—the Control Plane is the “brains”—the set of processes that determine how messages should be moved across the network.

The Management Plane

The Management Plane includes a variety of functions that don’t directly influence the forwarding of messages. Instead, Management Plane functions are related to configuring, managing, and monitoring network devices. Some protocols whose functions are part of the Management Plane include

SSH/Telnet—Used to connect to the CLI of network devices

Syslog—Used to keep logs of events that occur on a device

SNMP—Used to monitor the operations of a device

NTP—Used to maintain accurate time across the network

Although Management Plane functions don’t directly influence the forwarding of messages in the Data Plane, actions performed in the Management Plane can influence the Control Plane, thereby having an indirect effect on the Data Plane. For example, OSPF configurations made via a device’s CLI (Management Plane) affect how a router shares routing information and calculates routes (Control Plane), influencing how the router forwards packets (Data Plane).

Note In the following discussion of SDN, we will focus primarily on the separation of the Data Plane and the Control Plane. Just remember the role of the Management Plane: the configuration, management, and monitoring of the network.

22.2.2 SDN architecture
In traditional network architectures, each individual network device contains the necessary intelligence that is required for Control Plane functions. For example, each router runs a routing protocol (such as OSPF), communicates with its neighboring routers, and independently calculates the best route to each destination it learns about. This is called a distributed Control Plane—the “brains” of the network are distributed among each individual network device.

However, SDN takes a different approach. Instead of a distributed Control Plane, SDN solutions employ a centralized Control Plane, concentrating some or all of the Control Plane functions in a controller. Figure 22.5 illustrates SDN architecture’s centralized Control Plane: instead of routers communicating with each other using OSPF (or another routing protocol) and independently calculating routes, the controller performs these tasks centrally. The controller has a global view of the network, applies its own routing logic, and distributes the necessary forwarding instructions to each device under its control. Each network device’s role is simply to forward messages according to the controller’s instructions.



Figure 22.5 SDN architecture centralizes the Control Plane functions in the controller. However, the Data Plane functions (message forwarding) remain distributed among each network device.

SDN facilitates the programmatic control of the network through applications that interact with the SDN controller. This results in a three-layer architecture, as shown in figure 22.6:

Application Layer—Consists of applications that communicate network requirements and desired behaviors to the SDN controller.

Control Layer—Translates the high-level requirements from the Application Layer into actionable instructions for the network devices.

Infrastructure Layer—The network devices like routers and switches that execute the commands received from the Control Layer.

SDN architecture relies on communication between its three layers: the Application Layer must communicate the network requirements and desired behaviors to the Control Layer, and the Control Layer must translate those high-level requirements into instructions that it communicates to the devices in the Infrastructure Layer. This communication is achieved using application programming interfaces (APIs)—software interfaces that facilitate communications between different applications—and various communication protocols.



Figure 22.6 The three layers of SDN architecture: Application, Control, and Infrastructure. The NBI facilitates communication between the Application and Control Layers, and the SBI facilitates communications between the Control and Infrastructure Layers.

The interface between the Application and Control Layers is called the northbound interface (NBI), and the interface between the Control Layer and the Infrastructure Layer is called the southbound interface (SBI). These names simply come from how the SDN architecture is usually depicted in diagrams: the Application Layer on top (north), the Control Layer in the middle, and the Infrastructure Layer at the bottom (south).

The NBI typically uses a representational state transfer (REST) API with HTTP messages; we will cover REST APIs (and APIs in general) in chapter 23. A variety of APIs and communication protocols can be used in the SBI, depending on the SDN solution. Here are some examples:

OpenFlow—An open source protocol that allows the controller to directly interact with and control the Data Plane of network devices.

NETCONF—An industry-standard protocol defined by the IETF and used for modifying the configurations of network devices.

OpFlex—Developed by Cisco and used with Application-Centric Infrastructure (ACI), their data center SDN solution.

SSH, SNMP—Traditional protocols such as SSH and SNMP can also be used in the SBI to manage network devices.

Exam Tip You don’t have to know the details about these different SBI types. For the CCNA exam, know that REST APIs are used in the NBI and protocols like OpenFlow, NETCONF, OpFlex, and traditional protocols like SSH and SNMP are used in the SBI.

22.2.3 Cisco SDN solutions
SDN isn’t one single solution. Cisco and other networking vendors have developed a variety of SDN solutions based on the principles we have covered so far. In this section, we’ll take a high-level look at three SDN solutions from Cisco:

Cisco Software-Defined Access (SD-Access)—Cisco’s SDN solution for wired and wireless campus LANs

Cisco SD-WAN—Cisco’s SDN solution for WANs

Application Centric Infrastructure (ACI)—Cisco’s SDN solution for data center networks

All three of these solutions work by building a virtual network of tunnels (the overlay) on top of the underlying physical network (the underlay). The combination of the underlay and the overlay—the network infrastructure as a whole—is called the fabric.

Note To keep these concepts clear, just remember that the underlay is physical and the overlay is virtual. The fabric is the network as a whole, including all physical and virtual elements.

SD-Access

Software-Defined Access (SD-Access) is Cisco’s SDN solution for automating and securing wired and wireless campus LANs, applying the SDN principles we covered previously to automate, streamline, and secure campus LANs. Figure 22.7 illustrates the SD-Access fabric, consisting of a physical network (the underlay) and a virtual network of tunnels (the overlay) using Virtual Extensible LAN (VXLAN)—a protocol that allows for the creation of virtual Layer 2 networks over a Layer 3 underlay.



Figure 22.7 The Cisco SD-Access fabric, consisting of a physical underlay of switches and a virtual overlay of VXLAN tunnels. Cisco Catalyst Center is the SDN controller.

Cisco Catalyst Center—often called DNAC—functions as the SDN controller in their SD-Access solution. However, Catalyst Center can also be used in non-SD-Access networks as a network management platform; we’ll examine Catalyst Center’s management capabilities in section 22.3.

Note Catalyst Center used to be called Digital Network Architecture (DNA) Center, but Cisco renamed it in 2023. I recommend knowing both names; you could encounter either on the exam.

Software-Defined WAN

Software-Defined WAN (SD-WAN) is Cisco’s SDN solution for WANs. SD-WAN works by creating an overlay of IPsec tunnels over any physical WAN underlay: the internet, Multiprotocol Label Switching (MPLS), cellular 4G/5G, satellite, etc. This fabric is managed by a few different SDN controllers: one dedicated to onboarding new routers into the fabric, one dedicated to Control Plane functions, and one dedicated to Management Plane functions. Figure 22.8 illustrates the Cisco SD-WAN fabric.



Figure 22.8 The Cisco SD-WAN fabric, consisting of a physical underlay of WAN connections and a virtual overlay of IPsec tunnels. The SD-WAN fabric is controlled by a few different SDN controllers.

Application-Centric Infrastructure

The final Cisco SDN solution we’ll look at is Application-Centric Infrastructure (ACI)—Cisco’s data center SDN solution (see figure 6.9). Like in SD-Access, ACI creates an overlay of VXLAN tunnels over the underlay. In this case, the underlay is a physical spine-leaf network.



Figure 22.9 The Cisco ACI fabric, consisting of a spine-leaf underlay and an overlay of VXLAN tunnels. The APIC is the SDN controller.

The SDN controller used in ACI is called the Application Policy Infrastructure Controller (APIC). The APIC is responsible for translating high-level network policies into specific network configurations and deploying them across the network fabric.

Exam Tip For the CCNA exam, you don’t need to know the details of these SDN solutions. However, exam topic 6.3 explicitly mentions overlay, underlay, and fabric, so make sure you understand those core concepts.

Intent-based networking

One of the advantages of SDN is that it facilitates intent-based networking (IBN). The goal of IBN is to allow the engineer to communicate their intent for network behavior to the controller, which will take care of the details of the actual configurations and policies on the devices. Instead of focusing on individual devices and CLI configurations, IBN allows you to focus on high-level policies. For example, an engineer might state the intent “I want to prioritize video conferencing traffic over other types.” The controller will then implement the necessary configurations across the network to make this a reality, without the engineer having to configure QoS settings on each device.

22.3 Artificial intelligence and machine learning
Artificial intelligence (AI) refers to the simulation of intelligence in computers, allowing them to exhibit behaviors typically associated with humans such as learning and problem-solving. AI systems are programmed to analyze data, identify patterns, and make predictions or take actions based on those insights. Machine learning (ML) is a field within AI that allows computers to learn on their own, without requiring explicit programming.

Ever since the public release of OpenAI’s ChatGPT in 2022, AI and ML seem to be on everyone’s mind, and for good reason; these technologies, still in their early stages, have the potential to revolutionize many aspects of our private and professional lives. They promise to enhance productivity, automate complex tasks, and provide insights that were previously unattainable. In the realm of network operations, AI and ML are already making significant impacts by enabling more efficiency in network management, improving security through advanced threat detection, and optimizing performance through predictive analytics. As these technologies continue to evolve, their integration into network operations will only continue to grow. In this section we’ll examine first examine ML, move on to cover predictive and generative AI, and finally consider their applications in modern network operations.

Exam Tip AI and ML’s applications in network operations are exam topic 6.4, so make sure you have a solid grasp of these concepts.

22.3.1 Machine learning
Machine learning (ML) is a subfield of AI that focuses on enabling computers to learn from data and improve without the need for explicit programming. Figure 22.10 shows ML’s position within the field of AI, as well as the position of deep learning—a topic we’ll explore later—as a further subset of machine learning.



Figure 22.10 Machine learning is a subfield of artificial intelligence. Deep learning is a further subset of machine learning using artificial neural networks.

Unlike traditional software that relies on predefined instructions, ML algorithms can identify patterns and relationships within data sets. With ML, computers can learn from vast data sets in a few different ways that we’ll look at in this section:

Supervised learning—The ML algorithm is trained on labeled data sets.

Unsupervised learning—The ML algorithm is trained on unlabeled data sets.

Reinforcement learning—The ML algorithm learns by interacting with an environment and receiving positive or negative feedback.

Supervised, unsupervised, and reinforcement learning

Supervised learning involves training an ML algorithm on a labeled data set, meaning that each training example input into the algorithm has a corresponding label. By examining these labeled examples, the algorithm learns the relationships between the data and the given label.

For example, if you want to train an algorithm to recognize images of cats and dogs, you could input thousands of cat and dog photos labelled as such. With enough examples, the algorithm will learn to identify and distinguish cats from dogs in images. Figure 22.11 illustrates how supervised learning works.



Figure 22.11 Supervised machine learning. Labeled data is input into the ML algorithm, allowing it to learn the relationships between the data and the given label.

Unsupervised learning takes a different approach, training the algorithm on unlabeled data sets. The algorithm tries to learn the underlying structure of the data by identifying patterns and relationships without any predefined labels.

Using the same example of cat and dog images, an unsupervised learning algorithm would analyze a large set of unlabeled photos of cats and dogs. It wouldn’t know in advance which images are of cats and which are of dogs. Instead, it would identify patterns in the images and group them into clusters based on these patterns. However, the algorithm wouldn’t assign the labels “cat” or “dog” to these clusters—that would require a human to interpret. Figure 22.12 shows how unsupervised learning works.

NOTE Supervised learning is highly effective when clear and accurate labels are available, enabling precise predictions and classifications. However, unsupervised learning is also powerful for uncovering hidden patterns and relationships in data without predefined labels. There is also a middle ground between supervised and unsupervised learning called semi-supervised learning that involves a combination of labeled and unlabeled data, leveraging the strengths of both approaches.



Figure 22.12 Unsupervised machine learning. Unlabeled data is input into the ML algorithm, allowing it to identify patterns and relationships, categorizing the data into clusters. A human can then assign labels according to their interpretation of the grouped data.

Reinforcement learning is a distinct approach in which an agent interacts with an environment, receiving positive for actions that lead to desirable outcomes and negative feedback for actions with undesirable outcomes. A classic example of reinforcement learning is training an AI to play a game like chess. The AI learns by playing many games, receiving positive feedback for winning and negative feedback for losing. Over time, it learns to develop strategies that increase its changes of winning.

Deep learning

Deep learning (DL) is a subset of machine learning that uses artificial neural networks to analyze and learn from large amounts of data. An artificial neural network is a computational model inspired by the way biological neural networks in the human brain process information, consisting of many interconnected layers of nodes like the neurons in the human brain.

Just like traditional traditional machine learning, DL’s artificial neural networks can be trained using supervised, unsupervised, semi-supervised, and reinforcement learning, but their complex architecture allows them to extract more complex patterns and relationships from data then traditional machine learning algorithms.

DL has gained prominence in recent years due to its success in tackling complex tasks such as image and speech recognition, natural language processing, and autonomous driving. The ability of deep learning models to process vast amounts of unstructured data and uncover intricate patterns has led to significant advancements in AI-driven technologies, such as large language models (LLMs) like OpenAI’s GPT-4, Google’s Gemini, and Meta’s Llama.

NOTE Just as DL’s artificial neural networks are many layers deep, DL itself is a very deep topic that the CCNA doesn’t dive into. For an interesting look into DL combined with reinforcement learning, check out this video on MarI/O, an AI trained to play the video game Super Mario World: https://www.youtube.com/watch?v=qv6UVOQ0F44.

22.3.2 Predictive and generative AI
Predictive and generative AI are two important applications of ML and DL. While ML and DL empower computers to autonomously learn from large data sets, predictive and generative AI apply these techniques to solve specific problems and create new opportunities. In this section, we will examine these two types of AI. Figure 22.13 shows the position of predictive and generative AI within the fields of ML and DL.



Figure 22.13 Predictive and generative AI are applications of machine learning and deep learning to predict future events and generate new content.

Predictive AI

Predictive AI uses historical data to predict future events. Using ML and DL to identify patterns and relationships within data sets, predictive AI leverages these insights to make predictions about unseen data, such as forecasting future weather patterns. In addition to weather forecasting, some other common use cases for predictive AI are:

Stock market predictions—Historical stock market data and economic indicators can be used to predict future stock prices and market trends.

Customer behavior analysis—E-commerce platforms use predictive AI to analyze customer purchase history and browsing behavior, enabling personalized recommendations.

Healthcare—Predictive AI can analyze patient data to predict patient outcomes and personalize treatment plans.

Generative AI

Generative AI leverages ML and DL to create new content. After learning the underlying patterns and relationships within existing data, the AI can then produce novel outputs that resemble the training data. Generative AI tools have become particularly popular within the past couple of years. Two well-known use cases for generative AI are:

Text generation—Chatbots like OpenAI’s ChatGPT and Google’s Gemini use large language models (LLMs) to generate human-like text based on input.

Image generation—Tools like Midjourney and OpenAI’s DALL-E create detailed images from text descriptions.

22.3.3 Applications in network operations
We’ve covered the basics of AI, including machine learning, deep learning, and the predictive and generative AI applications that leverage them. But what does all of this mean for our networks? As modern networks grow in complexity, AI is proving to be a key tool to make networks more efficient, reliable, and secure.

ML and DL can be used to analyze vast amounts of network data to uncover patterns, anomalies, and insights that are not immediately apparent to us humans. By processing and learning from historical and real-time data, these models can make intelligent decisions and predictions that improve network performance, enhance security, and automate routine tasks. Although we’re still in the early days of using AI in network operations, I think it’s safe to say that AI has the potential to bring network automation to the next level. In this section, let’s consider some applications of AI and ML in network operations.

Predictive AI in networks

Predictive AI can use historical network data to forecast future events, enabling proactive management and decision-making. Some applications of predictive AI in network operations are:

Traffic forecasting—AI models can analyze network traffic patterns to predict future network load. With this information, you can proactively provision additional network resources to accommodate anticipated traffic spikes or optimize QoS policies to prioritize important traffic.

Predictive maintenance—By analyzing data from network devices, AI models can identify potential hardware failures before they occur, enabling proactive maintenance scheduling and minimizing downtime.

Capacity planning—Predictive AI can help plan for future network capacity by analyzing trends in traffic and user behavior, allowing an enterprise to scale its network infrastructure to meet increasing demand.

Security threat prediction—By analyzing historical security data and identifying patterns associated with cyber attacks, predictive AI can forecast potential security threats.

Generative AI in networks

In its current state, generative AI has fewer use cases in networking than predictive AI; it’s too early to hand off your network to an AI and let it handle everything for you. However, let’s consider some uses cases for generative AI that, combined with human oversight, can greatly improve network operations.

Automated scipt creation—Generative AI can assist by generating scripts or templates for network automation tasks. To put that in other words, it can automate network automation!

Network diagram generation—AI tools can gather information about a network and automatically generate network diagrams.

Network documentation—In addition to visual diagrams, AI can analyze information about the network to generate other network documentation about configurations, policies, etc.

Device configuration—AI can generate device configurations based on given requirements, reducing manual effort and improving documentation accuracy.

Network design—Generative AI can assist in creating optimal network designs according to given requirements.

Virtual assistant—Chatbots like ChatGPT can function as a virtual assistant, providing real-time answers to queries. You should always be weary of accepting what a chatbot says as truth, but chatbots’ use as a tool is undeniable.

AI in Cisco Catalyst Center

Cisco Catalyst Center—the SDN controller in Cisco’s SD-Access solution—can also serve as a general network management platform outside of an SDN context. Catalyst Center includes several AI features such as:

AI endpoint analytics—This feature uses deep packet inspection and other techniques to identify endpoint devices when they access the network. It then classifies these endpoints and assigns policies based on their classification, enhancing network management and security.

AI enhanced radio resource management (RRM)—By analyzing past radio frequency (RF) data, Catalyst Center can predict future network conditions and recommend optimal configurations for wireless LANs. This helps to deliver a consistent user experience across the network without manual tuning.

Machine reasoning (MR) engine—This feature automates network troubleshooting. It uses AI to perform a root cause analysis when network issues arise. Furthermore, it can take corrective actions, potentially resolving problems without requiring manual intervention.

If you want to check out Catalyst Center, Cisco has an always-on sandbox that you can access at https://sandboxdnac.cisco.com with username “devnetuser” and password “Cisco123!”. You don’t have to be familiar with the Catalyst Center for the CCNA exam, but it’s worth eploring a bit to familiarize yourself with DNAC’s features.

Summary
Network automation is a broad category of techniques and methods used to automate network-related tasks, ranging from simple scripts for routine tasks to more complex automation platforms.

For example, a Python script can be used to reliably perform configuration changes on large numbers of devices in a fraction of the time required for manual configuration.

Traditional network devices perform a variety of functions on top of forwarding messages, such as building routing/ARP/MAC address tables, using Syslog to log events, and using SSH to accept remote CLI connections.

The various functions can be divided into three logical planes: the Data Plane, the Control Plane, and the Management Plane.

The Data Plane includes all functions directly related to forwarding messages over the network: receiving a message on one interface, performing any necessary processing, and then forwarding it out of another interface.

The Control Plane controls the Data Plane. Functions in the Control Plane are not directly involved in the process of forwarding messages but instead perform necessary overhead work to enable the Data Plane’s operations.

The Management Plane includes a variety of functions that don’t directly influence the forwarding of messages—functions related to configuring, managing, and monitoring network devices.

Traditional network architectures use a distributed Control Plane—the “brains” of the network (the Control Plane) are distributed among each network device. For example, each router uses OSPF to learn routes and build a routing table.

SDN takes a different approach, centralizing some or all of the Control Plane functions in a controller. This is called a centralized Control Plane.

In SDN architecture, each network device’s role is simply to forward messages according to the controller’s instructions. Although the Control Plane is centralized, the Data Plane remains distributed among the network devices.

SDN facilitates the programmatic control of the network through applications that interact with the SDN controller, resulting in a three-layer architecture consisting of the Application, Control, and Infrastructure Layers.

The Application Layer consists of applications that communicate network requirements and desired behaviors to the SDN controller.

The Control Layer translates high-level requirements from the Application Layer into actionable instructions for the network devices.

The Infrastructure Layer consists of network devices like routers and switches that execute the command received from the Control Layer.

Communication between the three layers is achieved using application programming interfaces (APIs) and various communication protocols.

The interface between the Application and Control Layers is the northbound interface (NBI). It typically uses a representational state transfer (REST) API with HTTP messages.

The interface between the Control and Infrastructure Layers is the southbound interface (SBI). A variety of APIs and communication protocols can be used in the SBI, such as OpenFlow, NETCONF, OpFlex, and traditional protocols like SSH and SNMP.

SDN isn’t a single solution. Cisco’s SDN solutions include SD-Access for wired and wireless campus LANs, SD-WAN for WAN networks, and Application Centric Infrastructure (ACI) for data center networks.

These SDN solutions work by building a virtual network of tunnels (the overlay) on top of the underlying physical network (the underlay). The combination of virtual and physical networks is called the fabric.

Software-Defined Access (SD-Access) is Cisco’s SDN solution for campus LANs. The SD-Access fabric consists of a physical underlay of switches and a virtual overlay of tunnels using Virtual Extensible LAN (VXLAN).

Cisco Catalyst Center, formerly called Digital Network Architecture (DNA) Center, functions as the SDN controller in SD-Access.

Software-Defined WAN (SD-WAN) is Cisco’s SDN solution for WANs. SD-WAN creates an overlay of IPsec tunnels over any physical WAN underlay: the internet, MPLS, cellular 4G/5G, satellite, etc.

Application-Centric Infrastructure (ACI) is Cisco’s data center SDN solution. Like SD-Access, ACI creates an overlay of VXLAN tunnels over the underlay, which is a physical spine-leaf network.

The SDN controller used in ACI is called the Application Policy Infrastructure Controller (APIC).

Artificial intelligence (AI) refers to the simulation of intelligence in computers, allowing them to analyze data, identify patterns, and make predictions or take actions based on those insights.

Machine learning (ML) is a field within AI that allows computers to learn on their own, without requiring explicit programming.

With ML, computers can learn from vast data sets in a few different ways:

Supervised learning—The ML algorithm is trained on labeled data sets.

Unsupervised learning—The ML algorithm is trained on unlabeled data sets.

Reinforcement learning—The ML algorithm learns by interacting with an environment and receiving positive or negative feedback.

Semi-supervised learning is a middle ground between supervised and unsupervised learning that involves a combination of labeled and unlabeled data.

Deep learning (DL) is a subset of machine learning that uses artificial neural networks to analyze and learn from large amounts of data. These neural networks can extract more complex patterns and relationships from data than traditional ML algorithms.

Predictive and generative AI are two important applications of ML and DL.

Predictive AI uses historical data to predict future events, such as weather forecasts and stock market predictions.

Generative AI leverages ML and DL to create new content, such as text and image generation.

ML and DL can be used to analyze vast amounts of network data to uncover patterns, anomalies, and insights.

Predictive AI has applications in network operations such as traffic forecasting, predictive maintenance, capacity planning, and security threat prediction.

Generative AI has applications in network operations such as automated script creation, network diagram generation, network documentation, deug-and-play deployments, and intent-based networking (IBN).