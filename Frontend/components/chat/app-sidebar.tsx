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
  SidebarRail,
  useSidebar,
} from "@/components/ui/sidebar";
import { isPageRoute } from "@/lib/routes";
import { cn } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipTrigger } from "../ui/tooltip";

export function AppSidebar({ user }: { user: User | undefined }) {
  const router = useRouter();
  const pathname = usePathname();
  const { setOpenMobile, state, toggleSidebar } = useSidebar();
  const collapsed = state === "collapsed";

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
          <SidebarHeader className="pb-0 pt-3">
            <SidebarMenu>
              {/* Open: "Sri Lanka Telecom" on the left, toggle on the right.
              Collapsed: the SLT logo, which turns into the open icon on hover. */}
              <SidebarMenuItem
                className={cn(
                  "flex flex-row items-center",
                  collapsed ? "justify-center" : "justify-between"
                )}
              >
                {collapsed ? null : (
                  <button
                    className="rounded-lg px-2 py-1 font-semibold text-foreground text-lg tracking-normal"
                    onClick={handleNewChat}
                    type="button"
                  >
                    Sri Lanka Telecom
                  </button>
                )}
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      aria-label={collapsed ? "Open sidebar" : "Close sidebar"}
                      className="sidebar-toggle group/toggle relative size-9 rounded-lg text-foreground transition-colors duration-150 hover:bg-foreground/10 hover:text-foreground [&_svg]:size-5!"
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
                            className="size-7 rounded-lg bg-white object-contain p-1 transition-[opacity,scale] duration-200 group-hover/toggle:scale-75 group-hover/toggle:opacity-0"
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
                      <PenSquareIcon className="sidebar-icon-pencil" />
                      <span className="font-medium">New chat</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                  <SidebarMenuItem>
                    <SidebarMenuButton
                      className="h-8 rounded-lg px-1.5 text-[13px] [&>svg]:size-5 text-foreground transition-colors duration-150 hover:bg-foreground/10 hover:text-foreground data-[active=true]:bg-foreground/10"
                      data-testid="sidebar-saved-responses"
                      isActive={isPageRoute(pathname)}
                      onClick={handleSaved}
                      tooltip="Saved responses"
                    >
                      <BookmarkIcon className="sidebar-icon-bookmark" />
                      <span className="font-medium">Saved responses</span>
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
        </div>
      </div>
      <SidebarRail />
    </Sidebar>
  );
}
