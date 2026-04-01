#pragma once
#include "board.h"
#include <cmath>

using AICalculatePair = std::pair<std::pair<int, int>, int>;

class AiPlayer {
private:
  int getThisPosScore(const ChessPiece player, const Board &gameBoard,
                      const int x, const int y) const;

public:
  std::pair<int, int> aiFindBestPos(const ChessPiece player, Board &gameBoard,
                                    const int x, const int y) const;
};