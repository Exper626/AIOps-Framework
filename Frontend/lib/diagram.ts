// The kinds of device a diagram has, as the backend knows them
// (Backend/pipeline/devices.py): the AI picks one for each device, and it
// decides the device's row, default icon and the start of its name. New
// devices are named with a word people know (Router1, Switch1), keeping only
// the abbreviations everyone uses (PC, AP, L3). A device can also get any icon
// from lib/network-icons.json in the editor, and keeps its kind.
type DeviceKind = { label: string; prefix: string; icon: string; row: number };

const HOST_ROW = 6;

export const DEVICE_KINDS: Record<string, DeviceKind> = {
  access_point: {
    icon: "access-point",
    label: "Access point",
    prefix: "AP",
    row: 5,
  },
  building: { icon: "branch-office", label: "Site", prefix: "Site", row: 0 },
  camera: {
    icon: "video-camera",
    label: "Camera",
    prefix: "Camera",
    row: HOST_ROW,
  },
  cloud: { icon: "cloud", label: "Cloud / Internet", prefix: "Cloud", row: 0 },
  database: {
    icon: "relational-database",
    label: "Database",
    prefix: "DB",
    row: HOST_ROW,
  },
  firewall: { icon: "firewall", label: "Firewall", prefix: "Firewall", row: 1 },
  hub: { icon: "hub", label: "Hub", prefix: "Hub", row: 4 },
  ip_phone: {
    icon: "ip-phone",
    label: "IP phone",
    prefix: "Phone",
    row: HOST_ROW,
  },
  laptop: { icon: "laptop", label: "Laptop", prefix: "Laptop", row: HOST_ROW },
  load_balancer: {
    icon: "local-director",
    label: "Load balancer",
    prefix: "LB",
    row: 3,
  },
  modem: { icon: "modem", label: "Modem", prefix: "Modem", row: 1 },
  multilayer_switch: {
    icon: "layer-3-switch",
    label: "Layer 3 switch",
    prefix: "L3Switch",
    row: 3,
  },
  other: {
    icon: "general-appliance",
    label: "Other device",
    prefix: "Device",
    row: HOST_ROW,
  },
  pbx: { icon: "pbx", label: "Phone system", prefix: "PBX", row: HOST_ROW },
  pc: { icon: "pc", label: "PC", prefix: "PC", row: HOST_ROW },
  person: {
    icon: "standing-man",
    label: "User",
    prefix: "User",
    row: HOST_ROW,
  },
  printer: {
    icon: "printer",
    label: "Printer",
    prefix: "Printer",
    row: HOST_ROW,
  },
  router: { icon: "router", label: "Router", prefix: "Router", row: 2 },
  server: {
    icon: "file-server",
    label: "Server",
    prefix: "Server",
    row: HOST_ROW,
  },
  storage: {
    icon: "fc-storage",
    label: "Storage",
    prefix: "Storage",
    row: HOST_ROW,
  },
  switch: {
    icon: "workgroup-switch",
    label: "Switch",
    prefix: "Switch",
    row: 4,
  },
  tablet: { icon: "tablet", label: "Tablet", prefix: "Tablet", row: HOST_ROW },
  vpn_gateway: {
    icon: "vpn-gateway",
    label: "VPN gateway",
    prefix: "VPN",
    row: 1,
  },
  wan_equipment: {
    icon: "csu-dsu",
    label: "WAN device",
    prefix: "WAN",
    row: 1,
  },
  wireless_router: {
    icon: "wireless-router",
    label: "Wireless router",
    prefix: "WRouter",
    row: 4,
  },
  wlan_controller: {
    icon: "wlan-controller",
    label: "Wireless controller",
    prefix: "WLC",
    row: 3,
  },
};

// The everyday devices, first in "Add device"; the rest are under "More devices"
export const DEVICE_TYPES = [
  "cloud",
  "firewall",
  "router",
  "multilayer_switch",
  "switch",
  "access_point",
  "wireless_router",
  "server",
  "pc",
  "laptop",
  "ip_phone",
  "printer",
].map((type) => ({ type, ...DEVICE_KINDS[type] }));

export type NetworkDevice = {
  id: string;
  name: string;
  type: string;
  // An icon picked in the editor instead of the kind's own
  icon?: string;
  model?: string;
  x?: number | null;
  y?: number | null;
};

export type NetworkLink = {
  source: string;
  target: string;
};

export type NetworkDiagram = {
  devices: NetworkDevice[];
  links: NetworkLink[];
  // An answer's diagram as the backend drew it with Graphviz (a PNG data URL)
  image?: string;
};

