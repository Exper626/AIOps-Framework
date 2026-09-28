3 Domain Name System
This chapter covers

How Uniform Resource Locators identify a resource and how to access it
The hierarchical structure of the Domain Name System
The DNS name resolution process
Implementing a DNS on Cisco IOS devices
“What’s in a name?” Ask that to a computer, and you’ll learn that the answer is a number. Although we humans like to use memorable names to refer to the resources we access over a network (i.e., websites), computers use numbers—IP addresses—to identify each other. So when you type a name like “www.google.com” into a web browser’s address bar, how does your computer learn the IP address of the server that hosts Google’s website?

The answer is the Domain Name System (DNS). Using DNS, your computer resolves—or translates—the name “www.google.com” into the IP address of the appropriate server. DNS is one of the foundational protocols of the internet and is necessary knowledge not just for network engineers but for professionals in nearly any area of IT. DNS is the second half of CCNA exam topic 4.3: Explain the role of DHCP and DNS within the network. In this chapter, we’ll delve into the mechanics of DNS, its significance in network operations, and how to implement it on Cisco IOS.

3.1 How DNS works
Before looking at the Cisco-specific details of how to configure and verify DNS in IOS, let’s examine the protocol itself. DNS is an industry-standard protocol that is defined in a series of RFCs, and in this section, we’ll cover the fundamentals of how DNS works.

3.1.1 Uniform resource locators
To access a particular website, you can type the website’s address into the address bar of a web browser. For example, you might type https://www.google.com/maps to access Google Maps. An address like this is called a Uniform Resource Identifier (URI) or Uniform Resource Locator (URL); I’ll use the latter term.

URI, URN, and URL

A Uniform Resource Identifier (URI) is a unique sequence of characters that identifies a resource; that resource could be a file on a computer or a physical object like a book. URIs can be classified into two main types: Uniform Resource Names (URNs) and Uniform Resource Locators (URLs).

A URN is a unique identifier of a particular resource, without indicating its location or how to access it. An example is a book’s International Standard Book Number (ISBN); ISBN 9781633435780 identifies this volume but doesn’t tell you anything about where to buy it.

A URL, on the other hand, identifies both the resource itself and how to locate it. A web address like https://www.google.com/maps is an example of a URL; it identifies the resource (the Google Maps website) and tells your computer how to access it.

A URL consists of multiple elements; most URLs you encounter will include a scheme, authority, and path, as shown in figure 3.1. The scheme indicates the protocol that the browser will use to send its request to the web server—HTTPS, in this case. The authority indicates the name of the web server that the browser should send the request to; in this case, it’s Google’s web server at www.google.com. This name is called a domain name—more on domains and their names in section 3.1.3. The final element is the path, which identifies the specific resource on the server; in this case, it’s the /maps web page.



Figure 3.1 Elements of a URL. The scheme identifies the protocol, and the authority identifies the server’s name; they are separated by “://”. The path identifies the resource on the server.

Typing https://www.google.com/maps into the address bar and pressing Enter instructs the browser to use the HTTPS protocol to request the /maps resource on the www.google.com server. This is where DNS comes into play: your computer now has to translate the www.google.com domain name into an IP address that it can send packets to.

Note If you don’t specify a URL’s scheme when using a web browser, the browser will assume the default scheme—usually HTTPS. If you don’t specify the resource, you will be shown a default page, such as index.html or index.php. You can try it on my website: https://www.jeremysitlab.com/index.php should show the same page as www.jeremysitlab.com.

3.1.2 Name resolution
After you type a URL in a browser’s address bar and press the Enter key, your device will first check its DNS cache for a matching entry; the DNS cache temporarily stores previously resolved names and their corresponding IP addresses. If there is a matching entry in the DNS cache, the process is complete; your device knows the destination IP address, and there is no need to ask a DNS server.

Note A device’s DNS cache exists at multiple levels; the operating system (i.e., Windows) maintains its own cache, but many applications like web browsers maintain their own DNS cache as well.

If there isn’t a matching entry, your device has to send a DNS query to its DNS server asking the server to resolve the name to an IP address. Figure 3.2 shows a high-level overview of this process. PC1 uses DNS to resolve www.google.com to an IP address and then uses HTTPS to access the web server.



