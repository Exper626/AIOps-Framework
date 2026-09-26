// New devices are named with a word people know (Router1, Switch1), keeping
// only the abbreviations everyone uses (PC, AP, L3)
export const DEVICE_TYPES = [
  { label: "Cloud / Internet", prefix: "Cloud", type: "cloud" },
  { label: "Firewall", prefix: "Firewall", type: "firewall" },
  { label: "Router", prefix: "Router", type: "router" },
  { label: "Layer 3 switch", prefix: "L3Switch", type: "multilayer_switch" },
  { label: "Switch", prefix: "Switch", type: "switch" },
  { label: "Access point", prefix: "AP", type: "access_point" },
  { label: "Server", prefix: "Server", type: "server" },
  { label: "PC", prefix: "PC", type: "pc" },
  { label: "Laptop", prefix: "Laptop", type: "laptop" },
] as const;

export type DeviceType = (typeof DEVICE_TYPES)[number]["type"];

export type NetworkDevice = {
  id: string;
  name: string;
  type: string;
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
};

export const EMPTY_DIAGRAM: NetworkDiagram = { devices: [], links: [] };

const COLUMN_WIDTH = 150;
const ROW_HEIGHT = 130;

function knownType(type: string) {
  return DEVICE_TYPES.find((device) => device.type === type);
}

export function iconFor(type: string) {
  return `/network-icons/${knownType(type)?.type ?? "router"}.svg`;
}

// Hosts share the bottom row, so a PC and a server sit side by side
function rowOf(type: string) {
  const rank = DEVICE_TYPES.findIndex((device) => device.type === type);
  return rank === -1 ? 2 : Math.min(rank, 6);
}

export function nextDeviceName(type: string, devices: NetworkDevice[]) {
  const prefix = knownType(type)?.prefix ?? "Device";
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
