#pragma once
#include "chess.h"
#include "data-saver.h"
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

enum class ChessPiece { EMPTY, BLACK, WHITE };

enum class PutChessResult { SUCCESS, OUT_BOUNDS, OVERLAPPING };

enum class BattleResult { BLACK_WIN, WHITE_WIN, DRAW, CONTINUE };

std::ostream &operator<<(std::ostream &os, const ChessPiece &c);

std::ostream &operator<<(std::ostream &os, const PutChessResult &p);

std::ostream &operator<<(std::ostream &os, const BattleResult &b);

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
  int sizeLimit;
  ChessPiece whoPlay;
  int totalChesses;
  BattleResult battleState;

  BattleResult calculateBattleState() const;

  void changePlayer();

  PutChessResult isChessPositionValid(const int x, const int y) const;

public:
  Board(int size = 15);

  ChessPiece isWhoPlayNow() const;

  PutChessResult putChess(const int x, const int y);

  void resetBoard();

  BattleResult getBattleState() const;

  bool takeBackAMove(int &x, int &y);

  void overTimeProcess();

  std::pair<int, int> AIPutChess();
};