// Only the devices and links, without the picture, to send to the backend
export function diagramData(diagram: NetworkDiagram): NetworkDiagram {
  return { devices: diagram.devices, links: diagram.links };
}

export const EMPTY_DIAGRAM: NetworkDiagram = { devices: [], links: [] };

const COLUMN_WIDTH = 150;
const ROW_HEIGHT = 130;

function kindOf(type: string) {
  return DEVICE_KINDS[type] ?? DEVICE_KINDS.other;
}

// The picked icon, or else the kind's
export function iconFor(type: string, icon?: string) {
  return `/network-icons/${icon || kindOf(type).icon}.svg`;
}

// Hosts share the bottom row, so a PC and a server sit side by side
function rowOf(type: string) {
  return kindOf(type).row;
}

// The kind's prefix ("Router1"), or the given one for a device added by its icon ("VPNGateway1")
export function nextDeviceName(
  type: string,
  devices: NetworkDevice[],
  prefix = kindOf(type).prefix
) {
  const names = new Set(devices.map((device) => device.name));
  let number = 1;

  while (names.has(`${prefix}${number}`)) {
    number += 1;
  }

  return `${prefix}${number}`;
}

function neighboursOf(id: string, links: NetworkLink[]) {
  return links.flatMap((link) => {
    if (link.source === id) {
      return [link.target];
    }
    return link.target === id ? [link.source] : [];
  });
}

// Rows by device type (internet at the top, hosts at the bottom); each row is
// ordered by where its neighbours above sit, which keeps cables from crossing
function layeredPositions(diagram: NetworkDiagram) {
  const rows = new Map<number, NetworkDevice[]>();

  for (const device of diagram.devices) {
    const row = rowOf(device.type);
    rows.set(row, [...(rows.get(row) ?? []), device]);
  }

  const positions = new Map<string, { x: number; y: number }>();

  [...rows.keys()]
    .sort((a, b) => a - b)
    .forEach((row, rowIndex) => {
      const devices = rows.get(row) ?? [];
      const order = devices.map((device, index) => {
        const above = neighboursOf(device.id, diagram.links)
          .map((id) => positions.get(id)?.x)
          .filter((x): x is number => x !== undefined);
        const centre = above.length
          ? above.reduce((sum, x) => sum + x, 0) / above.length
          : index * COLUMN_WIDTH;
        return { centre, device, index };
      });

      order.sort((a, b) => a.centre - b.centre || a.index - b.index);

      order.forEach(({ device }, index) => {
        positions.set(device.id, {
          x: (index - (order.length - 1) / 2) * COLUMN_WIDTH,
          y: rowIndex * ROW_HEIGHT,
        });
      });
    });

  return positions;
}

function overlaps(
  point: { x: number; y: number },
  taken: { x: number; y: number }[]
) {
  return taken.some(
    (other) =>
      Math.abs(other.x - point.x) < COLUMN_WIDTH * 0.8 &&
      Math.abs(other.y - point.y) < ROW_HEIGHT * 0.8
  );
}

// Devices keep the place they were dragged to. A new device goes under a
// device it is cabled to, or below everything, in the first free spot.
export function layoutDiagram(diagram: NetworkDiagram) {
  const placed = diagram.devices.filter(
    (device) => typeof device.x === "number" && typeof device.y === "number"
  );

  if (placed.length === 0) {
    return layeredPositions(diagram);
  }

  const positions = new Map(
    placed.map((device) => [
      device.id,
      { x: device.x as number, y: device.y as number },
    ])
  );
  const bottom = Math.max(...placed.map((device) => device.y as number));

  for (const device of diagram.devices) {
    if (positions.has(device.id)) {
      continue;
    }

    const neighbour = neighboursOf(device.id, diagram.links)
      .map((id) => positions.get(id))
      .find((position) => position !== undefined);
    const point = neighbour
      ? { x: neighbour.x, y: neighbour.y + ROW_HEIGHT }
      : { x: 0, y: bottom + ROW_HEIGHT };
    const taken = [...positions.values()];
    let step = 0;

    while (overlaps(point, taken)) {
      step += 1;
      point.x += (step % 2 === 1 ? step : -step) * COLUMN_WIDTH;
    }

    positions.set(device.id, point);
  }

  return positions;
}

export function describeDiagram(diagram: NetworkDiagram) {
  const devices = diagram.devices.length;
  const links = diagram.links.length;
  return `${devices} device${devices === 1 ? "" : "s"}, ${links} cable${links === 1 ? "" : "s"}`;
}
