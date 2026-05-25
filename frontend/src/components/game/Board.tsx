import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import type { GameView } from "@/lib/types";
import { PlayingCard } from "./PlayingCard";

interface Props {
  game: GameView;
  onFlip: (position: number) => void;
  busy: boolean;
}

export function Board({ game, onFlip, busy }: Props) {
  const { t } = useTranslation();

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
    gridTemplateColumns: `repeat(${game.cols}, minmax(0, 1fr))`,
  };

  return (
    <div
      role="grid"
      aria-label={t("hud.scoreboard")}
      className="grid gap-2 sm:gap-3"
      style={gridStyle}
    >
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
  );
}
