#pragma once
#include "chess.h"
#include "data-saver.h"
#include "state.h"
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

using dualChessPieceVector = std::vector<std::vector<ChessPiece>>;
using AICalculatePair = std::pair<std::pair<int, int>, int>;

class Board {
  friend std::ostream &operator<<(std::ostream &os, const Board &board);
  friend int getHorizontalDistance(const Board &b1);
  friend int getVerticalDistance(const Board &b1);
  friend int getLeftDiagonalDistance(const Board &b1);
  friend int getRightDiagonalDistance(const Board &b1);

private:
  dualChessPieceVector board;
  Chess lastlyChess;
  DataSaver boardData;
  ChessPiece whoPlay;
  BattleResult battleState;
  int sizeLimit;
  int totalChesses;

  BattleResult calculateBattleState() const;

  void changePlayer();

  PutChessResult isChessPositionValid(const int x, const int y) const;

public:
  Board(int size = 15);

  ChessPiece isWhoPlayNow() const;

  BattleResult getBattleState() const;

  PutChessResult putChess(const int x, const int y);

  void resetBoard();

  void overTimeProcess();

  std::pair<int, int> takeBackAMove();

  std::pair<int, int> aiFindBestPos();
};
