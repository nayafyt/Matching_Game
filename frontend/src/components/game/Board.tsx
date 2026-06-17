import { useLayoutEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import type { GameView } from "@/lib/types";
import { PlayingCard } from "./PlayingCard";

interface Props {
  game: GameView;
  onFlip: (position: number) => void;
  busy: boolean;
}

// Gap between cards, in px (matches the visual rhythm of the rest of the UI).
const GAP = 12;
// Cards keep a 2:3 (width:height) playing-card ratio.
const CARD_RATIO = 2 / 3;

export function Board({ game, onFlip, busy }: Props) {
  const { t } = useTranslation();

  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });

  useLayoutEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const update = () => setSize({ w: el.clientWidth, h: el.clientHeight });
    update();
    const ro = new ResizeObserver(update);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  // Largest card width that lets the whole grid fit the available box in both
  // dimensions while preserving the card aspect ratio.
  const cardW = useMemo(() => {
    const { rows, cols } = game;
    if (!size.w || !size.h || !rows || !cols) return 0;
    const wBudget = (size.w - GAP * (cols - 1)) / cols;
    const hBudget = (size.h - GAP * (rows - 1)) / rows;
    return Math.max(0, Math.min(wBudget, hBudget * CARD_RATIO));
  }, [size, game.rows, game.cols]);

  const canFlip = useMemo(
    () =>
      !busy &&
      (game.phase === "awaiting_first" ||
        game.phase === "awaiting_second" ||
        game.phase === "awaiting_third"),
    [busy, game.phase],
  );

  const matchedSet = useMemo(() => {
    const set = new Set<number>();
    game.cards.forEach((c, i) => {
      if (c.face_up && !game.pending.includes(i)) set.add(i);
    });
    return set;
  }, [game.cards, game.pending]);

  const gridStyle = {
    gridTemplateColumns: `repeat(${game.cols}, ${cardW}px)`,
    gap: `${GAP}px`,
  };

  return (
    <div
      ref={containerRef}
      className="h-full w-full min-h-0 flex items-center justify-center"
    >
      <div role="grid" aria-label={t("hud.scoreboard")} className="grid" style={gridStyle}>
        {game.cards.map((card, i) => {
          const matched = matchedSet.has(i);
          const pending = game.pending.includes(i);
          const disabled = !canFlip || card.face_up;
          return (
            <PlayingCard
              key={i}
              card={card}
              matched={matched}
              pending={pending}
              disabled={disabled}
              onClick={() => onFlip(i)}
              ariaLabel={
                card.face_up
                  ? `${card.rank ?? ""} ${card.suit ?? ""}`
                  : `Card ${i + 1}, face down`
              }
            />
          );
        })}
      </div>
    </div>
  );
}
