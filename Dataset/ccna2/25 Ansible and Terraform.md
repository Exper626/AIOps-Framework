25 Ansible and Terraform
This chapter covers

Configuration management and its challenges
Template-based configuration
Automating configuration management with Ansible and Terraform
Configuring devices in the CLI is something many network engineers grow to love, but it simply doesn’t scale well. As networks grow in size and complexity, the manual, one-by-one configuration of devices makes managing each individual device’s configuration infeasible. Not only is configuring each device time-consuming and prone to human error, but tracking configuration changes and enforcing standards across numerous devices becomes unmanageable. Many modern networks require more efficient solutions.

In this chapter, we’ll cover CCNA exam topic 6.6: Recognize the capabilities of configuration management mechanisms such as Ansible and Terraform. These tools, which embody the principles of infrastructure as code (IaC), play a crucial role in automating and standardizing device configurations, ensuring accuracy and consistency. Automating configuration management tasks is essential in many modern networks, which are increasingly large and complex. We’ll begin by examining configuration management and its difficulties and then consider how automation tools like Ansible and Terraform help to solve those problems, streamlining and enhancing the process of configuration management.

25.1 Configuration management
Configuration management in networking involves various tasks aimed at maintaining, controlling, and documenting the configurations of network devices. Proper configuration management is important in networks of all sizes but becomes especially critical in larger networks. This section will discuss some key aspects of configuration management, including establishing standards, traditional configuration management techniques, and the importance of maintaining configuration consistency across devices in the network.

25.1.1 Establishing configuration standards
Although no two devices in a network will have identical configurations, they also shouldn’t be completely unique. To ensure the security and consistent operations of devices in a network, most elements of a device’s configuration can and should be standardized. The following are some examples of configurations that can be shared among most or all devices in a network:

DNS servers—All network devices should use the same DNS servers for consistent name resolution.

NTP servers—To maintain consistent time across all devices in the network, they should query and sync to the same NTP servers.

Routing protocols—Routers should use the same routing protocols with standardized configurations to ensure consistent and efficient routing decisions across the network.

QoS policies—To ensure consistent treatment of different types of traffic, QoS policies should be standardized.

AAA servers—Centralized AAA (RADIUS/TACACS+) servers should be used to control access to network resources and the network devices themselves.

Security policies—Uniform security policies, such as defining which traffic should be permitted or denied, are essential in maintaining a consistent security posture.

Logging and monitoring settings—Syslog messages should be sent to centralized servers to provide a complete and consistent view of network activities. This aids in troubleshooting and security monitoring.

This list is not comprehensive, but I think you get the idea. Key configurations like IP addresses and hostnames will vary per device, but standardizing the aforementioned core aspects is vital for managing large-scale environments, maintaining security, and ensuring operational consistency. Figure 25.1 shows partial output of two routers’ configurations; aside from hostnames and interface IP addresses, their configurations are identical, as they follow established standards.



Figure 25.1 Device configurations should be derived from standards, ensuring consistent operations across all devices. Although each device will have some unique configurations, most should be consistent across devices.

Developing these standards involves understanding the network’s needs, aligning with industry best practices, considering security and performance, and involving key stakeholders such as IT security teams, management, server teams, and external consultants or vendors. Typically, this is a task for more senior staff. If you’re new to networking, your role will likely focus on implementing, operating, and maintaining the network as per these established standards, which are equally important in the network lifecycle.

25.1.2 Configuration drift
Maintaining consistent configurations according to organizational standards is essential for the security and reliability of the network. However, it’s common for network configurations to gradually diverge from these standards over time. This phenomenon is called configuration drift, and it can pose significant challenges to network security and operational efficiency. Figure 25.2 illustrates the concept.



Figure 25.2 Accumulated individual changes result in deviation from standard configurations, called configuration drift.

Configuration drift typically arises from the traditional method of managing network configurations—the manual, device-by-device approach. Configuring each device individually often leads to inconsistencies due to human error, differing interpretations of the standards, and small ad hoc configuration changes that accumulate over time. As networks grow and become more complex, this manual approach proves increasingly inadequate, with implications like the following:

