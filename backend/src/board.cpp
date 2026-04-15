#include "board.h"

std::ostream &operator<<(std::ostream &os, const Board &b) {
  os << "   ";
  for (int y = 0; y < b.board[0].size(); ++y) {
    os << std::setw(2) << y << " ";
  }
  os << std::endl;
  for (int y = 0; y < b.size; ++y) {
    os << std::setw(2) << y;
    for (int x = 0; x < b.size; ++x) {
      os << "  " << b.board[y][x];
    }
    os << std::endl;
  }
  return os;
}

PutChessResult Board::getPutChessResult(const int x, const int y) const {
  if (!isXValid(x) || !isYValid(y)) {
    return PutChessResult::OUT_BOUNDS;
  }

  if (board[y][x] != ChessPiece::EMPTY) {
    return PutChessResult::OVERLAPPING;
  }

  return PutChessResult::SUCCESS;
}

Board::Board(int size) : size(size) { reset(); }

PutChessResult Board::putChess(const ChessPiece player, const int x,
                               const int y) {
  PutChessResult result = getPutChessResult(x, y);

  if (result == PutChessResult::SUCCESS) {
    totalChesses++;
    board[y][x] = player;
  }

  return result;
}

ChessPiece Board::getChess(const int x, const int y) const {
  if (!isXValid(x) || !isYValid(y)) {
    return ChessPiece::EMPTY;
  }

  return board[y][x];
}

bool Board::isFull() const { return totalChesses >= size * size; }

void Board::reset() {
  totalChesses = 0;
  board.assign(size, std::vector<ChessPiece>(size, ChessPiece::EMPTY));
}

void Board::takeBack(const int x, const int y) {
  if (!isXValid(x) || !isYValid(y) || board[y][x] == ChessPiece::EMPTY) {
    return;
  }

  board[y][x] = ChessPiece::EMPTY;
  totalChesses--;
}

bool Board::isXValid(const int x) const { return 0 <= x && x < size; }

bool Board::isYValid(const int y) const { return 0 <= y && y < size; }