"use client";

import type { UseChatHelpers } from "@ai-sdk/react";
import { motion } from "framer-motion";
import { ChevronLeftIcon, ChevronRightIcon } from "lucide-react";
import {
  type Dispatch,
  type KeyboardEvent,
  memo,
  type PointerEvent,
  type SetStateAction,
  useCallback,
  useEffect,
  useState,
} from "react";
import { FIXED_IDEAS, type Idea, ideas } from "@/lib/suggestions";
import type { ChatMessage } from "@/lib/types";
import { cn } from "@/lib/utils";
import { ideaPictures } from "./idea-pictures";
import type { VisibilityType } from "./visibility-selector";

const PER_PAGE = 3;

type SuggestedActionsProps = {
  chatId: string;
  sendMessage: UseChatHelpers<ChatMessage>["sendMessage"];
  setInput: Dispatch<SetStateAction<string>>;
  selectedVisibilityType: VisibilityType;
};

function shuffled<T>(items: T[]) {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const other = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[other]] = [copy[other], copy[index]];
  }
  return copy;
}

function focusComposer() {
  requestAnimationFrame(() => {
    const box = document.querySelector<HTMLTextAreaElement>(
      "[data-testid='multimodal-input']"
    );
    box?.focus();
    box?.setSelectionRange(box.value.length, box.value.length);
  });
}

// The purple light on a card follows the mouse (see .idea-card in globals.css)
function followPointer(event: PointerEvent<HTMLButtonElement>) {
  const card = event.currentTarget;
  const box = card.getBoundingClientRect();
  card.style.setProperty("--x", `${event.clientX - box.left}px`);
  card.style.setProperty("--y", `${event.clientY - box.top}px`);
}

function IdeaCard({
  idea,
  index,
  onPick,
  onFocusCard,
  onKeyDown,
}: {
  idea: Idea;
  index: number;
  onPick: (idea: Idea) => void;
  onFocusCard: (index: number) => void;
  onKeyDown: (event: KeyboardEvent<HTMLButtonElement>) => void;
}) {
  const handleClick = useCallback(() => onPick(idea), [idea, onPick]);
  const handleFocus = useCallback(
    () => onFocusCard(index),
    [index, onFocusCard]
  );

  return (
    <motion.div
      animate={{ opacity: 1, y: 0 }}
      className="flex shrink-0 basis-[calc((100%_-_76px)/3)] max-sm:basis-[78%] max-sm:snap-start"
      initial={{ opacity: 0, y: 16 }}
      transition={{
        delay: 0.06 * Math.min(index, PER_PAGE),
        duration: 0.4,
        ease: [0.22, 1, 0.36, 1],
      }}
    >
      <button
        className="idea-card relative flex w-full flex-col gap-2.5 rounded-2xl border border-border/60 bg-suggestion p-2 text-left outline-none transition-[transform,background-color] duration-200 ease-[cubic-bezier(0.22,1,0.36,1)] hover:-translate-y-0.5 hover:bg-suggestion-hover focus-visible:-translate-y-0.5"
        onClick={handleClick}
        onFocus={handleFocus}
        onKeyDown={onKeyDown}
        onPointerMove={followPointer}
        type="button"
      >
        <div className="idea-picture relative h-[92px] w-full overflow-hidden rounded-xl">
          {ideaPictures[idea.id]}
        </div>
        <div className="flex flex-col gap-0.5 px-1.5 pb-1">
          <span className="font-semibold text-[14px] leading-snug">
            {idea.title}
          </span>
          <span className="text-muted-foreground text-xs leading-snug">
            {idea.detail}
          </span>
        </div>
      </button>
    </motion.div>
  );
}

function PageDot({
  page,
  active,
  onShow,
}: {
  page: number;
  active: boolean;
  onShow: (page: number) => void;
}) {
  const handleClick = useCallback(() => onShow(page), [onShow, page]);

  return (
    <button
      aria-current={active}
      aria-label={`Ideas page ${page + 1}`}
      className={cn(
        "h-1.5 rounded-full transition-[width,background-color] duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]",
        active
          ? "w-5 bg-[#a78bfa]"
          : "w-1.5 bg-foreground/25 hover:bg-foreground/40"
      )}
      onClick={handleClick}
      type="button"
    />
  );
}

