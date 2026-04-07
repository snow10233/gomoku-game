# 五子棋 project

### 功能進度表
~~顯示 15×15 之標準棋盤~~

~~黑子 (先行)與白子兩邊輪流下棋於點上~~

~~能判斷結束並顯示贏家~~

盤面、按鈕、輪到誰等資訊清楚易讀

棋子顏色、外觀顯示美觀

操作過程不卡頓，下棋時有視覺反饋且流暢

有明確的操作提示與贏家提示，誤操作有反饋

支援悔棋功能，需可開關

支援落子限時功能，需可開關

支援儲存/載入棋局

支援回放系統、結果分享等進階功能

---
### 環境配置

#### C++
> 確保已安裝cmake WSL也要
1. 在當前目錄下建立build資料夾
2. 進入build後 在command 打 `make`
3. 等待gomoku檔案出現後 執行 `./gomoku`

#### python
> 使用venv避免汙染全局環境
1. 確定WSL已安裝venv
2. command : `python3 -m venv .venv` + `source .venv/bin/activate`
3. 確定command最左邊出現 (.venv)
5. command : `pip install -r requirement.txt`

---
### 功能測試流程
1. 輸入 `source .venv/bin/activate` 進入.venv
2. 進入 `backend/build` 輸入 `make`
3. 進入 `frontend` 輸入 `python3 main.py`

---
## 溝通格式

- 涵義說明
	- {傳送內容} : 溝通固定內容
	- {A / B} : 成功輸出A 失敗輸出B
	- 由上而下依序通訊
	- 多個資料用一個空格隔開

- 流程指令說明
    1. 單人 (AI)        
        1. 開啟新遊戲
            - py -> {AI_MODE} -> cpp
            - cpp -> {SUCCESS / INVALID} -> py
        2. 載入舊棋局
            - py -> {RELOAD_MODE} -> cpp
            - cpp -> {SUCCESS / INVALID} -> py

            1. 下棋 (相互通訊x, y) 
                - py ->{PUT_CHESS} -> cpp
                - cpp -> {SUCCESS / INVALID} -> py
                - py -> {x y} -> cpp
                - cpp -> {PUT_RESULT BOARD_STATE AI's x AI's y / PUT_RESULT BOARD_STATE -1 -1} -> py
            2. 悔棋 (可以無限悔棋)
                - py -> {TAKE_BACK} -> cpp
                - cpp -> {SUCCESS / INVALID} -> py 
                - cpp -> {SUCCESS x y/ INVALID -1 -1} -> py (悔棋將返回悔的那一顆棋的x, y 前端直接根據這個調整畫面)
                - cpp -> {SUCCESS x y/ INVALID -1 -1} -> py (限AI模式會有第二次 悔棋一次就要把AI跟自己的都悔回去)
            3. 超時 (換人下)
                - py -> {OVER_TIME} -> cpp
                - cpp -> {SUCCESS / INVALID} -> py
                - cpp -> {PUT_RESULT BOARD_STATE AI's x AI's y / PUT_RESULT CONTBOARD_STATEINUE -1 -1} -> py
            4. 儲存
                - py -> {SAVE} -> cpp
                - cpp -> {SUCCESS / INVALID} -> py
                - cpp -> {(棋局PNG字串)} -> py 
                - python負責把處理好的字串寫進檔案當中 *配合pySide6的檔案選取功能*
            5. 返回主選單
                - py -> {HOME_PAGE} -> cpp
                - cpp -> {SUCCESS / INVALID} -> py
            6. 重置棋盤
                - py -> {RESET} -> cpp
                - cpp -> {SUCCESS / INVALID} -> py
                
                1. 分享
                    - py -> {SHARE} -> cpp
                    - cpp -> {SUCCESS / INVALID} -> py
                2. 返回主選單
                    - py -> {HOME_PAGE} -> cpp
                    - cpp -> {SUCCESS / INVALID} -> py

    2. 雙人 (房號P2P連線)
        - py -> {TWO_PLAYER_MODE} -> cpp
        - cpp -> {SUCCESS / INVALID} -> py
        
    3. 回放 (選擇檔案) 
        - py -> {REVIEW_MODE} -> cpp
        - cpp -> {SUCCESS / INVALID} -> py

## PNG定義 (OT代表OVER_TIME)
    - ex. A0 C5 G3 OT A4 N11
        A B C D E F G H I J K L M N O
    00
    01
    02
    03
    04
    05
    06
    07
    08
    09
    10
    11
    12
    13
    14

## notes
	- linux pyside6 中文 `sudo apt update && sudo apt install fonts-noto-cjk -y`
	- (未來) 離開不要關閉棋局 保存下次進來繼續玩
