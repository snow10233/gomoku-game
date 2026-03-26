#include "ui.h"

void UI::showBoard(const Board &board) {
  std::cout << board << std::endl;
}

void UI::showWhichPlayer(const Board& board) {
  if (board.isWhoPlayNow() == ChessPiece::BLACK) {
    std::cout << "目前執棋: 黑子(●)" << std::endl;
  } else {
    std::cout << "目前執棋: 白子(○)" << std::endl;
  }
  std::cout << "請輸入位置 (行 列): ";
}

void UI::clearConsole() {
#ifdef _WIN32
  system("cls");
#else
  system("clear");
#endif
}

void UI::pauseConsole() {
  std::cout << "Press Enter key to continue...";

  // 1. 清空狀態 (預防前面的 cin 發生錯誤被鎖死)
  std::cin.clear();

  // 2. 把緩衝區裡面的殘留物（包含 \n）全部清空
  // 這行的意思是：忽略接下來的所有字元，直到遇到 \n 為止
  std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

  // 3. 真正等待玩家按下 Enter
  std::cin.get();
}