Inconsistency—Manual configurations can vary slightly from each change, especially when performed by different network admins or engineers. Over time, these small variations can lead to significant inconsistencies across the network.

Error-prone—The manual process is susceptible to human error. A mistyped command or overlooked configuration can create security vulnerabilities or performance problems that may go unnoticed until problems arise.

Not scalable—As the network expands, manually ensuring that every new device or update adheres to the standard configurations becomes infeasible.

Difficult to monitor and correct—Continuously monitoring each device for adherence to configuration standards is challenging. Correcting deviations can be impractical, as it often involves manually checking and adjusting the configurations of each device.

Even with the best of intentions to follow established standards, some degree of configuration drift is almost inevitable when managing a large and complex network manually. In the next section, we’ll look at how configuration management tools use automation to enforce configuration consistency, reducing the risk of configuration drift for more reliable and secure network operations.

Note The basic point to remember from this section is that as a network grows in size and complexity, manual configuration management can result in configuration drift, negatively affecting the reliable and secure operation of the network.

25.2 Configuration management tools
Configuration management tools use software to automate various tasks related to configuration management, from deploying initial configurations and configuration changes to enforcing configuration standards. Device configurations are centrally managed from a server, instead of individually managed on the devices themselves. Figure 25.3 gives a tool-agnostic overview of how configuring devices with one of these tools generally works.



Figure 25.3 Configuring devices with a configuration management tool. Configurations are centrally managed from a shared folder. A server running a configuration management tool applies configuration changes to devices.

Instead of configuring devices individually, configurations are centrally managed from a shared folder. A configuration management server is responsible for applying any changes to the appropriate devices.

Device configurations aren’t simply stored as is on the server; instead, a variety of files are used, each with a different purpose—the types of files and their names depend on the tool. However, two key elements are configuration templates that define the desired state of device configurations using a standardized format and variables that store specific values unique to each device.

Using the example of two routers with near-identical configurations that we saw in figure 25.1, the following example shows how a configuration template can be formatted to generate those two separate configurations, replacing the unique per-device configurations with variables:

hostname {{hostname}}                    ❶
ntp server 172.16.1.1
ip name-server 192.168.23.8
logging host 172.25.25.12
router ospf 1
 auto-cost reference-bandwidth 10000
interface GigabitEthernet 0/0
 ip address {{g0/0addr}} {{g0/0mask}}    ❷
 ip ospf 1 area 0
interface GigabitEthernet 0/1
 ip address {{g0/1addr}} {{g0/1mask}}    ❸
 ip ospf 1 area 0
 ip helper-address 10.0.0.63
❶ A variable for each router’s hostname

❷ Variables for the router’s G0/0 IP address and netmask

❸ Variables for the router’s G0/1 IP address and netmask

This single template can be used for all routers that require similar configurations, with a separate file listing the variable values for each router. The following example shows R1’s values; by inserting the appropriate values in the configuration template, the server can assemble R1’s configuration. A change to the configuration template or variable files will result in the server applying the changes to the appropriate devices:

---
hostname: R1                             ❶
g0/0addr: 192.168.12.1                   ❶
g0/0mask: 255.255.255.252                ❶
g0/1addr: 192.168.1.1                    ❶
g0/1mask: 255.255.255.0                  ❶
❶ Key:value pairs that provide values for the configuration template’s variables

In addition to configuring devices from a central server, configuration management tools can enforce conformity to the standards defined in the configuration files on the server. As shown in figure 25.4, the configuration management server is able to detect any deviations from the standard templates. It compares the active configuration on a device like R1 against the expected configuration as defined by the templates and variables. This comparison can be scheduled to occur at regular intervals or triggered manually by an administrator. If a discrepancy is found, the server alerts the administrators, who can then take appropriate action, ensuring that the network remains secure and operates as intended.



