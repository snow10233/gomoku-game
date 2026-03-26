#include "board.h"
#include "ui.h"
#include <iostream>
using namespace std;

const int boardSize = 15;

int main() {
  Board testB1{boardSize};
  int col = 0, row = 0;
  while (true) {
    UI::showBoard(testB1);
    BattleResult boardState = testB1.getBattleState();
    if (boardState == BattleResult::CONTINUE) {
      UI::showWhichPlayer(testB1);
      cin >> col >> row;

      if (cin.eof()) {
        return 0;
      }
      PutChessResult result = testB1.putChess(row, col);
      if (result == PutChessResult::ALL_RIGHT_ONE) {
        cout << "無法在該位置下棋，請重新輸入！" << endl; // 重疊到別人
      } else if (result == PutChessResult::OVER_EDGE) {
        cout << "位置無效，請重新輸入！" << endl; // 超出15x15
      }
      UI::pauseConsole();
      UI::clearConsole();
      continue;
    } else if (boardState == BattleResult::BLACK_WIN) {
      cout << "黑子(●)獲勝！" << endl;
      cout << "遊戲結束！" << endl;
    } else if (boardState == BattleResult::WHITE_WIN) {
      cout << "白子(○)獲勝！" << endl;
      cout << "遊戲結束！" << endl;
    } else {
      cout << "平手" << endl;
      cout << "遊戲結束！" << endl;
    }
    UI::pauseConsole();
    return 0;
  }
}
