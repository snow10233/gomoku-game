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
      GameManager singleGameManager{BOARDSIZE};
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

          auto putChessResultState = singleGameManager.putChess(col, row);

          pair<int, int> aiStep = {-1, -1};

          if (putChessResultState == PutChessResult::SUCCESS && singleGameManager.getBattleState() == BattleResult::CONTINUE) {
            aiStep = singleGameManager.AiPutChess();
          }

          cout << putChessResultState << " ";
          cout << singleGameManager.getBattleState() << " ";
          cout << aiStep.first << " ";
          cout << aiStep.second << endl;
        } else if (action == "TAKE_BACK") {
          auto aiDelete = singleGameManager.takeBack();

          if (aiDelete.first == -1) {
            cout << "INVALID -1 -1" << endl;
            continue;
          }

          cout << "SUCCESS" << " ";
          cout << aiDelete.first << " ";
          cout << aiDelete.second << endl;

          auto playerDelete = singleGameManager.takeBack();

          if (playerDelete.first == -1) {
            cout << "INVALID -1 -1" << endl;
            continue;
          }

          cout << "SUCCESS" << " ";
          cout << playerDelete.first << " ";
          cout << playerDelete.second << endl;
        } else if (action == "OVER_TIME") {
          auto step = singleGameManager.overTime();

          cout << "SUCCESS" << " ";
          cout << singleGameManager.getBattleState() << " ";
          cout << step.first << " ";
          cout << step.second << endl;
        } else if (action == "SAVE") {
          cout << singleGameManager.saveData() << endl;
        } else if (action == "HOME_PAGE") {
          singleGameManager.reset();
          break;
        } else if (action == "RESET") {
          singleGameManager.reset();
        }

        // cout << singleGameManager << endl;
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