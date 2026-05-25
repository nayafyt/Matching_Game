import { useState } from "react";
import { useTranslation } from "react-i18next";
import type { Difficulty } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Panel, PanelBody, PanelHeader, PanelTitle } from "@/components/ui/panel";

interface Props {
  busy: boolean;
  onStart: (difficulty: Difficulty, numPlayers: number) => void;
}

export function GameSetup({ busy, onStart }: Props) {
  const { t } = useTranslation();
  const [difficulty, setDifficulty] = useState<Difficulty>(1);
  const [players, setPlayers] = useState(2);

  return (
    <Panel className="max-w-md mx-auto w-full">
      <PanelHeader>
        <PanelTitle>{t("title")}</PanelTitle>
        <p className="text-sm text-muted-foreground mt-1">{t("subtitle")}</p>
      </PanelHeader>
      <PanelBody className="space-y-5">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="difficulty">
            {t("setup.difficulty")}
          </label>
          <select
            id="difficulty"
            value={difficulty}
            onChange={(e) => setDifficulty(Number(e.target.value) as Difficulty)}
            className="h-10 w-full rounded-lg border border-input bg-background px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value={1}>{t("setup.easy")}</option>
            <option value={2}>{t("setup.medium")}</option>
            <option value={3}>{t("setup.hard")}</option>
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="players">
            {t("setup.players")}: <span className="tabular-nums">{players}</span>
          </label>
          <input
            id="players"
            type="range"
            min={2}
            max={8}
            value={players}
            onChange={(e) => setPlayers(Number(e.target.value))}
            className="w-full"
          />
        </div>

        <Button
          size="lg"
          className="w-full"
          disabled={busy}
          onClick={() => onStart(difficulty, players)}
        >
          {busy ? t("setup.starting") : t("setup.start")}
        </Button>
      </PanelBody>
    </Panel>
  );
}
