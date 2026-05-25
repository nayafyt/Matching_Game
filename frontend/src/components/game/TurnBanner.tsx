import { useTranslation } from "react-i18next";
import type { GameView } from "@/lib/types";
import { cn } from "@/lib/cn";

interface Props {
  game: GameView;
}

export function TurnBanner({ game }: Props) {
  const { t } = useTranslation();

  const phaseKey = `hud.phase.${game.phase}` as const;
  const result = game.last_result;

  const resultMessage =
    result &&
    (game.phase === "awaiting_first" ||
      game.phase === "reveal_pair" ||
      game.phase === "reveal_triple" ||
      game.phase === "finished")
      ? t(`outcome.${result.outcome}`, { points: result.points })
      : null;

  return (
    <div className="flex flex-col items-center gap-2 text-center">
      <div className="text-sm font-medium text-muted-foreground">
        {t("hud.turn", { n: game.current_player })}
      </div>
      <div className="text-lg sm:text-xl font-semibold">{t(phaseKey)}</div>
      {resultMessage && (
        <div
          className={cn(
            "text-sm rounded-full px-3 py-1",
            result?.outcome.endsWith("miss")
              ? "bg-muted text-muted-foreground"
              : "bg-success/10 text-success",
          )}
        >
          {resultMessage}
        </div>
      )}
    </div>
  );
}
