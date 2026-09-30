"use client";

import type { User } from "next-auth";
import { useSession } from "next-auth/react";
import { useCallback, useState } from "react";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { guestRegex } from "@/lib/constants";
import { LoaderIcon } from "./icons";
import { SettingsDialog } from "./settings-dialog";

export function SidebarUserNav({ user }: { user: User }) {
  const { data, status } = useSession();
  const [settingsOpen, setSettingsOpen] = useState(false);
  const openSettings = useCallback(() => setSettingsOpen(true), []);

  const isGuest = guestRegex.test(data?.user?.email ?? "");
  const displayName = isGuest ? "Guest" : (user.name ?? user.email ?? "User");

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

  // A tall row with room around the avatar, like a card when hovered; closed,
  // just the avatar, in the same place
  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton
          className="h-14 gap-1.5 rounded-xl bg-transparent px-1 transition-colors duration-150 hover:bg-foreground/10 group-data-[collapsible=icon]:size-10! group-data-[collapsible=icon]:px-1!"
          data-testid="user-nav-button"
          onClick={openSettings}
          size="lg"
          tooltip="Settings"
        >
          <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-[#3b5b8f] font-semibold text-[14px] text-white">
            {/* Trimmed to the capital letter's height, so it sits in the
                middle of the circle whatever the font */}
            <span className="leading-none [text-box:trim-both_cap_alphabetic]">
              {displayName.charAt(0).toUpperCase()}
            </span>
          </div>
          <div className="flex min-w-0 flex-col text-left leading-tight">
            <span
              className="truncate font-medium text-[14px] text-sidebar-foreground"
              data-testid="user-email"
            >
              {displayName}
            </span>
            <span className="truncate text-[12.5px] text-sidebar-foreground/55">
              Settings
            </span>
          </div>
        </SidebarMenuButton>
      </SidebarMenuItem>

      <SettingsDialog onOpenChange={setSettingsOpen} open={settingsOpen} />
    </SidebarMenu>
  );
}
