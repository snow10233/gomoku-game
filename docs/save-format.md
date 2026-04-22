# Save Format

## Game Mode Header

儲存檔案的第一行標識遊戲模式，避免後端重複解析邏輯：

- `AI_MODE SWITCHS` - 單人 vs AI 模式（進行中）
- `TWO_PLAYER_MODE SWITCHS` - 本地雙人模式（進行中）
- `AI_MODE ENDING` - 單人 vs AI 模式（已結束）
- `TWO_PLAYER_MODE ENDING` - 本地雙人模式（已結束）
- `SWITCHS` - 代表三個開關，分別對應悔棋 計時 重置(只需在前端進行判斷即可)，ON 代表開啟，OFF 代表關閉
- `ENDING` - 棋局已結束（勝負分出或平局），載入時前端只顯示提示，不進入遊戲

範例：
```
AI_MODE ON ON ON
A0 C5 G3 OT A4 N11
```
```
TWO_PLAYER_MODE ON OFF ON
A0 C5 G3 OT A4 N11
```
```
AI_MODE ENDING
A0 C5 G3 N11
```

## PNG String Definition

- `OT` 代表 `OVER_TIME`。
- 範例：`A0 C5 G3 OT A4 N11`

## Coordinate Mapping

Columns:

`A B C D E F G H I J K L M N O`

Rows:

- `00`
- `01`
- `02`
- `03`
- `04`
- `05`
- `06`
- `07`
- `08`
- `09`
- `10`
- `11`
- `12`
- `13`
- `14`
