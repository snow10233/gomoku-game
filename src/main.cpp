#include "board.h"
#include <iostream>
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

void clearScreen() {
#ifdef _WIN32
  system("cls");
#else
  system("clear");
#endif
}

int main() {
  Board testB1{boardSize};
  int x = 0, y = 0, c;
  while (everyRoundStartMessage(testB1), cin >> x >> y) {
    PutChessResult result = testB1.putChess(x, y);
    if (result == PutChessResult::ALL_RIGHT_ONE) {
      cout << "無法在該位置下棋，請重新輸入！" << endl; // 重疊到別人
    } else if (result == PutChessResult::OVER_EDGE) {
      cout << "位置無效，請重新輸入！" << endl; // 超出15x15
    }

    cout << "Press Enter key to continue..." << endl;
    // cin.clear();
    // c = getchar();
    fgetc(stdin);
    clearScreen();
  }
  cout << testB1 << endl;
}
