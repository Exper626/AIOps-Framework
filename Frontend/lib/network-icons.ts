import catalog from "./network-icons.json";

// Every icon the diagram editor offers, from "Image Generation/icons", with
// its category and the kind of device it is (scripts/build-network-icons.mjs
// makes the SVGs and the backend's PNGs from this list)
export type NetworkIcon = {
  id: string;
  name: string;
  category: string;
  kind: string;
};

export const ICON_CATEGORIES: string[] = catalog.categories;
export const NETWORK_ICONS: NetworkIcon[] = catalog.icons;

const BY_ID = new Map(NETWORK_ICONS.map((icon) => [icon.id, icon]));

export function getIcon(id: string) {
  return BY_ID.get(id);
}

// Icons whose name or category has every word of the search
export function searchIcons(query: string) {
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  return NETWORK_ICONS.filter((icon) =>
    words.every((word) =>
      `${icon.name} ${icon.category}`.toLowerCase().includes(word)
    )
  );
}

// A device added by its icon is named after it when the name is short
// ("Satellite" gives Satellite1); a longer one would be cut off on the device's
// card, so it gets its kind's name instead ("VPN Concentrator" gives VPN1)
const MAX_PREFIX = 10;

export function iconPrefix(icon: NetworkIcon) {
  const prefix = icon.name
    .replace(/\(.*?\)/g, "")
    .split(/[^A-Za-z0-9]+/)
    .filter(Boolean)
    .map((word) => word[0].toUpperCase() + word.slice(1))
    .join("");
  return prefix && prefix.length <= MAX_PREFIX ? prefix : undefined;
}

// The icons picked from "More devices" lately, newest first, for the Recent
// row in "Add device" (kept in this browser only)
const RECENT_KEY = "diagram-recent-icons";
const RECENT_COUNT = 5;

export function getRecentIcons(): NetworkIcon[] {
  try {
    const ids = JSON.parse(localStorage.getItem(RECENT_KEY) ?? "[]");
    return Array.isArray(ids)
      ? ids.flatMap((id) => (typeof id === "string" && BY_ID.get(id)) || [])
      : [];
  } catch {
    return [];
  }
}

export function rememberIcon(icon: NetworkIcon) {
  try {
    const ids = [
      icon.id,
      ...getRecentIcons()
        .map((recent) => recent.id)
        .filter((id) => id !== icon.id),
    ].slice(0, RECENT_COUNT);
    localStorage.setItem(RECENT_KEY, JSON.stringify(ids));
  } catch {
    // Without storage there is just no Recent row
  }
}
