17 Virtualization and cloud
This chapter covers

Virtualization with virtual machines and containers
Dividing a router into multiple virtual routers with Virtual Routing and Forwarding
Cloud computing and its characteristics, service models, and deployment models
Virtualization and cloud computing are two technologies that have transformed modern IT infrastructure. Virtualization refers to a variety of technologies that enable you to create virtual versions of something—servers, routers, etc.—that are abstracted from the underlying physical hardware. Taking advantage of the flexibility of virtualization, cloud computing provides on-demand computing services that can be accessed remotely over a network and scaled to meet user demands.

In this chapter, we will delve into server virtualization with virtual machines (VMs), a technology that allows multiple virtual servers to run on a single physical server. We will also look at containers, a technology that runs applications in isolated environments offering flexibility, portability, and efficient resource usage. We will then explore Virtual Routing and Forwarding (VRF), which divides a single physical router into multiple virtual routers. Finally, we will cover the concept of cloud computing and the various service models used by modern enterprises of all sizes. Here are the CCNA exam topics we will address:

1.2 Describe characteristics of network topology architectures

1.2.f On-premises and cloud

1.12 Explain virtualization fundamentals (server virtualization, containers, and VRFs)

17.1 Virtual machines and containers
Before we delve into VMs and containers, think back to a technology we previously covered that includes the word “virtual”: virtual LANs (VLANs). Figure 17.1 shows how VLANs segment a single physical network into multiple distinct logical networks. Although all six PCs are connected to the same physical switch and are therefore in the same physical LAN, they are grouped into three different VLANs. Hosts in one VLAN cannot communicate directly with hosts in another VLAN, despite being physically connected to the same switch.



Figure 17.1 VLANs create distinct virtual LANs from a single physical LAN.

We covered another “virtual” technology in the previous chapter: virtual private networks (VPNs). As shown in figure 17.2, VPNs overlay private networks on top of shared infrastructure like the public internet, creating secure tunnels between devices. VPNs are distinct virtual networks that enable secure communication over a shared physical network.

VLANs and VPNs are both examples of network virtualization—creating logically separate networks on shared physical infrastructure. This concept of virtualization extends beyond networking into the realm of computing resources with the topics of this section: VMs and containers. These technologies allow operating systems and applications to run in isolated environments on a single physical server.



Figure 17.2 A VPN is a secure virtual network created over a physical network.

Exam Tip The CCNA, as a networking certification, places less emphasis on VMs and containers than network virtualization technologies. However, they are part of CCNA exam topic 1.12: Explain virtualization fundamentals (server virtualization, containers, and VRFs), so make sure you have a solid grasp of the basics that we will cover.

17.1.1 Virtual machines
In the past, a physical server would run a single operating system (OS)—for example, Windows Server or some variety of Linux. This meant that all of the hardware resources—CPU, RAM, storage, etc.—were tied to that one OS and its applications. This often led to resource underutilization, as the dedicated hardware could far exceed the needs of the single OS and its applications—modern server hardware can be very powerful. Figure 17.3 shows this traditional setup: one OS and its apps running on top of the server hardware.



Figure 17.3 A physical server running one OS and its apps

Server hardware is quite expensive, and in addition to the cost of the hardware itself, each server requires physical space, cooling, and electrical power. A data center full of underutilized servers is not an efficient use of these resources. Virtualization addresses inefficiencies like these by consolidating servers and maximizing resource utilization.

Virtual machines break the one-to-one relationship of hardware to OS, allowing multiple OSs to run on a single physical server. This is facilitated by a hypervisor, a layer of software that allows multiple operating systems to share a single hardware host. It sits between the hardware and the VMs, managing and allocating the hardware resources (CPU, RAM, Storage, etc.) to each VM. There are two main types of hypervisors:

Type 1 hypervisors run directly on top of the hardware.

Type 2 hypervisors run as an application on a host OS.

Note Another name for a hypervisor is virtual machine monitor (VMM).

Type 1 hypervisors

A type 1 hypervisor is installed directly on the underlying physical hardware, managing and allocating the physical hardware resources to each VM running on top of it. Figure 17.4 illustrates a type 1 hypervisor running three VMs.



Figure 17.4 A type 1 hypervisor runs directly on the server hardware.

Note Type 1 hypervisors are also called bare-metal hypervisors because they run directly on the hardware (the “metal”). Another term is native hypervisor. Two common type 1 hypervisors are VMware ESXi and Microsoft Hyper-V.

