23 REST APIs
This chapter covers

How applications communicate and share data
HTTP requests and responses
REST API architecture
Making REST API calls to Cisco Catalyst Center
Programming and automating networks require seamless communication between software running on various devices—from network equipment like routers and switches to servers, controllers in an SDN architecture, and the network administrator or engineer’s own PC. There are two essential elements that facilitate communication between these software applications: an interface that opens up each application’s data to external applications and standard data formats for exchanging information efficiently.

In this chapter, we’ll cover the first piece of the puzzle: application programming interfaces (APIs). APIs are software interfaces that enable two or more software applications to communicate with each other. Specifically, we will examine representational state transfer (REST) APIs, which are commonly used in network automation contexts, such as the northbound interface (NBI) of an SDN controller. Specifically, we will cover CCNA exam topic 6.5: Describe characteristics of REST-based APIs (authentication types, CRUD, HTTP verbs, and data encoding).

23.1 The purpose of APIs
Enabling two applications to communicate and share data is no simple task, especially when they are written by different developers in different programming languages. Without APIs, achieving communication between applications often requires building custom integrations between each pair of applications—a time-consuming and expensive process that results in a tangled web of point-to-point connections between applications. A custom integration between app A and app B wouldn’t help either communicate with app C.

An API is a software interface that opens up an application’s data in a way that allows other applications to access it in a uniform manner. Figure 23.1 illustrates how an API facilitates communications between applications.



Figure 23.1 An API on app D provides a uniform interface for external apps to access app D’s internal data.

Apps A, B, and C don’t need to know the intricate details of app D’s inner workings; they can simply make an API call (request) to app D’s API. The API interprets and fulfills the request, returning the relevant information in a response. Basically, APIs simplify and standardize the way applications communicate, making an otherwise complex and costly process manageable and scalable.

23.2 HTTP
APIs can be used to facilitate communications between applications, whether they’re running on the same system or remote systems. For applications on different machines to communicate over a network, a suitable communication protocol is required; for most REST APIs, HTTP is the protocol of choice. Figure 23.2 illustrates an API call in the form of an HTTP request, receiving a response in the form of an HTTP response.



Figure 23.2 An API call in the form of an HTTP request receives a response in the form of an HTTP response. The HTTP request includes an HTTP method and a URI, and the response includes a response code and the relevant data.

HTTP is a natural choice for REST APIs due to its ubiquity on the web and its alignment with REST’s architectural principles; we’ll cover those in section 23.3. In this section, let’s take a look at the various HTTP methods that define a request’s desired action, and then we’ll look at the response codes that can be sent in reply.

23.2.1 HTTP requests
HTTP uses a client-server architecture in which clients send requests and servers send responses. In an HTTP request, the client specifies the Uniform Resource Identifier (URI) of the resource it wants to access. But specifying the resource’s URI isn’t enough for the server to take action; the client needs to tell the server exactly what action it wants the server to take on the specified resource. Consider what kinds of actions can be taken on a resource:

Create—Create a new resource on the server

For example, create variable "ip_address", and set the value to 10.1.1.1.

Read—Retrieve a resource from the server

For example, what is the value of variable "ip_address"?

Update—Modify an existing resource on the server

For example, change the value of variable "ip_address" to 10.2.3.4.

Delete—Delete a resource from the server

For example, delete variable "ip_address".

These four types of actions are called CRUD (Create-Read-Update-Delete) operations. CRUD isn’t an HTTP-specific term but rather a general description of the four basic operations for manipulating and managing data. To specify exactly what action the client wants to perform on the specified resource, it includes an HTTP method in its request.

Figure 23.3 shows the format of an HTTP request message. It begins with a start line (containing the method, URI, and HTTP version of the request), optional headers that provide additional information, a blank link separating the headers from the body, and then the optional message body (which is only present in some request types).



Figure 23.3 The format of an HTTP request, consisting of a start line, headers, a blank line, and a message body. This message is an API call requesting to create a new ACL rule.

Note CCNA exam topic 6.5 specifically refers to HTTP verbs—another term for HTTP methods (although not all HTTP methods are verbs—some are nouns). I will use the more accurate term: method.

