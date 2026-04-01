#pragma once
#include "state.h"
#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

class Board {
  friend std::ostream &operator<<(std::ostream &os, const Board &board);
private:
  std::vector<std::vector<ChessPiece>> board;
  int size;
  int totalChesses;

  PutChessResult getPutChessResult(const int x, const int y) const;

public:
  Board(int size = 15);

  PutChessResult putChess(const ChessPiece player, const int x, const int y);

  int getHorizontalDistance(const ChessPiece player, const int x,
                            const int y) const;

  int getVerticalDistance(const ChessPiece player, const int x,
                          const int y) const;

  int getLeftDiagonalDistance(const ChessPiece player, const int x,
                              const int y) const;

  int getRightDiagonalDistance(const ChessPiece player, const int x,
                               const int y) const;

  bool isFull() const;

  void reset();

  void takeBack(const int x, const int y);

  bool isXValid(const int x) const;

  bool isYValid(const int y) const;
};