Figure 3.2 DNS name resolution. (1) PC1 sends a DNS query to its DNS server (8.8.8.8) asking for the IP address of www.google.com. (2) The DNS server replies, informing PC1 of the IP address. (3) PC1 communicates with the web server via HTTPS (for example, to retrieve a web page).

Note A device learns the IP address of its DNS server via either Dynamic Host Configuration Protocol (DHCP)—the next chapter’s topic—or manual configuration.

After successfully resolving the name www.google.com to an IP address, PC1 stores this mapping in its DNS cache. This means that it doesn’t have to send a new DNS query every time it wants to access the same website; it can use the cached information instead. The following example shows the entry for www.google.com in my PC’s DNS cache; on a Windows PC, you can view the DNS cache with the ipconfig /displaydns command in the Command Prompt:

C:\Users\jmcdo> ipconfig /displaydns
. . .
    www.google.com
    ----------------------------------------
    Record Name . . . . . : www.google.com
    Record Type . . . . . : 1
    Time To Live  . . . . : 267
    Data Length . . . . . : 4
    Section . . . . . . . : Answer
    A (Host) Record . . . : 142.250.196.100
. . .
DNS queries are sent to port 53 on the DNS server. However, DNS is different from most other protocols in that it can use both TCP and UDP as its Layer 4 protocol. While UDP is the most common Layer 4 protocol for standard DNS queries and responses (like the one in figure 3.2), TCP is used in certain situations, such as when the server’s response exceeds a certain size.

Exam Tip Don’t expect questions on the CCNA exam about whether DNS will use TCP or UDP in a particular situation. Just know that DNS can use both TCP and UDP and that DNS servers listen on port 53 in either case.

The hosts file

Many devices have a file that contains mappings of IP addresses to hostnames; for example, on my Windows 11 PC, the file is located in the C:\Windows\System32\drivers\etc folder and is called hosts. Before sending a DNS request, the device will check the hosts file to see if there is a mapping; this is entirely separate from the DNS resolution process. Before DNS existed, devices relied on this file for name resolution, but the lack of scalability led to the creation of DNS. Although the hosts file is still present on many devices, its use is limited.

3.1.3 The DNS hierarchy
In the previous section, we took a high-level look at how a host uses DNS to translate a name—such as the authority of a URL—to an IP address. However, within DNS, the name itself also consists of multiple elements, and knowing them is essential to understanding how DNS works.

DNS is a hierarchical naming system for computers connected to the internet. The DNS hierarchy is organized in a tree-like structure, and a domain is a subtree of that structure, under the administrative control of a particular organization or individual. Figure 3.3 illustrates a small portion of the DNS hierarchy, highlighting Google’s domain under “com.”



Figure 3.3 The DNS hierarchy. All domains are under the root domain, represented by “.”. Under the root domain, there are various top-level domains. Under each top-level domain, there are various second-level domains. The “google” domain, a subtree under the “com” top-level domain, is highlighted.

At the top of the DNS hierarchy, there is the root domain, which is usually represented by a single dot (.). Under the root domain, there are various top-level domains (TLDs). The most common TLD is com, but you’re likely familiar with other TLDs such as net and org. Likewise, under each TLD there are various second-level domains (SLDs), such as google or my own jeremysitlab. Then, under each SLD, there can be various third-level domains, fourth-level domains, etc. Each domain is a subdomain of the domains above it in the hierarchy. For example, in figure 3.3, google is a subdomain of com, which is a subdomain of the root domain.

The www domain name

You might be aware that WWW stands for World Wide Web, a global system that allows computers to share web pages over the internet. Given that meaning, you might expect www to be at the top of the hierarchy, encompassing all of the web. However, in this context, www doesn’t represent the entire web but is just a name that has been conventionally used for the server hosting the main website of an organization. This is not a technical standard, but rather a long-standing conventional practice. Many websites these days do not use www at all.

You may also notice that some websites can be accessed both through www.example.com and simply example.com. Technically, these could be two different addresses, but most organizations configure their DNS to redirect one to the other, making them effectively the same website for the end user.

A host’s complete name on the internet is called a fully qualified domain name (FQDN); an FQDN is written with a dot separating each part. One example of an FQDN is “www.google.com.”. You may have noticed an extra dot at the end of that FQDN; that represents the root domain. The final dot is often omitted, such as when typing a URL in an address bar—we usually write “www.google.com”. However, strictly speaking, a domain name without the final dot is not an FQDN but a partially qualified domain name (PQDN).

