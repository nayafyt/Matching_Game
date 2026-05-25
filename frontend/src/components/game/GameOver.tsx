import { useTranslation } from "react-i18next";
import type { GameView } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Panel, PanelBody, PanelHeader, PanelTitle } from "@/components/ui/panel";

interface Props {
  game: GameView;
  onPlayAgain: () => void;
}

export function GameOver({ game, onPlayAgain }: Props) {
  const { t } = useTranslation();
  const topScore = Math.max(...game.scores);
  const single = game.winners.length === 1;

  return (
    <Panel className="max-w-md mx-auto w-full">
      <PanelHeader>
        <PanelTitle>{t("hud.phase.finished")}</PanelTitle>
      </PanelHeader>
      <PanelBody className="space-y-4 text-center">
        <p className="text-lg font-medium">
          {single
            ? t("finished.winner", { n: game.winners[0], points: topScore })
            : t("finished.tie", { players: game.winners.join(", "), points: topScore })}
        </p>
        <Button size="lg" onClick={onPlayAgain} className="w-full">
          {t("finished.playAgain")}
        </Button>
      </PanelBody>
    </Panel>
  );
}
