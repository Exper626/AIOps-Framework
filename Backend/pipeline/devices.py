"""The kinds of device a diagram has. The AI picks one of these for each device; in the diagram editor a
device can also get any of the ~280 icons in Frontend/lib/network-icons.json, while keeping its kind.
Frontend/lib/diagram.ts has the same list, for the editor."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceKind:
    # Row in the Graphviz picture: the internet at the top, end devices at the bottom
    level: int
    # The icon when the device has none of its own (Backend/icons/<icon>.png)
    icon: str
    # How captions count it: "1 switch", "3 switches"
    names: tuple[str, str]


END_DEVICE_LEVEL = 5

DEVICE_KINDS: dict[str, DeviceKind] = {
    "cloud": DeviceKind(0, "cloud", ("cloud", "clouds")),
    "building": DeviceKind(0, "branch-office", ("site", "sites")),
    "wan_equipment": DeviceKind(1, "csu-dsu", ("WAN device", "WAN devices")),
    "modem": DeviceKind(1, "modem", ("modem", "modems")),
    "router": DeviceKind(1, "router", ("router", "routers")),
    "vpn_gateway": DeviceKind(1, "vpn-gateway", ("VPN gateway", "VPN gateways")),
    "firewall": DeviceKind(1, "firewall", ("firewall", "firewalls")),
    "multilayer_switch": DeviceKind(2, "layer-3-switch", ("multilayer switch", "multilayer switches")),
    "wlan_controller": DeviceKind(2, "wlan-controller", ("wireless controller", "wireless controllers")),
    "load_balancer": DeviceKind(2, "local-director", ("load balancer", "load balancers")),
    "switch": DeviceKind(3, "workgroup-switch", ("switch", "switches")),
    "hub": DeviceKind(3, "hub", ("hub", "hubs")),
    "wireless_router": DeviceKind(3, "wireless-router", ("wireless router", "wireless routers")),
    "access_point": DeviceKind(4, "access-point", ("access point", "access points")),
    "server": DeviceKind(4, "file-server", ("server", "servers")),
    "database": DeviceKind(4, "relational-database", ("database", "databases")),
    "storage": DeviceKind(4, "fc-storage", ("storage device", "storage devices")),
    "pbx": DeviceKind(4, "pbx", ("phone system", "phone systems")),
    "pc": DeviceKind(END_DEVICE_LEVEL, "pc", ("PC", "PCs")),
    "laptop": DeviceKind(END_DEVICE_LEVEL, "laptop", ("laptop", "laptops")),
    "tablet": DeviceKind(END_DEVICE_LEVEL, "tablet", ("tablet", "tablets")),
    "ip_phone": DeviceKind(END_DEVICE_LEVEL, "ip-phone", ("IP phone", "IP phones")),
    "printer": DeviceKind(END_DEVICE_LEVEL, "printer", ("printer", "printers")),
    "camera": DeviceKind(END_DEVICE_LEVEL, "video-camera", ("camera", "cameras")),
    "person": DeviceKind(END_DEVICE_LEVEL, "standing-man", ("user", "users")),
    "other": DeviceKind(END_DEVICE_LEVEL, "general-appliance", ("other device", "other devices")),
}


def device_kind(kind: str) -> DeviceKind:
    return DEVICE_KINDS.get(kind, DEVICE_KINDS["other"])