The HTTP method is key because it is how the client specifies what it wants to do with the resource it is trying to access. Table 23.1 lists common HTTP methods and their equivalent CRUD operations. The HTTP POST operation is most often used to create a new resource on the server. GET is used to retrieve a resource from the server (or read its contents); your PC sends a GET request to retrieve a web page from a web server. PUT and PATCH are used to update a resource; the difference between the two is that PUT replaces the specified resource, and PATCH modifies it. Finally, DELETE is used to—you guessed it—delete the specified resource.

Table 23.1 CRUD operations and HTTP methods

| CRUD operation | Purpose             | HTTP method |
|----------------|---------------------|-------------|
| Create         | Create new resource | POST        |
| Read           | Retrieve resource   | GET         |
| Update         | Modify resource     | PUT, PATCH  |
| Delete         | Delete resource     | DELETE      |


Note Although the mappings listed in table 23.1 are generally accepted, they are not 1:1 equivalents, and some can map to different CRUD operations in different situations. For example, the PUT method can also be used to create resources. Each API has documentation that specifies exactly how it uses the HTTP methods.

23.2.2 HTTP responses
The example HTTP request we saw in figure 23.3 was an API call to create (POST) a new ACL rule on an SDN controller. After receiving and processing the request, the server (the SDN controller) will send an HTTP response. Figure 23.4 shows the HTTP response message format.



Figure 23.4 The format of an HTTP response. The response code 201 Created indicates that the resource (the ACL rule requested in figure 23.3) was successfully created.

Note Figures 23.3 and 23.4 both include the Content-Type: application/json header, indicating that the message body uses the JavaScript Object Notation (JSON) data format—foreshadowing! We’ll cover JSON and other data formats in chapter 24.

The response code in the start line is the key element here; this code indicates the result of the request (i.e., success or failure). There are five main categories of response codes, indicated by their first digit:

1xx informational—A provisional response. The initial part of the request has been received, and additional actions may be expected to follow.

2xx successful—The request was received without problems, understood, and processed as expected.

3xx redirection—Additional steps are required to complete the request.

4xx client error—Points to an error on the client’s part, either due to incorrect syntax or because the request is infeasible.

5xx server error—Indicates that the server encountered an error and can’t perform the request, even though the request appears to be valid.

Each response code consists of a three-digit numeric code and a short name. Table 23.2 lists and describes some common response codes (one or two from each category). For a complete list of HTTP response codes, check out this page from Mozilla: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status.

Table 23.2 HTTP response codes


| Code                      | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| 102 Processing            | The server is processing the request, but the response is not yet available. |
| 200 OK                    | The request succeeded.                                                      |
| 201 Created               | The request succeeded and a new resource was created.                       |
| 301 Moved Permanently     | The requested resource has been moved.                                      |
| 403 Forbidden             | The client is not authorized to access the resource.                        |
| 404 Not Found             | The requested resource was not found.                                       |
| 500 Internal Server Error | The server encountered something unexpected that prevented it from fulfilling the request. |



Figure 23.5 illustrates the client–server exchange that we saw in figures 23.3 and 23.4. The client sends a POST request to create a new ACL rule, and the server receives the request, processes it (creating the ACL rule), and sends a response with the code 201 Created.


Figure 23.5 An HTTP exchange. (1) The client requests to create (POST) a new ACL rule. (2) The server creates the new rule. (3) The server sends a response with code 201 Created, indicating the ACL rule was created.

23.3 REST APIs
Representational state transfer (REST) is a type of software architecture that forms the basis of the World Wide Web. APIs that conform to REST architecture are called REST APIs or RESTful APIs. Most REST APIs are HTTP-based, using the various HTTP methods described in the previous section to interact with resources. In this section, we’ll delve into REST architecture and make an API call to Cisco Catalyst Center.

23.3.1 REST architecture
REST architecture is defined by six constraints:

Uniform interface

Client-server

Stateless

Cacheable or noncacheable

Layered system

Code on demand (optional)

For the purpose of the CCNA exam, it’s not worth digging into the details of all six constraints, but let’s cover three to give you an idea of how REST APIs work.

REST: Client-server

