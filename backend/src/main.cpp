#include "board.h"
#include "console-ui.h"
#include <iostream>
using namespace std;

const int boardSize = 15;

int main() {
  Board gameBoard{boardSize};
  string gameMode;
  bool gameContinue = true;
  int col = 0, row = 0;
  while (gameContinue) {
    cin >> gameMode;

    if (!CONSOLE_UI::isGameModeInputValid(gameMode)) {
      cout << "INVALID" << endl;
      continue;
    }
    cout << "SUCCESS" << endl;

    if (gameMode == "AI_MODE") {
      string action;
      while (true) {
        cin >> action;

        if (!CONSOLE_UI::isGameActionInputValid(action)) {
          cout << "INVALID" << endl;
          continue;
        }
        cout << "SUCCESS" << endl;

        if (action == "PUTCHESS") {
          // CONSOLE_UI::showBoard(gameBoard);

          cin >> col >> row;

          if (!CONSOLE_UI::isInputValid()) {
            cout << "INVALID CONTINUE" << endl;
            continue;
          }

          PutChessResult putChessResultState = gameBoard.putChess(row, col);
          BattleResult boardState = gameBoard.getBattleState();

          cout << putChessResultState << " " << boardState << endl;
        } else if (action == "TAKE_BACK") {
          if (!gameBoard.takeBackAMove()) {
            cout << "INVALID" << endl;
            continue;
          }
          cout << "SUCCESS" << endl;
        } else if (action == "SAVE") {
          // 敬請期待
        }
      } 
    } else if (gameMode == "TWO_PLAYER_MODE") {
      // 敬請期待

    } else if (gameMode == "REVIEW_MODE") {
      // 敬請期待

    } else if (gameMode == "RELOAD_MODE") {
      // 敬請期待
    }
  }
}
