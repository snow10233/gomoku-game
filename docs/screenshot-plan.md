# Screenshot Plan

Use this checklist to capture README-ready images after the UI is in its final visual state.

## Recommended Shots

1. Home menu
   - Show the project title and the main mode choices.
   - Useful for presenting the application entry point.

2. Single-player AI game
   - Capture an in-progress board with both black and white stones.
   - Include the timer and right-side controls.
   - Current example: `docs/assets/screenshots/gomoku-runtime.png`.

3. Local two-player setup
   - Show the undo, timer, and reset toggles before starting a game.
   - Useful for demonstrating configurable game rules.

4. Save/load dialog or saved `.gmk` file
   - Show that game state can be exported as a replay file.
   - Avoid exposing unrelated local file paths if sharing publicly.

5. Replay viewer
   - Show the replay page after loading a `.gmk` file.
   - Capture the step counter and next/previous controls.

6. End-game overlay
   - Show a black win, white win, or draw result.
   - Include the save and copy replay actions.

## Capture Guidelines

- Use a clean board state with visible tactical structure, not an empty board.
- Keep image sizes consistent, preferably 800x700 for raw app screenshots.
- Crop only if it does not hide important controls.
- Use PNG for UI screenshots.
- Store final images under `docs/assets/screenshots/`.
- Suggested filenames:
  - `home-menu.png`
  - `single-player-ai.png`
  - `local-two-player-setup.png`
  - `replay-viewer.png`
  - `end-game-overlay.png`

## Markdown Embeds

```md
![Home menu](docs/assets/screenshots/home-menu.png)
![Single-player AI game](docs/assets/screenshots/single-player-ai.png)
![Replay viewer](docs/assets/screenshots/replay-viewer.png)
![End-game overlay](docs/assets/screenshots/end-game-overlay.png)
```