REST APIs employ a client-server architecture. Clients use API calls (HTTP requests) to access resources on the server, which receives, processes, and responds to those requests. The strict separation between the client and server applications is essential; the client and the server must be able to change and evolve independently without breaking the interface between them (the API).

REST: Stateless

REST API exchanges are stateless, meaning that each API exchange is a separate event, independent of all past exchanges between the client and server. We’ve covered a few stateful and stateless concepts previously:

Stateful—Stateful firewalls, TCP

Stateless—Access control lists (ACLs), UDP

Stateful firewalls and TCP are considered stateful because they remember and keep track of past interactions to make decisions about future interactions. Stateful firewalls don’t just consider individual packets with no other context; they consider each packet’s relationship to other packets when deciding whether the packet should be permitted or denied. And TCP, a connection-oriented protocol, keeps track of the state of connections and the delivery of packets.

ACLs and UDP do neither of those things and are therefore stateless; each message is its own event, independent of those before or after it. In the context of REST APIs, stateless means that the server does not store information about previous requests from the client to determine how it should respond to new requests.

Note Although REST APIs use HTTP, which employs TCP (stateful) as its Layer 4 protocol, HTTP and REST APIs themselves are stateless. Don’t forget that the functions of each layer of the TCP/IP model are independent!

One implication of REST’s stateless nature is that if authentication is required, the client must provide authentication credentials in every single request. This can be done with a simple username/password that is included with each request, but a more robust approach is to require clients to generate an access token (also called an authorization token). We’ll examine a few authentication methods in section 23.3.2.

REST: Cacheable or non-cacheable

If a resource is cacheable, it means that it can be cached—temporarily stored for reuse. This can significantly improve efficiency; there’s no need to retrieve the same resource repeatedly when accessing it multiple times. For example, frequently accessed web pages can be cached to improve load times.

However, not all resources should be cached; sensitive and frequently updated information should not be cached. For example, a user’s personal dashboard showing a real-time account balance in a banking application is not a good candidate for caching. Caching the data could lead to outdated information being displayed, and it poses a security risk if the sensitive data is stored inappropriately.

In REST architecture, resources can be cacheable or noncacheable, but they must be marked as such, whether implicitly or explicitly. Cacheable resources must be marked as cacheable, and noncacheable resources must be marked as noncacheable.

Note Check out https://restfulapi.net/rest-architectural-constraints/ for an explanation of all six REST architectural constraints.

23.3.2 REST API authentication
APIs provide access to an application and its data, so security is a major concern when designing and using APIs. Instead of responding to all requests, the server should properly authenticate and authorize clients. If the process is successful, the server fulfills the request. If the process fails (e.g., due to invalid credentials or insufficient permissions), the server refuses the request.

In this section, we’ll examine a few common REST API authentication methods:

Basic authentication—a simple username/password are provide for authentication

Bearer authentication—a token the client obtains from an authentication server and then includes in its API calls

API key authentication—a unique identifier assigned to a client application that allows it to access the API

OAuth 2.0—an industry-standard framework that provides access delegation

Basic authentication

Basic authentication is a simple method where a username and password are provided in the HTTP header for authentication. While simple and convenient to implement, basic authentication is not considered secure because it suffers from the same weaknesses as other simple username/password-based solutions: if a malicious user obtains the credentials, they can gain access to the API. If using basic authentication, it’s critical to use HTTPS to encrypt the API calls; if using standard HTTP, the credentials are sent in unencrypted cleartext.

Bearer authentication

In bearer authentication, the client obtains a token (the “access token” mentioned in section 23.3.1) that it then provides for authentication in its API calls. This token can be obtained in various ways; often, the client obtains the token from an authorization server by first going through a separate authentication process, often using a username and password. Access tokens are typically valid for a limited time, requiring renewal for continued use.

Bearer authentication is generally considered more secure than basic authentication because the client does not have to repeatedly transmit the same username/password. However, like basic authentication, bearer authentication should only be used with HTTPS to ensure the token is transmitted securely. Even though the token itself doesn’t contain sensitive information like a username/password, it grants access to API resources. Interception of the token could allow an attacker unauthorized access to the resources.

