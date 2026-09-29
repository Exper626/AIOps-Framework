24 Data formats
This chapter covers

Why data serialization formats are needed
JSON’s primitive and structured data types
Interpreting JSON-formatted data
Other data serialization formats: XML and YAML
In the previous chapter, we established that communication between software applications on different devices is essential for network automation. We also covered one essential part of making that possible: application programming interfaces (APIs). APIs open up an application’s data to allow external applications to access it in an efficient and uniform manner.

In this chapter, we’ll cover the second half of the puzzle. For successful communication between applications, it’s not enough for App A to be able to access App B’s data; the data itself must be in a format that App A understands. That’s the role of data serialization formats—standardized data formats that allow applications to communicate data in an agreed-upon format that both parties understand. With regard to the CCNA exam topics, we will cover topic 6.7: Recognize components of JSON-encoded data.

24.1 Data serialization
When we covered the TCP/IP networking model in chapter 4 of volume 1, I emphasized the importance of standardized protocols to enable communications between devices over a network. This doesn’t just apply to the communication protocols used to carry messages; it applies to the contents of those messages as well. Applications, which can be developed in many different programming languages, store and interpret data in different ways. Figure 24.1 shows what happens when different applications attempt to communicate without using a data serialization format.



Figure 24.1 Communicating between applications without a data serialization format. Apps A and B, written in Python and Ruby, can’t interpret App C’s internal data structures.

Data serialization is the process of converting data into a standardized format for the purpose of storage or transmission. The data serialization process takes an application’s data structures from a computer’s memory and converts them into a series of bytes (hence the term serialization) that can be stored in a file or transmitted over a network. This process enables the data to be later reconstructed (i.e., by a different application). Data formats used for this purpose are called data serialization formats. In this chapter, we’ll cover three:

JavaScript Object Notation (JSON)

Extensible Markup Language (XML)

YAML Ain’t Markup Language (YAML)

Data serialization enables an application to communicate its data to another application in a format both parties understand. Figure 24.2 shows how it works: App C’s API converts its data structures into JSON-formatted data, allowing Apps A and B to interpret and reconstruct the data in their own languages.



Figure 24.2 Data serialization formats like JSON allow applications to communicate data in a format understood by both parties.

Note The term data serialization might sound complex, but it just means converting data into a format that’s easy to store or transfer. JSON, XML, and YAML are all standard data formats that many applications can understand, making them common choices for sharing data among different applications.

24.2 JSON
JavaScript Object Notation (JSON) is an open-standard data serialization format. It was originally derived from JavaScript, but is language independent; applications in many programming languages can generate and interpret JSON-formatted data. REST APIs often support JSON, which is likely why Cisco chose to include JSON as a CCNA exam topic.

One of JSON’s main characteristics is its human readability. Although it is designed for communication between computer applications, properly formatted JSON data is easy for us to read, too. To prove that, here’s an example of JSON-formatted data:

{
  "interface_name": "GigabitEthernet1/1",
  "is_up": true,
  "ip_address": "192.168.1.1",
  "netmask": "255.255.255.0",
  "speed": 1000,
  "description": null
}
Even if you don’t know anything about JSON yet, I’d bet that you can read and understand that data. It’s composed of a series of variables—logical containers for values—and the values they hold. For example, the variable "interface_name" holds the value "GigabitEthernet1/1".

Note A variable and its value are often called a key-value pair. We’ll examine JSON key-value pairs in this section.

You might not understand the significance of the curly braces or the double quotes in the previous example, but you can probably deduce that the data pertains to an interface with the following characteristics:

Its name is GigabitEthernet1/1.

Its status is up.

Its IP address is 192.168.1.1.

Its netmask is 255.255.255.0.

Its speed is 1000 (Mbps).

It currently has no description.

In this section, we’ll explore the different JSON data types and practice interpreting JSON-formatted data by looking at some examples.

Exam Tip JSON is explicitly mentioned in exam topic 6.7: Recognize components of JSON-encoded data. Make sure that you can differentiate between the different data types we cover and interpret simple JSON-formatted data.

24.2.1 JSON primitive data types
JSON data is represented using four fundamental forms called primitive data types. Here are the four primitive data types and some examples of each:

String—An alphanumeric text value. JSON strings are always enclosed in double quotes. Examples:
    "Hello."
    "5"
    "true"
    "null"
    