Type 1 hypervisors are what you’ll most often find used for server virtualization in data center environments (including the cloud). By interacting directly with the physical hardware without any intermediaries, they provide very efficient use of hardware resources when compared with type 2 hypervisors.

Type 2 hypervisors

Whereas a type 1 hypervisor runs directly on the underlying hardware, a type 2 hypervisor runs as an application on an OS, like a regular computer application. Figure 17.5 shows a type 2 hypervisor running two VMs.



Figure 17.5 A type 2 hypervisor runs as an application on a host OS.

Note Another name for a type 2 hypervisor is a hosted hypervisor. Two common type 2 hypervisors are Oracle VM VirtualBox and VMware Workstation. VirtualBox is free, and Workstation has free and paid versions.

The OS running directly on the hardware is called the host OS, and an OS running in a VM is called a guest OS. Unlike type 1 hypervisors, which have direct access to hardware resources, type 2 hypervisors must go through the host OS to access these resources. Furthermore, the host OS itself consumes hardware resources. Both of these points mean that type 2 hypervisors are less resource-efficient than type 1 hypervisors, making them less suited for resource-intensive applications; type 2 hypervisors are rare in the context of virtual servers in a data center environment.

However, the advantage of type 2 hypervisors lies in their ease of setup and use. A user can install and run a type 2 hypervisor on their PC just like any other application, making it more accessible for those who may not have the technical expertise to set up a type 1 hypervisor. This also means that a type 2 hypervisor can coexist with other applications on the host OS, allowing a PC to be used for virtualization without needing dedicated hardware.

For these reasons, type 2 hypervisors are more common on personal-use devices. For example, if a Mac/Linux user needs to run an app that is only supported on Windows (or vice versa), a type 2 hypervisor can be used to easily run another OS without the need to buy another computer. Type 2 hypervisors are also popular for software development, testing, and educational purposes.

Networking virtual machines

Each VM—whether it is running on a type 1 or type 2 hypervisor—operates as an independent host on the network, much like a physical computer. Although a VM doesn’t have its own physical network interface card (NIC) like a standalone physical host, it uses a virtual NIC (vNIC). Through this vNIC, the VM can communicate with other hosts, whether they are other VMs on the same physical server or devices on the external physical network.

To manage network traffic to and from VMs, the hypervisor uses a virtual switch, which forwards frames between the vNICs of the VMs and the physical NIC (or NICs) of the host machine. Figure 17.6 illustrates how this works.



Figure 17.6 VMs connect to each other and the external physical network via a virtual switch. VMs are often segmented into separate VLANs, requiring trunk links.

Note Figure 17.6 shows two NICs on the physical server. It’s common for servers to have multiple NICs (each connected to a different physical switch) to provide redundancy, allowing the server to remain accessible if one NIC or switch fails.

Just like a physical switch, a virtual switch’s ports can operate in access or trunk mode, enabling the use of VLANs to segment the VMs. To allow VMs in different VLANs to communicate over the network, the virtual switch connects to the physical host’s NICs via trunk links. Likewise, the physical host’s NICs connect to external physical switches via trunk links. Although switch ports connected to end hosts are almost always access ports, ports connected to servers running VMs are rare examples of trunk ports connected to end hosts; they need to be able to carry traffic to and from VMs in multiple VLANs.

The benefits of virtualization

Virtualization provides a variety of benefits for an enterprise. Here are a few:

Reduced costs—By efficiently using server hardware resources, fewer physical servers are needed, reducing capital expenses (upfront costs). This also reduces the space, cooling, and power demands, reducing operating expenses (ongoing costs).

Mobility—An entire VM can be easily saved as a file. This facilitates easy transfer, duplication, or migration (for example, if a problem occurs on one physical server).

Isolation—Each VM operates independently from the others, providing enhanced security and stability. Problems within one VM, such as crashes or malware infections, do not affect the rest of the system.

Faster provisioning—New VMs can be rapidly provisioned and deployed. This allows the organization to quickly respond to changing business needs, with the ability to roll out new applications and services in minutes rather than the days or weeks required for setting up new physical servers.

17.1.2 Containers
While VMs offer full hardware virtualization, providing complete OSs for their applications, a more agile approach is gaining prominence in modern IT infrastructure: containers. A container is a lightweight, stand-alone package that includes everything needed to run a particular application. A container is similar to a VM in that it provides an isolated environment for the application but is different in that it’s more lightweight (smaller in size), requiring less overhead. Instead of running an independent OS, a container only contains an application and its dependencies (the various files and services it needs to run).

Figure 17.7 illustrates container architecture. Containers run on a container engine; a popular example is Docker Engine. The container engine itself runs on a host OS (usually Linux); notice that each container does not run its own OS.



