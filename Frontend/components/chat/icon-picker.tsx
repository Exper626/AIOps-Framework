"use client";

import { SearchIcon } from "lucide-react";
import Image from "next/image";
import { type ChangeEvent, useCallback, useMemo, useState } from "react";
import { DEVICE_TYPES, iconFor } from "@/lib/diagram";
import {
  ICON_CATEGORIES,
  NETWORK_ICONS,
  type NetworkIcon,
  searchIcons,
} from "@/lib/network-icons";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

// A kind of device, and the icon picked for it when it isn't one of the
// everyday devices (those use their kind's icon)
export type PickedDevice = { type: string; icon?: NetworkIcon };

const TILE =
  "flex flex-col items-center gap-1.5 rounded-xl px-1 py-2 text-center outline-none transition-colors hover:bg-foreground/10 focus-visible:bg-foreground/10";

function Tile({
  label,
  src,
  onClick,
}: {
  label: string;
  src: string;
  onClick: () => void;
}) {
  return (
    <button className={TILE} onClick={onClick} title={label} type="button">
      <Image
        alt=""
        className="pointer-events-none size-9 select-none object-contain"
        height={36}
        src={`${BASE_PATH}${src}`}
        unoptimized
        width={36}
      />
      <span className="line-clamp-2 text-[11px] text-foreground/85 leading-tight">
        {label}
      </span>
    </button>
  );
}

function KindTile({
  type,
  label,
  onPick,
}: {
  type: string;
  label: string;
  onPick: (picked: PickedDevice) => void;
}) {
  const handleClick = useCallback(() => onPick({ type }), [onPick, type]);
  return <Tile label={label} onClick={handleClick} src={iconFor(type)} />;
}

function IconTile({
  icon,
  onPick,
}: {
  icon: NetworkIcon;
  onPick: (picked: PickedDevice) => void;
}) {
  const handleClick = useCallback(
    () => onPick({ icon, type: icon.kind }),
    [icon, onPick]
  );
  return (
    <Tile
      label={icon.name}
      onClick={handleClick}
      src={iconFor(icon.kind, icon.id)}
    />
  );
}

const GRID = "grid grid-cols-4 gap-1 sm:grid-cols-6";

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="flex flex-col gap-1">
      <h3 className="px-1 pt-2 font-medium text-[12px] text-muted-foreground">
        {title}
      </h3>
      <div className={GRID}>{children}</div>
    </section>
  );
}

const GROUPED = ICON_CATEGORIES.map(
  (category) =>
    [
      category,
      NETWORK_ICONS.filter((icon) => icon.category === category),
    ] as const
);

// The everyday devices first, then every icon by category, with a search over
// all of them; for adding a device, or changing a device's icon
export function IconPicker({
  open,
  onOpenChange,
  title,
  onPick,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  onPick: (picked: PickedDevice) => void;
}) {
  const [query, setQuery] = useState("");
  const results = useMemo(
    () => (query.trim() ? searchIcons(query) : null),
    [query]
  );

  const handleOpenChange = useCallback(
    (next: boolean) => {
      if (!next) {
        setQuery("");
      }
      onOpenChange(next);
    },
    [onOpenChange]
  );

  const handleQuery = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => setQuery(event.target.value),
    []
  );

  const pick = useCallback(
    (picked: PickedDevice) => {
      onPick(picked);
      handleOpenChange(false);
    },
    [handleOpenChange, onPick]
  );

  return (
    <Dialog onOpenChange={handleOpenChange} open={open}>
      <DialogContent
        className="flex h-[80vh] flex-col gap-3 sm:max-w-2xl"
        data-testid="icon-picker"
      >
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>
            The everyday devices first, then all {NETWORK_ICONS.length} icons by
            category.
          </DialogDescription>
        </DialogHeader>

        <div className="relative">
          <SearchIcon className="-translate-y-1/2 pointer-events-none absolute top-1/2 left-3 size-4 text-muted-foreground" />
          <input
            aria-label="Search devices"
            autoFocus
            className="h-10 w-full rounded-xl border border-border bg-transparent pr-3 pl-9 text-sm outline-none focus:border-foreground/30"
            data-testid="icon-search"
            onChange={handleQuery}
            placeholder="Search, like VPN, PBX or satellite"
            value={query}
          />
        </div>

        <div className="-mx-2 min-h-0 flex-1 overflow-y-auto px-2 pb-1">
          {results ? (
            results.length > 0 ? (
              <div className={GRID}>
                {results.map((icon) => (
                  <IconTile icon={icon} key={icon.id} onPick={pick} />
                ))}
              </div>
            ) : (
              <p className="py-8 text-center text-muted-foreground text-sm">
                No devices match “{query.trim()}”.
              </p>
            )
          ) : (
            <>
              <Section title="Everyday devices">
                {DEVICE_TYPES.map((device) => (
                  <KindTile
                    key={device.type}
                    label={device.label}
                    onPick={pick}
                    type={device.type}
                  />
                ))}
              </Section>
              {GROUPED.map(([category, icons]) => (
                <Section key={category} title={category}>
                  {icons.map((icon) => (
                    <IconTile icon={icon} key={icon.id} onPick={pick} />
                  ))}
                </Section>
              ))}
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
