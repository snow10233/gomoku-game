import subprocess


class GomokuEngine:
    def __init__(self, exe_path="../backend/build/gomoku"):
        self.mode = None  # AI_MODE, TWO_PLAYER_MODE, 或 RELOAD_MODE
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
            return False

        print(f"py -> {cmd} -> cpp")
        self.process.stdin.write(f"{cmd}\n")
        self.process.stdin.flush()

        temp = self.process.stdout.readline().strip()
        print(f"cpp -> {temp} -> py")
        return temp == "SUCCESS"

    def ai_mode(self):
        """進入單人 AI 模式"""
        success = self.send_command("AI_MODE")
        if success:
            self.mode = "AI_MODE"
        return success

    def two_player_mode(self):
        """進入本地雙人模式"""
        success = self.send_command("TWO_PLAYER_MODE")
        if success:
            self.mode = "TWO_PLAYER_MODE"
        return success

    def reload_mode(self, sub_mode, board_state):
        """載入舊棋局：依協議 A 送兩行 (子模式 + 棋譜字串)。"""
        if not self.process:
            return False
        if sub_mode not in ("AI_MODE", "TWO_PLAYER_MODE"):
            return False

        if not self.send_command("RELOAD_MODE"):
            return False

        print(f"py -> {sub_mode} -> cpp")
        print(f"py -> {board_state} -> cpp")
        self.process.stdin.write(f"{sub_mode}\n{board_state}\n")
        self.process.stdin.flush()

        resp = self.process.stdout.readline().strip()
        print(f"cpp -> {resp} -> py")
        if resp != "SUCCESS":
            return False

        self.mode = sub_mode
        return True

    def home_page(self):
        """返回主選單"""
        success = self.send_command("HOME_PAGE")
        if success:
            self.mode = None
        return success

    def reset(self):
        """重置棋盤"""
        return self.send_command("RESET")

    def share(self):
        """分享遊戲"""
        return self.send_command("SHARE")

    def put_chess(self, x, y):
        """
        執行下棋的完整通訊流程
        - AI_MODE: 回傳 (success, board_state, ai_x, ai_y)
        - TWO_PLAYER_MODE: 回傳 (success, board_state)
        """
        if not self.process:
            return False, "ERROR", -1, -1

        # 1. 傳送下棋請求
        success = self.send_command("PUT_CHESS")
        if not success:
            return False, "ERROR", -1, -1

        # 2. 傳送玩家座標 (x y)
        print(f"py -> {x} {y} -> cpp")
        self.process.stdin.write(f"{x} {y}\n")
        self.process.stdin.flush()

        # 3. 讀取 C++ 回傳的結果
        response = self.process.stdout.readline().strip().split()

        if self.mode == "AI_MODE":
            # 格式: PUT_RESULT BOARD_STATE AI_X AI_Y 或 PUT_RESULT BOARD_STATE -1 -1
            put_result, board_state, ai_x, ai_y = response
            print(f"cpp -> {put_result} {board_state} {ai_x} {ai_y} -> py")
            return put_result == "SUCCESS", board_state, ai_x, ai_y
        elif self.mode == "TWO_PLAYER_MODE":
            # 格式: PUT_RESULT BOARD_STATE (無 AI 坐標)
            put_result, board_state = response
            print(f"cpp -> {put_result} {board_state} -> py")
            return put_result == "SUCCESS", board_state
        else:
            return False, "ERROR"

    def undo(self):
        """
        執行 TAKE_BACK 流程
        - AI_MODE: 返回兩顆棋 (AI 的最後一步, 玩家的最後一步)
        - TWO_PLAYER_MODE: 返回一顆棋 (上一個玩家的最後一步)
        """
        if not self.process:
            return False, []

        # 1. 傳送指令並讀取第一次確認
        success = self.send_command("TAKE_BACK")
        if not success:
            return False, []  # C++ 拒絕悔棋 (可能是剛開局還沒下)

        undo_positions = []

        if self.mode == "AI_MODE":
            # 2a. AI_MODE: 讀取第一顆要收回的棋子 (AI 的最後一步)
            resp1 = self.process.stdout.readline().strip().split()
            if resp1[0] == "SUCCESS":
                undo_positions.append((int(resp1[1]), int(resp1[2])))
            else:
                return False, []

            # 2b. 讀取第二顆要收回的棋子 (玩家的最後一步)
            resp2 = self.process.stdout.readline().strip().split()
            if resp2[0] == "SUCCESS":
                undo_positions.append((int(resp2[1]), int(resp2[2])))
        elif self.mode == "TWO_PLAYER_MODE":
            # 2. TWO_PLAYER_MODE: 只讀取一顆要收回的棋子
            resp = self.process.stdout.readline().strip().split()
            if resp[0] == "SUCCESS":
                undo_positions.append((int(resp[1]), int(resp[2])))
            else:
                return False, []

        # 回傳 True 代表通訊成功，並附上要清空的座標清單
        return True, undo_positions

    def over_time(self):
        """
        執行 OVER_TIME 流程
        - AI_MODE: 回傳 (success, board_state, ai_x, ai_y)
        - TWO_PLAYER_MODE: 回傳 (success, board_state)
        """
        if not self.process:
            return False, "ERROR", -1, -1

        # 1. 傳送指令並讀取第一次確認
        success = self.send_command("OVER_TIME")
        if not success:
            if self.mode == "AI_MODE":
                return False, "ERROR", -1, -1
            else:
                return False, "ERROR"

        response = self.process.stdout.readline().strip().split()

        if self.mode == "AI_MODE":
            # 格式: PUT_RESULT BOARD_STATE AI_X AI_Y 或 PUT_RESULT BOARD_STATE -1 -1
            put_result, board_state, ai_x, ai_y = response
            print(f"cpp -> {put_result} {board_state} {ai_x} {ai_y} -> py")
            return put_result == "SUCCESS", board_state, int(ai_x), int(ai_y)
        elif self.mode == "TWO_PLAYER_MODE":
            # 格式: PUT_RESULT BOARD_STATE (無 AI 坐標)
            put_result, board_state = response
            print(f"cpp -> {put_result} {board_state} -> py")
            return put_result == "SUCCESS", board_state
        else:
            return False, "ERROR"

    def save(self):
        """
        執行 SAVE 流程：回傳 (success, mode, board_state)。
        後端依序送出 SUCCESS -> 模式行 -> 棋譜行，全都要讀乾淨。
        """
        if not self.process:
            return False, None, None

        success = self.send_command("SAVE")
        if not success:
            return False, None, None

        mode_line = self.process.stdout.readline().strip()
        print(f"cpp -> {mode_line} -> py")

        board_state = self.process.stdout.readline().strip()
        print(f"cpp -> {board_state} -> py")

        return True, mode_line, board_state

    def review_mode(self):
        """進入回放模式"""
        success = self.send_command("REVIEW_MODE")
        if success:
            self.mode = "REVIEW_MODE"
        return success

    def close(self):
        """關閉遊戲時，把 C++ 行程也殺掉"""
        if self.process:
            self.process.terminate()
