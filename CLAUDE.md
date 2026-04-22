# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Two-process Gomoku game:
- **Backend (`backend/`)**: C++17 engine, single executable `gomoku`, owns all rule logic (win detection, AI, undo history, save string).
- **Frontend (`frontend/`)**: Python + PySide6 GUI. Spawns the backend as a child process and talks to it over **stdin/stdout line-based text protocol**.

Everything about the game state lives in the backend. The frontend is effectively a view that mirrors what the backend tells it.

## Common Commands

Build backend (produces `backend/build/gomoku`):
```bash
make -C backend/build
```
(If `backend/build` doesn't exist yet: `cmake -B backend/build -S backend`.)

Run the full app (frontend auto-spawns the backend):
```bash
cd frontend && .venv/bin/python3 main.py
```
or `bash run.bash` from the repo root.

Frontend dependency install:
```bash
cd frontend && pip install -r requirements.txt
```

CI runs only `cmake --build` on the backend and `python -m compileall .` on the frontend — there is no test suite and no linter configured.

## Architecture

### IPC boundary

`frontend/core/engine.py::GomokuEngine` is the only place that speaks to the backend. It wraps `subprocess.Popen` and exposes methods (`ai_mode`, `two_player_mode`, `put_chess`, `undo`, `over_time`, `save`, `reload_mode`, `reset`, `home_page`). Each method is a script of `stdin.write` / `stdout.readline` calls matching the state machine in `docs/protocol.md` — when you change the protocol, both sides plus that doc must move together.

Protocol shape:
- Every py→cpp **command** gets a `SUCCESS` / `INVALID` ack back first.
- Some commands then have additional structured payload lines (e.g. `PUT_CHESS` payload is `PUT_RESULT BOARD_STATE AI_X AI_Y` in AI mode, or `PUT_RESULT BOARD_STATE` in two-player mode).
- `TAKE_BACK` in AI mode returns **two** position lines (AI first, then player). Two-player mode returns one.
- `RELOAD_MODE` takes two extra payload lines (`SUB_MODE` + replay string) before its final ack.

### Backend state machine

`backend/src/main.cpp` has three layers:
1. Outer loop waits for a mode token (`AI_MODE`, `TWO_PLAYER_MODE`, `RELOAD_MODE`, `REVIEW_MODE`).
2. For `AI_MODE` / `TWO_PLAYER_MODE` it instantiates one `GameManager` and hands it to `runAiGameLoop()` / `runTwoPlayerGameLoop()`. These inner loops consume actions (`PUT_CHESS`, `TAKE_BACK`, `OVER_TIME`, `SAVE`, `RESET`, `HOME_PAGE`).
3. `RELOAD_MODE` reads the saved `SUB_MODE` + replay string, rebuilds a `GameManager` via `rebuildFromReplay()`, then dispatches into the matching inner loop. The same loops therefore serve both fresh and loaded games.

Key rule: `HOME_PAGE` breaks out of the inner loop back to the outer mode selector. Anything that re-enters the inner loop must re-set the mode first.

`GameManager` composes `Board`, `DataSaver` (undo stack), `AiPlayer`, and `Distance_calculator`. `DataSaver` stores `(-2, -2)` as an **OT placeholder** — a "time-out swap-player with no stone placed". `takeBack()` handles this specially (pops OT, swaps player, recurses to pop the real previous stone). When parsing a replay, `OT` tokens hit `overTime(false)` so the swap-without-placement is reproduced.

AI: `AiPlayer::findBestPos()` is a one-ply heuristic — scores every empty cell by longest same-colour run in 4 directions (via `Distance_calculator`), picks max of (AI offensive score, player's threat score). Not minimax.

### Frontend structure

- `main.py::MainWindow` owns all page instances, the `Router`, and the `AudioManager`. Pages communicate back via Qt `Signal`s (`request_home`, `request_start_game`, …); `MainWindow` wires them up in `__init__`.
- `core/engine.py`: the IPC wrapper.
- `ui/navigation/router.py`: thin wrapper over `QStackedWidget` keyed by a `Route` enum. Prefer adding a `Route` value and calling `router.register` + `router.go`, not switching widgets directly.
- `ui/pages/game_page.py::GamePage` is the shared base for both single-player (AI) and local-multiplayer. The multi page (`ui/pages/multi/multi_game_page.py`) overrides `handle_user_move`, `handle_time_out`, and `handle_undo` to remove AI-specific behaviour and to swap the active player on undo (AI mode retreats two stones and keeps the player on black; multiplayer retreats one and must flip turn).
- `ui/pages/replay_page.py`: **does not** talk to the backend. It parses the `.gmk` replay string itself and implements next/prev via two Python stacks (`future` / `history`). `OT` tokens in `history` get auto-skipped on `prev`; on `next` they trigger an AlertDialog per Q11 (user decision in project history) and then auto-advance one more step.
- `ui/components/battle_result.py` is a full-window overlay; it lives as a child of `GamePage` and is re-geometry'd in `resizeEvent`.

### Save format (`.gmk`)

Two lines of plain text:
```
AI_MODE              # or TWO_PLAYER_MODE
A0 C5 OT G3 N11      # space-separated tokens
```
Tokens: `<col-letter><row-number>` where `A..O` = column `0..14`. `OT` is the time-out placeholder described above. See `docs/save-format.md`.

### Audio

`AudioManager` keeps two `QMediaPlayer` instances for BGM crossfading and a third for SFX. BGM switching is guarded by `current_bgm_key` so redundant calls with the same key are no-ops — that's what allows navigating between menu pages without the music restarting.

## Conventions

- User-facing strings (labels, dialogs, log prints) are written in Traditional Chinese. Keep new ones in the same language when modifying nearby code.
- Backend never emits anything that isn't part of the protocol (no debug prints to `stdout`). Debug lines in `main.cpp` are commented out on purpose.
- `backend/build/` is committed with a prebuilt `Makefile`; don't delete it — `run.bash` and the top-level `make -C backend/build` assume it exists.
- Formatter config (from `.cursor/settings.json`): clang-format for C/C++, Black for Python, format-on-save enabled.

## Docs Index

- `docs/protocol.md` — authoritative IPC state machine
- `docs/save-format.md` — `.gmk` token grammar
- `docs/roadmap.md` — feature progress checklist
- `docs/getting-started.md`, `docs/development.md`, `docs/troubleshooting.md` — setup / WSL font notes

## TODO / Known Gaps

Outstanding roadmap work (see `docs/roadmap.md` for scoring context):

- **Network multiplayer (`MultiRemotePage`)**: explicitly deferred — "建立房間" / "加入房間" still route through `WipDialog`. No socket layer, no remote protocol.

Recently resolved (so don't re-report as bugs):
- `GameManager::takeBack()` now handles OT placeholders by swapping player and recursing to pop the real previous stone.
- `MultiGamePage.handle_undo` now swaps the active player after a single-stone undo.
- `GomokuEngine.save()` now reads both mode line and replay line (previously only read one, leaving the other in the pipe).
- `RELOAD_MODE` is fully implemented on both sides; save/load via `.gmk` files works through `GamePage.handle_save` / `MainWindow._load_game_file`.
- **Audio SFX wiring** complete: `place.wav`/`victory.mp3`/`fail.mp3` registered in `AudioManager.songs`; `place_signal`/`win_signal`/`lose_signal` on `GamePage` drive `play_sfx`. AI mode emits one place sound per round (player + AI combined); local multi emits per move and plays victory for either colour. No game-start sound by design.
- **Replay button** now routes `HomePage.btn_replay` through `request_replay` → `Route.REPLAY`; `ReplayPage` talks directly to files and implements prev/next via its own stacks.
- **Dead files removed**: `choose_mode_page.py`, `multi/multi_local_page.py`.
- **README typo** fixed.
- **Ctrl+C shutdown**: `HomePage` has a `Ctrl+C` `QShortcut` emitting `request_quit`, wired to `MainWindow.close`. `MainWindow.closeEvent` terminates both game-page engines. A terminal `SIGINT` handler + 200ms `QTimer` pump also closes the app from the shell, so a stuck backend after a bad `.gmk` load can always be torn down.
