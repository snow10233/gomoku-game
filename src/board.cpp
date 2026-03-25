#include "board.h"

ChessPiece Board::isWhoPlayNow() const { return whoPlay; }

bool Board::putChess(const int &xPosition, const int &yPosition) {
  if (isChessPositionVaild(xPosition, yPosition)) {
    board[yPosition][xPosition] = whoPlay;
    this->lastlyChess.setPosition(xPosition, yPosition);
    if (whoPlay == ChessPiece::BLACK) {
      whoPlay = ChessPiece::WHITE;
    } else {
      whoPlay = ChessPiece::BLACK;
    }
    return true;
  }
  return false;
}

bool Board::isChessPositionVaild(const int &xPosition,
                                 const int &yPosition) const {
  return this->lastlyChess.isXVaild(xPosition) &&
         this->lastlyChess.isYVaild(yPosition) &&
         board[yPosition][xPosition] == ChessPiece::EMPTY;
}

void Board::resetBoard() {
  for (std::vector<ChessPiece> &line : this->board) {
    for (ChessPiece &c : line) {
      c = ChessPiece::EMPTY;
    }
  }
}

std::ostream &operator<<(std::ostream &os, const Board &b) {
  os << "   ";
  for (int i = 0; i < b.board[0].size(); ++i) {
    os << std::setw(2) << i << " ";
  }
  os << std::endl;
  for (int i = 0; i < b.board.size(); ++i) {
    os << std::setw(2) << i;
    for (int j = 0; j < b.board[0].size(); ++j) {
      os << "  " << b.board[i][j];
    }
    os << std::endl;
  }
  return os;
}

std::ostream &operator<<(std::ostream &os, const ChessPiece &c) {
  if (c == ChessPiece::BLACK) {
    os << "●";
  } else if (c == ChessPiece::WHITE) {
    os << "○";
  } else {
    os << ".";
  }
  return os;
}