Figure 17.7 Containers run on a container engine, such as Docker Engine. The container engine runs on a host OS, but each container does not run a guest OS.

A software platform called a container orchestrator is typically used to automate the deployment, management, and scaling of containers; Kubernetes, originally designed by Google, is the industry standard. In small numbers, manual operation is possible, but large-scale systems can use many thousands (sometimes hundreds of thousands) of containers. This is especially true of applications that employ a microservices architecture, which breaks an application into many small, self-contained services. Containers are perfect for this, as they can isolate and manage these services independently.

Comparing VMs and containers

VMs and containers are both methods of virtualization that improve resource utilization and provide isolated environments for applications. Let’s briefly compare them:

Startup time—VMs can take minutes to boot up as each runs its own OS. Containers can boot up in milliseconds.

Disk space—VMs take up more disk space (often many gigabytes) due to requiring a full OS. Containers take up relatively little disk space (megabytes).

CPU/RAM efficiency—VMs use more CPU/RAM resources; once again, this is because each VM runs its own OS. Containers share an OS and therefore use fewer CPU/RAM resources.

Portability—VMs are portable across different physical systems running the same hypervisor. Containers offer even greater portability—they are smaller, are faster to start, and can run on any modern container engine with Docker compatibility.

Isolation—VMs offer strong isolation; a problem on one VM won’t affect others. Containers run on the same host OS, so a problem on that host OS can affect all containers.

Although there is a major movement toward the use of containers, especially with the rise of microservices, automation, and DevOps (the combination of software development and IT operations), VMs and containers serve different needs, and both are widely used.

17.2 Virtual Routing and Forwarding
Let’s move away from virtual machines and containers back to network virtualization. Similar to how VLANs segment a switch into multiple virtual switches, Virtual Routing and Forwarding (VRF) segments a router into multiple virtual routers. Service providers often use VRF to allow a customer’s traffic to travel over the service provider’s shared infrastructure while remaining isolated from other customers. As mentioned in the previous chapter, MPLS L3VPNs implement VRF for this purpose.

Figure 17.8 demonstrates VRF in the same manner we saw in the context of VLANs back in figure 17.1. SPR1 (service provider router 1) physically connects to six routers belonging to three customers (C1R1 = customer 1 router 1, C2R1 = customer 2 router 1, etc.). Using VRF, SPR1 is able to act as three independent routers: one for each customer.



Figure 17.8 VRF segments a physical router into multiple virtual routers.

Note Each VRF virtual router is called a VRF instance or simply a VRF. Figure 17.8 depicts three VRFs—one for each customer.

Like VLANs, each VRF is isolated from other VRFs; traffic in one VRF cannot be forwarded out of an interface that belongs to another VRF. There is one exception; VRF leaking can be configured to allow traffic to pass between VRFs. However, VRF leaking and its use cases are a more advanced topic beyond the scope of the CCNA.

Although VRF configuration itself isn’t tested on the CCNA exam, it’s a useful tool to demonstrate how VRF works. So let’s walk through a basic VRF configuration and examine its effects. Figure 17.9 adds IP addresses and interface IDs to the network shown in figure 17.8. To examine how VRF works, we’ll configure SPR1 as shown in this example.



Figure 17.9 SPR1 is divided into three VRFs. Because each VRF functions as an independent router, overlapping IP addresses are not a problem.

Note As mentioned previously, VRF is often used to enable MPLS L3VPNs. VRF without MPLS is called VRF-lite, and that’s what we’re covering in this example; MPLS L3VPN implementation is a more advanced topic.

Basic VRF-lite configuration consists of the following three steps:

Create the VRFs.

Assign interfaces to each VRF.

Configure routing for each VRF.

To create a VRF, use the ip vrf vrf-name command in global config mode. That will bring you to VRF configuration mode, from which you can configure various VRF-related settings. However, for the most basic VRF-lite configuration, just creating the VRF is sufficient. In the following example, I create three VRFs on SPR1 and verify with show ip vrf:

SPR1(config)# ip vrf C1_VRF                                 ❶
SPR1(config-vrf)# ip vrf C2_VRF                             ❶
SPR1(config-vrf)# ip vrf C3_CRF                             ❶
SPR1(config-vrf)# do show ip vrf 
  Name                             Default RD            Interfaces
  C1_VRF                           <not set>                ❷
  C2_VRF                           <not set>                ❷
  C3_CRF                           <not set>                ❷
❶ Creates three VRFs

❷ Three VRFs exist on SPR1.

