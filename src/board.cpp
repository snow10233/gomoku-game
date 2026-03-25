#include "board.h"

Chess Board::isWhoPlayNow() const { return whoPlay; }

bool Board::putChess(const int &xPos, const int &yPos) { return true; }

void Board::resetBoard() {
  for (std::vector<Chess> &line : this->board) {
    for (Chess &c : line) {
      c = Chess::EMPTY;
    }
  }
}

bool Board::isChessPositionVaild() const { return true; }

std::ostream &operator<<(std::ostream &os, const Board &b) {
  for (const std::vector<Chess> &line : b.board) {
    for (const Chess &c : line) {
      os << c;
    }
    os << std::endl;
  }
  return os;
}

std::ostream &operator<<(std::ostream &os, const Chess &c) {
  if (c == Chess::BLACK) {
    os << 'B';
  } else if (c == Chess::WHITE) {
    os << 'W';
  } else {
    os << '*';
  }
  return os;
}