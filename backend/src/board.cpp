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

bool Board::isXValid(const int x) const { return 0 <= x && x < size; }

bool Board::isYValid(const int y) const { return 0 <= y && y < size; }

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

void Board::reset() {
  totalChesses = 0;
  board.assign(size, std::vector<ChessPiece>(size, ChessPiece::EMPTY));
}

bool Board::isFull() const { return totalChesses >= size * size; }

int Board::getHorizontalDistance(const ChessPiece player, const int x,
                                 const int y) const {
  int distance = 1;
  int leftIndex = x - 1;
  int rightIndex = x + 1;

  while (isXValid(leftIndex) && board[y][leftIndex] == player) {
    distance++;
    leftIndex--;
  }

  while (isYValid(rightIndex) && board[y][rightIndex] == player) {
    distance++;
    rightIndex++;
  }

  return distance;
}

int Board::getVerticalDistance(const ChessPiece player, const int x,
                               const int y) const {
  int distance = 1;
  int upIndex = y + 1;
  int downIndex = y - 1;

  while (isYValid(upIndex) && board[upIndex][x] == player) {
    distance++;
    upIndex++;
  }

  while (isYValid(downIndex) && board[downIndex][x] == player) {
    distance++;
    downIndex--;
  }

  return distance;
}

int Board::getLeftDiagonalDistance(const ChessPiece player, const int x,
                                   const int y) const {
  int distance = 1;
  int leftIndex = x - 1;
  int rightIndex = x + 1;
  int upIndex = y + 1;
  int downIndex = y - 1;

  while (isXValid(leftIndex) && isYValid(downIndex) &&
         board[downIndex][leftIndex] == player) {
    distance++;
    downIndex--;
    leftIndex--;
  }

  while (isXValid(rightIndex) && isYValid(upIndex) &&
         board[upIndex][rightIndex] == player) {
    distance++;
    upIndex++;
    rightIndex++;
  }

  return distance;
}

int Board::getRightDiagonalDistance(const ChessPiece player, const int x,
                                    const int y) const {
  int distance = 1;
  int leftIndex = x - 1;
  int rightIndex = x + 1;
  int upIndex = y + 1;
  int downIndex = y - 1;

  while (isXValid(rightIndex) && isYValid(downIndex) &&
         board[downIndex][rightIndex] == player) {
    distance++;
    downIndex--;
    rightIndex++;
  }

  while (isXValid(leftIndex) && isYValid(upIndex) &&
         board[upIndex][leftIndex] == player) {
    distance++;
    upIndex++;
    leftIndex--;
  }

  return distance;
}

PutChessResult Board::putChess(const ChessPiece player, const int x,
                               const int y) {
  PutChessResult result = getPutChessResult(x, y);

  if (result == PutChessResult::SUCCESS) {
    totalChesses++;
    board[y][x] = player;
  }

  return result;
}

void Board::takeBack(const int x, const int y) {
  if (x == -1 || y == -1 || board[y][x] == ChessPiece::EMPTY) {
    return;
  }

  board[y][x] = ChessPiece::EMPTY;
  totalChesses--;
}