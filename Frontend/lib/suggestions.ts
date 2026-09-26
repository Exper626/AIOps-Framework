// The cards on the start screen. Each has a small picture, drawn in
// components/chat/suggested-actions.tsx under the same id.
export type IdeaId =
  | "diagram"
  | "image"
  | "interface-down"
  | "ospf-bgp"
  | "vlans"
  | "subnet"
  | "wifi"
  | "firewall"
  | "config";

export type Idea = {
  id: IdeaId;
  title: string;
  detail: string;
  // Sent as the message when the card is clicked
  prompt?: string;
  // Put in the message box instead, for the user to finish
  draft?: string;
  // Also opens the image picker, for questions about a picture
  pickImage?: boolean;
};

// The first page always shows the first three; the rest are shuffled on each
// visit
export const FIXED_IDEAS = 3;

export const ideas: Idea[] = [
  {
    detail: "Get a diagram you can edit",
    id: "diagram",
    prompt:
      "Design a small office network with one router, one switch and three PCs, and draw the diagram.",
    title: "Design a small office network",
  },
  {
    detail: "Upload a Packet Tracer screenshot",
    draft:
      "Explain this network topology: the devices and how they're connected.",
    id: "image",
    pickImage: true,
    title: "Ask about a topology image",
  },
  {
    detail: "Step-by-step checks and commands",
    id: "interface-down",
    prompt:
      "My router interface Gi0/1 shows down/down. How do I troubleshoot it step by step?",
    title: "Fix an interface that's down",
  },
  {
    detail: "Plain-language answers",
    id: "ospf-bgp",
    prompt: "What is the difference between OSPF and BGP? Explain it simply.",
    title: "OSPF vs BGP, explained simply",
  },
  {
    detail: "Commands for each port, explained",
    id: "vlans",
    prompt:
      "How do I set up VLANs 10, 20 and 30 on a Cisco switch and assign ports to them?",
    title: "Set up VLANs on a switch",
  },
  {
    detail: "Ranges, masks and hosts worked out",
    id: "subnet",
    prompt:
      "Split 192.168.1.0/24 into /26 subnets. List each subnet's range, mask and usable hosts.",
    title: "Subnet a /26 network",
  },
  {
    detail: "Access points, channels and coverage",
    id: "wifi",
    prompt:
      "How should I plan Wi-Fi for an office floor: where to put access points, which channels to use and how to get good coverage?",
    title: "Plan Wi-Fi for an office floor",
  },
  {
    detail: "Allow what's needed, block the rest",
    id: "firewall",
    prompt:
      "Help me write firewall rules that allow web traffic (HTTPS, port 443) and block Telnet (port 23).",
    title: "Write firewall rules",
  },
  {
    detail: "Paste it and get problems pointed out",
    draft: "Check this config for mistakes:\n\n",
    id: "config",
    title: "Check a config for mistakes",
  },
];
