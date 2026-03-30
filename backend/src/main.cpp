#include "board.h"
#include "console-ui.h"
#include <iostream>
using namespace std;

const int boardSize = 15;

int main() {
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
      Board gameBoard{boardSize};
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
          pair<int, int> aiPos{-1, -1};

          if (boardState == BattleResult::CONTINUE &&
              putChessResultState == PutChessResult::SUCCESS) {
            aiPos = gameBoard.aiFindBestPos();
            gameBoard.putChess(aiPos.first, aiPos.second);
            boardState = gameBoard.getBattleState();
          }

          cout << putChessResultState << " ";
          cout << boardState << " ";
          cout << aiPos.first << " ";
          cout << aiPos.second << endl;

          // CONSOLE_UI::showBoard(gameBoard);
        } else if (action == "TAKE_BACK") {
          pair<int, int> aiDelete = gameBoard.takeBackAMove();

          if (aiDelete.first == -1) {
            cout << "INVALID -1 -1" << endl;
            continue;
          }

          cout << "SUCCESS" << " ";
          cout << aiDelete.first << " ";
          cout << aiDelete.second << endl;

          pair<int, int> playerDelete = gameBoard.takeBackAMove();

          if (playerDelete.first == -1) {
            cout << "INVALID -1 -1" << endl;
            continue;
          }

          cout << "SUCCESS" << " ";
          cout << playerDelete.first << " ";
          cout << playerDelete.second << endl;

          // CONSOLE_UI::showBoard(gameBoard);
        } else if (action == "OVER_TIME") {
          gameBoard.overTimeProcess();

          pair<int, int> aiPos = gameBoard.aiFindBestPos();
          PutChessResult putChessResultState =
              gameBoard.putChess(aiPos.first, aiPos.second);

          BattleResult boardState = gameBoard.getBattleState();

          cout << putChessResultState << " ";
          cout << boardState << " ";
          cout << aiPos.first << " ";
          cout << aiPos.second << endl;
        } else if (action == "SAVE") {
          // 敬請期待
        } else if (action == "HOME_PAGE") {
          break;
        } else if (action == "RESET") {
          gameBoard.resetBoard();
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