The next step is to assign interfaces to each VRF. In our example network, all three VRFs use overlapping IP addresses in the 192.168.1.0/30 and 192.168.4.0/30 subnets. As the following example shows, this is not possible on a router without using VRFs:

SPR1(config)# interface g0/0                                ❶
SPR1(config-if)# no shutdown                                ❶
SPR1(config-if)# ip address 192.168.1.1 255.255.255.252     ❶
SPR1(config)# interface g0/2                                ❷
SPR1(config-if)# no shutdown                                ❷
SPR1(config-if)# ip address 192.168.1.1 255.255.255.252     ❷
% 192.168.1.0 overlaps with GigabitEthernet0/0              ❸
❶ Enables G0/0 and configures its IP address

❷ Enables G0/2 and configures its IP address

❸ G0/2’s IP address is rejected because it’s in the same subnet as G0/0.

Because the purpose of a router is to connect different networks, it can’t have multiple interfaces connected to the same network (multiple interfaces in the same subnet). In the previous output, I attempted to configure the exact same IP address on G0/0 and G0/2, but the same problem would occur even if the IP addresses were different (i.e., 192.168.1.1/30 and 192.168.1.2/30); if there is any overlap between the interfaces’ subnets, IOS will reject the command.

VRFs, however, are virtually isolated from each other. Interfaces in different VRFs can use overlapping subnets and even identical IP addresses. This allows for different customers to maintain their addressing schemes without worrying about other customers’ addressing. In our example, each VRF is used to support a different customer network, and each customer network uses the same subnets.

To assign an interface to a VRF, use the ip vrf forwarding vrf-name command in interface config mode. In the following example, I assign each of SPR1’s interfaces to the appropriate VRF and configure each interface’s IP address. To spare some lines, I’ve omitted the no shutdown command from each interface:

SPR1(config)# interface g0/0
SPR1(config-if)# ip vrf forwarding C1_VRF                  ❶
% Interface GigabitEthernet0/0 IPv4 disabled and address(es) removed due to enabling 
VRF C1_VRF                                                 ❷
SPR1(config-if)# ip address 192.168.1.1 255.255.255.252    ❸
SPR1(config-if)# interface g0/1                            ❹
SPR1(config-if)# ip vrf forwarding C1_VRF                  ❹
SPR1(config-if)# ip add 192.168.1.5 255.255.255.252        ❹
SPR1(config-if)# interface g0/2                            ❺
SPR1(config-if)# ip vrf forwarding C2_VRF                  ❺
SPR1(config-if)# ip add 192.168.1.1 255.255.255.252        ❺
SPR1(config-if)# interface g0/3                            ❺
SPR1(config-if)# ip vrf forwarding C2_VRF                  ❺
SPR1(config-if)# ip add 192.168.1.5 255.255.255.252        ❺
SPR1(config-if)# interface g0/4                            ❻
SPR1(config-if)# ip vrf forwarding C3_VRF                  ❻
SPR1(config-if)# ip add 192.168.1.1 255.255.255.252        ❻
SPR1(config-if)# interface g0/5                            ❻
SPR1(config-if)# ip vrf forwarding C3_VRF                  ❻
SPR1(config-if)# ip add 192.168.1.5 255.255.255.252        ❻
❶ Assigns G0/0 to C1_VRF

❷ G0/0’s IP address is removed.

❸ Reconfigures G0/0’s IP address

❹ Assigns G0/1 to C1_VRF and configures its IP address

❺ Assigns G0/2 and G0/3 to C2_VRF and configures their IP addresses

❻ Assigns G0/4 and G0/5 to C3_VRF and configures their IP addresses

Note As the previous output shows, if an interface already has an IP address, it will be removed when you assign the interface to a VRF. I configured G0/0’s IP address in the example before this one, but I had to reconfigure it after assigning G0/0 to C1_VRF.

Although we won’t cover how to configure static and dynamic routing when using VRFs, let’s look at the connected and local routes that are automatically added to the routing table after configuring IP addresses on a router’s interfaces:

SPR1# show ip route    ❶
. . .                  ❷
❶ Views SPR1’s routing table

❷ No routes are shown.

The show ip route command on its own doesn’t show any routes. That’s because the router builds a unique routing table for each VRF, and you have to specify which VRF’s routing table you want to see with show ip route vrf vrf-name. In the following example, I show the routing table for C1_VRF:

SPR1# show ip route vrf C1_VRF                                       ❶
. . .
C        192.168.1.0/30 is directly connected, GigabitEthernet0/0    ❷
L        192.168.1.1/32 is directly connected, GigabitEthernet0/0    ❷
C        192.168.1.4/30 is directly connected, GigabitEthernet0/1    ❷
L        192.168.1.5/32 is directly connected, GigabitEthernet0/1    ❷
❶ Views the C1_VRF routing table

❷ Connected and local routes for G0/0 and G0/1 are displayed.

Other commands require you to specify a particular VRF too. In the following example, I ping 192.168.1.2, which is the IP address of C1R1, C2R1, and C3R1. Note the differing results when I do and don’t specify a VRF:

SPR1# ping 192.168.1.2                                               ❶
. . .
.....                                                                ❶
Success rate is 0 percent (0/5)                                      ❶
SPR1# ping vrf C1_VRF 192.168.1.2                                    ❷
. . .
!!!!!                                                                ❷
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/3 ms ❷
SPR1# ping vrf C2_VRF 192.168.1.2                                    ❸
. . .
!!!!!                                                                ❸
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/3 ms ❸
SPR1# ping vrf C3_VRF 192.168.1.2                                    ❹
. . .
!!!!!                                                                ❹
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/2 ms ❹
❶ Without specifying a VRF, the ping fails.

❷ The ping works when specifying C1_VRF (the ping is sent to C1R1).

❸ The ping works when specifying C2_VRF (the ping is sent to C2R1).

❹ The ping works when specifying C3_VRF (the ping is sent to C3R1).

The global routing instance and routing table

Even when using VRFs, the router can have interfaces that aren’t assigned to any particular VRF. These interfaces are part of the global routing instance, and their associated routes are part of the global routing table—this is the “normal” routing table you can view with show ip route (without specifying a VRF). If you issue a ping without specifying a VRF, the router will search for the ping’s destination in the global routing table. However, in our example network, all interfaces are assigned to specific VRF instances and none to the global routing instance, so the global routing table does not contain any routes.

Although VRF configuration is not included on the exam, remember these key takeaways that we demonstrated with this basic configuration:

VRF divides a physical router into multiple virtual routers (VRFs), each with its own routing table.

VRF allows for the use of overlapping subnets on the same physical router (although they must be in different VRFs).

Traffic in one VRF will only be forwarded within the same VRF, not to different VRFs (or the global routing instance).

17.3 Cloud computing
Now that we’ve covered the foundational technologies of VMs, containers, and VRF, we’re almost ready to ascend into the cloud. These virtualization technologies underpin the vast and scalable architectures of the cloud, enabling the dynamic provisioning, management, and deployment capabilities that are characteristic of cloud computing.

But before we look at cloud computing, let’s briefly consider the bedrock of traditional IT infrastructure: on-premises and colocation setups. On-premises (often abbreviated as on-prem) solutions represent the classic approach in which a company’s infrastructure (servers and key network devices) is located within its own facilities, offering complete control over the IT environment. All equipment is purchased and owned by the company using it, and the company is responsible for the necessary space, power, cooling, and physical security.

In contrast, colocation services allow a business to rent space in third-party data centers to house its infrastructure. While the business is still responsible for purchasing and operating the servers, the necessary space, power, and cooling are provided by the data center, as well as robust physical security. The proximity to the colocation data center’s other customers also has the benefit of facilitating connections between customers, enabling them to share resources efficiently. Figure 17.10 shows such a setup.



Figure 17.10 Two customers (Enterprise A and Enterprise B) house their servers in a colocation data center. They connect their networks in the data center, allowing them to share resources.

Cloud computing is a third approach that provides on-demand access to shared computing resources over a network. It provides an alternative to on-prem and colocation solutions that is not only hugely popular but is also continuing to grow year on year. In the rest of this section, we’ll explore exactly what cloud computing is, covering its essential characteristics, service models, and deployment models.

The NIST definition of cloud computing

In 2011, the American National Institute of Standards and Technology (NIST) published a paper titled “The NIST Definition of Cloud Computing.” Despite being published over a decade ago, it remains a cornerstone for understanding cloud computing fundamentals. The PDF file is seven pages in length, but the actual substance of the paper is only the last two pages. In this section, I will mainly expand upon and provide diagrams to help clarify the contents of the NIST’s paper, but I highly recommend reading the paper yourself; you can access it for free at https://mng.bz/Y7vB.

17.3.1 The essential characteristics of cloud computing
So what exactly is cloud computing? How can you identify if a particular service is cloud computing or not? The NIST defines five essential characteristics of cloud computing:

On-demand self-service

Broad network access

Resource pooling

Rapid elasticity

Measured service