Note Strictly speaking, the dot at the end of an FQDN doesn’t actually represent the root domain; it’s a delimiting character between the TLD and the root domain, which has no name. For the rest of this chapter, I will omit this final dot.

The DNS hierarchy is a global system, and the same FQDN can be used to refer to the same host anywhere in the world. However, there are situations in which we refer to a host by a PQDN—a domain name that doesn’t include all of the information about the host’s location in the DNS hierarchy. For example, www could be the hostname of a business’ main web server, and its FQDN might be www.business.com. In the context of DNS, the hostname www is a PQDN—it identifies the www server within its domain business.com but doesn’t provide enough information to identify the host globally; there are countless other servers named www in different domains.

Note Domain names are not case-sensitive, but all lower-case is standard.

Domain name vs. hostname

These two familiar terms are frequently confused, and both can refer to different things (or the same thing) depending on the context. Let’s clarify them:

Domain name—This term refers to a region of administrative control within the DNS hierarchy, such as example.com, and includes any subdomains under it, such as www.example.com. Alternatively, this term can also specify a particular node within a domain; srv1.example.com is the domain name of a server within that domain.
In some cases, the same domain name can have both meanings. For example, google.com refers to Google’s realm of administrative control within the DNS hierarchy but also to a particular web server. If you access google.com in a web browser, your device will be directed to a web server that hosts Google’s website; this server’s domain name is google.com.

Hostname—This is an identifier for a specific device on the network. It could be a simple name like srv1 or an FQDN like srv1.example.com. Of course, an FQDN is also an example of a domain name (hence the name “fully qualified domain name”). So keep in mind that these terms can have different meanings depending on the context and can often be used interchangeably.

3.1.4 Recursive and iterative lookups
Now that you have a basic understanding of the DNS hierarchy, we can dig deeper into the DNS name resolution process by looking at two types of DNS lookups: recursive and iterative. Figure 3.4 shows how a combination of recursive and iterative DNS lookups are used to resolve mail.google.com to an IP address.



Figure 3.4 Recursive and iterative DNS requests resolve a domain name. In step 1, PC1 attempts to access mail.google.com. Steps 2 and 9 are a recursive DNS exchange between PC1 and the 8.8.8.8 DNS server. Steps 3 through 8 are iterative DNS exchanges between 8.8.8.8 and other DNS servers. Step 10 is an HTTPS exchange between PC1 and mail.google.com.

In step 1 of the diagram, a user tries to check his Gmail by accessing mail.google.com. In step 2, PC1 sends a recursive DNS query to its configured DNS server: 8.8.8.8 (a public DNS server run by Google). A recursive DNS query asks the DNS server to give the client a definite answer: either the IP address or an error message stating that the domain name could not be resolved. This is where the second type of DNS query comes into play; 8.8.8.8 will now query other DNS servers to find the answer for PC1. To do so, it will start at the top of the DNS hierarchy.

Note If 8.8.8.8 has a cached entry for mail.google.com, it will reply to PC1 with that information, and the name resolution process will be complete. Caching is used at every step of the name resolution process to reduce the number of DNS queries needed. However, for this demonstration, assume that each device’s cache is empty.

In step 3, 8.8.8.8 sends an iterative DNS query to a root DNS server—a DNS server at the top of the DNS hierarchy. 8.8.8.8 asks the root DNS server to resolve mail.google.com. However, instead of replying with an IP address, in step 4, the root DNS server replies with a referral to another DNS server. This is how iterative DNS queries work; they can be answered with an IP address or with a referral to another DNS server that might have the answer. Basically, the root DNS server is saying, “I don’t know the IP address of mail.google.com, but I know another server that might.”

The root DNS server refers 8.8.8.8 to a TLD server—specifically, a server responsible for the com TLD. In step 5, 8.8.8.8 sends an iterative query to the TLD server. The TLD server also doesn’t know mail.google.com’s IP address, so in step 6, the TLD server replies with a referral to another DNS server—the authoritative DNS server for the google.com domain. An authoritative DNS server holds the definitive set of records for a specific domain and, therefore, can give a definite answer in reply to queries about the domain.

