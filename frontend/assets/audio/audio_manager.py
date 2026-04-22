import os
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices
from PySide6.QtCore import QUrl, QObject, QTimer


class AudioManager(QObject):
    def __init__(self):
        super().__init__()

        self._log_startup_env()

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
        self._wire_player_logging("BGM_P1", self.p1["player"], self.p1["output"])
        self._wire_player_logging("BGM_P2", self.p2["player"], self.p2["output"])
        self._wire_player_logging("SFX", self.sfx_player, self.sfx_output)

    def _log_startup_env(self):
        """啟動期音訊環境快照：env vars + Qt 看到的輸出裝置。"""
        env_keys = ("PULSE_SERVER", "XDG_RUNTIME_DIR", "WAYLAND_DISPLAY", "DISPLAY")
        env_snap = ", ".join(f"{k}={os.environ.get(k) or '<unset>'}" for k in env_keys)
        print(f"[AUDIO_ENV] {env_snap}")

        outputs = QMediaDevices.audioOutputs()
        default = QMediaDevices.defaultAudioOutput()
        print(f"[AUDIO_ENV] Qt audio outputs: {len(outputs)}")
        for d in outputs:
            mark = " (default)" if d.id() == default.id() else ""
            print(f"[AUDIO_ENV]   - {d.description()!r}{mark}")
        if not outputs:
            print("[AUDIO_ENV]   (無輸出裝置，音訊將無聲)")

    def _wire_player_logging(self, tag, player, audio_output):
        """接上播放器/輸出裝置的狀態 signal，方便診斷 WSLg 斷線等問題。"""
        player.mediaStatusChanged.connect(
            lambda s: print(f"[{tag}] mediaStatus: {s.name}")
        )
        player.playbackStateChanged.connect(
            lambda s: print(f"[{tag}] playbackState: {s.name}")
        )
        player.sourceChanged.connect(
            lambda u: print(f"[{tag}] source: {u.toString()}")
        )
        player.errorOccurred.connect(
            lambda e, m: print(f"[{tag}] Error[{e.name}]: {m}")
        )
        audio_output.deviceChanged.connect(
            lambda: print(
                f"[{tag}] device -> {audio_output.device().description()!r}"
            )
        )

    def play_bgm(self, name, fade_ms=2500):
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

    def stop_bgm(self):
        """直接切掉當前 BGM (例如勝負揭曉時讓給勝負音效)"""
        if self.current_bgm_key is None:
            return
        self.active_p["output"].setVolume(0)
        self.active_p["player"].stop()
        self.current_bgm_key = None
        print("🎵 切掉 BGM")

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
        """舊 BGM 直接切掉，新 BGM 漸入"""
        if old_p["player"] != new_p["player"]:
            old_p["output"].setVolume(0)
            old_p["player"].stop()

        steps = 40
        interval = max(10, duration // steps)
        volume_step = 0.5 / steps  # 最終目標音量 0.5

        self.fade_timer = QTimer()
        self.fade_count = 0

        def update_fade():
            self.fade_count += 1
            new_p["output"].setVolume(min(0.5, new_p["output"].volume() + volume_step))
            if self.fade_count >= steps:
                self.fade_timer.stop()

        self.fade_timer.timeout.connect(update_fade)
        self.fade_timer.start(interval)