These five characteristics are essential to understanding cloud computing, so let’s walk through them. On-demand self-service means that the customer is able to use the service (or stop using the service) as needed, without direct human interaction with the service provider—for example, via a web portal. Figure 17.11 shows the Amazon Web Services (AWS) web portal; AWS is the most popular public cloud service provider. Some other major players in the business are (in order of market share, with AWS at the top):

Microsoft Azure

Google Cloud Platform (GCP)

Alibaba Cloud

IBM Cloud



Figure 17.11 The AWS web portal through which customers can access services. Human-to-human interaction with AWS isn’t necessary.

Broad network access means that the services should be made available over standard network connections (i.e., the internet or private WAN connections) and should be accessible by many kinds of devices, including mobile phones, desktop PCs, etc. Figure 17.12 shows some ways an enterprise can connect to cloud resources: a private WAN connection, a simple internet connection, or an IPsec VPN tunnel.



Figure 17.12 Cloud resources are accessible over standard network connections. For example, private WAN connections, simple internet connections, or internet VPNs can be used to access cloud resources.

Resource pooling means that a shared pool of resources is provided to serve multiple customers. When a customer requests a service, the resources to fulfill that request are dynamically allocated from the shared pool. AWS, for example, has data centers all over the world with countless powerful servers. When a customer creates a VM on AWS, a small portion of that huge resource pool is dynamically allocated to the new VM. If the customer deletes the VM, the allocated resources are released back into the pool.

Rapid elasticity means that customers can quickly scale their cloud resources up or down as needed. This scaling can often be automated, adjusting to resource demands in real time. To understand the utility of rapid elasticity, imagine an e-commerce business gearing up for the Christmas season. Anticipating increased website traffic, the company can easily scale up its cloud resources to accommodate the surge. Once the holiday rush calms down, they can just as easily scale down, ensuring they only pay for the resources they need. Without the cloud, the business would be forced to maintain enough physical servers to support their peak periods year-round, resulting in unnecessary costs for servers that are underutilized most of the year.

The final essential characteristic is measured service, which means that the cloud service provider measures the customer’s use of cloud resources, providing transparency for both the provider and the customer. The customer is typically charged based on their usage (for example, X dollars per gigabyte of storage per day). Figure 17.13 shows a billing report on GCP, showing the cost increasing and decreasing according to use.



Figure 17.13 A GCP billing report. Cloud providers like GCP measure customers’ resource usage and charge according to that usage.

17.3.2 Cloud service models
In a traditional on-prem or colocation setup, an enterprise purchases its own resources, using them according to its specific needs. Cloud computing service providers like AWS, Microsoft Azure, and GCP offer these resources—servers, storage, networking, and even entire platforms and applications—as services on a subscription basis. The customer benefits from access to these resources without the responsibilities of ownership and maintenance. But what kinds of services are available through these providers? Cloud service providers offer a variety of different services that can largely be categorized into three main types:

Software as a Service (SaaS)

Platform as a Service (PaaS)

Infrastructure as a Service (IaaS).

Figure 17.14 illustrates what is offered by each of these cloud service models and compares them to colocation and on-prem solutions.



Figure 17.14 The spectrum of what is offered in each cloud service model in comparison to colocation and on-prem solutions

Note Runtime refers to the environment that executes application code, while middleware provides essential services and capabilities, such as database management systems, that enable applications to communicate and manage data.

Software as a Service (SaaS) delivers applications as a service over a network (typically the internet). Instead of installing and using applications on their own devices, users simply access them via the internet. SaaS applications run on the provider’s infrastructure and are typically accessible from any device with a web browser. Some popular examples of SaaS are

Microsoft 365 (formerly Office 365): Word, Excel, PowerPoint, Outlook, etc.

Google Workspace (formerly G Suite): Gmail, Docs, Drive, Calendar, etc.

Slack

Dropbox

Zoom

Note While some applications are offered primarily as SaaS, others may also provide versions that can be installed locally on individual devices.

Platform as a Service (PaaS) provides a platform for customers to develop, run, and manage applications without the complexity of building and maintaining the infrastructure typically associated with developing and launching an app. As shown in figure 17.14, the service includes everything except the applications themselves, which the customer develops using the provided platform. They don’t have the name recognition of famous SaaS products, but some popular PaaS offerings are AWS Lambda, Azure App Service, and Google App Engine.

Infrastructure as a Service (IaaS) offers essential computing resources, storage, and networking capabilities on demand. Customers can create virtual machines, install OSs, run applications, etc., on the provider’s infrastructure, customizing the CPU, RAM, and storage for each virtual machine and configuring their interconnections to form a virtual network. Some popular examples are AWS EC2, Azure Virtual Machines, and Google Compute Engine.

