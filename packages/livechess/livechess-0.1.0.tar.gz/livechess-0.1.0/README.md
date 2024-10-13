# Command line utility for DGT LiveChess

This CLI utility is meant to assist with your broadcast.

## Global Options

As all commands require communication with DGT LiveChess, a global option `--host` is provided as well as an environment variable `LIVECHESS_HOST`.
The option takes precedence over the environment variable.

## Commands

+---------+-------------+
| Command | Description |
+---------+-------------+
| tournaments | List tournaments in LiveChess |
| tournament | Show current games in a tournament |
| eboards | List known e-boards in LiveChess |
| events | Show list of events requiring operator attention |
| watch | Check for events requiring operator attention, with notification option |
+---------+-------------+

### tournaments

List all tournaments.

### tournament

Show games in acive rounds of the specified tournament.

### eboards

Show all eboards.
Options:

```
--state=(ACTIVE|INACTIVE)
```

Example:
```
livechess eboards --state=ACTIVE
```

### events

List events requiring operator attention.

### watch

Watch for events requiring operator attention.
Each event is printed with a timestamp of its first occurance.

Options:
```
--ntfy CHANNEL|URL   # Specify a ntfy.sh channel/URL as notification target
--[no-]ignore-start  # Ignore events present when starting the command
```