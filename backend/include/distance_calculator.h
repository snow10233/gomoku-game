#pragma once
#include "board.h"
#include <algorithm>

class Distance_calculator {
public:
  int getHorizontalDistance(const Board &gameBoard, const ChessPiece player,
                            const int x, const int y) const;

  int getVerticalDistance(const Board &gameBoard, const ChessPiece player,
                          const int x, const int y) const;

  int getLeftDiagonalDistance(const Board &gameBoard, const ChessPiece player,
                              const int x, const int y) const;

  int getRightDiagonalDistance(const Board &gameBoard, const ChessPiece player,
                               const int x, const int y) const;

  int getlongestDistance(const Board &gameBoard, const ChessPiece player,
                         const int x, const int y) const;
};