Of these three cloud service models, IaaS provides the greatest control to the customer. The service provider is responsible for the data center that hosts the physical infrastructure, the physical infrastructure itself, and the virtualization platforms that enable customers to freely create, run, and manage virtual machines with their choice of OSs and applications. On the other end of the spectrum, SaaS provides the least control; the service provider offers a complete software product for the customer to use.

Note In addition to SaaS, PaaS, and IaaS, there are a variety of services with similar XaaS names, but for the CCNA exam, you should know these primary three.

17.3.3 Cloud deployment models
When you think of “the cloud,” cloud service providers like AWS probably come to mind. However, the NIST defines four distinct cloud deployment models, encompassing a variety of cloud environments:

Public cloud

Private cloud

Community cloud

Hybrid cloud

AWS, Azure, GCP, and similar services fit into the public cloud deployment model—the most common of the four—but understanding all four deployment models is essential. Let’s take a look at each of them.

In a public cloud deployment, the infrastructure, which is located on the cloud provider’s premises, is available for open use by the public (for a fee, of course); anyone who wants to use the cloud resources is free to become a customer. This is by far the most common deployment and is used by individuals and organizations of all sizes. Figure 17.15 shows customers of various sizes connected to different public cloud providers.



Figure 17.15 Customers of all sizes can connect to and use public cloud resources.

In a private cloud deployment, the cloud infrastructure is provided for use by a single organization—typically a very large organization (i.e., government or large business). The cloud resources can be used by different consumers within that organization (i.e., different departments of a business) but are not available for use by those outside of the specific organization.

Note Private cloud infrastructure may exist on or off the premises of the organization that uses it. Cloud and on-prem are not always mutually exclusive!

Although the cloud is private—reserved for use by a single organization—it may be owned by a third party. For example, AWS provides private cloud services for the US Department of Defense (DoD). Figure 17.16 depicts the DoD connecting to a private cloud provided by AWS, separate from the AWS public cloud.



Figure 17.16 AWS provides private cloud services to the US Department of Defense, separate from the AWS public cloud.

A community cloud is a collaborative effort where the cloud infrastructure is reserved for use by consumers in multiple organizations. This provides a balance between the shared model of a public cloud and the dedicated resources of a private cloud. The infrastructure itself can be managed by one or more of the organizations or a third-party provider and can exist on or off the premises of any of the member organizations.

The final deployment model is hybrid cloud, which is any combination of two or more of the previous models. An example use case for a hybrid cloud is a private cloud that can offload work to a public cloud when necessary when the private cloud does not have sufficient resources.

The advantages of cloud computing

There are various reasons why so many modern enterprises are moving significant portions of their IT infrastructure to the cloud. Here are some advantages of cloud computing:

Cost efficiency—Upfront capital expenditures for hardware, software, and data centers are significantly reduced or even eliminated.

Global scaling—Cloud services can scale globally at a rapid pace. Services can be set up and offered to customers from a geographic location close to them, reducing latency.

Speed and agility—Services are provided on demand, and vast amounts of resources can be provisioned within minutes if needed.

Productivity—By outsourcing physical infrastructure concerns, cloud services reduce the need for labor-intensive tasks associated with hardware setup and other routine IT management chores.

Reliability—Backing up systems in the cloud is simple, and data can be mirrored at multiple sites in diverse geographic locations to support disaster recovery (i.e., if a natural disaster affects one site).

Despite these advantages, moving infrastructure to the cloud is not always the correct answer. If you follow tech-related news, you will occasionally see stories about companies that gained huge savings by moving their infrastructure out of the cloud, returning to on-prem/colocation setups. Each organization should carefully consider whether moving its infrastructure to the cloud will deliver a net benefit; many organizations use a combination of all three.

Summary
VLANs and VPNs are forms of network virtualization. VLANs segment a physical LAN into separate logical LANs, whereas VPNs create secure, private network connections over shared or public networks like the internet.

Virtual machines (VMs) and containers are also examples of virtualization, allowing operating systems and applications to run in isolated environments on a server.

Before virtualization, a physical server would run a single operating system (OS). This meant that all of the hardware resources were tied to that one OS and its applications. This often led to resource underutilization.

Virtual machines (VMs) break the one-to-one relationship of hardware to OS, allowing multiple OSs to run on a single physical server.

VMs are facilitated by a hypervisor that sits between the hardware and the VMs, managing and allocating hardware resources to each VM. Another name for a hypervisor is a virtual machine monitor (VMM).