Figure 23.6 shows an example of bearer authentication; the client obtains a token from an authorization server and then uses the token to access the API of the server that hosts the desired resource.

A close-up of a list of access Description automatically generated

Figure 23.6 REST API bearer authentication. A client obtains an access token from an authorization token and uses the token to access the desired resource on the resource server.

Note In some cases, the same server might function as both the authorization server and the resource server in bearer authentication. We’ll see an example of this in section 23.3.3.

API key authentication

API key authentication involves the use of a unique identifier assigned to each client application. The client application includes this key in its API calls, similar to an access token used in bearer authentication. However, it’s important to note that an API key identifies an application, not a user; for user-based authentication and authorization, access tokens are more appropriate.

Unlike access tokens, which are generally short-lived and expire after a set period of time, API keys typically do not automatically expire (unless revoked by the server). This makes them less secure if not managed properly, as they can be used indefinitely if compromised.

API keys are usually easier to implement and use, but they lack the fine-grained control and security features offered by more sophisticated authentication methods. And once again, if security is a concern, always use HTTPS to encrypt API calls; otherwise, the API key can easily be intercepted in transit.

OAuth 2.0

Open Authorization 2.0 (OAuth 2.0) is an industry-standard framework that is widely used in modern web applications. OAuth 2.0 provides access delegation, allowing third-party applications to access resources (i.e. via a REST API) on behalf of a user without sharing the user’s credentials. You’ve almost certainly used OAuth 2.0 before. Some common examples you might be familiar with are:

Logging in with Google—Many websites and apps offer the option to log in using your Google account instead of creating a new account on the website itself. OAuth 2.0 allows the website or app to access your basic Google profile information without sharing your password with the third-party service.

Connecting apps to social media accounts—When you connect apps to your account on Instagram, Facebook, LinkedIn, or other social media platforms, OAuth 2.0 is used to grant these tools permission to read your social media data or post on your behalf.

Calendar integration—A third-party tool might request access to your Google Calendar to check your availability and schedule meetings. When you authorize this, Google provides an access token to the tool, which allows it to view and manage your calendar without needing your Google account password.

There are countless other examples. Figure 23.7 gives a high-level overview of how OAuth 2.0 works. To make sense of the diagram, consider the third example listed previously: a third-party tool requesting access to Google Calendar on your behalf. The client in figure 23.7 is the third-party tool requesting access. The resource owner is you—the person who owns the Google account associated with the calendar and is, therefore, capable of granting access to the calendar. The auth server is Google’s authorization server, and the resource server is Google’s server that hosts the information relevant to your Google Calendar.

A diagram of a flowchart Description automatically generated

Figure 23.7 The basic OAuth 2.0 process. Through access delegation, the client application is able to access the resource owner’s protected resources on behalf of the owner.

Let’s walk through the basic process as illustrated in figure 23.7:

The client (third-party tool) requests authorization from the resource owner (you) to access the resource (your Google Calendar data).

The resource owner grants the authorization by logging into their account and giving permission.

The client exchanges the authorization grant for an access token from the auth server (Google’s authorization server).

The auth server provides an access token to the client.

The client uses the access token to request the protected resource from the resource server (Google’s server).

The resource server validates the access token and provides the requested resource (calendar data) to the client.

The access token granted in step 4 of the process functions just like the access token used in bearer authentication, as covered previously. The token grants access to the specified resources within the appropriate scope of access and is typically valid only for a limited period, requiring regular renewal. This could require the user to manually grant authorization again, or the client might receive a refresh token from the authorization server that allows it to automatically refresh its access token multiple times within a longer period of time.

Note The access token granted to the client has a specific scope that dictates exactly what resources the client can access and what actions it can perform; this scope is enforced by the resource server. It’s best to be cautious about granting third-party apps access to your accounts beyond what is necessary.

23.3.3 Making REST API calls to Catalyst Center
In this section, we’ll make a couple of API calls to Cisco’s always-on Catalyst Center sandbox that I introduced in the previous chapter. To do so, we’ll use Postman, a versatile platform for building, testing, and using APIs.

