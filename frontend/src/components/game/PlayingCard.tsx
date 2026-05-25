import type { CardView, Suit } from "@/lib/types";
import { cn } from "@/lib/cn";

const SUIT_GLYPH: Record<Suit, string> = {
  H: "♥",
  D: "♦",
  C: "♣",
  S: "♠",
};

const SUIT_THEME: Record<Suit, { surface: string; fg: string }> = {
  H: { surface: "bg-suit-hearts-bg", fg: "text-suit-hearts" },
  D: { surface: "bg-suit-diamonds-bg", fg: "text-suit-diamonds" },
  C: { surface: "bg-suit-clubs-bg", fg: "text-suit-clubs" },
  S: { surface: "bg-suit-spades-bg", fg: "text-suit-spades" },
};

interface Props {
  card: CardView;
  matched: boolean;
  pending: boolean;
  disabled: boolean;
  onClick: () => void;
  ariaLabel: string;
}

export function PlayingCard({ card, matched, pending, disabled, onClick, ariaLabel }: Props) {
  const flipped = card.face_up;
  const theme = card.suit ? SUIT_THEME[card.suit] : null;
  const glyph = card.suit ? SUIT_GLYPH[card.suit] : "";

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
      <div className={cn("card-3d relative h-full w-full", flipped && "card-flipped")}>
        {/* Back face */}
        <div
          className={cn(
            "card-face absolute inset-0 rounded-xl border border-border shadow-sm",
            "bg-card-back",
            "flex items-center justify-center",
            !disabled && "transition-transform group-hover:scale-[1.02] group-active:scale-95",
            pending && "ring-2 ring-ring",
          )}
        >
          <div className="text-foreground/40 text-3xl font-black tracking-tighter select-none">
            ♠♥
          </div>
        </div>

        {/* Front face */}
        <div
          className={cn(
            "card-face card-face-back absolute inset-0 rounded-xl border border-border shadow-sm",
            theme?.surface ?? "bg-card",
            matched && "ring-2 ring-success/60",
            pending && !matched && "ring-2 ring-ring",
          )}
        >
          {/* Top-left corner */}
          <div
            className={cn(
              "absolute top-1.5 left-2 flex flex-col items-center leading-none font-bold tabular-nums select-none",
              theme?.fg,
            )}
          >
            <span className="text-sm sm:text-base">{card.rank}</span>
            <span className="text-xs sm:text-sm">{glyph}</span>
          </div>

          {/* Centered glyph */}
          <div
            className={cn(
              "absolute inset-0 flex items-center justify-center text-3xl sm:text-5xl select-none",
              theme?.fg,
            )}
          >
            {glyph}
          </div>

          {/* Bottom-right corner (rotated) */}
          <div
            className={cn(
              "absolute bottom-1.5 right-2 flex flex-col items-center leading-none font-bold tabular-nums select-none rotate-180",
              theme?.fg,
            )}
          >
            <span className="text-sm sm:text-base">{card.rank}</span>
            <span className="text-xs sm:text-sm">{glyph}</span>
          </div>
        </div>
      </div>
    </button>
  );
}
