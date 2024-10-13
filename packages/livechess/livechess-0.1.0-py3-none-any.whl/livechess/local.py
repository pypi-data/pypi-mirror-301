import os
import re
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from io import StringIO
from typing import Optional, Literal, Iterable

import chess.pgn
import requests
from chess import Board
from more_itertools.more import doublestarmap


@dataclass
class TournamentSummary:
    uuid: str
    description: str
    rounds: int


@dataclass
class TournamentDetail:
    uuid: str
    name: str
    description: str
    location: str
    country: str
    rounds: int
    eboards: list[str]


class EboardState(str, Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"


@dataclass
class EboardClock:
    white: int
    black: int
    run: bool | None
    time: int

    @property
    def paused(self):
        return self.run is None

    @property
    def terminal_string(self) -> str:
        white = str(timedelta(seconds=self.white))
        black = str(timedelta(seconds=self.black))
        white_running = self.run == True
        black_running = self.run == False
        paused = self.run is None
        return (
            f"{'●' if white_running else ' '} {white}"
            f" {'‖' if paused else '-'} "
            f"{black} {'○' if black_running else ' '}"
        )


@dataclass
class Eboard:
    serialnr: str
    source: str
    state: Literal["ACTIVE"] | Literal["INACTIVE"]
    battery: None | bool
    comment: None | str
    board: str  # FEN
    flipped: bool
    clock: None | EboardClock

    def __post_init__(self):
        if self.clock is not None and isinstance(self.clock, dict):
            self.clock = EboardClock(**self.clock)


@dataclass
class Player:
    fname: str | None
    mname: str | None
    lname: str | None
    title: str | None
    federation: str | None
    gender: str | None
    fideid: str | None

    @property
    def name(self):
        parts = [self.fname, self.mname, self.lname]
        return " ".join(part for part in parts if part)


def result_string(result: str | None) -> str:
    match result:
        case "WHITEWIN":
            return "1-0"
        case "WHITEFORFAIT":
            return "1-0F"
        case "BLACKWIN":
            return "0-1"
        case "BLACKFORFAIT":
            return "0-1F"
        case "DRAW":
            return "½-½"
        case _:
            return result


@dataclass
class Pairing:
    nr: int
    uuid: str
    white: Player
    black: Player
    live: bool
    result: str | None

    def __post_init__(self):
        if isinstance(self.white, dict):
            self.white = Player(**self.white)
        if isinstance(self.black, dict):
            self.black = Player(**self.black)

    @property
    def result_string(self):
        return result_string(self.result)


@dataclass
class Round:
    nr: int
    date: None | str
    pairings: list[Pairing]

    def __post_init__(self):
        self.pairings = [
            Pairing(**pairing) if isinstance(pairing, dict) else pairing
            for pairing in self.pairings
        ]


@dataclass
class Game:
    chess960: int
    result: str | None
    comment: str | None
    clock: EboardClock | None
    moves: list[str]

    def __post_init__(self):
        if self.clock is not None and isinstance(self.clock, dict):
            self.clock = EboardClock(**self.clock)

    @property
    def result_string(self):
        return result_string(self.result)

    @property
    def last_move(self):
        if len(self.moves) == 0:
            return None
        move, _ = self.moves[-1].split(" ")
        index = (len(self.moves) + 1) // 2
        return f"{index}{'' if len(self.moves) & 1 else '..'}. {move}"


class EventType(str, Enum):
    board_missing = "board_missing"
    game_finished = "game_finished"
    clock_paused = "clock_paused"
    long_move_bug = "long_move_bug"
    king_move_bug = "king_move_bug"
    premature_result = "premature_result"
    error_reconstructing_game = "error_reconstructing_game"


@dataclass
class Event:
    type: EventType
    round: int
    board: int
    args: tuple[str, ...] | None = field(default=None)

    @property
    def description(self):
        match self.type:
            case EventType.board_missing:
                return "Board missing"
            case EventType.game_finished:
                return "Game finished"
            case EventType.clock_paused:
                return "Clock paused"
            case EventType.long_move_bug:
                return f"Wrong move guessed by LiveChess on move {self.args[0]} of {self.args[1]}"
            case EventType.king_move_bug:
                return "Non-played king move added by LiveChess"
            case EventType.error_reconstructing_game:
                return "Error reconstructing game"
            case EventType.premature_result:
                return "Premature result"
            case _:
                return "Unknown event"

    def __hash__(self):
        return hash((self.type, self.round, self.board, self.args))

    def __eq__(self, other):
        return (
            self.type == other.type
            and self.round == other.round
            and self.board == other.board
            and self.args == other.args
        )

    def __lt__(self, other):
        if self.round != other.round:
            return self.round < other.round

        if self.board != other.board:
            return self.board < other.board

        if self.type != other.type:
            return self.type.value < other.type.value

        if self.type == EventType.long_move_bug:
            if self.args[0] != other.args[0]:
                return self.args[0] < other.args[0]
            return self.args[0] > other.args[0]

        return False


REGEX_MADE_UP_KING_MOVE = re.compile(r"K[de][45]( +\d+)?")


class LiveChessLocal:
    def __init__(self, host: Optional[str] = None, port: int = 1982) -> None:
        self.host = host or os.environ.get("LIVECHESS_HOST") or "localhost"
        self.port = port

    def _get(self, path: str) -> dict | list:
        response = requests.get(f"http://{self.host}:{self.port}/{path}")
        response.raise_for_status()
        return response.json()

    def tournaments(self) -> list[TournamentSummary]:
        return list(doublestarmap(TournamentSummary, self._get("api/v1.0/tournaments")))

    def tournament(self, tournament_id: str) -> TournamentDetail:
        return TournamentDetail(**self._get(f"api/v1.0/tournament/{tournament_id}"))

    def eboards(self) -> list[Eboard]:
        return list(doublestarmap(Eboard, self._get("api/v1.0/eboards")))

    def round(self, tournament_id: str, round: int) -> Round:
        return Round(**self._get(f"api/v1.0/round/{tournament_id}/{round}"))

    def rounds(self, tournament_id: str, rounds: Iterable[int]) -> Iterable[Round]:
        for round in rounds:
            yield self.round(tournament_id, round)

    def game(self, game_id: str) -> Game:
        return Game(**self._get(f"api/v1.0/game/{game_id}"))

    def events(self, tournament_id: str) -> Iterable[Event]:
        tournament = self.tournament(tournament_id)
        eboards = {eboard.serialnr: eboard for eboard in self.eboards()}
        rounds = [
            round
            for round in self.rounds(tournament_id, range(tournament.rounds))
            if any(pairing.live for pairing in round.pairings)
        ]
        for round in rounds:
            for pairing in round.pairings:
                if not pairing.live:
                    continue

                eboard = eboards[tournament.eboards[pairing.nr - 1]]
                if eboard.state == "INACTIVE":
                    yield Event(EventType.board_missing, round.nr, pairing.nr)

                game = self.game(pairing.uuid)
                if game.clock is not None and game.clock.paused:
                    if game.result != pairing.result and game.result is not None:
                        yield Event(EventType.game_finished, round.nr, pairing.nr)
                        if len(game.moves) > 0 and REGEX_MADE_UP_KING_MOVE.match(
                            game.moves[-1]
                        ):
                            yield Event(EventType.king_move_bug, round.nr, pairing.nr)
                    elif len(game.moves) > 0:
                        yield Event(EventType.clock_paused, round.nr, pairing.nr)
                        if REGEX_MADE_UP_KING_MOVE.match(game.moves[-1]):
                            yield Event(EventType.king_move_bug, round.nr, pairing.nr)
                elif game.clock is None and pairing.result is None:
                    yield Event(EventType.game_finished, round.nr, pairing.nr)
                elif (
                    game.clock is not None
                    and (not game.clock.paused or pairing.live)
                    and game.result is not None
                ):
                    yield Event(EventType.premature_result, round.nr, pairing.nr)

                for index, move in enumerate(game.moves):
                    if " " not in move:
                        wrong_move_index = index + 1
                        yield Event(
                            EventType.long_move_bug,
                            round.nr,
                            pairing.nr,
                            (
                                str(wrong_move_index // 2),
                                "white" if wrong_move_index % 2 == 0 else "black",
                            ),
                        )
                moves = [move.split(" ")[0] for move in game.moves]

                if len(moves) > 0:
                    pgn = chess.pgn.read_game(StringIO(" ".join(moves)))
                    end_position = pgn.end()

                    eboard_board = Board(eboard.board)
                    pgn_board = end_position.board()
                    differences = [
                        index
                        for index in range(64)
                        if eboard_board.color_at(index) is not pgn_board.color_at(index)
                        or eboard_board.piece_at(index) != pgn_board.piece_at(index)
                    ]

                    if game.result is None and end_position.board().is_game_over():
                        yield Event(EventType.game_finished, round.nr, pairing.nr)
                    elif game.result is None and len(differences) >= 3:
                        yield Event(
                            EventType.error_reconstructing_game, round.nr, pairing.nr
                        )
