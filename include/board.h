#pragma once
#include "chess.h"
#include <iostream>
#include <vector>
#include <iomanip>

enum class ChessPiece { EMPTY, BLACK, WHITE };

enum class PutChessResult { SUCCESS, OVER_EDGE, ALL_RIGHT_ONE};

std::ostream &operator<<(std::ostream &os, const ChessPiece &c);

using dualChessPieceVector = std::vector<std::vector<ChessPiece>>;

class Board {
  friend std::ostream &operator<<(std::ostream &os, const Board &board);

private:
  dualChessPieceVector board;
  Chess lastlyChess;
  int sizeLimit;
  ChessPiece whoPlay;

public:
  Board(const int &size = 15) : sizeLimit(size) {
    whoPlay = ChessPiece::BLACK;
    lastlyChess.setXLimit(0, size - 1);
    lastlyChess.setYLimit(0, size - 1);
    for (int i = 0; i < size; i++) {
      board.push_back(std::vector<ChessPiece>{});
      for (int j = 0; j < size; ++j) {
        board[i].push_back(ChessPiece::EMPTY);
      }
    }
  }

  ChessPiece isWhoPlayNow() const;

  PutChessResult putChess(const int &xPosition, const int &yPosition);

  void resetBoard();

  PutChessResult isChessPositionVaild(const int &xPosition, const int &yPosition) const;
};
