"use client";

import { BookmarkIcon, PanelLeftIcon, PenSquareIcon } from "lucide-react";
import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import type { User } from "next-auth";
import { useCallback } from "react";
import telecomIcon from "@/public/images/slt-logo.png";
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
  useSidebar,
} from "@/components/ui/sidebar";
import { isPageRoute } from "@/lib/routes";
import { cn } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipTrigger } from "../ui/tooltip";

// A 40px row with the 20px icon in its middle, so the icon sits in the same
// place whether the sidebar is open (full width) or closed (40px wide)
const NAV_BUTTON =
  "h-10 gap-3 rounded-xl px-[10px] text-sm [&>svg]:size-5 text-foreground transition-colors duration-150 hover:bg-foreground/10 hover:text-foreground group-data-[collapsible=icon]:size-10! group-data-[collapsible=icon]:px-[10px]!";

export function AppSidebar({ user }: { user: User | undefined }) {
  const router = useRouter();
  const pathname = usePathname();
  const { isMobile, setOpenMobile, state, toggleSidebar } = useSidebar();
  // On a phone the sidebar always opens full width
  const collapsed = state === "collapsed" && !isMobile;

  const handleNewChat = useCallback(() => {
    setOpenMobile(false);
    router.push("/");
  }, [router, setOpenMobile]);

  const handleSaved = useCallback(() => {
    setOpenMobile(false);
    router.push("/saved");
  }, [router, setOpenMobile]);

  return (
    <Sidebar collapsible="icon">
      {/* Laid out at full width while the sidebar opens and clipped, so the
          sidebar slides open over its contents instead of the title and list
          re-wrapping (and jumping) as it widens */}
      <div className="flex min-h-0 flex-1 flex-col overflow-hidden">
        <div className="flex min-h-0 w-full flex-1 flex-col md:w-(--sidebar-width) md:group-data-[collapsible=icon]:w-(--sidebar-width-icon)">
          {/* Open or closed, the logo, icons and avatar keep their places (11px in,
              40px rows): the logo on its own, then New chat and Saved as a pair,
              so opening the sidebar only shows the labels */}
          <SidebarHeader className="px-[11px] pt-4 pb-0">
            <SidebarMenu>
              <SidebarMenuItem className="flex flex-row items-center justify-between">
                {collapsed ? null : (
                  <button
                    className="flex h-10 min-w-0 items-center gap-0.5 rounded-xl pr-2 font-display font-semibold text-[15px] text-foreground tracking-normal"
                    onClick={handleNewChat}
                    type="button"
                  >
                    <span className="flex size-10 shrink-0 items-center justify-center">
                      <Image
                        alt="SLT"
                        className="size-7 rounded-full bg-white object-contain p-1"
                        src={telecomIcon}
                      />
                    </span>
                    <span className="truncate">Sri Lanka Telecom</span>
                  </button>
                )}
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      aria-label={collapsed ? "Open sidebar" : "Close sidebar"}
                      className="sidebar-toggle group/toggle relative size-10 shrink-0 rounded-xl text-foreground transition-colors duration-150 hover:bg-foreground/10 hover:text-foreground [&_svg]:size-5!"
                      data-collapsed={collapsed}
                      onClick={toggleSidebar}
                      size="icon-sm"
                      variant="ghost"
                    >
                      {collapsed ? (
                        <>
                          {/* The logo fades into the open icon on hover */}
                          <Image
                            alt="SLT"
                            className="size-7 rounded-full bg-white object-contain p-1 transition-[opacity,scale] duration-200 group-hover/toggle:scale-75 group-hover/toggle:opacity-0"
                            src={telecomIcon}
                          />
                          <PanelLeftIcon className="sidebar-icon-panel absolute inset-0 m-auto scale-75 opacity-0 transition-[opacity,scale] duration-200 group-hover/toggle:scale-100 group-hover/toggle:opacity-100" />
                        </>
                      ) : (
                        <PanelLeftIcon className="sidebar-icon-panel" />
                      )}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent
                    className="hidden md:block"
                    side={collapsed ? "right" : "bottom"}
                    sideOffset={collapsed ? 19 : 4}
                  >
                    {collapsed ? "Open sidebar" : "Close sidebar"}
                  </TooltipContent>
                </Tooltip>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarHeader>
          <SidebarContent>
            <SidebarGroup className="px-[11px] pt-4">
              <SidebarGroupContent>
                <SidebarMenu className="gap-1">
                  <SidebarMenuItem>
                    <SidebarMenuButton
                      className={NAV_BUTTON}
                      onClick={handleNewChat}
                      tooltip="New chat"
                    >
                      <PenSquareIcon className="sidebar-icon-pencil" />
                      <span>New chat</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                  <SidebarMenuItem>
                    <SidebarMenuButton
                      className={cn(
                        NAV_BUTTON,
                        "data-[active=true]:bg-foreground/10"
                      )}
                      data-testid="sidebar-saved-responses"
                      isActive={isPageRoute(pathname)}
                      onClick={handleSaved}
                      tooltip="Saved responses"
                    >
                      <BookmarkIcon className="sidebar-icon-bookmark" />
                      <span>Saved responses</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                </SidebarMenu>
              </SidebarGroupContent>
            </SidebarGroup>
            <SidebarHistory user={user} />
          </SidebarContent>
          <SidebarFooter className="px-[11px] pt-2 pb-2 group-data-[collapsible=icon]:pb-4">
            {user ? <SidebarUserNav user={user} /> : null}
          </SidebarFooter>
        </div>
      </div>
    </Sidebar>
  );
}
