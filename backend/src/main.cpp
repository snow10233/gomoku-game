#include "board.h"
#include "console-ui.h"
#include <iostream>
using namespace std;

const int boardSize = 15;

int main() {
  Board gameBoard{boardSize};
  string gameMode;
  bool gameContinue = true;
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

        if (action == "PUT_CHESS") {
          int col = 0, row = 0;
          cin >> col >> row;

          if (!CONSOLE_UI::isInputValid()) {
            cout << "INVALID CONTINUE" << endl;
            continue;
          }

          PutChessResult putChessResultState = gameBoard.putChess(col, row);

          BattleResult boardState = gameBoard.getBattleState();
          pair<int, int> AIPos{-1, -1};
          if (boardState == BattleResult::CONTINUE && putChessResultState == PutChessResult::SUCCESS) {
            AIPos = gameBoard.AIPutChess();
            gameBoard.putChess(AIPos.first, AIPos.second);
            boardState = gameBoard.getBattleState();
          }

          // CONSOLE_UI::showBoard(gameBoard);

          cout << putChessResultState << " ";
          cout << boardState << " ";
          cout << AIPos.first << " ";
          cout << AIPos.second << endl;

        } else if (action == "TAKE_BACK") {
          int deleteX = 0, deleteY = 0;
          if (!gameBoard.takeBackAMove(deleteY, deleteX)) {
            cout << "INVALID -1 -1" << endl;
            continue;
          }
          cout << "SUCCESS" << " " << deleteY << " " << deleteX << endl;
        } else if (action == "SAVE") {
          // 敬請期待
        } else if (action == "OVER_TIME") {
          gameBoard.overTimeProcess();
          cout << "SUCCESS" << endl;
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
