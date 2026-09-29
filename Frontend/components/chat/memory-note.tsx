import { BrainIcon } from "lucide-react";
import type { MemoryChange } from "@/lib/types";

const ACTIONS: Record<MemoryChange["action"], string> = {
  deleted: "Memory deleted",
  saved: "Memory saved",
  updated: "Memory updated",
};

// What the message changed in the user's memories, under the answer; they
// can all be seen and deleted in Settings → Memory
export function MemoryNote({ changes }: { changes: MemoryChange[] }) {
  if (changes.length === 0) {
    return null;
  }

  return (
    <ul className="flex flex-col gap-0.5 text-muted-foreground text-xs">
      {changes.map((change) => (
        <li
          className="flex items-start gap-1.5"
          key={`${change.action}-${change.memory}`}
        >
          <BrainIcon className="mt-px size-3.5 shrink-0" />
          <span>
            <span className="text-foreground/70">{ACTIONS[change.action]}</span>
            {" · "}
            {change.memory}
          </span>
        </li>
      ))}
    </ul>
  );
}
