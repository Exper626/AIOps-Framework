"use client";

import { PanelLeftIcon, PenSquareIcon } from "lucide-react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import type { User } from "next-auth";
import { useCallback } from "react";
import telecomIcon from "@/app/icon.png";
import { SidebarHistory } from "@/components/chat/sidebar-history";
import { SidebarUserNav } from "@/components/chat/sidebar-user-nav";
import { Button } from "@/components/ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  useSidebar,
} from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipTrigger } from "../ui/tooltip";

export function AppSidebar({ user }: { user: User | undefined }) {
  const router = useRouter();
  const { setOpenMobile, state, toggleSidebar } = useSidebar();
  const collapsed = state === "collapsed";

  const handleNewChat = useCallback(() => {
    setOpenMobile(false);
    router.push("/");
  }, [router, setOpenMobile]);

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="pb-0 pt-3">
        <SidebarMenu>
          {/* Open: "SLT" on the left, toggle on the right.
              Collapsed: the SLT logo, which turns into the open icon on hover. */}
          <SidebarMenuItem
            className={cn(
              "flex flex-row items-center",
              collapsed ? "justify-center" : "justify-between"
            )}
          >
            {collapsed ? null : (
              <button
                className="rounded-lg px-2 py-1 font-semibold text-foreground text-lg tracking-tight"
                onClick={handleNewChat}
                type="button"
              >
                SLT
              </button>
            )}
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  aria-label={collapsed ? "Open sidebar" : "Close sidebar"}
                  className="group/toggle size-9 rounded-lg text-foreground transition-colors duration-150 hover:bg-foreground/10 hover:text-foreground [&_svg]:size-5!"
                  onClick={toggleSidebar}
                  size="icon-sm"
                  variant="ghost"
                >
                  {collapsed ? (
                    <>
                      <Image
                        alt="SLT"
                        className="size-7 rounded-lg bg-white object-contain p-1 group-hover/toggle:hidden"
                        src={telecomIcon}
                      />
                      <PanelLeftIcon className="hidden group-hover/toggle:block" />
                    </>
                  ) : (
                    <PanelLeftIcon />
                  )}
                </Button>
              </TooltipTrigger>
              <TooltipContent
                className="hidden md:block"
                side={collapsed ? "right" : "bottom"}
                sideOffset={0}
              >
                {collapsed ? "Open sidebar" : "Close sidebar"}
              </TooltipContent>
            </Tooltip>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup className="pt-3">
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton
                  className="h-8 rounded-lg px-1.5 text-[13px] [&>svg]:size-5 text-foreground transition-colors duration-150 hover:bg-foreground/10 hover:text-foreground"
                  onClick={handleNewChat}
                  tooltip="New Chat"
                >
                  <PenSquareIcon />
                  <span className="font-medium">New chat</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarHistory user={user} />
      </SidebarContent>
      <SidebarFooter className="border-t border-sidebar-border px-1 pt-2 pb-3">
        {user ? <SidebarUserNav user={user} /> : null}
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