Figure 25.4 The configuration management server compares device configurations to the standards defined in the configuration files and notifies admins of a discrepancy.

The CCNA exam topics list mentions two configuration management tools and Terraform. Table 25.1 summarizes some key details about each of these tools, such as the programming language each is written in, the names of their key files and the file formats they use to store configurations. In addition to Ansible and Terraform, table 25.1 also lists Puppet and Chef—two other configuration management tools that we will briefly touch on in this section.

The table identifies each tool as agent-based or agentless; agent-based tools require a software “agent” on managed devices, and agentless tools don’t. It also lists each tool as being mainly procedural or mainly declarative; a procedural approach involves defining a series of steps to configure the target system, and a declarative approach involves defining the desired end state of the system and letting the tool figure out how to achieve that desired state. Finally, it also differentiates between push and pull models; in a push model, the server sends the configuration to the client, while in a pull model the client requests the configuration from the server. In the rest of this section, we will examine these points in greater detail.

Table 25.1 Configuration management tools

|                        | Ansible          | Terraform              | Puppet      | Chef        |
|------------------------|------------------|------------------------|-------------|-------------|
| Language               | Python           | Go                     | Ruby        | Ruby        |
| Configuration file format | YAML          | HashiCorp Language (HCL) | Puppet DSL | Ruby       |
| Communication protocol | SSH, NETCONF     | HTTP (API)             | HTTP (API)  | HTTP (API)  |
| Agent-based/agentless  | Agentless        | Agentless              | Agent-based | Agent-based |
| Procedural/declarative | Procedural       | Declarative            | Declarative | Procedural  |
| Push/pull              | Push             | Push                   | Pull        | Pull        |



Ansible, Terraform, Puppet, and Chef are all examples of infrastructure as code (IaC). Rather than the traditional method of provisioning and managing IT infrastructure through manually configuring servers and network devices, IaC provisions and manages infrastructure through code—configuration files that describe the desired state of the infrastructure and how to configure the available resources to achieve that desired state. By treating infrastructure as code, organizations can version control their infrastructure configurations, apply consistent settings across environments, and automate the entire lifecycle of infrastructure provisioning, management, and decommissioning.

25.2.1 Ansible
Ansible is a configuration management tool that was acquired by Red Hat (the creators of the popular Linux distribution Red Hat Enterprise Linux). Ansible itself is written in Python, although most of the files it employs are written in YAML. One of Ansible’s defining features is that it is agentless, meaning it doesn’t require any special software (an “agent”) to run on the managed devices. Instead, the Ansible control node—a server on which you have installed Ansible—uses SSH to connect to managed devices and push configuration changes to them.

Note In addition to SSH, Ansible can use NETCONF—a protocol developed to address some of SNMP’s limitations—to configure devices.

This is called a push model; instead of managed devices connecting to and pulling (retrieving) configuration information from the control node, the control node connects to and pushes (sends) configurations to its managed devices. Ansible primarily uses a procedural approach, where you define a sequence of steps or tasks to be executed on the managed devices in a specific order. Terraform, which we’ll cover next, takes a different approach. Figure 25.5 gives a high-level overview of how Ansible works.

Note The Ansible control node connects to TCP port 22 on the managed devices—the standard port used by SSH.



Figure 25.5 Basic Ansible operations. Inventory, template, and variable files define configurations, and playbooks define actions. The control node uses SSH to connect and push configurations to managed devices.

Push or pull?

The push model and the pull model each have their own advantages. The main advantages of a push model are centralized control and immediate updates. For example, if you need to send a critical configuration update to devices, you can configure the changes on the server, which can immediately push the changes to the managed devices.

On the other hand, the pull model tends to distribute the workload across the network, as each managed device independently checks for and applies updates. However, this can introduce delays, as you have to wait for devices to check in, rather than immediately pushing new configurations from the server. Neither approach is the correct answer in all situations; it depends on which suits your organization and network.

Ansible uses four main types of files:

