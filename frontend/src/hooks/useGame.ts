import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError } from "@/api/client";
import type { Difficulty, GameView } from "@/lib/types";

const REVEAL_DELAY_MS = 1100;

interface State {
  game: GameView | null;
  busy: boolean;
  error: string | null;
}

export function useGame() {
  const [state, setState] = useState<State>({ game: null, busy: false, error: null });
  const resolveTimer = useRef<number | null>(null);

  const setGame = useCallback((g: GameView) => {
    setState((s) => ({ ...s, game: g, error: null }));
    if (g.phase === "reveal_pair" || g.phase === "reveal_triple") {
      scheduleResolve(g.id);
    }
  }, []);

  const scheduleResolve = (id: string) => {
    if (resolveTimer.current) window.clearTimeout(resolveTimer.current);
    resolveTimer.current = window.setTimeout(() => {
      void doResolve(id);
    }, REVEAL_DELAY_MS);
  };

  const handleError = (e: unknown) => {
    const msg =
      e instanceof ApiError
        ? e.status === 409
          ? "errors.invalidMove"
          : `errors.network`
        : "errors.network";
    setState((s) => ({ ...s, busy: false, error: msg }));
  };

  const doResolve = useCallback(async (id: string) => {
    try {
      const next = await api.resolve(id);
      setGame(next);
    } catch (e) {
      handleError(e);
    }
  }, [setGame]);

  const start = useCallback(
    async (difficulty: Difficulty, numPlayers: number) => {
      setState((s) => ({ ...s, busy: true, error: null }));
      try {
        const g = await api.createGame(difficulty, numPlayers);
        setState({ game: g, busy: false, error: null });
      } catch (e) {
        handleError(e);
      }
    },
    [],
  );

  const flip = useCallback(
    async (position: number) => {
      if (!state.game) return;
      try {
        const g = await api.flip(state.game.id, position);
        setGame(g);
      } catch (e) {
        handleError(e);
      }
    },
    [setGame, state.game],
  );

  const reset = useCallback(() => {
    if (resolveTimer.current) window.clearTimeout(resolveTimer.current);
    setState({ game: null, busy: false, error: null });
  }, []);

  useEffect(() => {
    return () => {
      if (resolveTimer.current) window.clearTimeout(resolveTimer.current);
    };
  }, []);

  return { ...state, start, flip, reset };
}
