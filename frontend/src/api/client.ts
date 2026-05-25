import type { Difficulty, GameView } from "@/lib/types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new ApiError(res.status, text || res.statusText);
  }
  return res.json() as Promise<T>;
}

export const api = {
  createGame(difficulty: Difficulty, numPlayers: number): Promise<GameView> {
    return request<GameView>("/api/games", {
      method: "POST",
      body: JSON.stringify({ difficulty, num_players: numPlayers }),
    });
  },
  flip(id: string, position: number): Promise<GameView> {
    return request<GameView>(`/api/games/${id}/flip`, {
      method: "POST",
      body: JSON.stringify({ position }),
    });
  },
  resolve(id: string): Promise<GameView> {
    return request<GameView>(`/api/games/${id}/resolve`, { method: "POST" });
  },
};

export { ApiError };
