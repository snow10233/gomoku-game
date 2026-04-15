# Protocol Spec

## Convention

- `{TOKEN}`：固定訊息內容。
- `{A / B}`：成功回傳 `A`、失敗回傳 `B`。
- 流程由上而下依序進行。
- 多個資料欄位以空白分隔。

## Single Player

### 1) 模式選擇階段

#### 1.1 開啟新遊戲

- `py -> {AI_MODE} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`

#### 1.2 載入舊棋局

- `py -> {RELOAD_MODE} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`

### 2) 對局進行階段 (進入遊戲後)

#### 2.1 下棋 (傳送 x, y)

- `py -> {PUT_CHESS} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`
- `py -> {x y} -> cpp`
- `cpp -> {PUT_RESULT BOARD_STATE AI_X AI_Y / PUT_RESULT BOARD_STATE -1 -1} -> py`

#### 2.2 悔棋 (可連續悔棋)

- `py -> {TAKE_BACK} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`
- `cpp -> {SUCCESS x y / INVALID -1 -1} -> py`
- AI 模式下會有第二次回傳（一次悔棋需同時回退玩家與 AI）。

#### 2.3 超時 (換人)

- `py -> {OVER_TIME} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`
- `cpp -> {PUT_RESULT BOARD_STATE AI_X AI_Y / PUT_RESULT BOARD_STATE -1 -1} -> py`

#### 2.4 儲存

- `py -> {SAVE} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`
- `cpp -> {(棋局 PNG 字串)} -> py`
- Python 端負責將字串寫入檔案（可搭配 PySide6 檔案選取功能）。

#### 2.5 返回主選單

- `py -> {HOME_PAGE} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`

#### 2.6 重置棋盤

- `py -> {RESET} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`

### 3) 結束對局階段

#### 3.1 分享

- `py -> {SHARE} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`

#### 3.2 返回主選單

- `py -> {HOME_PAGE} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`

## Multiplayer (P2P 房號連線)

### 1) 本地雙人

- `py -> {LOCAL_PVP} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`

### 2) 遠端雙人

- `py -> {REMOTE_PVP} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`

## Replay

- `py -> {REVIEW_MODE} -> cpp`
- `cpp -> {SUCCESS / INVALID} -> py`
