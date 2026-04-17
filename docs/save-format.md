# Save Format

## Game Mode Header

儲存檔案的第一行標識遊戲模式，避免後端重複解析邏輯：

- `AI_MODE` - 單人 vs AI 模式
- `TWO_PLAYER_MODE` - 本地雙人模式

範例：
```
AI_MODE
A0 C5 G3 OT A4 N11
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
