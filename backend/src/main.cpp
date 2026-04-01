#include "console_ui.h"
#include "game_manager.h"
#include <iostream>
using namespace std;

const int BOARDSIZE = 15;

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
      GameManager singalGameManager{BOARDSIZE};
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

          auto putChessResultState = singalGameManager.putChess(col, row);

          pair<int, int> step = {-1, -1};

          if (putChessResultState == PutChessResult::SUCCESS) {
            step = singalGameManager.AiPutChess();
          }

          cout << putChessResultState << " ";
          cout << singalGameManager.getBattleState() << " ";
          cout << step.first << " ";
          cout << step.second << endl;
        } else if (action == "TAKE_BACK") {
          auto aiDelete = singalGameManager.takeBack();

          if (aiDelete.first == -1) {
            cout << "INVALID -1 -1" << endl;
            continue;
          }

          cout << "SUCCESS" << " ";
          cout << aiDelete.first << " ";
          cout << aiDelete.second << endl;

          auto playerDelete = singalGameManager.takeBack();

          if (playerDelete.first == -1) {
            cout << "INVALID -1 -1" << endl;
            continue;
          }

          cout << "SUCCESS" << " ";
          cout << playerDelete.first << " ";
          cout << playerDelete.second << endl;
        } else if (action == "OVER_TIME") {
          auto step = singalGameManager.overTime();

          cout << "SUCCESS" << " ";
          cout << singalGameManager.getBattleState() << " ";
          cout << step.first << " ";
          cout << step.second << endl;
        } else if (action == "SAVE") {
          cout << singalGameManager.saveData() << endl;
        } else if (action == "HOME_PAGE") {
          break;
        } else if (action == "RESET") {
          singalGameManager.reset();
        }

        // cout << singalGameManager << endl;
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