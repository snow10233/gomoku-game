#pragma once
#include "position.h"
#include <iostream>
#include <vector>

enum class Chess { EMPTY, BLACK, WHITE };

std::ostream &operator<<(std::ostream &os, const Chess &c);

using dualChessVector = std::vector<std::vector<Chess>>;

class Board {
  friend std::ostream &operator<<(std::ostream &os, const Board &board);

private:
  dualChessVector board;
  Position black, white;
  int sizeLimit;
  Chess whoPlay;

public:
  Board(const int &size = 15) : sizeLimit(size) {
    whoPlay = Chess::BLACK;
    black.setXLimit(-size, size);
    black.setYLimit(-size, size);
    white.setXLimit(-size, size);
    white.setYLimit(-size, size);
    for (int i = 0; i < size; i++) {
      board.push_back(std::vector<Chess>{});
      for (int j = 0; j < size; ++j) {
        board[i].push_back(Chess::EMPTY);
      }
    }
  }

  Chess isWhoPlayNow() const;

  bool putChess(const int &xPos, const int &yPos);

  void resetBoard();

  bool isChessPositionVaild() const;
};
