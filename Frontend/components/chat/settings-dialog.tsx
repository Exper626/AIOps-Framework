"use client";

import { DatabaseIcon, SettingsIcon, UserIcon, XIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import type { User } from "next-auth";
import { signOut } from "next-auth/react";
import { type ReactNode, useState } from "react";
import { toast } from "sonner";
import { useSWRConfig } from "swr";
import { unstable_serialize } from "swr/infinite";
import { getChatHistoryPaginationKey } from "@/components/chat/sidebar-history";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";

type Tab = "general" | "data" | "account";

const TABS: { id: Tab; label: string; icon: ReactNode }[] = [
  { icon: <SettingsIcon />, id: "general", label: "General" },
  { icon: <DatabaseIcon />, id: "data", label: "Data controls" },
  { icon: <UserIcon />, id: "account", label: "Account" },
];

function Row({
  label,
  description,
  children,
}: {
  label: string;
  description?: string;
  children?: ReactNode;
}) {
  return (
    <div className="flex min-h-14 items-center justify-between gap-4 border-b border-border/60 py-3 last:border-b-0">
      <div className="flex min-w-0 flex-col gap-0.5">
        <span className="text-sm">{label}</span>
        {description ? (
          <span className="text-muted-foreground text-xs">{description}</span>
        ) : null}
      </div>
      <div className="shrink-0 text-muted-foreground text-sm">{children}</div>
    </div>
  );
}

export function SettingsDialog({
  open,
  onOpenChange,
  user,
  isGuest,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  user: User;
  isGuest: boolean;
}) {
  const router = useRouter();
  const { mutate } = useSWRConfig();
  const [tab, setTab] = useState<Tab>("general");
  const [confirmDelete, setConfirmDelete] = useState(false);

  const handleOpenChange = (next: boolean) => {
    if (!next) {
      setConfirmDelete(false);
    }
    onOpenChange(next);
  };

  const handleDeleteAll = () => {
    if (!confirmDelete) {
      setConfirmDelete(true);
      return;
    }
    setConfirmDelete(false);
    handleOpenChange(false);
    router.replace("/");
    mutate(unstable_serialize(getChatHistoryPaginationKey), [], {
      revalidate: false,
    });
    fetch(`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/api/history`, {
      method: "DELETE",
    });
    toast.success("All chats deleted");
  };

  const displayName = isGuest ? "Guest" : (user.name ?? user.email ?? "User");

  return (
    <Dialog onOpenChange={handleOpenChange} open={open}>
      <DialogContent
        className="flex h-[min(600px,85dvh)] flex-col gap-0 overflow-hidden rounded-2xl p-0 sm:max-w-[680px]"
        showCloseButton={false}
      >
        <div className="flex items-center justify-between border-b border-border/60 px-5 py-4">
          <DialogTitle className="font-semibold text-lg">Settings</DialogTitle>
          <DialogClose asChild>
            <Button aria-label="Close" size="icon-sm" variant="ghost">
              <XIcon />
            </Button>
          </DialogClose>
        </div>
        <DialogDescription className="sr-only">
          Manage your settings, data and account.
        </DialogDescription>

        <div className="flex min-h-0 flex-1 flex-col md:flex-row">
          <nav className="flex shrink-0 gap-1 overflow-x-auto border-b border-border/60 p-2 md:w-48 md:flex-col md:border-r md:border-b-0 md:p-3">
            {TABS.map((t) => (
              <button
                className={cn(
                  "flex items-center gap-2.5 whitespace-nowrap rounded-lg px-3 py-2 text-left text-sm transition-colors [&_svg]:size-4",
                  tab === t.id
                    ? "bg-muted text-foreground"
                    : "text-muted-foreground hover:bg-muted/50 hover:text-foreground",
                )}
                key={t.id}
                onClick={() => {
                  setTab(t.id);
                  setConfirmDelete(false);
                }}
                type="button"
              >
                {t.icon}
                {t.label}
              </button>
            ))}
          </nav>

          <div className="min-h-0 flex-1 overflow-y-auto px-5 py-2">
            {tab === "general" ? (
              <>
                <Row label="Assistant">SLT Network Assistant</Row>
                <Row label="Signed in as">{displayName}</Row>
                <Row
                  description={
                    isGuest
                      ? "Guest chats are tied to this browser session."
                      : "Your chats are saved to your account."
                  }
                  label="Session type"
                >
                  {isGuest ? "Guest" : "Account"}
                </Row>
              </>
            ) : null}

            {tab === "data" ? (
              <Row
                description="Permanently removes every chat in your history. This can't be undone."
                label="Delete all chats"
              >
                <Button
                  onClick={handleDeleteAll}
                  size="sm"
                  variant="destructive"
                >
                  {confirmDelete ? "Confirm delete" : "Delete all"}
                </Button>
              </Row>
            ) : null}

            {tab === "account" ? (
              <>
                <Row label="Name">{displayName}</Row>
                {isGuest ? null : (
                  <>
                    <Row label="Email">
                      <span className="block max-w-[220px] truncate">
                        {user.email}
                      </span>
                    </Row>
                    <Row label="Log out on this device">
                      <Button
                        onClick={() => signOut({ redirectTo: "/" })}
                        size="sm"
                        variant="outline"
                      >
                        Log out
                      </Button>
                    </Row>
                  </>
                )}
              </>
            ) : null}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
