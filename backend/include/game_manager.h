#pragma once
#include "ai_player.h"
#include "board.h"
#include "chess.h"
#include "data_saver.h"
#include "distance_calculator.h"

class GameManager {
  friend std::ostream &operator<<(std::ostream &os, const GameManager &game);

private:
  Board gameBoard;
  DataSaver gameDatas;
  AiPlayer aiPlayer;
  ChessPiece currentPlayer;
  BattleResult battleState;
  Chess lastlyChess;
  Distance_calculator distanceCalculator;

  void refreshBattleState();

  void changePlayer();

public:
  GameManager(int size = 15);

  ChessPiece getCurrentPlayer() const;

  BattleResult getBattleState() const;

  std::pair<int, int> overTime(bool isAiMode);

  std::string saveData();

  void reset();

  PutChessResult putChess(const int x, const int y);

  std::pair<int, int> AiPutChess();

  std::pair<int, int> takeBack();
};