A type 1 hypervisor is installed directly on the underlying physical hardware. Other names for this are bare-metal or native hypervisor.

Type 1 hypervisors are most often used for server virtualization in data center environments (including the cloud). By interacting directly with the physical hardware, they provide very efficient use of those resources.

A type 2 hypervisor runs as a program on an OS, like a regular computer application. The OS running directly on the hardware is called the host OS, and an OS running in a VM is called a guest OS.

Type 2 hypervisors use hardware resources less efficiently than type 1 hypervisors, but their advantage lies in their ease of setup and use. They are more common on personal-use devices for software development, testing, and educational purposes.

Each VM operates as an independent host on the network. Instead of a physical network interface card (NIC), it has a virtual NIC (vNIC).

To manage network traffic to and from VMs, the hypervisor uses a virtual switch, which forwards frames between the vNICs of the VMs and the physical NICs of the host machine.

Just like a physical switch, a virtual switch’s ports can operate in access or trunk mode, enabling the use of VLANs to segment the VMs.

While VMs offer full hardware virtualization, providing complete OSs for their applications, containers provide a more agile approach.

A container is a lightweight, stand-alone package that includes everything needed to run a particular application.

Containers are more lightweight than VMs, requiring less overhead. Instead of running an independent OS, the container only contains an application and its dependencies. Containers do not run independent OSs.

Containers run on a container engine such as Docker Engine. The container engine runs on a host OS (usually Linux).

A container orchestrator (such as Kubernetes) is typically used to automate the deployment, management, and scaling of containers.

Virtual Routing and Forwarding (VRF) segments a router into multiple virtual routers. Service providers often use VRF to allow a customer’s traffic to travel over shared infrastructure while remaining isolated from other customers.

Each VRF virtual router is called a VRF instance or simply a VRF.

Each VRF is isolated from other VRFs; traffic in one VRF cannot be forwarded out of an interface that belongs to another VRF.

VRF is often used to enable MPLS L3VPNs. VRF without MPLS is called VRF-lite.

Use ip vrf vrf-name to create a VRF and show ip vrf to view the existing VRFs.

Use ip vrf forwarding vrf-name in interface config mode to assign an interface to a particular VRF.

The router builds a separate routing table for each VRF. Use show ip route vrf vrf-name to view the routing table of the specified VRF.

Before the cloud, traditional IT infrastructure was typically a combination of on-premises and colocation setups.

On-premises (on-prem) means the company’s infrastructure (servers and key network devices) are located within its own facilities, offering complete control.

All equipment is purchased by the company using it, and the company is responsible for the necessary space, power, cooling, and physical security.

Colocation services allow a business to rent space in third-party data centers to house its infrastructure.

Cloud computing is a third approach that provides on-demand access to shared computing resources over a network (such as the internet).

The five essential characteristics of cloud computing are

On-demand self-service—The customer is able to use (or stop using) the service as needed without direct human-to-human interaction.

Broad network access—The services should be made available over standard network connections and accessible by many kinds of devices.

Resource pooling—A shared pool of resources is provided to serve multiple customers. The resources are dynamically allocated as needed.

Rapid elasticity—Customers can quickly scale their cloud resources up or down as needed.

Measured service—The cloud service provider measures the customer use of cloud resources and typically charges based on the usage.

The three main cloud service models are Software as a Service (SaaS), Platform as a Service (PaaS), and Infrastructure as a Service (IaaS).

SaaS delivers applications as a service over a network (typically the internet). Instead of installing applications on their own devices, users simply access them over the internet. Popular examples are Microsoft 365 and Google Workspace.

PaaS provides a platform for customers to develop, run, and manage applications without the complexity of building and maintaining the necessary infrastructure.

IaaS offers essential computing resources, storage, and networking capabilities on demand. Customers can create VMs, install Oss, run applications, etc., on the provider’s infrastructure.

The four cloud deployment models are public, private, community, and hybrid.

In a public cloud deployment, the infrastructure, which is located on the cloud provider’s premises, is available for use by the public. Popular examples are Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP).

In a private cloud deployment, the cloud infrastructure is provided for use by a single organization. The cloud infrastructure may be owned by a third party and may be on or off the premises of the organization that uses the cloud.

A community cloud is a collaborative effort where the cloud infrastructure is reserved for use by consumers in multiple organizations. The infrastructure can be managed by one or more of the member organizations or a third party and can exist on or off the premises of any of the member organizations.

A hybrid cloud is a combination of two or more of the other deployment models (for example, a private cloud that can offload work to a public cloud when necessary).