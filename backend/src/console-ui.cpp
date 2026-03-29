#include "console-ui.h"

void CONSOLE_UI::showBoard(const Board &board) {
  std::cout << board << std::endl;
}

void CONSOLE_UI::showWhichPlayer(const Board &board) {
  if (board.isWhoPlayNow() == ChessPiece::BLACK) {
    std::cout << "目前執棋: 黑子(●)" << std::endl;
  } else {
    std::cout << "目前執棋: 白子(○)" << std::endl;
  }
  std::cout << "請輸入位置 (行 列): ";
}

void CONSOLE_UI::clearConsole() {
#ifdef _WIN32
  system("cls");
#else
  system("clear");
#endif
}

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

bool CONSOLE_UI::isGameModeInputValid(std::string &gameMode) {
  if (!isInputValid()) {
    return false;
  }
  return gameMode == "AI_MODE" || gameMode == "TWO_PLAYER_MODE" ||
         gameMode == "REVIEW_MODE" || gameMode == "RELOAD_MODE";
}

bool CONSOLE_UI::isGameActionInputValid(std::string &action) {
  if (!isInputValid()) {
    return false;
  }
  return action == "PUT_CHESS" || action == "TAKE_BACK" || action == "SAVE" ||
         action == "OVER_TIME";
}