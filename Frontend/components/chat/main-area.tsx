"use client";

import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import { isPageRoute } from "@/lib/routes";
import { cn } from "@/lib/utils";

// Pages such as Saved responses take the chat's place. The chat stays mounted
// (only hidden), so an answer being written isn't lost by looking at them.
export function MainArea({
  chat,
  children,
}: {
  chat: ReactNode;
  children: ReactNode;
}) {
  const pathname = usePathname();
  const showsPage = isPageRoute(pathname);

  return (
    <>
      <div className={cn("contents", showsPage && "hidden")}>{chat}</div>
      {children}
    </>
  );
}
