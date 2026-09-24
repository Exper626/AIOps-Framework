"use client";

import type { User } from "next-auth";
import { useSession } from "next-auth/react";
import { useState } from "react";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { guestRegex } from "@/lib/constants";
import { LoaderIcon } from "./icons";
import { SettingsDialog } from "./settings-dialog";

function emailToHue(email: string): number {
  let hash = 0;
  for (const char of email) {
    hash = char.charCodeAt(0) + ((hash << 5) - hash);
  }
  return Math.abs(hash) % 360;
}

export function SidebarUserNav({ user }: { user: User }) {
  const { data, status } = useSession();
  const [settingsOpen, setSettingsOpen] = useState(false);

  const isGuest = guestRegex.test(data?.user?.email ?? "");
  const displayName = isGuest ? "Guest" : (user.name ?? user.email ?? "User");
  const hue = emailToHue(user.email ?? "");

  if (status === "loading") {
    return (
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton
            className="justify-between rounded-lg bg-transparent text-sidebar-foreground/50"
            size="lg"
          >
            <div className="flex flex-row items-center gap-2">
              <div className="size-8 animate-pulse rounded-full bg-sidebar-foreground/10" />
              <span className="animate-pulse rounded-md bg-sidebar-foreground/10 text-[13px] text-transparent">
                Loading...
              </span>
            </div>
            <div className="animate-spin text-sidebar-foreground/50">
              <LoaderIcon />
            </div>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    );
  }

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton
          className="rounded-lg bg-transparent transition-colors duration-150 hover:bg-sidebar-accent"
          data-testid="user-nav-button"
          onClick={() => setSettingsOpen(true)}
          size="lg"
          tooltip="Settings"
        >
          <div
            className="flex size-8 shrink-0 items-center justify-center rounded-full font-medium text-[13px] text-white ring-1 ring-sidebar-border/50"
            style={{
              background: `linear-gradient(135deg, oklch(0.45 0.1 ${hue}), oklch(0.3 0.06 ${hue + 40}))`,
            }}
          >
            {displayName.charAt(0).toUpperCase()}
          </div>
          <div className="flex min-w-0 flex-col text-left leading-tight">
            <span
              className="truncate font-medium text-[13px] text-sidebar-foreground"
              data-testid="user-email"
            >
              {displayName}
            </span>
            <span className="truncate text-[12px] text-sidebar-foreground/50">
              Settings
            </span>
          </div>
        </SidebarMenuButton>
      </SidebarMenuItem>

      <SettingsDialog
        isGuest={isGuest}
        onOpenChange={setSettingsOpen}
        open={settingsOpen}
        user={user}
      />
    </SidebarMenu>
  );
}