Number—A numeric value. Examples:
    5
    101.25

Boolean—A data type with only two possible values: true and false.
Null—A data type that represents the intentional absence of a value and is always represented as null.

Take a close look at the examples I gave for strings: "5" is a string, not a number; "true" is a string, not a Boolean; "null" is a string, not null. Any value enclosed in double quotes is a string (a text value), even if it would be a different data type without double quotes.

Exam Tip Remember that point for the exam! Don’t be fooled by a numeric value in double quotes; with regard to JSON data types, it’s a string, not a number.

Take another look at the previous example of JSON data. The key of each key-value pair is a string, and each of the four primitive data types is present in the values:

{
  "interface_name": "GigabitEthernet1/1",    ❶
  "is_up": true,                             ❷
  "ip_address": "192.168.1.1",               ❸
  "netmask": "255.255.255.0",                ❹
  "speed": 1000,                             ❺
  "description": null                        ❻
}
❶ “GigabitEthernet1/1” is a string.

❷ true is a Boolean.

❸ “192.168.1.1” is a string.

❹ “255.255.255.0” is a string.

❺ 1000 is a number.

❻ null is a null value.

Note The Boolean and null data types must be lowercase: true, false, and null.

24.2.2 JSON structured data types
While primitive data types in JSON represent singular values, structured data types, as the name implies, are used to organize information into more complex structures. JSON has two structured data types:

Object—An unordered set of key-value pairs

Array—An ordered set of values

JSON objects

A JSON object is an unordered set of key-value pairs. Unordered means that the order of the key-value pairs in the object is insignificant; they can be reordered without affecting the meaning of the object. The example of JSON data that we already looked at a couple of times is an object: curly braces enclosing six key-value pairs. Here it is once again:

{                                         ❶
  "interface_name": "GigabitEthernet1/1",
  "is_up": true,
  "ip_address": "192.168.1.1",
  "netmask": "255.255.255.0",
  "speed": 1000,
  "description": null
}                                         ❷
❶ An opening curly brace indicates the start of an object.

❷ A closing curly brace indicates the end of an object.

Here are some important points about objects in JSON:

Objects are enclosed in curly braces.

The key of each key-value pair must be a string.

The value of each key-value pair can be any valid JSON data type: string, number, Boolean, null, or even another object (or array—the next data type).

The key and value of each key-value pair are separated by a colon.

If there are multiple key-value pairs, each pair is separated by a comma.

There must not be a trailing comma after the final key-value pair.

In all of the previous example’s key-value pairs, the value is a primitive data type: string, number, Boolean, or null. However, structured data types are also valid values for an object’s key-value pairs. These “objects within objects” are called nested objects. The following example shows an object that contains two key-value pairs. The two keys are "device" and "interface_config", and the value of each of those keys is a nested object with its own set of key-value pairs:

{
  "device": {                                ❶
    "name": "R1",                            ❶
    "vendor": "Cisco",                       ❶
    "model": "1101"                          ❶
  },                                         ❶
  "interface_config": {                      ❷
    "interface_name": "GigabitEthernet1/1",  ❷
    "is_up": true,                           ❷
    "ipaddress": "192.168.1.1",              ❷
    "netmask": "255.255.255.0",              ❷
    "speed": 1000,                           ❷
    "description": null                      ❷
  }                                          ❷
}
❶ Nested object 1

❷ Nested object 2

Figure 24.3 shows that same object, highlighting the keys and values to illustrate the nested objects.



Figure 24.3 An object consisting of two key-value pairs. The value of each key-value pair is a nested object with its own set of key-value pairs.

Now is a good time to introduce another key point about JSON: whitespace—including spaces, line breaks, and tabs—is insignificant in terms of data interpretation. All of the examples shown so far have used whitespace to enhance their readability, but that whitespace has no actual meaning in JSON. Here’s that previous example with all whitespace removed:

{"device":{"name":"R1","vendor":"Cisco","model":"1101"},"interface_config":
{"interface_name":"GigabitEthernet1/1","is_up":true,"ipaddress":
"192.168.1.1","netmask":"255.255.255.0","speed":1000,"description":null}}
Although it makes no difference to the application interpreting the data, I’m sure you’ll agree that the previous examples are more human readable.

Note We won’t cover the general best practices regarding whitespace for making human-readable JSON; the CCNA exam just requires you to interpret JSON-formatted data, not write it yourself.