Note Although 8.8.8.8 is a public DNS server operated by Google, it’s not the authoritative DNS server for the google.com domain. 8.8.8.8 is an example of a recursive resolver—a DNS server that resolves clients’ recursive DNS queries. It does so by sending iterative queries to other DNS servers, which may include root servers, TLD servers, and authoritative servers for the specific domain.

In step 7, 8.8.8.8 queries the authoritative server and receives a reply in step 8. In step 9, 8.8.8.8 finally replies to PC1’s recursive query, informing PC1 of mail.google.com’s IP address. Then, in step 10, PC1 initiates its HTTPS communication with mail.google.com.

Exam Tip Remember the general sequence of events in this process: a client sends a recursive query to a DNS server, and the server iteratively queries other DNS servers (starting at the root DNS server) to resolve the query.

3.1.5 DNS record types
DNS maps domain names to IP addresses, and each of these mappings is called a DNS record. However, there are various types of DNS records that can contain information other than IP addresses. In this section, we’ll briefly look at some different DNS record types that you should know for the CCNA exam. Table 3.1 summarizes the record types we’ll cover.

Table 3.1 DNS record types


| Record type | Description                                                          | Example                                                          |
|-------------|----------------------------------------------------------------------|------------------------------------------------------------------|
| `A`         | Points to an IPv4 address                                            | example.com -> 192.0.2.1                                         |
| `AAAA`      | Points to an IPv6 address                                            | example.com -> 2001:db8::1                                       |
| `CNAME`     | Points to another domain name                                        | www.example.com -> example.com                                   |
| `MX`        | Specifies the domain's mail server(s)                                | example.com -> mail1.example.com                                 |
| `NS`        | Specifies the domain's authoritative DNS server(s)                   | example.com -> ns1.example.com                                   |
| `PTR`       | Used for reverse DNS lookups, mapping an IP address back to a domain name | 192.0.2.1 -> example.com                                   |
| `SOA`       | Provides administrative information such as admin contact details, a serial number, etc. | example.com -> Admin: admin.example.com; Serial: 123456789; etc. |




Note You can look up DNS records for different domain names at https://www.whatsmydns.net/dns-lookup. You can view all of the available records or filter by type (A, AAAA, CNAME, etc.).
A DNS A record (address record) maps a domain name to an IPv4 address. All of the examples in this chapter so far have been A records. For another example, the A record for manning.com points to the IP address 35.166.24.88 (at the time of writing).
AAAA records (quad-A records) are similar to A records, except they map a domain name to an IPv6 address, not an IPv4 address. IPv6 addresses are quadruple the length of IPv4 addresses, hence the name.

A CNAME record (canonical name record) is used to create an alias for a domain name; it maps one domain name to another. One common use is to map www.example.com to example.com. For example, no A record exists for my website www.jeremysitlab.com. Instead, there is a CNAME record pointing to jeremysitlab.com. This means that you will be taken to the same page, regardless of whether you visit www.jeremysitlab.com or jeremysitlab.com.

An MX record (mail exchange record) is used to specify the domain’s mail servers. For example, I use Gmail as my email service, so my domain’s MX records point to Google’s email servers.

An NS record (name server record) is used to specify the domain’s authoritative DNS servers. For example, I use Bluehost to host my website, so my domain’s NS records point to Bluehost’s DNS servers.

A PTR record (pointer record) is unique; instead of mapping a domain name to an IP address, it maps an IP address to a domain name. This allows for reverse DNS lookups, which allow you to find the domain name that is associated with a particular IP address.

The final record type we’ll cover is the SOA record (start of authority record). An SOA record stores administrative information about the domain. Some example information stored is the contact information of the person or company responsible for the domain and a serial number that is used to keep track of updates to the domain’s records. The contact information will be listed, like admin.example.com, but the first dot should be replaced with an @ symbol to make an email address, such as admin@example.com.

Exam Tip You should know these different record types for the CCNA exam. There’s no need to know all the details; the level of depth covered in this section is fine.

DNS propagation delay

DNS propagation delay is the time it takes for changes to DNS records to be reflected across the internet, generally taking anywhere from a few minutes to 48 to 72 hours. One factor determining this is the time to live (TTL) value of the DNS records. Each record has a TTL value that specifies how long the record should be cached by DNS servers—the lower the value, the more frequently the record will be refreshed. Although the name is the same, this is a different concept than an IPv4 packet’s TTL.

