#pragma once
#include "board.h"
#include "distance_calculator.h"
#include <cmath>

using AICalculatePair = std::pair<std::pair<int, int>, int>;

class AiPlayer {
private:
  Distance_calculator distanceCalculator;

  int getThisPosScore(const ChessPiece player, const Board &gameBoard,
                      const int x, const int y) const;

public:
  std::pair<int, int> findBestPos(const ChessPiece player,
                                  Board &gameBoard) const;
};