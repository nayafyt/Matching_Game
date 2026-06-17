import { useTranslation } from "react-i18next";
import { useGame } from "@/hooks/useGame";
import { Board } from "@/components/game/Board";
import { GameOver } from "@/components/game/GameOver";
import { GameSetup } from "@/components/game/GameSetup";
import { HelpButton } from "@/components/game/HelpButton";
import { LanguageToggle } from "@/components/game/LanguageToggle";
import { Scoreboard } from "@/components/game/Scoreboard";
import { TurnBanner } from "@/components/game/TurnBanner";
import { Button } from "@/components/ui/button";

export default function App() {
  const { t } = useTranslation();
  const { game, busy, error, start, flip, reset } = useGame();

  return (
    <div className="h-full flex flex-col">
      <header className="border-b border-border">
        <div className="mx-auto max-w-6xl w-full flex items-center justify-between px-4 sm:px-6 py-3">
          <h1 className="text-base sm:text-lg font-semibold">{t("title")}</h1>
          <div className="flex items-center gap-2">
            {game && (
              <Button variant="ghost" size="sm" onClick={reset}>
                {t("hud.newGame")}
              </Button>
            )}
            <LanguageToggle />
            <HelpButton />
          </div>
        </div>
      </header>

      <main className="flex-1 min-h-0 mx-auto w-full max-w-[1800px] px-4 sm:px-6 py-6 sm:py-10 flex flex-col">
        {error && (
          <div
            role="alert"
            className="mb-4 rounded-lg border border-destructive/30 bg-destructive/10 px-4 py-2 text-sm text-destructive"
          >
            {t(error)}
          </div>
        )}

        {!game && <GameSetup busy={busy} onStart={start} />}

        {game && game.is_finished && <GameOver game={game} onPlayAgain={reset} />}

        {game && !game.is_finished && (
          <div className="flex-1 min-h-0 flex flex-col gap-6 lg:grid lg:grid-cols-[1fr_280px]">
            <div className="flex-1 min-h-0 flex flex-col gap-4">
              <TurnBanner game={game} />
              <div className="flex-1 min-h-0">
                <Board game={game} onFlip={flip} busy={busy} />
              </div>
            </div>
            <aside className="space-y-4">
              <Scoreboard game={game} />
            </aside>
          </div>
        )}
      </main>

      <footer className="border-t border-border">
        <div className="mx-auto max-w-6xl w-full px-4 sm:px-6 py-3 text-xs text-muted-foreground text-center">
          Matching Game · FastAPI + React
        </div>
      </footer>
    </div>
  );
}