If you change a DNS record (for example, to reflect your website’s new IP address) without considering propagation delay, visitors might be directed to the old IP address until the update fully propagates, leading to potential downtime or accessibility problems. One option to minimize the effect is to reduce the TTL values for the DNS records you plan to change well in advance of making the changes, allowing enough time for the previous TTL to expire before making the change.

3.2 DNS on Cisco IOS
You may have noticed something missing from this chapter up to this point—any mention of Cisco routers and switches! That’s because DNS is an exchange between a client and its DNS server; the role of the network infrastructure devices like routers and switches is simply to forward the messages between the communicating hosts.

Figure 3.5 demonstrates this point. PC1 uses DNS to learn the IP address of youtube.com and then uses HTTPS to access youtube.com. R1’s role in these exchanges is to forward packets between the communicating hosts: PC1 and 8.8.8.8 (the DNS server) and PC1 and youtube.com. SW1’s role is to forward frames between PC1 and R1.



Figure 3.5 The roles of R1 and SW1 in PC1’s DNS and HTTPS exchanges. R1’s role is to forward packets between the communicating hosts, and SW1’s role is to forward frames.

However, Cisco network devices themselves can be DNS clients and are also capable of functioning as DNS servers. In this section, we’ll take a look at various DNS-related configurations on R1; figure 3.6 shows the configurations we’ll cover.



Figure 3.6 DNS configurations on R1, enabling it to function as a DNS client and server and configuring manual name-to-IP-address mappings

3.2.1 Cisco IOS as a DNS client
For a Cisco IOS device, such as a Cisco router, to function as a DNS client—for it to be able to query a DNS server to resolve domain names to IP addresses—two commands are needed. The first command is ip domain lookup (it can also be configured with a hyphen: ip domain-lookup). This command enables the router to perform DNS queries, whether it is solely as a DNS client or as a DNS server querying other DNS servers.

Note The ip domain lookup command is enabled by default, so configuring it is actually unnecessary; I included it here to demonstrate the command. You can use no ip domain lookup if you want to disable DNS queries on the router.

The second command is ip name-server ip-address, which allows you to configure the router’s DNS server—the server it will send DNS queries to (name server is another name for a DNS server). In the following example, I attempt to ping google.com from R1 before configuring this command, but it fails. However, after configuring 8.8.8.8 as R1’s DNS server, the second ping succeeds:

R1# ping google.com
Translating "google.com"...domain server (255.255.255.255)
% Unrecognized host or address, or protocol not running.                 ❶
R1# configure terminal
R1(config)# ip name-server 8.8.8.8                                       ❷
R1(config)# do ping google.com
Translating "google.com"...domain server (8.8.8.8) [OK]                  ❸
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 172.217.161.46, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 8/8/9 ms     ❹
❶ R1 fails to resolve google.com.

❷ Configures 8.8.8.8 as R1’s DNS server

❸ The domain name is successfully resolved.

❹ The ping works.

Note You can specify multiple DNS servers (up to six) with the ip name-server command, either with a single command (i.e., ip name-server 8.8.8.8 1.1.1.1) or with separate commands. If the first server fails to resolve the domain name, the router will query the other server(s).

R1 is now a DNS client, capable of resolving domain names to IP addresses by querying its DNS server. To relate this to the previous chapter’s topic, we can configure R1 as an NTP client by specifying an NTP server’s domain name instead of its IP address. I demonstrate that in the following example by configuring R1 as an NTP client of one of Google’s NTP servers, time1.google.com:

R1(config)# ntp server time1.google.com                                       ❶
R1(config)# do show ntp associations
  address       ref clock  st   when  poll  reach  delay   offset  disp
*~216.239.35.0  .GOOG.     1    1     64    1      44.273  59.769  1937.5     ❷
 * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured
❶ Specifies the domain name of Google’s NTP server

❷ R1 resolved the domain name to an IP address.

