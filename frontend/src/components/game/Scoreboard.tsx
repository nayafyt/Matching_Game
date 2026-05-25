import { useTranslation } from "react-i18next";
import type { GameView } from "@/lib/types";
import { Panel, PanelBody, PanelHeader, PanelTitle } from "@/components/ui/panel";
import { cn } from "@/lib/cn";

interface Props {
  game: GameView;
}

export function Scoreboard({ game }: Props) {
  const { t } = useTranslation();

  return (
    <Panel>
      <PanelHeader>
        <PanelTitle>{t("hud.scoreboard")}</PanelTitle>
      </PanelHeader>
      <PanelBody className="space-y-2">
        {game.scores.map((score, idx) => {
          const playerNum = idx + 1;
          const isActive = playerNum === game.current_player && !game.is_finished;
          const isWinner = game.is_finished && game.winners.includes(playerNum);
          return (
            <div
              key={playerNum}
              className={cn(
                "flex items-center justify-between rounded-lg px-3 py-2 transition-colors",
                isActive && "bg-accent",
                isWinner && "bg-success/10 text-success",
              )}
            >
              <div className="flex items-center gap-2">
                <span
                  className={cn(
                    "inline-flex h-7 w-7 items-center justify-center rounded-full text-sm font-semibold",
                    isActive ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground",
                  )}
                >
                  {playerNum}
                </span>
                <span className="text-sm font-medium">{t("hud.player", { n: playerNum })}</span>
              </div>
              <span className="text-base font-bold tabular-nums">{score}</span>
            </div>
          );
        })}
      </PanelBody>
    </Panel>
  );
}
