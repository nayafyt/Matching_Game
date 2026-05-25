import { memo } from "react";
import type { CardView, Rank, Suit } from "@/lib/types";
import { cn } from "@/lib/cn";

const SUIT_GLYPH: Record<Suit, string> = {
  H: "♥",
  D: "♦",
  C: "♣",
  S: "♠",
};

const RED_SUITS = new Set<Suit>(["H", "D"]);

interface Props {
  card: CardView;
  matched: boolean;
  pending: boolean;
  disabled: boolean;
  onClick: () => void;
  ariaLabel: string;
}

function PlayingCardImpl({ card, matched, pending, disabled, onClick, ariaLabel }: Props) {
  const flipped = card.face_up;
  const suitColor =
    card.suit && RED_SUITS.has(card.suit) ? "text-suit-red" : "text-suit-black";

  return (
    <button
      type="button"
      aria-label={ariaLabel}
      aria-pressed={flipped}
      disabled={disabled}
      onClick={onClick}
      className={cn(
        "group relative aspect-[2/3] w-full perspective-[1000px]",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-xl",
        disabled && !flipped && "cursor-not-allowed",
      )}
    >
      <div
        className={cn(
          "card-3d relative h-full w-full",
          flipped && "card-flipped",
        )}
      >
        {/* Back face */}
        <div
          className={cn(
            "card-face absolute inset-0 rounded-xl border border-border",
            "bg-gradient-to-br from-primary to-primary/80",
            "flex items-center justify-center",
            !disabled && "transition-transform group-hover:scale-[1.02] group-active:scale-95",
            pending && "ring-2 ring-ring",
          )}
        >
          <div className="text-primary-foreground/80 text-2xl font-black tracking-tighter">
            ♠♥
          </div>
        </div>

        {/* Front face */}
        <div
          className={cn(
            "card-face card-face-back absolute inset-0 rounded-xl border border-border bg-card",
            "p-2 flex flex-col justify-between shadow-sm",
            matched && "ring-2 ring-success/60",
            pending && !matched && "ring-2 ring-ring",
          )}
        >
          <div className={cn("text-left text-sm sm:text-base font-bold leading-none", suitColor)}>
            <div>{card.rank}</div>
            <div className="text-base sm:text-lg">{card.suit ? SUIT_GLYPH[card.suit] : ""}</div>
          </div>
          <div className={cn("self-center text-2xl sm:text-4xl", suitColor)}>
            {card.suit ? SUIT_GLYPH[card.suit] : ""}
          </div>
          <div className={cn("text-right text-sm sm:text-base font-bold leading-none rotate-180", suitColor)}>
            <div>{card.rank}</div>
            <div className="text-base sm:text-lg">{card.suit ? SUIT_GLYPH[card.suit] : ""}</div>
          </div>
        </div>
      </div>
    </button>
  );
}

export const PlayingCard = memo(PlayingCardImpl);

export function rankLabel(rank: Rank | null): string {
  return rank ?? "?";
}