Inventory—A file (usually in YAML format) that lists the hosts Ansible manages, optionally organizing them into groups. It can include variables specific to each individual host or group.

Template—Files containing configuration syntax and variables that are processed by Ansible to produce final configuration files for hosts. Templates use the Jinja2 templating language.

Variables—YAML files that list variables and their values. These values are inserted into the templates to create complete configuration files.

Playbook—A YAML file that outlines tasks and procedures to manage configurations on the managed devices defined in the inventory.

In addition to these four file types, there are two additional terms you should know:

Module—A discrete unit of code that can be used by a playbook to perform a specific task. Modules are essentially plugins or components of the Ansible application itself.

Task—A single operation or action as defined in a playbook.Of the tools we cover in this chapter, Ansible is the one that is most often used for managing network device configurations. Thanks to Ansible’s agentless design, no additional software is required on the managed devices; they just need to accept SSH connections from the control node. For this reason, Ansible is generally considered the simplest to set up and use to configure your network devices.

25.2.2 Terraform
Terraform is an IaC tool developed by HashiCorp. Whereas Ansible is primarily focused on configuration management, Terraform is primarily a provisioning tool, focused on deploying and provisioning new infrastructure (servers, databases, networks, etc.) rather than managing the configurations of existing infrastructure. While CCNA exam topic 6.6 refers to Terraform as a configuration management tool, that is typically not its main use case.

Note While Ansible and Terraform can both perform both roles (provisioning and configuration management), they are sometimes used together to take advantage of the strengths of each: Terraform to provision infrastructure and Ansible to manage its configuration.

Figure 25.6 gives a high-level look at how Terraform can be used to provision resources on various platforms.

A diagram of a software process Description automatically generated

Figure 25.6 Provisioning resources with Terraform. Configuration files are processed byTerraform Core to interact with various providers (i.e., public cloud providers) and manage infrastructure resources while maintaining state information in the state file.

Note Like Ansible, Terraform uses a push model and also doesn’t require a software agent to be installed on the devices it provisions or manages; it takes an agentless approach.

The basic Terraform workflow consists of three main steps:

Write—Define the desired state of your infrastructure resources in configuration files using HCL.

Plan—Verify the changes that will be executed before applying them.

Apply—Execute the plan to provision and manage the infrastructure resources according to the configuration files.

At the heart of Terraform is Terraform Core, the central part of Terraform that processes configuration files, manages the state of the infrastructure, and communicates with various providers to provision resources. Unlike Ansible’s procedural approach, Terraform employs a more declarative approach in which you define the desired end state for the infrastructure using configuration files rather than specifying the step-by-step instructions for how to achieve that desired state. Terraform Core compares the desired end state defined in the configuration files to the current state in the Terraform state file and takes the necessary steps to bring the infrastructure in line with the desired end state.

Terraform Core communicates with various providers to provision infrastructure resources; for example, public cloud providers like Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP). It does so via each provider’s APIs, allowing Terraform to interact with and manage a wide array of resources. Beyond public clouds, Terraform also supports on-premises infrastructure providers such as VMware vSphere and OpenStack, and container orchestration platforms like Kubernetes.

Note Most importantly for a CCNA candidate, Terraform can interact with a variety of Cisco platforms to provision and manage infrastructure. For example, there are Terraform integrations with Cisco Catalyst Center, Application-Centric Infrastructure (ACI—Cisco’s data center automatization solution), and IOS XE (a modern version of IOS that is run by many Cisco network devices, such as their Catalyst switches).

While Terraform itself is written in Go (a programming language developed by employees at Google), Terraform defines and provisions infrastructure using a configuration language called HashiCorp Configuration Language (HCL). HCL is an example of a domain-specific language (DSL)—a type of computer language that is specialized to a particular purpose (unlike general-purpose languages such as Python and Go).

The main benefits of a DSL such as HCL stem from its specialization; it’s designed specifically for its intended purpose and can often perform complex tasks with much less effort than a general language would require. However, it does mean you have to learn another language specifically for the purpose of using Terraform, which can be considered a downside.

