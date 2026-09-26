"use client";

import { useCallback, useState } from "react";
import { EMPTY_DIAGRAM, type NetworkDiagram } from "@/lib/diagram";
import { Button } from "../ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";
import { NetworkDiagramEditor } from "./network-diagram";

// Mounted each time the dialog opens, so it starts from the attached diagram
function DrawDiagramBody({
  initial,
  onAttach,
  onCancel,
}: {
  initial: NetworkDiagram;
  onAttach: (diagram: NetworkDiagram) => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState(initial);
  const handleAttach = useCallback(() => onAttach(draft), [draft, onAttach]);

  return (
    <>
      <DialogHeader>
        <DialogTitle>Draw a network diagram</DialogTitle>
      </DialogHeader>

      <NetworkDiagramEditor
        className="h-[70vh]"
        diagram={initial}
        onChange={setDraft}
      />

      <DialogFooter>
        <Button onClick={onCancel} variant="outline">
          Cancel
        </Button>
        <Button
          data-testid="diagram-attach"
          disabled={draft.devices.length === 0}
          onClick={handleAttach}
        >
          Attach to message
        </Button>
      </DialogFooter>
    </>
  );
}

// Escape while renaming a device only stops the renaming
function keepOpenWhileTyping(event: KeyboardEvent) {
  if (event.target instanceof HTMLInputElement) {
    event.preventDefault();
  }
}

export function DrawDiagramDialog({
  diagram,
  onAttach,
  onOpenChange,
  open,
}: {
  diagram: NetworkDiagram | null;
  onAttach: (diagram: NetworkDiagram) => void;
  onOpenChange: (open: boolean) => void;
  open: boolean;
}) {
  const close = useCallback(() => onOpenChange(false), [onOpenChange]);
  const attachAndClose = useCallback(
    (next: NetworkDiagram) => {
      onAttach(next);
      onOpenChange(false);
    },
    [onAttach, onOpenChange]
  );

  return (
    <Dialog onOpenChange={onOpenChange} open={open}>
      <DialogContent
        // No description under the title, which Radix otherwise warns about
        aria-describedby={undefined}
        className="gap-4 rounded-2xl sm:max-w-6xl"
        onEscapeKeyDown={keepOpenWhileTyping}
      >
        <DrawDiagramBody
          initial={diagram ?? EMPTY_DIAGRAM}
          onAttach={attachAndClose}
          onCancel={close}
        />
      </DialogContent>
    </Dialog>
  );
}
