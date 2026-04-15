# Development Workflow

## Local Test Flow

1. 啟用虛擬環境：
   - `source .venv/bin/activate`
2. 建置後端：
   - 進入 `backend/build`
   - 執行 `make`
3. 啟動前端：
   - 進入 `frontend`
   - 執行 `python3 main.py`

## Notes

- 建議所有 Python 套件安裝都在 `.venv` 下進行，避免污染系統環境。
- 協議細節與命令格式請參考 `docs/protocol.md`。