Note You can access Postman at https://www.postman.com/. You’ll have to make a Postman account if you want to follow along (it’s free). Another option is Insomnia, available at https://insomnia.rest/, but I will use Postman for this demonstration.

Our objective is to retrieve Catalyst Center’s inventory list—the list of devices it manages. First, we need to generate an access token. After logging in to Postman, click Workspaces, and then open My Workspace, as shown in figure 23.8.



Figure 23.8 Accessing My Workspace in Postman to make an API call

From My Workspace, click New and then HTTP, as shown in figure 23.9; we are going to send HTTP requests to Catalyst Center’s REST API.



Figure 23.9 Click New and HTTP to send HTTP requests to Catalyst Center’s REST API.

Now it’s time to make the first API call: a POST request to generate an access token that we will use in the next API call. Figure 23.10 shows how to do this:

Specify the POST method and URI https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token.

Click Authorization, and select Basic Auth.

Enter the username devnetuser and password Cisco123!.

Click Send to send the API call to Catalyst Center.

Copy the token from the response.



Figure 23.10 Generating an access token with a POST request to Catalyst Center

After sending the POST, you should receive a response with code 200 OK (you can see Status: 200 OK under the user credentials in figure 23.8) and the token itself. The following output shows the access token generated from my POST request; your token will be different:

{
"Token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MGVjNGU0ZjRjYTdmOTIyMmM4M
mRhNjYiLCJhdXRoU291cmNlIjoiaW50ZXJuYWwiLCJ0ZW5hbnROYW1lIjoiVE5UMCIsInJvbGVz
IjpbIjVlOGU4OTZlNGQ0YWRkMDBjYTJiNjQ4ZSJdLCJ0ZW5hbnRJZCI6IjVlOGU4OTZlNGQ0YWR
kMDBjYTJiNjQ4NyIsImV4cCI6MTcwMzEzMDEyOSwiaWF0IjoxNzAzMTI2NTI5LCJqdGkiOiJhN2
NhY2UyMS0wNTkxLTQxOWUtOGE4OC00MzA4NGQ1NWM2ODQiLCJ1c2VybmFtZSI6ImRldm5ldHVzZ
XIifQ.qQPwxcfIds3VwrXBuDL4QWbZmw4yC8cpP-
aiieCoIR_8D6DQRXLIp7dO_bTJw_V2jKbZSSrZZXQebqXJNriIQIeB-
6JBTPatLNDbpYxIik4WtuANTh0dp6DOhIlrZ_x68tZYhI-AklzLAMq-lrhiER-
etexXGUORjfs4UqdjKkgrNq7tFfX7d3_OtrsmfSySuyE9ib3WS-
DaegHsjYm5Zj6I0o_BgHc3YNxJVgyrioXDC2EssK4pmjwH4yfSTOhwGP2dUfuCb8So6P82skuKM
0WChXgZW-oPOkoCt0bTucwqnxWZ1xwPT2VNw-MIYA4ZrMC1t5WpFpX2NKGMM3N1nw"
}
Note The token is the long string of characters inside of double quotes; don’t copy the double quotes themselves. The output is JSON-formatted, and the double quotes indicate a JSON string—more on that in the next chapter!

Now that we have an access token, let’s make a second API call to retrieve Catalyst Center’s inventory list. Figure 23.11 shows the process:

Specify the GET method and URI https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device.

Select Header to add an additional HTTP header to the API call.

Add the key X-Auth-Token, and paste the token you generated previously as the value.

Click Send to send the API call to Catalyst Center.



Figure 23.11 Sending a GET request to Catalyst Center to retrieve its inventory list

The Catalyst Center sandbox only manages four devices, but the message body of the response is 193 lines in length—too long to include all of it here. The following output shows a portion of the first device’s information, including details like its MAC address, software version, hostname, and serial number. Once again, this data uses the JSON format:

