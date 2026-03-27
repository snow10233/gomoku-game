#include "board.h"
#include "console-ui.h"
#include <iostream>
using namespace std;

const int boardSize = 15;

int main() {
  Board gameBoard{boardSize};
  int col = 0, row = 0;
  while (true) {
    CONSOLE_UI::showBoard(gameBoard);
    BattleResult boardState = gameBoard.getBattleState();
    if (boardState == BattleResult::CONTINUE) {
      CONSOLE_UI::showWhichPlayer(gameBoard);
      cin >> col >> row;

      if (cin.eof()) {
        return 0;
      }
      PutChessResult result = gameBoard.putChess(row, col);
      if (result == PutChessResult::ALL_RIGHT_ONE) {
        cout << "無法在該位置下棋，請重新輸入！" << endl; // 重疊到別人
      } else if (result == PutChessResult::OVER_EDGE) {
        cout << "位置無效，請重新輸入！" << endl; // 超出15x15
      }
      CONSOLE_UI::pauseConsole();
      CONSOLE_UI::clearConsole();
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
    CONSOLE_UI::pauseConsole();
    return 0;
  }
}
