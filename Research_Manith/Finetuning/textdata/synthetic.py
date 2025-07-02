import re
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


TOPICS = [
    "MPLS Architecture (control plane/data plane separation)",
    "IP VPN Layer 3 VPN architecture (RFC 4364, formerly 2547bis)",
    "Route distinguisher and route target planning",
    "PE-CE routing protocol selection (BGP, OSPF, RIP, static)",
    "VPN topology types (hub-and-spoke, full mesh, partial mesh)",
    "MPLS label allocation and label stack behavior",
    "QoS design in MPLS networks",
    "Hierarchical VPNs (e.g., Carrier Supporting Carrier, CSC)",
    "Physical and logical topology diagrams",
    "Site classification (hub, branch, data center)",
    "Link provisioning & redundancy planning",
    "Addressing plan (IPv4/IPv6)",
    "Security zoning in MPLS VPN",
    "PE/CE device configuration plans",
    "IGP design (OSPF areas, ISIS levels)",
    "MP-BGP configuration between PEs",
    "VRF table design",
    "SLA parameters and measurement points",
    "PE router VRF and BGP configuration",
    "MPLS LDP/RSVP configuration",
    "CE device routing configuration (static, BGP, OSPF)",
    "QoS policy maps and class maps",
    "IPsec over MPLS (if hybrid design)",
    "YAML/JSON intent-based configurations",
    "YANG models for MPLS/VPN (OpenConfig, IETF models)",
    "Ansible playbooks for VPN provisioning",
    "Python/Netmiko/NAPALM scripts",
    "Steps to provision a new site",
    "PE-CE onboarding checklist",
    "Multi-vendor CLI syntax handling (Cisco, Juniper, Huawei)",
    "APIs for provisioning (NetConf, RESTConf, SNMP)",
    "SNMP OIDs for MPLS LDP/BGP session state",
    "MPLS performance monitoring (latency, jitter, loss)",
    "NetFlow/IPFIX analysis",
    "Syslog-based alerting (VPN flap, LDP errors)",
    "VPN reachability issues",
    "LDP/BGP session establishment failure",
    "MPLS label stack corruption or misprogramming",
    "Path tracing with MPLS-aware traceroute",
    "Packet capture and label inspection",
    "VPN service outage SOP",
    "CE-to-PE connectivity issues",
    "Label binding mismatch",
    "Maintenance windows and rollback plans",
    "Router OS/software upgrade strategy (ISSU)",
    "MPLS/VPN feature deprecation and migration",
    "IP renumbering or route target renumbering",
    "Link utilization trending",
    "PE router VRF scaling limits",
    "BGP table growth projection",
    "VRF addition/removal procedures",
    "Route target modifications",
    "Automated CI/CD for network changes",
    "VRF audit reports",
    "MPLS tunnel validation",
    "Routing protocol compliance (BGP timers, hold time, etc.)"
]

template = """
Generate a prompt and response style formatted using json on the given topic related topic.
From the given topic generate much as possible amount of prompts and responses.

{{
{
    "prompt": "......",
    "response": "......"
}
}}

Just put the generated content 

"prompt": "generated prompt",
"response": "generated response"


Instructions to follow when generating the prompt and response:

- The topic is related to IT sector networking. Use your knowledge to generate.
- From the topic just generate highly accurate content, which will be used to fine-tune a small LLM.
- Do NOT include any markdown, text outside the JSON, or extra formatting or summary of the task.
- The output MUST be valid JSON.

Below is the Topic to generate the prompt and response:
{segment}
"""

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

for topic in TOPICS:
    prompt = template.format(segment=topic)
    
    completion = client.chat.completions.create(
        model="qwen/qwen3-235b-a22b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        top_p=0.1,
        stream=False
    )

    if completion and completion.choices and completion.choices[0].message and completion.choices[0].message.content:
        reply = completion.choices[0].message.content.strip()

        sanitized_name = sanitize_filename(topic[:60])  
        output_path = f"outputs/{sanitized_name}.json"
        os.makedirs("outputs", exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(reply)

        try:
            json.loads(reply)
            print(f"✅ Topic: {topic} — Valid JSON, saved to {output_path}")
        except json.JSONDecodeError:
            print(f"⚠️ JSON decode error for topic: {topic}, but saved raw content to {output_path}")
    else:
        print(f"⚠️ No response for topic: {topic}")