{
    "response": [
        {
. . .
            "lastUpdateTime": 1703094122734,
            "bootDateTime": "2023-12-19 17:25:02",
            "macAddress": "52:54:00:01:c2:c0",
            "apManagerInterfaceIp": "",
            "deviceSupportLevel": "Supported",
            "softwareType": "IOS-XE",
            "softwareVersion": "17.9.20220318:182713",
            "hostname": "sw1",
            "serialNumber": "9SB9FYAFA2O",
. . .
In summary, we made two API calls to Catalyst Center: a POST request to generate an access token and a GET request to retrieve Catalyst Center’s inventory list. For a more detailed walkthrough and further resources on Catalyst Center, you can check out this guide on Cisco DevNet: https://mng.bz/WE6a.

Cisco DevNet

DevNet is a program by Cisco to support developers and other IT professionals looking to create applications and integrations using Cisco’s suite of products and APIs. It provides resources such as documentation, courses, learning labs, and sandbox platforms for experimentation. If you want to dive deeper into network automation, DevNet is an invaluable resource. Check it out at https://developer.cisco.com/.

Summary
Application programming interfaces (APIs) are software interfaces that open up an application’s data in a way that allows other applications to access it in a uniform manner, facilitating communications between applications.

To access an application’s internal data, other applications can simply make an API call (request) to the application’s API. The API interprets and fulfills the request, returning the relevant information in a response.

For applications on different machines to communicate over a network, a communication protocol is required. For most REST APIs, HTTP is the protocol of choice.

HTTP uses a client–server architecture in which clients send requests and servers send responses.

The essential actions that can be taken on a resource are called CRUD (Create-Read-Update-Delete) operations.

An HTTP request can include various pieces of information. The two key elements are the HTTP method (also called the HTTP verb), which defines the request’s desired action (CRUD operation), and the Uniform Resource Identifier (URI), which indicates the target of the request.

HTTP methods can generally be mapped to one of the four CRUD operations: create (POST), read (GET), update (PUT, PATCH), and delete (DELETE).

An HTTP response uses a similar format to an HTTP request. The key element is the response code, which indicates the result of the request.

There are five main categories of HTTP responses, indicated by their first digit:

1xx informational

2xx successful

3xx redirection

4xx client error

5xx server error

Some common response codes are 102 Processing, 200 OK, 201 Created, 301 Moved Permanently, 403 Forbidden, 404 Not Found, and 500 Internal Server Error.

Representational State Transfer (REST) is a type of software architecture that forms the basis of the World Wide Web. APIs that conform to REST architecture are called REST APIs or RESTful APIs.

REST architecture is defined by six constraints:

Uniform interface

Client-server

Stateless

Cacheable or noncacheable

Layered system

Code on demand (optional)

REST APIs employ a client-server architecture. The client and server applications must be able to change and evolve independently without breaking the interface between them (the API).

REST API exchanges are stateless, meaning that each API exchange is a separate event, independent of all past exchanges between the client and server.

The server does not store information about previous requests from the client to determine how it should respond to new requests.

If a resource is cacheable, it means that it can be cached—temporarily stored for reuse. This can significantly improve efficiency because there’s no need to retrieve the same resource repeatedly when accessing it multiple times.

Frequently updated and sensitive information should not be cached. Caching such data could lead to outdated information being displayed, and it poses a security risk if sensitive data is stored inappropriately.

In REST architecture, resources can be cacheable or noncacheable, but they must be marked as such, whether implicitly or explicitly.

REST APIs can use a variety of methods to authenticate requests. Some common authentication types include basic authentication, bearer authentication, API key authentication, and OAuth 2.0.

Basic authentication uses a username and password (provided in the HTTP header) for authentication. While simple and convenient to implement, it is not considered secure.

In bearer authentication, the client obtains an access token from an authorization server, which it then uses to access the desired resource. The token is typically valid for a limited time, requiring renewal for continued use.

API key authentication involves the use of a unique identifier assigned to each client application. The client application includes this key in its API calls, similar to an access token used in bearer authentication. The API key uniquely identifies an application, not a user.

Unlike access tokens, API keys typically do not automatically expire, making them less secure if not managed properly.

Open Authorization 2.0 (OAuth 2.0) is an industry-standard framework that provides access delegation, allowing third-party applications to access resources (i.e., via a REST API) on behalf of a user without sharing the user’s credentials.

The client application requests authorization from the resource owner, receives an authorization grant, and then uses the authorization grant to obtain an access token from the authorization server. It then uses the access token to access the desired resource on the resource server.