25.2.3 Puppet and Chef
Puppet and Chef are two other prominent IaC tools that, like Ansible, are primarily used for the purpose of configuration management. Puppet and Chef were both included as topics in version 1.0 of the current CCNA exam (exam code 200-301), but were removed in version 1.1. However, it is worth taking a brief look at these two tools to compare and contrast them with Ansible and Terraform. There are two key differences:

In contrast to Ansible and Terraform’s push model, Puppet and Chef primarily use a pull model.

Whereas Ansible and Terraform use an agentless architecture, Puppet and Chef use an agent-based architecture.

Puppet

Puppet is an IaC tool for configuration management that is written in the Ruby programming language. It uses an agent-based architecture, meaning that a software agent needs to be installed on each managed device. Each device’s agent periodically connects to a central server, known as the Puppet master, to retrieve configuration information. This is known as a pull model. Instead of the management server connecting to managed devices to push configurations, the manage devices connect to the server to pull their configurations.

Like Terraform, Puppet uses a declarative DSL called Puppet DSL to define the desired state of the infrastructure. The Puppet master sends configuration instructions to the agents, which then apply the necessary changes to bring the devices into compliance with the defined state. The following example shows the simplicity of Puppet’s DSL.

service { 'ssh':        ❶
  ensure => running,    ❶
}                       ❶
❶ Ensures that the SSH service is running on the device

NOTE For an explanation of the reasoning behind Puppet’s use of a DSL, you can go straight to the source—Puppet’s founder wrote a short blog about it at https://www.puppet.com/blog/puppet-language. It’s an interesting read to learn about the benefits of a DSL.

While a popular tool for managing the IT infrastructure configuration, its level of adoption is relatively low compared to Ansible when it comes to managing networks; not all network devices support a Puppet agent, so Puppet is often not a viable choice.

Chef

Chef is another IaC tool for configuration management that bears some similarity to Puppet. Like Puppet, Chef is written in the Ruby programming language. Chef also uses an agent-based approach, requiring a Chef client to be installed on each managed device; this agent connects to the Chef server to pull and apply the latest configurations.

However, unlike Puppet, Chef uses a procedural approach. In Chef, you define a sequence of steps or tasks, known as recipes, which outline the specific actions needed to configure the system. These recipes are grouped into cookbooks, which can include additional components such as templates, files, and metadata. When the Chef client runs, it executes the recipes in the specified order to bring the managed device into the desired state.

Like Puppet, Chef doesn’t have the popularity of Ansible in the context of managing networks. This is likely why Puppet and Chef were removed from the CCNA exam topics list. However, I recommend knowing their basic characteristics. Specifically, you should understand how a pull model differs from a push model, and the difference between an agentless and agent-based approach.

Which tool to use?

We’ve explored some basic characteristics of these four tools, but which should an organization use? The choice depends on the needs of the particular organization. For example, if an organization’s network devices don’t support a Puppet or Chef agent, Ansible is the natural choice for configuration management. But even if device support isn’t an issue, the simplicity of Ansible’s agentless approach makes it the preferred tool in many networks.

Another key consideration is the operational mode: push or pull? Depending on the organization’s workflows and specific needs, Ansible may be favored for its push model. If a pull model is preferred, the choice is between Puppet and Chef. Of the two, Puppet’s declarative nature allows you to define the desired end state without specifying the specific steps to get there. Chef, on the other hand, takes a procedural approach, which may be preferred for those who want detailed control over the configuration process.

Terraform is primarily used for infrastructure provisioning rather than configuration management. If your primary need is to deploy infrastructure across various platforms, including cloud and on-premises environments, Terraform’s declarative approach and support for different providers make it an excellent choice. Terraform excels in provisioning complex multi-cloud environments and ensuring that the infrastructure remains consistent and reliable by maintaining the desired state through its configuration files.

