import { PaperclipIcon, WifiIcon } from "lucide-react";
import Image from "next/image";
import type { ReactNode } from "react";
import { iconFor } from "@/lib/diagram";
import type { IdeaId } from "@/lib/suggestions";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

function Device({
  type,
  x,
  y,
  size = 24,
}: {
  type: string;
  x: number | string;
  y: number;
  size?: number;
}) {
  const height = Math.round(size * 0.84);

  return (
    <Image
      alt=""
      className="pointer-events-none absolute select-none object-contain"
      height={height}
      src={`${BASE_PATH}${iconFor(type)}`}
      style={{ height, left: x, top: y, width: size }}
      unoptimized
      width={size}
    />
  );
}

// Pictures are drawn on a 210 x 92 area in the middle of the card, so they
// look the same at any card width
function Stage({ children }: { children: ReactNode }) {
  return (
    <div className="absolute top-0 left-1/2 h-[92px] w-[210px] -translate-x-1/2">
      {children}
    </div>
  );
}

function Cables({ lines }: { lines: [number, number, number, number][] }) {
  return (
    <svg
      aria-hidden="true"
      className="absolute inset-0 size-full stroke-muted-foreground/60"
      viewBox="0 0 210 92"
    >
      {lines.map(([x1, y1, x2, y2]) => (
        <line
          key={`${x1}-${y1}-${x2}-${y2}`}
          strokeWidth={1.4}
          x1={x1}
          x2={x2}
          y1={y1}
          y2={y2}
        />
      ))}
    </svg>
  );
}

function Terminal({ children }: { children: ReactNode }) {
  return (
    <div className="absolute inset-2.5 overflow-hidden whitespace-pre rounded-lg border border-neutral-800 bg-neutral-950 px-2.5 py-2 font-mono text-[10.5px] text-neutral-400 leading-[1.6]">
      {children}
    </div>
  );
}

const Tag = ({
  children,
  className,
}: {
  children: ReactNode;
  className: string;
}) => (
  <span
    className={`absolute rounded-md px-1.5 py-px font-bold text-[9.5px] text-neutral-900 ${className}`}
  >
    {children}
  </span>
);