3.2.2 Cisco IOS as a DNS server
A Cisco router can also be configured as a DNS server to be used by hosts in your network, and there are some advantages to doing so. One advantage is performance; the router can cache queries for commonly accessed websites. For example, if one host in the LAN accesses youtube.com, the router will cache the DNS mapping and use it to respond to other hosts’ queries for the same name. This means that an external DNS server doesn’t have to be queried every time another host wants to access the same website.

The command to configure a router to become a DNS server is ip dns server. With that command configured, the router will be able to respond to clients’ DNS queries. Of course, it’s not expected that the router will be able to resolve all DNS queries itself; it will query other DNS servers (as configured with the ip name-server command) to do so. Figure 3.7 shows how a Cisco router, R1, queries its own DNS server (8.8.8.8) to resolve a query it receives from a DNS client, PC1.

Note Both DNS queries shown in figure 3.7—PC1’s query to R1 and R1’s query to 8.8.8.8—are recursive queries. 8.8.8.8 will perform iterative queries to resolve the domain name if needed. Basically, R1’s role is to forward clients’ DNS queries on to 8.8.8.8 and cache the responses, allowing R1 to quickly respond to other clients who send DNS queries for the same domain names.



Figure 3.7 R1 is a DNS server for hosts in its connected LAN. (1) PC1 queries R1 to resolve the domain name youtube.com. (2) R1 can’t resolve the name itself, so R1 queries 8.8.8.8. (3) 8.8.8.8 responds to R1, informing it of youtube.com’s IP address, and then (4) R1 responds to PC1. In step 5, PC1 communicates with youtube.com via HTTPS.

You can also manually configure name-to-IP-address mappings on a router; creating such mappings for hosts in the internal network allows them to communicate with each other via hostnames instead of IP addresses. In the following example, I demonstrate the necessary configurations and verify:

R1(config)# ip domain name jeremysitlab.com           ❶
R1(config)# ip host r1.jeremysitlab.com 10.0.0.1      ❷
R1(config)# ip host pc1.jeremysitlab.com 10.0.0.11    ❷
R1(config)# ip host pc2.jeremysitlab.com 10.0.0.12    ❷
❶ Defines a default domain name

❷ Configures manual name-to-IP-address mappings

The first command is ip domain name name, which can also be configured as ip domain-name name (with a hyphen). This command defines a default domain name that R1 will append to DNS queries that specify only a hostname instead of a full domain name. For this example, I used the domain name jeremysitlab.com.

The ip domain name command is optional but useful: users will be able to use hosts’ hostnames without having to specify each host’s full domain name. For example, a user on PC1 can ping PC2 with ping pc2 instead of ping pc2.jeremysitlab.com; R1 will append the domain name itself.

Note The ip domain name command is also a step in configuring Secure Shell (SSH) on a device to enable remote access to its CLI; SSH is the topic of chapter 5.

The command to manually configure a name-to-IP-address mapping is ip host name ip-address. I configured three: one for R1 itself, one for PC1, and one for PC2. To confirm the mappings, you can use the show hosts command; this shows both the manually configured mappings as well as mappings that the device learned via DNS. The following example shows the output. Notice that R1 has an entry for youtube.com, which it resolved via DNS (figure 3.7’s example), and the three manually configured entries:

R1# show hosts
Default domain is jeremysitlab.com
Name/address lookup uses domain service
Name servers are 8.8.8.8
 
Codes: UN - unknown, EX - expired, OK - OK, ?? - revalidate
       temp - temporary, perm - permanent
       NA - Not Applicable None - Not defined
 
Host                      Port  Flags      Age Type   Address(es)
youtube.com               None  (temp, OK)  0   IP    142.251.42.174     ❶
r1.jeremysitlab.com       None  (perm, OK)  0   IP    10.0.0.1           ❷
pc1.jeremysitlab.com      None  (perm, OK)  0   IP    10.0.0.11          ❷
pc2.jeremysitlab.com      None  (perm, OK)  0   IP    10.0.0.12          ❷
❶ Dynamically learned mapping for youtube.com

❷ Manually configured mappings for R1, PC1, and PC2

In the following example, I ping PC2 from PC1 (a Linux host) with the ping pc2 command, resulting in PC1 sending a DNS query to R1 to learn PC2’s IP address. Although R1 doesn’t have a mapping for pc2, R1 appends the default domain name jeremysitlab.com, resulting in pc2.jeremysitlab.com, for which R1 does have a mapping. R1 then responds to PC1’s DNS query, and as the example shows, PC1’s ping is successful:

