import json
from pathlib import Path

from graphviz import Digraph
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent
ICON_DIR = BASE_DIR / "icons"
GENERATED_DIR = BASE_DIR / "generated_nodes"
JSON_FILE = BASE_DIR / "network.json"

GENERATED_DIR.mkdir(exist_ok=True)

ICON_MAP = {
    "router": ICON_DIR / "router.png",
    "switch": ICON_DIR / "switch.png",
    "firewall": ICON_DIR / "firewall.png",
    "server": ICON_DIR / "server.png",
    "pc": ICON_DIR / "pc.png",
}

ICON_SIZE_MAP = {
    "router": (110, 75),
    "switch": (180, 80),
    "firewall": (110, 75),
    "server": (90, 90),
    "pc": (90, 90),
}


def load_font(size: int):
    font_paths = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibri.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
    ]

    for font_path in font_paths:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size)

    return ImageFont.load_default()


def create_device_image(
    device: dict,
    icon_path: Path,
    device_type: str,
) -> Path:
    scale = 3

    device_id = str(device["id"])
    ip_address = str(device.get("ip", "No IP"))

    output_path = GENERATED_DIR / f"{device_id}.png"

    icon = Image.open(icon_path).convert("RGBA")

    base_icon_size = ICON_SIZE_MAP.get(
        device_type,
        (110, 75),
    )

    max_icon_size = (
        base_icon_size[0] * scale,
        base_icon_size[1] * scale,
    )

    icon.thumbnail(
        max_icon_size,
        Image.Resampling.LANCZOS,
    )

    font_name = load_font(18 * scale)
    font_ip = load_font(16 * scale)

    padding = 10 * scale
    text_gap = 3 * scale
    icon_text_gap = 6 * scale

    temp_image = Image.new("RGBA", (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)

    name_box = temp_draw.textbbox(
        (0, 0),
        device_id,
        font=font_name,
    )

    ip_box = temp_draw.textbbox(
        (0, 0),
        ip_address,
        font=font_ip,
    )

    name_width = name_box[2] - name_box[0]
    name_height = name_box[3] - name_box[1]

    ip_width = ip_box[2] - ip_box[0]
    ip_height = ip_box[3] - ip_box[1]

    canvas_width = max(
        icon.width,
        name_width,
        ip_width,
    ) + padding * 2

    canvas_height = (
        padding
        + icon.height
        + icon_text_gap
        + name_height
        + text_gap
        + ip_height
        + padding
    )

    canvas = Image.new(
        "RGBA",
        (canvas_width, canvas_height),
        "white",
    )

    draw = ImageDraw.Draw(canvas)

    icon_x = (canvas_width - icon.width) // 2
    icon_y = padding

    canvas.alpha_composite(
        icon,
        (icon_x, icon_y),
    )

    name_x = (canvas_width - name_width) // 2
    name_y = icon_y + icon.height + icon_text_gap

    draw.text(
        (name_x, name_y),
        device_id,
        fill="black",
        font=font_name,
    )

    ip_x = (canvas_width - ip_width) // 2
    ip_y = name_y + name_height + text_gap

    draw.text(
        (ip_x, ip_y),
        ip_address,
        fill="black",
        font=font_ip,
    )

    canvas.save(
        output_path,
        dpi=(300, 300),
    )

    return output_path


def add_device(dot: Digraph, device: dict) -> None:
    device_id = str(device["id"])
    device_type = str(device.get("type", "")).lower()
    ip_address = str(device.get("ip", "No IP"))

    icon_path = ICON_MAP.get(device_type)

    if icon_path and icon_path.exists():
        node_image = create_device_image(
            device=device,
            icon_path=icon_path,
            device_type=device_type,
        )

        dot.node(
            device_id,
            label="",
            image=str(node_image.resolve()),
            shape="none",
            imagescale="true",
            fixedsize="true",
            width="1.8",
            height="1.3",
        )

    else:
        print(
            f"No icon found for {device_id} "
            f"with type '{device_type}'. Using a box."
        )

        dot.node(
            device_id,
            label=f"{device_id}\n{ip_address}",
            shape="box",
        )


def add_connection(dot: Digraph, connection: dict) -> None:
    source = str(connection["source"])
    target = str(connection["target"])
    interface = str(connection.get("interface", ""))

    dot.edge(
        source,
        target,
        label=interface,
        dir="none",
    )


def generate_network_diagram(
    data: dict,
    output_file: str = "network_topology",
) -> None:
    dot = Digraph(
        "Network",
        format="png",
    )

    dot.attr(
        rankdir="LR",
        nodesep="0.7",
        ranksep="1.0",
        pad="0.3",
        bgcolor="white",
        splines="line",
        dpi="200",
    )

    dot.attr(
        "edge",
        fontname="Arial",
        fontsize="10",
    )

    for device in data.get("devices", []):
        add_device(dot, device)

    for connection in data.get("connections", []):
        add_connection(dot, connection)

    output_path = BASE_DIR / output_file

    rendered_file = dot.render(
        filename=str(output_path),
        cleanup=True,
    )

    print(f"Saved to: {rendered_file}")


def load_network_data(json_path: Path) -> dict:
    if not json_path.exists():
        raise FileNotFoundError(
            f"Could not find network JSON file: {json_path}"
        )

    with json_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


if __name__ == "__main__":
    try:
        network_data = load_network_data(JSON_FILE)

        generate_network_diagram(
            data=network_data,
            output_file="network_topology",
        )

    except FileNotFoundError as error:
        print(error)

    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error}")

    except KeyError as error:
        print(f"Missing required JSON field: {error}")

    except Exception as error:
        print(f"Failed to generate diagram: {error}")