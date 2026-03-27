#include "board.h"
// #include "console-ui.h"
#include <iostream>
#include <limits>
using namespace std;

const int boardSize = 15;

int main() {
  Board gameBoard{boardSize};
  int col = 0, row = 0;
  while (true) {
    cin >> col >> row;
    if (cin.fail()) {
      // 將fail or badbit 恢復成 goodbit
      cin.clear();

      // 清空console
      cin.ignore(numeric_limits<streamsize>::max(), '\n');

      cout << "INVALID CONTINUE" << endl;
      continue;
    }

    PutChessResult putChessResultState = gameBoard.putChess(row, col);
    BattleResult boardState = gameBoard.getBattleState();

    // CONSOLE_UI::showBoard(gameBoard);
    cout << putChessResultState << " " << boardState << endl;

    if (boardState != BattleResult::CONTINUE) {
      break;
    }
  }
}