jeremy@PC1:~$ ping pc2
PING pc2 (10.0.0.12): 56 data bytes
64 bytes from 10.0.0.12: seq=0 ttl=255 time=5.825 ms
64 bytes from 10.0.0.12: seq=1 ttl=255 time=2.962 ms
. . .
Summary
Domain Name System (DNS) is a protocol that resolves (i.e., translates) names like www.google.com to IP addresses.

An address like https://www.google.com/maps is called a Uniform Resource Identifier (URI) or Uniform Resource Locator (URL)—a URL is a type of URI that identifies both the resource (the web page) and how to locate it.

A URL consists of multiple elements, such as the scheme—the protocol that should be used to access the resource (https); the authority—the server that hosts the resource (www.google.com); and the path—the specific resource on the server (/maps).

When you type a URL into a web browser, your computer will use DNS to translate the authority (the domain name of the server) into an IP address.

DNS lookups consist of a DNS query from the client and a DNS query response from the server. The client will then store the name-to-IP-address mapping in temporary storage called the DNS cache for future use.

Client devices learn the IP address of their DNS server either via Dynamic Host Configuration Protocol (DHCP) or manual configuration.

DNS queries are sent to port 53 on the DNS server. Standard queries and responses use UDP, but TCP is used in certain situations.

DNS is a hierarchical naming system, organized in a tree-like structure. A domain is a subtree of that structure.

The root domain (.) is at the top of the DNS hierarchy, and there are various top-level domains (TLDs) under it, such as com. Each TLD has various second-level domains (SLDs) under it, such as google.com, and each SLD can have various subdomains, such as www.google.com.

A domain name that specifies its exact location in the DNS hierarchy is called a fully qualified domain name (FQDN). The dot at the end of an FQDN is a delimiter between the TLD and the root domain, which has no name; the dot is often omitted.

A domain name that only includes partial information, such as only the hostname configured on the device, is a partially qualified domain name (PQDN).

When a host sends a DNS query to its DNS server, it sends a recursive query—a query that asks for a definite answer: an IP address or an error message stating that the domain name could not be resolved. The DNS server responsible for resolving recursive queries is called a recursive resolver.

The recursive resolver will then send a DNS query to a root DNS server—a DNS server at the top of the DNS hierarchy. This is an iterative query—a query that can be answered with an IP address or with a referral to another DNS server.

The root server will refer the recursive resolver to a TLD server—a DNS server responsible for the relevant TLD.

The TLD server will refer the recursive resolver to an authoritative DNS server—a server that holds the definitive set of records for the specific domain and can, therefore, give a definite answer in reply to queries.

After receiving a response from the authoritative server, the recursive resolver will reply to the client’s recursive query.

Caching is used at every step of the name resolution process to reduce the number of DNS queries required. For example, if the recursive resolver had a cached entry for the domain name that the client queried, it would reply with that information.

DNS records can contain information other than IP addresses. Some record types include A, AAAA, CNAME, MX, NS, PTR, and SOA:

A records map a domain name to an IPv4 address.

AAAA records map a domain name to an IPv6 address.

CNAME records map a domain name to another domain name.

MX records specify the domain’s mail servers.

NS records specify the domain’s authoritative DNS servers.

PTR records map an IP address back to a domain name.

SOA records provide administrative information such as admin contact details and a serial number.

Beyond forwarding packets and frames, network devices like routers and switches don’t participate in DNS exchanges between DNS clients and servers. However, Cisco IOS devices themselves can be DNS clients and servers.

Cisco IOS devices need the ip domain lookup (or ip domain-lookup) command to be able to send queries to DNS servers; this command is enabled by default.

Use ip name-server ip-address to specify the device’s DNS server—the server it will send DNS queries to.

Use ip dns server to configure the device as a DNS server to allow it to respond to clients’ DNS queries.

Use ip domain name name (or ip domain-name name) to configure the device’s default domain name. It will automatically append this domain name to DNS queries that don’t specify a domain name.

Use ip host name ip-address to manually configure name-to-IP-address mappings. This is useful for hosts in the internal network.

Use show hosts to display all name-to-IP-address mappings, including manually configured mappings and those learned via DNS.