function PureSuggestedActions({
  chatId,
  sendMessage,
  setInput,
}: SuggestedActionsProps) {
  // Shuffled after the first render, so the server and the browser agree on it
  const [ordered, setOrdered] = useState(ideas);
  const [page, setPage] = useState(0);
  const pages = Math.ceil(ordered.length / PER_PAGE);

  useEffect(() => {
    setOrdered([
      ...ideas.slice(0, FIXED_IDEAS),
      ...shuffled(ideas.slice(FIXED_IDEAS)),
    ]);
  }, []);

  const showPage = useCallback(
    (target: number) => setPage(Math.max(0, Math.min(pages - 1, target))),
    [pages]
  );
  const showPrevious = useCallback(() => showPage(page - 1), [page, showPage]);
  const showNext = useCallback(() => showPage(page + 1), [page, showPage]);

  // Tabbing to a card on another page slides to it
  const showCard = useCallback(
    (index: number) => showPage(Math.floor(index / PER_PAGE)),
    [showPage]
  );

  // ← and → slide the row while a card or arrow has focus
  const handleKeyDown = useCallback(
    (event: KeyboardEvent<HTMLButtonElement>) => {
      if (event.key === "ArrowRight") {
        event.preventDefault();
        showNext();
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        showPrevious();
      }
    },
    [showNext, showPrevious]
  );

  const handlePick = useCallback(
    (idea: Idea) => {
      if (idea.draft !== undefined) {
        setInput(idea.draft);
        focusComposer();

        if (idea.pickImage) {
          document
            .querySelector<HTMLButtonElement>(
              "[data-testid='attachments-button']"
            )
            ?.click();
        }
        return;
      }

      window.history.pushState(
        {},
        "",
        `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/chat/${chatId}`
      );
      sendMessage({
        parts: [{ text: idea.prompt ?? idea.title, type: "text" }],
        role: "user",
      });
    },
    [chatId, sendMessage, setInput]
  );

  const isLastPage = page === pages - 1;
  // Fades the card peeking in on the right, while there are more to see
  const fade = isLastPage
    ? undefined
    : "linear-gradient(to right, #000 calc(100% - 64px), transparent)";

  return (
    <section aria-label="Suggestions" className="flex w-full flex-col gap-3.5">
      <div className="flex min-h-[30px] items-center justify-between">
        <span className="font-medium text-[13.5px] text-muted-foreground">
          Not sure where to start?
        </span>
        <div className="flex gap-1.5 max-sm:hidden">
          <button
            aria-label="Previous ideas"
            className="grid size-[30px] place-items-center rounded-full border border-border bg-suggestion text-foreground/80 transition-colors hover:border-[#a78bfa]/40 hover:bg-suggestion-hover disabled:pointer-events-none disabled:opacity-30"
            disabled={page === 0}
            onClick={showPrevious}
            onKeyDown={handleKeyDown}
            type="button"
          >
            <ChevronLeftIcon className="size-4" />
          </button>
          <button
            aria-label="More ideas"
            className="grid size-[30px] place-items-center rounded-full border border-border bg-suggestion text-foreground/80 transition-colors hover:border-[#a78bfa]/40 hover:bg-suggestion-hover disabled:pointer-events-none disabled:opacity-30"
            disabled={isLastPage}
            onClick={showNext}
            onKeyDown={handleKeyDown}
            type="button"
          >
            <ChevronRightIcon className="size-4" />
          </button>
        </div>
      </div>

      <div
        className="-my-2 overflow-hidden py-2 max-sm:snap-x max-sm:snap-mandatory max-sm:overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
        style={{ maskImage: fade, WebkitMaskImage: fade }}
      >
        <div
          className="flex gap-3 transition-transform duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] max-sm:transform-none!"
          data-testid="suggested-actions"
          style={{ transform: `translateX(calc(${page} * (40px - 100%)))` }}
        >
          {ordered.map((idea, index) => (
            <IdeaCard
              idea={idea}
              index={index}
              key={idea.id}
              onFocusCard={showCard}
              onKeyDown={handleKeyDown}
              onPick={handlePick}
            />
          ))}
        </div>
      </div>

      <div className="flex justify-center gap-1.5 max-sm:hidden">
        {Array.from({ length: pages }, (_, index) => (
          <PageDot
            active={index === page}
            // biome-ignore lint/suspicious/noArrayIndexKey: pages are just numbers
            key={index}
            onShow={showPage}
            page={index}
          />
        ))}
      </div>
    </section>
  );
}

export const SuggestedActions = memo(
  PureSuggestedActions,
  (prevProps, nextProps) => {
    if (prevProps.chatId !== nextProps.chatId) {
      return false;
    }
    if (prevProps.selectedVisibilityType !== nextProps.selectedVisibilityType) {
      return false;
    }

    return true;
  }
);
