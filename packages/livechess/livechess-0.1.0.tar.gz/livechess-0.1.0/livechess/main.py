from datetime import datetime
from operator import attrgetter
from time import sleep
from typing import Annotated, Optional
from uuid import UUID

import requests
import typer
from rich.console import Console
from rich.table import Table

from livechess.local import LiveChessLocal, EboardState

app = typer.Typer()

HostType = Annotated[
    str,
    typer.Option(help="Hostname or IP address of machine running DGT LiveChess"),
]
TournamentId = Annotated[
    UUID,
    typer.Argument(
        metavar="tournament",
        help="The tournament ID as given by the tournaments command or used in the LiveChessCloud URL",
    ),
]


@app.command()
def tournaments(host: HostType = None):
    client = LiveChessLocal(host)
    console = Console()

    tournaments = sorted(client.tournaments(), key=attrgetter("description"))

    table = Table(title="Tournaments")

    table.add_column("ID", style="cyan")
    table.add_column("Description", style="magenta")
    table.add_column("Rounds", justify="right", style="green")

    for tournament in tournaments:
        table.add_row(tournament.uuid, tournament.description, str(tournament.rounds))

    console.print(table)


@app.command()
def eboards(state: Optional[EboardState] = None, host: HostType = None):
    client = LiveChessLocal(host)
    console = Console()

    eboards = sorted(client.eboards(), key=attrgetter("serialnr"))

    table = Table(title="Eboards")
    table.add_column("ID", style="cyan")
    table.add_column("Source", style="magenta")
    table.add_column("State", style="magenta")
    table.add_column("FEN", style="green")
    table.add_column("Clock", style="green")

    for eboard in eboards:
        if state is not None and state != eboard.state:
            continue

        table.add_row(
            eboard.serialnr,
            eboard.source,
            eboard.state,
            eboard.board,
            eboard.clock.terminal_string if eboard.clock else "",
        )

    console.print(table)


@app.command()
def tournament(
    tournament_id: TournamentId,
    host: HostType = None,
):
    client = LiveChessLocal(host)
    console = Console()

    tournament = client.tournament(str(tournament_id))
    rounds = list(client.rounds(tournament.uuid, range(tournament.rounds)))

    pairings = [(round.nr, pairing) for round in rounds for pairing in round.pairings]
    live = [(rnd, pairing) for (rnd, pairing) in pairings if pairing.live]
    live_rounds = set(rnd for rnd, pairing in live)
    games = [(rnd, pairing) for (rnd, pairing) in pairings if rnd in live_rounds]

    table = Table(title=tournament.description)
    table.add_column("Rnd", style="cyan")
    table.add_column("Brd", style="red")
    table.add_column("White", style="yellow")
    table.add_column("Black", style="yellow")
    table.add_column("Result", style="green")
    table.add_column("Clock", style="magenta")
    table.add_column("Last move", style="cyan")

    for rnd, pairing in games:
        game = client.game(pairing.uuid)

        table.add_row(
            str(rnd),
            str(pairing.nr),
            pairing.white.name,
            pairing.black.name,
            pairing.result_string or game.result_string,
            game.clock.terminal_string if game.clock else "",
            game.last_move,
        )
    console.print(table)


@app.command()
def events(
    tournament_id: TournamentId,
    host: HostType = None,
):
    client = LiveChessLocal(host)
    console = Console()

    tournament = client.tournament(str(tournament_id))
    events = sorted(client.events(str(tournament_id)))

    if len(events) == 0:
        console.print("No events")
        return

    table = Table(title=f"Events for {tournament.name}")
    table.add_column("Round", style="cyan")
    table.add_column("Board", style="green")
    table.add_column("Event", style="red")

    for event in events:
        table.add_row(str(event.round), str(event.board), event.description)

    console.print(table)


@app.command()
def watch(
    tournament_id: TournamentId,
    host: HostType = None,
    ntfy: Annotated[
        Optional[str],
        typer.Option(
            help="Send events to th specified ntfy.sh channel. To use your own server, specify the full URL."
        ),
    ] = None,
    ignore_start: Annotated[
        bool, typer.Option(help="Ignore events already happening")
    ] = False,
):
    client = LiveChessLocal(host)
    console = Console()

    tournament = client.tournament(str(tournament_id))
    events = set() if ignore_start else set(client.events(str(tournament_id)))

    while True:
        past_events = events
        events = set(client.events(str(tournament_id)))
        new_events = events - past_events

        if len(new_events) > 0:
            messages = [
                f"{event.round}-{event.board}: {event.description}"
                for event in sorted(new_events)
            ]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for message in messages:
                console.print(f"[{timestamp}] {message}")
            if ntfy is not None:
                url = ntfy if ntfy.startswith("https://") else f"https://ntfy.sh/{ntfy}"
                requests.post(
                    url,
                    "\n".join(messages),
                    headers={
                        "Title": f"New events for {tournament.name}",
                        "Priority": "high",
                        "Tags": "warning",
                    },
                )

        sleep(5)
