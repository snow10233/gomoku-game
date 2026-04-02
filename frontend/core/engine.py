import subprocess


class GomokuEngine:
    def __init__(self, exe_path="../backend/build/gomoku"):
        try:
            # 啟動 C++ 子行程
            self.process = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered，確保不卡 buffer
            )
            print("✅ C++ 引擎連線成功！")
        except FileNotFoundError:
            print(f"❌ 找不到 C++ 引擎執行檔：{exe_path}")
            self.process = None

    def send_command(self, cmd):
        """傳送單一指令 (如 AI_MODE, HOME_PAGE) 並讀取 SUCCESS/INVALID"""
        if not self.process:
            return "INVALID"

        self.process.stdin.write(f"{cmd}\n")
        self.process.stdin.flush()

        temp = self.process.stdout.readline().strip()
        print(f"c++ say:{temp}")
        return temp

    def put_chess(self, x, y):
        """執行下棋的完整通訊流程"""
        if not self.process:
            return "INVALID", "ERROR", -1, -1

        # 1. 傳送下棋請求
        status = self.send_command("PUT_CHESS")
        if status != "SUCCESS":
            return "INVALID", "ERROR", -1, -1

        # 2. 傳送玩家座標 (x y)
        self.process.stdin.write(f"{x} {y}\n")
        self.process.stdin.flush()

        # 3. 讀取 C++ 回傳的結果
        # 預期格式: {PUT_RESULT BOARD_STATE AI's_x AI's_y} 或 {INVALID CONTINUE -1 -1}
        
        temp = self.process.stdout.readline().strip()
        print(f"c++ say:{temp}")
        response = temp.split()

        if len(response) >= 4:
            put_result = response[0]  # SUCCESS 或 INVALID
            board_state = response[1]  # CONTINUE, WIN_BLACK, WIN_WHITE, DRAW
            ai_x = int(response[2])
            ai_y = int(response[3])
            return put_result, board_state, ai_x, ai_y

        return "INVALID", "CONTINUE", -1, -1

    def undo(self):
        """
        執行文件定義的 TAKE_BACK 流程：
        py -> {TAKE_BACK}
        cpp -> {SUCCESS / INVALID}
        cpp -> {SUCCESS x y / INVALID -1 -1} (第一顆)
        cpp -> {SUCCESS x y / INVALID -1 -1} (第二顆 AI模式限定)
        """
        if not self.process:
            return False, []

        # 1. 傳送指令並讀取第一次確認
        status = self.send_command("TAKE_BACK")
        if status != "SUCCESS":
            return False, []  # C++ 拒絕悔棋 (可能是剛開局還沒下)

        undo_positions = []

        # 2. 讀取第一顆要收回的棋子 (通常是 AI 的最後一步)
        resp1 = self.process.stdout.readline().strip().split()
        if resp1[0] == "SUCCESS":
            undo_positions.append((int(resp1[1]), int(resp1[2])))
        else:
            return False, []

        # 3. 讀取第二顆要收回的棋子 (玩家的最後一步)
        resp2 = self.process.stdout.readline().strip().split()
        if resp2[0] == "SUCCESS":
            undo_positions.append((int(resp2[1]), int(resp2[2])))

        # 回傳 True 代表通訊成功，並附上要清空的座標清單
        return True, undo_positions

    def over_time(self):
        if not self.process:
            return False, []

        # 1. 傳送指令並讀取第一次確認
        status = self.send_command("OVER_TIME")
        if status != "SUCCESS":
            return "INVALID", "CONTINUE", -1, -1

        response = self.process.stdout.readline().strip().split()

        put_result = response[0]  # SUCCESS 或 INVALID
        board_state = response[1]  # CONTINUE, WIN_BLACK, WIN_WHITE, DRAW
        ai_x = int(response[2])
        ai_y = int(response[3])
        return put_result, board_state, ai_x, ai_y

    def close(self):
        """關閉遊戲時，把 C++ 行程也殺掉"""
        if self.process:
            self.process.terminate()
