#include "console_ui.h"

/**
 * @brief 顯示目前輪到哪位玩家（黑子或白子）
 * 
 * @param gameManager 遊戲管理器實例，用於獲取當前玩家狀態
 */
void CONSOLE_UI::showWhichPlayer(const GameManager &gameManager) {
  if (gameManager.getCurrentPlayer() == ChessPiece::BLACK) {
    std::cout << "目前執棋: 黑子(●)" << std::endl;
  } else {
    std::cout << "目前執棋: 白子(○)" << std::endl;
  }
  std::cout << "請輸入位置 (行 列): ";
}

/**
 * @brief 清空終端機/控制台畫面
 * 
 * 根據編譯的作業系統自動選擇對應的指令 (Windows 使用 cls，類 Unix 使用 clear)。
 */
void CONSOLE_UI::clearConsole() {
#ifdef _WIN32
  system("cls");
#else
  system("clear");
#endif
}

/**
 * @brief 暫停畫面並等待玩家按下 Enter 鍵
 * 
 * 為了避免先前的輸入殘留導致直接跳過，此函式會先清除 cin 狀態與緩衝區。
 */
void CONSOLE_UI::pauseConsole() {
  std::cout << "Press Enter key to continue...";

  // 1. 清空狀態 (預防前面的 cin 發生錯誤被鎖死)
  std::cin.clear();

  // 2. 把緩衝區裡面的殘留物（包含 \n）全部清空
  // 這行的意思是：忽略接下來的所有字元，直到遇到 \n 為止
  std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

  // 3. 真正等待玩家按下 Enter
  std::cin.get();
}

/**
 * @brief 檢查標準輸入 (std::cin) 的狀態是否有效
 * 
 * 若 cin 發生錯誤 (例如輸入型態不符)，會重置狀態並清空緩衝區。
 * 
 * @return true 輸入狀態正常
 * @return false 輸入發生錯誤 (已進行復原與清空)
 */
bool CONSOLE_UI::isInputValid() {
  if (std::cin.fail()) {
    // 將fail or badbit 恢復成 goodbit
    std::cin.clear();

    // 清空console
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    return false;
  }
  return true;
}

/**
 * @brief 檢查輸入的遊戲模式指令是否合法
 * 
 * @param gameMode 從終端機讀入的遊戲模式字串
 * @return true 字串為合法的遊戲模式指令
 * @return false 字串非法或讀取失敗
 */
bool CONSOLE_UI::isGameModeInputValid(std::string &gameMode) {
  if (!isInputValid()) {
    return false;
  }
  return gameMode == "AI_MODE" || gameMode == "TWO_PLAYER_MODE" ||
         gameMode == "REVIEW_MODE" || gameMode == "RELOAD_MODE";
}

/**
 * @brief 檢查輸入的遊戲操作指令是否合法
 * 
 * @param action 從終端機讀入的操作指令字串
 * @return true 字串為合法的操作指令
 * @return false 字串非法或讀取失敗
 */
bool CONSOLE_UI::isGameActionInputValid(std::string &action) {
  if (!isInputValid()) {
    return false;
  }
  return action == "PUT_CHESS" || action == "TAKE_BACK" || action == "SAVE" ||
         action == "OVER_TIME" || action == "HOME_PAGE" || action == "RESET";
}