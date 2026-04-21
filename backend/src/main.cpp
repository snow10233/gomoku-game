#include "console_ui.h"
#include "game_manager.h"
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

const int BOARDSIZE = 15;

// 解析棋譜字串並在 GameManager 上重建 (支援 OT 佔位)。
// 成功回傳 true；遇到格式錯誤或落子失敗回傳 false。
static bool rebuildFromReplay(GameManager &gm, const string &replay) {
  istringstream iss(replay);
  string token;
  while (iss >> token) {
    if (token == "OT") {
      // 只換手、不落子，與遊戲中 OT 雙人語意一致
      gm.overTime(false);
      continue;
    }

    if (token.size() < 2) {
      return false;
    }

    char colChar = token[0];
    if (colChar < 'A' || colChar > 'O') {
      return false;
    }
    int col = colChar - 'A';

    int row = 0;
    try {
      row = stoi(token.substr(1));
    } catch (...) {
      return false;
    }

    if (gm.putChess(col, row) != PutChessResult::SUCCESS) {
      return false;
    }
  }
  return true;
}

static void runAiGameLoop(GameManager &gameManager) {
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

      auto putChessResultState = gameManager.putChess(col, row);

      pair<int, int> aiStep = {-2, -2}; // -2 -2為悔棋代號

      if (putChessResultState == PutChessResult::SUCCESS &&
          gameManager.getBattleState() == BattleResult::CONTINUE) {
        aiStep = gameManager.AiPutChess();
      }

      cout << putChessResultState << " ";
      cout << gameManager.getBattleState() << " ";
      cout << aiStep.first << " ";
      cout << aiStep.second << endl;
    } else if (action == "TAKE_BACK") {
      auto aiDelete = gameManager.takeBack();

      if (aiDelete.first == -1) {
        cout << "INVALID -1 -1" << endl;
        continue;
      }

      cout << "SUCCESS" << " ";
      cout << aiDelete.first << " ";
      cout << aiDelete.second << endl;

      auto playerDelete = gameManager.takeBack();

      if (playerDelete.first == -1) {
        cout << "INVALID -1 -1" << endl;
        continue;
      }

      cout << "SUCCESS" << " ";
      cout << playerDelete.first << " ";
      cout << playerDelete.second << endl;
    } else if (action == "OVER_TIME") {
      auto step = gameManager.overTime(true);

      cout << "SUCCESS" << " ";
      cout << gameManager.getBattleState() << " ";
      cout << step.first << " ";
      cout << step.second << endl;
    } else if (action == "SAVE") {
      cout << "AI_MODE " << endl;
      cout << gameManager.saveData() << endl;
    } else if (action == "HOME_PAGE") {
      gameManager.reset();
      break;
    } else if (action == "RESET") {
      gameManager.reset();
    }
  }
}

static void runTwoPlayerGameLoop(GameManager &gameManager) {
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

      auto putChessResultState = gameManager.putChess(col, row);

      cout << putChessResultState << " ";
      cout << gameManager.getBattleState() << endl;
    } else if (action == "TAKE_BACK") {
      auto playerDelete = gameManager.takeBack();

      if (playerDelete.first == -1) {
        cout << "INVALID -1 -1" << endl;
        continue;
      }

      cout << "SUCCESS" << " ";
      cout << playerDelete.first << " ";
      cout << playerDelete.second << endl;
    } else if (action == "OVER_TIME") {
      gameManager.overTime(false);

      cout << "SUCCESS" << " ";
      cout << gameManager.getBattleState() << endl;
    } else if (action == "SAVE") {
      cout << "TWO_PLAYER_MODE " << endl;
      cout << gameManager.saveData() << endl;
    } else if (action == "HOME_PAGE") {
      gameManager.reset();
      break;
    } else if (action == "RESET") {
      gameManager.reset();
    }
  }
}

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
      GameManager gm{BOARDSIZE};
      runAiGameLoop(gm);
    } else if (gameMode == "TWO_PLAYER_MODE") {
      GameManager gm{BOARDSIZE};
      runTwoPlayerGameLoop(gm);
    } else if (gameMode == "RELOAD_MODE") {
      // 協議 A：先回 SUCCESS，再由前端送「subMode\n棋譜\n」兩行
      string subMode;
      cin >> subMode;

      if (subMode != "AI_MODE" && subMode != "TWO_PLAYER_MODE") {
        cout << "INVALID" << endl;
        continue;
      }

      cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
      string replay;
      getline(cin, replay);

      GameManager gm{BOARDSIZE};
      if (!rebuildFromReplay(gm, replay)) {
        cout << "INVALID" << endl;
        continue;
      }

      cout << "SUCCESS" << endl;

      if (subMode == "AI_MODE") {
        runAiGameLoop(gm);
      } else {
        runTwoPlayerGameLoop(gm);
      }
    } else if (gameMode == "REVIEW_MODE") {
      // 回放由前端自行處理，後端只要確認指令合法即可
      // 前端會直接讀檔並用 stack push/pop 呈現，不需要 cpp 重算棋局
    }
  }
}
