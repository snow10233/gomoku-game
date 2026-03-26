#pragma once
#include "chess.h"
#include <iomanip>
#include <iostream>
#include <vector>

enum class ChessPiece { EMPTY, BLACK, WHITE };

enum class PutChessResult { SUCCESS, OVER_EDGE, ALL_RIGHT_ONE };

enum class BattleResult { BLACK_WIN, WHITE_WIN, DRAW, CONTINUE };

std::ostream &operator<<(std::ostream &os, const ChessPiece &c);

using dualChessPieceVector = std::vector<std::vector<ChessPiece>>;
class Board {
  friend std::ostream &operator<<(std::ostream &os, const Board &board);
  friend int getHorizaonlDistance(const Board &b1);
  friend int getVerticalDistance(const Board &b1);
  friend int getLeftDiagonalDistance(const Board &b1);
  friend int getRightDiagonalDistance(const Board &b1);

private:
  dualChessPieceVector board;
  Chess lastlyChess;
  int sizeLimit;
  ChessPiece whoPlay;
  int totalChesses;
  BattleResult battleState;

  BattleResult calculateBattleState() const;

public:
  Board(int size = 15);

  ChessPiece isWhoPlayNow() const;

  PutChessResult putChess(const int &xPosition, const int &yPosition);

  void resetBoard();

  PutChessResult isChessPositionValid(const int &xPosition,
                                      const int &yPosition) const;

  BattleResult getBattleState() const;
};