JSON arrays

The previous examples of key-value pairs showed one value for each key. However, a key can hold multiple values using the array data type. A JSON array is an ordered set of values.

Note Unlike JSON objects, arrays are ordered. The order of the object’s values is significant, so changing their order would change the meaning of the array.

The following example is a JSON object with two key-value pairs; the value of each is an array containing multiple values. The "interfaces" array contains three strings, and the "random_values" array contains four values of different data types: a string, a number, a Boolean, and null:

{
  "interfaces": [           ❶
    "GigabitEthernet1/1",   ❶
    "GigabitEthernet1/2",   ❶
    "GigabitEthernet1/3"    ❶
  ],                        ❶
  "random_values": [        ❷
    "Hi",                   ❷
    42,                     ❷
    false,                  ❷
    null                    ❷
  ]                         ❷
}
❶ An array containing three string values

❷ An array containing four values of different data types

Here are the key points about arrays:

Arrays are enclosed in square brackets.

The values can be of any valid JSON data type.

The values don’t have to be of the same data type.

The values are separated by commas.

There must not be a trailing comma after the final value.

24.2.3 Identifying invalid JSON
The previous examples all showed valid JSON-formatted data. In this section, we’ll look at a few examples of invalid JSON. This is useful practice for “trick questions” on the CCNA exam and for checking your understanding of JSON syntax. Here’s the first example:

{
  "routerConfig": {
    "hostname": "Router01",
    "interfaces": [
      "GigabitEthernet0/0",
      "GigabitEthernet0/1"
    ],
    "enabled": TRUE,
    "ipAddress": "192.168.1.1",
    "subnetMask": "255.255.255.0"
    "gateway": NULL
  }
}
There are three issues with this example:

Booleans must be lowercase: true, not TRUE.

Null must be lowercase: null, not NULL.

There is a missing comma after the value of "subnetMask". There must be a comma between each of an object’s key-value pairs.

Note If you want to validate JSON data, you can use a website like https://jsonlint.com/. Paste the data and click Validate JSON; it will indicate whether the data is valid or not. Try it with the examples in this section.

The following example is also invalid JSON, but for different reasons than the previous example:

{
  "switchSettings": {
    "model": "WS-C2960C-8PC-L",
    "ports": 8,
    "management": {
        "accessMode"-"ssh",
        "port": 22
    },
    "firmwareVersion": "15.2(7)E7",
    "location": "Data Center A",
  }
}
Here are the two issues with the second example:

There is an invalid character (-) separating the "accessMode" key from its value "ssh". A key-value pair’s key and value must be separated by a colon.

There is a trailing comma after "location"’s value. An object’s key-value pairs must be separated by commas, but there must not be a trailing comma after the final pair.

Let’s look at one more example, again with two new issues that render it invalid:

{
  "firewallConfig": {
    "rules": [
      {
        "id": 1,
        "action": "allow",
        "sourceIp": "10.0.0.0/24"
      },
      {
        "id": 2,
        "action": "deny",
        "sourceIp": "10.0.1.0/24"
      }
  },
  "defaultAction": "deny"
This example’s issues are related to closing objects and arrays:

The final closing curly brace (to close the opening curly brace at the start of the example) is missing.

The value of "rules" is an array, but it has no closing square bracket.

You now know (almost) all of JSON’s rules! JSON is fairly simple, and there’s not much to it beyond what we’ve covered here. JSON is defined in RFC 8259, and you can read it for free at https://datatracker.ietf.org/doc/html/rfc8259 for more details. Compared to most RFCs, it’s a relatively simple read, but it goes beyond what you need to know for the CCNA. Feel free to check it out for reference, but you don’t have to read all of it.

Exam scenario

The following question illustrates how you might be tested on your knowledge of JSON on the CCNA exam.

Q: Examine the JSON-formatted data below. Which of the following statements is true?

{
  "deviceName": "Switch-01",
  "location": "Office Building B",
  "deviceType": "Switch",
  "firmwareVersion": "4.5.7",
  "uptimeHours": 1023,
  "managementAccess": {
    "enabled": true,
    "port": "22"
  },
  "allowedIPs": ["192.168.1.100", "192.168.1.101", "192.168.1.102"],
  "lastUpdated": null
}
A. The value of "allowedIPs" is a JSON object.

B. The value of "port" is a JSON number.

C. There is one nested object.

D. It is invalid JSON data.

Let’s examine each statement to determine which is true:

The value of "allowedIPs" is an object.

False. It is an array, not an object.

The value of "port" is a number.

False. It is enclosed in double quotes, so it is a string, not a number.

There is one nested object.

True. The entire example is an object consisting of various key-value pairs, and the value of "managementAccess" is a nested object.

It is invalid JSON data.

False. After identifying that the previous statement is true, you can rule out this one through the process of elimination. There are no missing or extra curly braces or square brackets, no trailing or missing commas, or any other elements that would render the data invalid.

24.3 XML and YAML
The CCNA exam topics list only explicitly mentions JSON. However, it’s worth taking a brief look at two other popular data serialization formats: XML and YAML. In this section, we’ll cover their basic characteristics and compare them to JSON.

24.3.1 XML
Extensible Markup Language (XML) is a data serialization format with syntax similar to HyperText Markup Language (HTML), which is the standard markup language for web pages. A markup language is used for annotating documents (i.e., web pages), specifying structure, and formatting. XML has become a popular choice to format data for storage and transmission, although it is less common than JSON or YAML. Like JSON, XML is commonly supported by REST APIs.

XML uses HTML-like tags for its key-value pairs, with an opening and closing tag: <key>value</key>. Interestingly, many Cisco IOS show commands can be displayed in XML format by adding | format to the end of the command. The following example shows the partial output of show ip interface brief on a router, in the standard IOS format and in XML format:

R1# show ip interface brief
Interface              IP-Address    OK?   Method   Status    Protocol
GigabitEthernet0/0     192.168.1.1   YES   manual   up        up 
GigabitEthernet0/1     unassigned    YES   unset    down      down
. . .
R1# show ip interface brief | format
<?xml version="1.0" encoding="UTF-8"?>
<ShowIpInterfaceBrief xmlns="ODM://built-in//show_ip_interface_brief">
  <SpecVersion>built-in</SpecVersion>
  <IPInterfaces>
    <entry>                                         ❶
      <Interface>GigabitEthernet0/0</Interface>
      <IP-Address>192.168.1.1</IP-Address>
      <OK>YES</OK>
      <Method>manual</Method>
      <Status>up</Status>
      <Protocol>up</Protocol>
    </entry>                                        ❶
    <entry>                                         ❷
      <Interface>GigabitEthernet0/1</Interface>
      <OK>YES</OK>
      <Method>unset</Method>
      <Status>down</Status>
      <Protocol>down</Protocol> 
    </entry>                                        ❷
. . .
  </IPInterfaces>
</ShowIpInterfaceBrief>
❶ Beginning and end of R1’s G0/0 interface

❷ Beginning and end of R1’s G0/1 interface

XML is generally considered less human readable than JSON, but you can probably decipher the meaning of that output. Like JSON, whitespace in XML is insignificant, but it’s usually formatted to make it more readable. The following example shows the same output with whitespace removed—easy for a computer to read, but not so readable for a human!

<?xml version="1.0" encoding="UTF-8"?><ShowIpInterfaceBrief xmlns="ODM://
built-in//show_ip_interface_brief"><SpecVersion>built-in</SpecVersion>
<IPInterfaces><entry><Interface>GigabitEthernet0/0</Interface><IP-Address>
192.168.1.1</IP-Address><OK>YES</OK><Method>manual</Method><Status>up
</Status><Protocol>up</Protocol></entry><entry><Interface>GigabitEthernet0/1
</Interface><OK>YES</OK><Method>unset</Method><Status>down</Status>
<Protocol>down</Protocol></entry></IPInterfaces></ShowIpInterfaceBrief>
24.3.2 YAML
YAML Ain’t Markup Language (YAML—it rhymes with “camel”) is another popular data serialization format. YAML originally stood for “Yet Another Markup Language,” but it was officially renamed to the recursive acronym “YAML Ain’t Markup Language” to emphasize its purpose as a data serialization format rather than a document markup language.

YAML is quite readable; of the three formats we have covered, it is perhaps the most human friendly. One of the notable differences between YAML and JSON/XML is that whitespace is significant in YAML. Proper indentation in YAML is not just about readability; it defines the structure and hierarchy of the data. Take a look at the following YAML-formatted data:

---
wirelessAccessPoint:
  name: AP350
  location: Office Floor 3
  operatingMode: dual-band
  ssids:
    - name: OfficeWiFi-2G
      band: 2.4GHz
      maxClients: 30
    - name: OfficeWiFi-5G
      band: 5GHz
      maxClients: 50
Compared to JSON and XML, YAML-formatted data looks quite minimalistic, contributing to its readability. In YAML, the structure of the data is defined through indentation levels without the need for many additional markers like those found in JSON (like commas and curly braces) or the tag structure of XML. For comparison, here’s the same data represented in JSON:

{
  "wirelessAccessPoint": {
    "name": "AP350",
    "location": "Office Floor 3",
    "operatingMode": "dual-band",
    "ssids": [
      {
        "name": "OfficeWiFi-2G",
        "band": "2.4GHz",
        "maxClients": 30
      },
      {
        "name": "OfficeWiFi-5G",
        "band": "5GHz",
        "maxClients": 50
      }
    ]
  }
}
And finally, the same data in XML format. I think you’ll probably agree that, of the three, the YAML data is the easiest to read.

<wirelessAccessPoint>
  <name>AP350</name>
  <location>Office Floor 3</location>
  <operatingMode>dual-band</operatingMode>
  <ssids>
    <ssid>
      <name>OfficeWiFi-2G</name>
      <band>2.4GHz</band>
      <maxClients>30</maxClients>
    </ssid>
    <ssid>
      <name>OfficeWiFi-5G</name>
      <band>5GHz</band>
      <maxClients>50</maxClients>
    </ssid>
  </ssids>
</wirelessAccessPoint>
Summary
Data serialization is the process of converting data into a standardized format suitable for storage or transmission. This process enables the data to be later reconstructed (i.e., by a different application).

Data serialization formats like JSON, XML, and YAML enable an application to communicate its data to another application in a format that both parties understand.

JavaScript Object Notation (JSON) is a human-readable data serialization format. Applications in many programming languages can generate and interpret JSON-formatted data, and REST APIs often support JSON.

A variable is a logical container for values. A variable and its value are often called a key-value pair.

JSON data is represented using four fundamental forms called primitive data types.

A JSON string is a text value that is enclosed in double quotes, such as "Hello.", "5", "true", and "null".

A JSON number is a numeric value, such as 5 or 101.25.

The JSON Boolean data type has only two possible values: true and false.

The JSON null data type represents the intentional absence of a value and is always represented as null.

Any value enclosed in double quotes is a string (a text value), even if it would be a different data type without double quotes (i.e., "5")

The JSON Boolean and null data types must be lowercase: true, false, and null.

JSON structured data types (object and array) are used to organize information into more complex structures.

A JSON object is an unordered set of key-value pairs. Unordered means that the order of the key-value pairs in an object is insignificant.

Important points about objects:

Objects are enclosed in curly braces.

The key of each key-value pair must be a string.

The value of each key-value pair can be any valid JSON data type.

The key and value of each key-value pair are separated by a colon.

If there are multiple key-value pairs, each pair is separated by a comma.

There must not be a trailing comma after the final key-value pair.

Structured data types (object/array) are valid values for an object’s key-value pairs.

An object within an object is called a nested object.

Whitespace—spaces, line breaks, and tabs—is insignificant in JSON. Whitespace is often used to enhance readability, but it doesn’t affect the data’s meaning.

A JSON array is an ordered set of values. Important points about arrays:

Arrays are enclosed in square brackets.

The values can be of any valid JSON data type.

The values don’t have to be of the same data type.

The values are separated by commas.

There must not be a trailing comma after the final value.

A single error like a misplaced comma will render JSON data invalid, so precision is essential.

Extensible Markup Language (XML) is a data serialization format with syntax similar to HyperText Markup Language (HTML), which is the standard markup language for web pages.

XML is a popular choice as a data serialization format used to format data for storage and transmission. Like JSON, it is commonly supported by REST APIs.

XML uses HTML-like tags for its key-value pairs, with an opening and closing tag: <key>value</key>.

Many Cisco IOS commands can be displayed in XML by adding | format to the end of the command, such as show ip interface brief | format.

Whitespace in XML is insignificant.

YAML Ain’t Markup Language (YAML)—formerly “Yet Another Markup Language”—is a popular data serialization format known for being human friendly.

Whitespace is significant in YAML. Proper indentation is not just important for readability; it defines the structure and hierarchy of the data.