export const ideaPictures: Record<IdeaId, ReactNode> = {
  config: (
    <Terminal>
      {"interface Gi0/1\n ip address 10.0.1.1/24\n "}
      <span className="rounded-sm bg-amber-400/20 px-0.5 text-amber-200">
        shutdown
      </span>
    </Terminal>
  ),
  diagram: (
    <>
      <Stage>
        <Cables
          lines={[
            [105, 22, 105, 44],
            [105, 54, 63, 72],
            [105, 54, 105, 72],
            [105, 54, 147, 72],
          ]}
        />
        <Device type="router" x={93} y={5} />
        <Device type="switch" x={93} y={37} />
        <Device type="pc" x={51} y={66} />
        <Device type="pc" x={93} y={66} />
        <Device type="laptop" x={135} y={66} />
      </Stage>
      <span className="absolute top-1.5 right-1.5 rounded-full bg-[#4db749]/15 px-2 py-0.5 font-semibold text-[#4db749] text-[10px]">
        Diagram
      </span>
    </>
  ),
  firewall: (
    <Stage>
      <Cables
        lines={[
          [48, 36, 105, 36],
          [105, 36, 162, 36],
        ]}
      />
      <Device type="cloud" x={36} y={26} />
      <Device type="firewall" x={93} y={26} />
      <Device type="switch" x={150} y={26} />
      <span className="absolute top-[62px] left-[40px] rounded-md bg-[#4db749]/20 px-1.5 py-0.5 font-mono font-semibold text-[#4db749] text-[9.5px]">
        allow 443
      </span>
      <span className="absolute top-[62px] left-[112px] rounded-md bg-red-500/20 px-1.5 py-0.5 font-mono font-semibold text-[9.5px] text-red-400">
        deny 23
      </span>
    </Stage>
  ),
  image: (
    <>
      <div className="absolute top-3 left-1/2 h-[68px] w-[138px] -translate-x-1/2 -rotate-[4deg] rounded-lg bg-[#f4f4f2] shadow-[0_10px_24px_-10px_rgba(0,0,0,0.8)]">
        <svg
          aria-hidden="true"
          className="absolute inset-0 size-full stroke-neutral-400"
          viewBox="0 0 138 68"
        >
          <line strokeWidth={1.2} x1={36} x2={102} y1={22} y2={22} />
          <line strokeWidth={1.2} x1={69} x2={69} y1={28} y2={48} />
        </svg>
        <Device size={19} type="router" x={19} y={13} />
        <Device size={19} type="multilayer_switch" x={59} y={13} />
        <Device size={19} type="firewall" x={99} y={13} />
        <Device size={19} type="server" x={59} y={44} />
      </div>
      <span className="absolute top-1.5 left-[calc(50%+52px)] grid size-6 place-items-center rounded-full bg-[#01b6ed] text-[#04202b]">
        <PaperclipIcon className="size-3.5" />
      </span>
    </>
  ),
  "interface-down": (
    <Terminal>
      <span className="text-[#4db749]">R1#</span>
      {" show ip int brief\nGi0/0  10.0.0.1  up    up\nGi0/1  10.0.1.1  "}
      <span className="text-red-400">down down</span>
    </Terminal>
  ),
  "ospf-bgp": (
    <div className="absolute inset-0 flex items-center justify-center gap-2.5">
      {[
        ["router", "OSPF"],
        ["cloud", "BGP"],
      ].map(([type, label], index) => (
        <span className="contents" key={label}>
          {index > 0 ? (
            <em className="font-semibold text-[10.5px] text-muted-foreground not-italic">
              vs
            </em>
          ) : null}
          <span className="relative flex items-center gap-1.5 rounded-lg border border-border bg-background py-1.5 pr-2.5 pl-8 font-semibold text-xs">
            <Device size={18} type={type} x={9} y={7} />
            {label}
          </span>
        </span>
      ))}
    </div>
  ),
  subnet: (
    <>
      <div className="absolute inset-x-3.5 top-6 flex h-[26px] gap-[3px] font-mono font-semibold text-[10.5px] text-neutral-900">
        {[
          [".0", "bg-[#01b6ed]"],
          [".64", "bg-[#4db749]"],
          [".128", "bg-[#f2a93b]"],
          [".192", "bg-[#a78bfa]"],
        ].map(([label, color]) => (
          <div
            className={`grid flex-1 place-items-center rounded-md ${color}`}
            key={label}
          >
            {label}
          </div>
        ))}
      </div>
      <div className="absolute inset-x-0 top-[60px] text-center font-mono text-[10.5px] text-muted-foreground">
        /26 → 4 subnets × 62 hosts
      </div>
    </>
  ),
  vlans: (
    <Stage>
      <Cables
        lines={[
          [105, 26, 45, 62],
          [105, 26, 105, 62],
          [105, 26, 165, 62],
        ]}
      />
      <Device type="switch" x={93} y={10} />
      <Device type="pc" x={33} y={58} />
      <Device type="pc" x={93} y={58} />
      <Device type="server" x={153} y={58} />
      <Tag className="top-10 left-3 bg-[#01b6ed]">VLAN 10</Tag>
      <Tag className="top-10 left-[78px] bg-[#4db749]">VLAN 20</Tag>
      <Tag className="top-10 left-[144px] bg-[#f2a93b]">VLAN 30</Tag>
    </Stage>
  ),
  wifi: (
    <Stage>
      <WifiIcon className="absolute top-1.5 left-[91px] size-7 text-[#01b6ed]" />
      <Device type="access_point" x={93} y={38} />
      <Device type="laptop" x={33} y={62} />
      <Device type="laptop" x={153} y={62} />
    </Stage>
  ),
};