Ultimately, the decision on which tool to use should be based on the specific requirements of your infrastructure and the workflows of your organizaon process.

Summary
Configuration management in networking involves various tasks aimed at maintaining, controlling, and documenting the configurations of network devices.

Although no two devices in a network will have identical configurations, they also shouldn’t be completely unique. To ensure the security and consistent operations of devices in a network, most configurations can be standardized.

Some configuration elements that can and should be standardized include DNS servers, NTP servers, routing protocols, QoS policies, AAA servers, security policies, and logging and monitoring settings.

Maintaining consistent configurations according to organizational standards is essential for the security and reliability of the network.

It’s common for network configurations to gradually diverge from standards due to human error, differing interpretations of the standards, and small ad hoc changes that accumulate over time. This is called configuration drift.

Configuration drift can pose significant challenges to network security and operational efficiency but is almost inevitable when managing a large and complex network manually.

Configuration management tools use software to automate various tasks related to configuration management, from deploying initial configurations and configuration changes to enforcing configuration standards.

Configuration management tools manage device configuration from centralized servers instead of on the devices themselves.

Configuration files are stored on the server, and the configuration management server is responsible for applying any changes to the appropriate devices.

Configuration management tools employ configuration templates that define the desired state and structure of device configurations using a standardized format and variables that store specific values unique to each device.

Configuration management tools can also monitor managed devices to enforce conformity to the standards defined in the configuration files on the server.

Ansible is a configuration management tool written in Python. One of its defining features is that it is agentless, meaning it doesn’t require any special software (an agent) to run on the managed devices.

The Ansible control node—a server on which you have installed Ansible—uses SSH to connect to managed devices and configure them.

Ansible uses a push model. Instead of managed devices connecting to and pulling configuration information from the control node, the control node connects to and pushes configurations to the managed devices.

Ansible primarily uses a procedural approach, where you define a sequence of steps or tasks to be executed on the managed devices in a specific order.

Ansible uses four main types of files:

Inventory—A YAML file that lists the managed hosts

Template—Jinja2 files containing configuration syntax and variables that are processed to produce final configuration files for hosts

Variables—YAML files that list variables and their values

Playbook—A YAML file that outlines tasks and procedures to manage configuration on the managed devices

Two other key terms are module—a discrete unit of code that can be used by a playbook to perform a specific task—and task—a single operation or action as defined in a playbook.

Terraform is an infrastructure as code (IaC) tool developed by Hashicorp. Whereas Ansible is primarily focused on configuration management, Terraform is primarily a provisioning tool, focused on deploying and provisioning new infrastructure.

Like Ansible, Terraform uses a push model and also doesn’t require a software agent to be installed on the devices it provisions or manages; it takes an agentless approach.

Terraform Core is the central part of Terraform that processes configuration files, manages the state of the infrastructure, and communicates with various providers to provision resources.

Terraform employs a declarative approach in which you define the desired end state for the infrastructure using configuration files rather than specifying the step-by-step instructions for how to achieve that desired state.

Terraform Core compares the desired end state defined in the configuration files to the current state in the Terraform state file and takes the necessary steps to bring the infrastructure in line with the desired end state.

Terraform is written in the programming language Go, but defines and provisions infrastructure using a language called HashiCorp Configuration Language (HCL). HCL is an example of a domain-specific language (DSL)—a type of computer language that is specialized to a particular purpose.

Puppet and Chef are two other prominent IaC tools that, like Ansible, are primarily used for the purpose of configuration management. Puppet and Chef are both written in Ruby.

In contrast to Ansible and Terraform’s push model, Puppet and Chef primarily use a pull model in which the managed devices connect to the management server to retrieve their configurations.

Whereas Ansible and Terraform use an agentless architecture, Puppet and Chef use an agent-based architecture. A software agent must be installed on managed devices.

Like Terraform, Puppet uses a declarative DSL called Puppet DSL to define the desired state of the infrastructure.

In contrast to Puppet’s declarative approach, Chef uses a procedural approach, similar to Ansible.