export type Phase =
  | "awaiting_first"
  | "awaiting_second"
  | "reveal_pair"
  | "awaiting_third"
  | "reveal_triple"
  | "finished";

export type Outcome =
  | "match"
  | "miss"
  | "bonus_turn"
  | "skip_next"
  | "triple_match"
  | "triple_miss";

export type Difficulty = 1 | 2 | 3;

export type Suit = "H" | "D" | "C" | "S";
export type Rank =
  | "A" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10"
  | "J" | "Q" | "K";

export interface CardView {
  rank: Rank | null;
  suit: Suit | null;
  face_up: boolean;
}

export interface TurnResultView {
  outcome: Outcome;
  points: number;
  player: number;
  positions: number[];
}

export interface GameView {
  id: string;
  difficulty: Difficulty;
  num_players: number;
  rows: number;
  cols: number;
  current_player: number;
  phase: Phase;
  scores: number[];
  cards: CardView[];
  pending: number[];
  last_result: TurnResultView | null;
  is_finished: boolean;
  winners: number[];
}
