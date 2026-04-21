import os
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QObject, QTimer


class AudioManager(QObject):
    def __init__(self):
        super().__init__()

        # --- BGM 播放器 (雙播放器架構，用於淡入淡出) ---
        self.p1 = {"player": QMediaPlayer(), "output": QAudioOutput()}
        self.p2 = {"player": QMediaPlayer(), "output": QAudioOutput()}

        for p in [self.p1, self.p2]:
            p["player"].setAudioOutput(p["output"])
            p["output"].setVolume(0)  # 初始靜音，由淡入控制

        self.active_p = self.p1  # 當前主播放器
        self.current_bgm_key = None

        # --- SFX 播放器 (音效專用，獨立於 BGM) ---
        self.sfx_player = QMediaPlayer()
        self.sfx_output = QAudioOutput()
        self.sfx_player.setAudioOutput(self.sfx_output)
        self.sfx_output.setVolume(0.8)  # 音效設定大聲一點

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.songs = {
            "menu": os.path.join(base_dir, "backgroundmusic", "menu.mp3"),
            "play": os.path.join(base_dir, "backgroundmusic", "game.mp3"),
            "victory": os.path.join(base_dir, "soundeffect", "victory.mp3"),
            "defeat": os.path.join(base_dir, "soundeffect", "fail.mp3"),
            "place": os.path.join(base_dir, "soundeffect", "place.wav"),
        }

        print(f"載入選單音樂: {self.songs['menu']}")
        # 錯誤監控
        self.p1["player"].errorOccurred.connect(
            lambda e, m: print(f"BGM_P1 Error: {m}")
        )
        self.p2["player"].errorOccurred.connect(
            lambda e, m: print(f"BGM_P2 Error: {m}")
        )
        self.sfx_player.errorOccurred.connect(lambda e, m: print(f"SFX Error: {m}"))

    def play_bgm(self, name, fade_ms=1000):
        """播放背景音樂 (支援不中斷檢查與淡入淡出)"""
        if name == self.current_bgm_key:
            return  # 如果正在播同一首歌，直接跳過 (這就是選單間不中斷的秘訣)

        path = os.path.abspath(self.songs.get(name, ""))
        if not os.path.exists(path):
            print(f"找不到 BGM 檔案: {path}")
            return

        # 切換到另一個播放器
        next_p = self.p2 if self.active_p == self.p1 else self.p1

        next_p["player"].setSource(QUrl.fromLocalFile(path))
        next_p["player"].setLoops(QMediaPlayer.Loops.Infinite)
        next_p["output"].setVolume(0)  # 新音樂先靜音
        next_p["player"].play()

        # 啟動淡入淡出計時器
        self.start_crossfade(self.active_p, next_p, fade_ms)

        self.active_p = next_p
        self.current_bgm_key = name
        print(f"🎵 開始切換 BGM: {name}")

    def play_sfx(self, name):
        # 播放音效
        path = os.path.abspath(self.songs.get(name, ""))
        if os.path.exists(path):
            self.sfx_player.setSource(QUrl.fromLocalFile(path))
            self.sfx_player.setLoops(0)  # 只播一次
            self.sfx_player.play()
            print(f"播放音效: {name}")
        else:
            print(f"找不到音效檔案: {path}")

    def start_crossfade(self, old_p, new_p, duration):
        """音量淡入淡出邏輯"""
        steps = 20
        interval = max(10, duration // steps)
        volume_step = 0.5 / steps  # 最終目標音量 0.5

        self.fade_timer = QTimer()
        self.fade_count = 0

        def update_fade():
            self.fade_count += 1
            # 舊的淡出
            old_p["output"].setVolume(max(0, old_p["output"].volume() - volume_step))
            # 新的淡入
            new_p["output"].setVolume(min(0.5, new_p["output"].volume() + volume_step))

            if self.fade_count >= steps:
                self.fade_timer.stop()
                if old_p["player"] != new_p["player"]:  # 停止舊的播放
                    old_p["player"].stop()

        self.fade_timer.timeout.connect(update_fade)
        self.fade_timer.start(interval)
