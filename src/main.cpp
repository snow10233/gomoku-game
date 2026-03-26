#include "board.h"
#include <iostream>
#include <limits> // 需要引入這個才能使用 numeric_limits
using namespace std;

const int boardSize = 15;

void everyRoundStartMessage(const Board &b) {
  cout << b << endl;
  string chessInfo = "";
  if (b.isWhoPlayNow() == ChessPiece::BLACK) {
    chessInfo = "黑子(●)";
  } else {
    chessInfo = "白子(○)";
  }
  cout << "目前執棋: " << chessInfo << endl;
  cout << "請輸入位置 (行 列): ";
}

void clearConsole() {
#ifdef _WIN32
  system("cls");
#else
  system("clear");
#endif
}

void pauseConsole() {
    cout << "Press Enter key to continue...";
    
    // 1. 清空狀態 (預防前面的 cin 發生錯誤被鎖死)
    cin.clear(); 
    
    // 2. 把緩衝區裡面的殘留物（包含 \n）全部清空
    // 這行的意思是：忽略接下來的所有字元，直到遇到 \n 為止
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    
    // 3. 真正等待玩家按下 Enter
    cin.get();
}

int main() {
  Board testB1{boardSize};
  int x = 0, y = 0;
  while (everyRoundStartMessage(testB1), cin >> x >> y) {
    PutChessResult result = testB1.putChess(x, y);
    if (result == PutChessResult::ALL_RIGHT_ONE) {
      cout << "無法在該位置下棋，請重新輸入！" << endl; // 重疊到別人
    } else if (result == PutChessResult::OVER_EDGE) {
      cout << "位置無效，請重新輸入！" << endl; // 超出15x15
    }
    pauseConsole();
    clearConsole();
  }
  cout << testB1 << endl;
}
