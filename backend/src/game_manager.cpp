#include "game_manager.h"

std::ostream &operator<<(std::ostream &os, const GameManager &game) {
  os << game.gameBoard;
  return os;
}

void GameManager::refreshBattleState() {
  int x = lastlyChess.x;
  int y = lastlyChess.y;
  if (distanceCalculator.getlongestDistance(gameBoard, currentPlayer, x, y) >=
      5) {
    if (currentPlayer == ChessPiece::BLACK) {
      battleState = BattleResult::BLACK_WIN;
    } else if (currentPlayer == ChessPiece::WHITE) {
      battleState = BattleResult::WHITE_WIN;
    }
  } else if (gameBoard.isFull()) {
    battleState = BattleResult::DRAW;
  } else {
    battleState = BattleResult::CONTINUE;
  }
}

void GameManager::changePlayer() {
  if (currentPlayer == ChessPiece::BLACK) {
    currentPlayer = ChessPiece::WHITE;
  } else {
    currentPlayer = ChessPiece::BLACK;
  }
}

GameManager::GameManager(int size) : gameBoard(size) {
  battleState = BattleResult::CONTINUE;
  currentPlayer = ChessPiece::BLACK;
  lastlyChess = {-1, -1};
}

ChessPiece GameManager::getCurrentPlayer() const { return currentPlayer; }

BattleResult GameManager::getBattleState() const { return battleState; }

std::pair<int, int> GameManager::overTime(bool isAiMode) {
  // 將-2 -2寫入data做為佔位使用 後續進行存檔才不會亂
  gameDatas.addData(-2, -2);
  changePlayer();

  if(isAiMode) {
    return AiPutChess();
  }

  // 不重要的回傳值 因為前端不會使用到
  return {-1, -1};
}

std::pair<int, int> GameManager::takeBack() {
  auto dataTemp = gameDatas.takeBack();

  if (dataTemp.first == -1) {
    return dataTemp;
  }

  gameBoard.takeBack(lastlyChess.x, lastlyChess.y);
  lastlyChess.x = gameDatas.getTop().first;
  lastlyChess.y = gameDatas.getTop().second;
  changePlayer();

  return dataTemp;
}

std::string GameManager::saveData() {
  std::string temp;
  temp << gameDatas;
  return temp;
}

void GameManager::reset() {
  gameBoard.reset();
  gameDatas.reset();
  battleState = BattleResult::CONTINUE;
  currentPlayer = ChessPiece::BLACK;
  lastlyChess = {-1, -1};
}

PutChessResult GameManager::putChess(const int x, const int y) {
  PutChessResult result = gameBoard.putChess(currentPlayer, x, y);

  if (result == PutChessResult::SUCCESS) {
    lastlyChess = {x, y};
    gameDatas.addData(x, y);
    refreshBattleState();
    changePlayer();
  }

  return result;
}

std::pair<int, int> GameManager::AiPutChess() {
  if (battleState != BattleResult::CONTINUE) {
    return {-1, -1};
  }

  auto step = aiPlayer.findBestPos(currentPlayer, gameBoard);

  putChess(step.first, step.second);

  return step;
}