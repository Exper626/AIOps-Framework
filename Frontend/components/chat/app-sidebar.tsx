"use client";

import { PenSquareIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import type { User } from "next-auth";
import { useCallback } from "react";
import { SidebarHistory } from "@/components/chat/sidebar-history";
import { SidebarUserNav } from "@/components/chat/sidebar-user-nav";
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
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipTrigger } from "../ui/tooltip";

export function AppSidebar({ user }: { user: User | undefined }) {
  const router = useRouter();
  const { setOpenMobile, state } = useSidebar();

  const handleNewChat = useCallback(() => {
    setOpenMobile(false);
    router.push("/");
  }, [router, setOpenMobile]);

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="pb-0 pt-3">
        <SidebarMenu>
          {/* Toggle sits on the right when open, centred when collapsed */}
          <SidebarMenuItem
            className={cn(
              "flex flex-row items-center",
              state === "collapsed" ? "justify-center" : "justify-end"
            )}
          >
            <Tooltip>
              <TooltipTrigger asChild>
                <SidebarTrigger className="size-9 rounded-lg [&_svg]:size-5! text-foreground transition-colors duration-150 hover:bg-foreground/10 hover:text-foreground" />
              </TooltipTrigger>
              <TooltipContent
                className="hidden md:block"
                side={state === "collapsed" ? "right" : "bottom"}
                sideOffset={0}
              >
                {state === "collapsed" ? "Open sidebar" : "Close sidebar"}
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