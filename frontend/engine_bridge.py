import subprocess

class GomokuEngine:
    def __init__(self, executable_path="../backend/build/gomoku"):
        # 在背景啟動你的 C++ 引擎
        self.process = subprocess.Popen(
            [executable_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True, # 自動處理字串編碼
            bufsize=1  # 行緩衝模式 (非常重要，避免 C++ 的輸出卡在管線裡)
        )

    def put_chess(self, col, row):
        """傳送座標給 C++ 引擎，並回傳結果"""
        # 1. 把座標傳給 C++ (記得加換行符號)
        self.process.stdin.write(f"{col} {row}\n")
        self.process.stdin.flush()

        # 2. 讀取 C++ 算完後吐出來的一行結果
        output = self.process.stdout.readline().strip()
        
        # 3. 把字串切開，回傳給隊友的 GUI 使用
        result, state = output.split(" ")
        return result, state

    def close(self):
        """關閉引擎"""
        self.process.terminate()