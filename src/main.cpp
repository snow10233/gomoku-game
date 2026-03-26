#include "board.h"
#include "ui.h"
#include <iostream>
using namespace std;

const int boardSize = 15;

int main() {
  Board testB1{boardSize};
  int x = 0, y = 0;
  while (UI::everyRoundStartMessage(testB1), cin >> x >> y) {
    PutChessResult result = testB1.putChess(x, y);
    if (result == PutChessResult::ALL_RIGHT_ONE) {
      cout << "無法在該位置下棋，請重新輸入！" << endl; // 重疊到別人
    } else if (result == PutChessResult::OVER_EDGE) {
      cout << "位置無效，請重新輸入！" << endl; // 超出15x15
    }
    UI::pauseConsole();
    UI::clearConsole();
  }
  cout << testB1 << endl;
}
