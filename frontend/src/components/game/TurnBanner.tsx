import { useTranslation } from "react-i18next";
import type { GameView, Outcome } from "@/lib/types";
import { cn } from "@/lib/cn";

interface Props {
  game: GameView;
}

const MISS_OUTCOMES = new Set<Outcome>(["miss", "triple_miss"]);
const PHASES_WITH_RESULT = new Set<GameView["phase"]>([
  "awaiting_first",
  "reveal_pair",
  "reveal_triple",
  "finished",
]);

export function TurnBanner({ game }: Props) {
  const { t } = useTranslation();
  const result = game.last_result;
  const showResult = result && PHASES_WITH_RESULT.has(game.phase);
  const isMiss = result ? MISS_OUTCOMES.has(result.outcome) : false;

  return (
    <div className="flex flex-col items-center gap-2 text-center">
      <div className="text-sm font-medium text-muted-foreground">
        {t("hud.turn", { n: game.current_player })}
      </div>
      <div className="text-lg sm:text-xl font-semibold">{t(`hud.phase.${game.phase}`)}</div>
      {showResult && (
        <div
          className={cn(
            "text-sm rounded-full px-3 py-1",
            isMiss ? "bg-muted text-muted-foreground" : "bg-success/10 text-success",
          )}
        >
          {t(`outcome.${result.outcome}`, { points: result.points })}
        </div>
      )}
    </div>
  );
}
