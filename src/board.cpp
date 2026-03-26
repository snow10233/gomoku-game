#include "board.h"

Board::Board(int size) {
  battleState = BattleResult::CONTINUE;
  sizeLimit = size;
  totalChesses = 0;
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

ChessPiece Board::isWhoPlayNow() const { return whoPlay; }

PutChessResult Board::putChess(const int &xPosition, const int &yPosition) {
  PutChessResult result = isChessPositionValid(xPosition, yPosition);
  if (result == PutChessResult::SUCCESS) {
    board[yPosition][xPosition] = whoPlay;
    this->lastlyChess.setPosition(xPosition, yPosition);
    battleState = calculateBattleState();
    if (whoPlay == ChessPiece::BLACK) {
      whoPlay = ChessPiece::WHITE;
    } else {
      whoPlay = ChessPiece::BLACK;
    }
    return PutChessResult::SUCCESS;
  }
  return result;
}

PutChessResult Board::isChessPositionValid(const int &xPosition,
                                           const int &yPosition) const {
  if (!this->lastlyChess.isXValid(xPosition) ||
      !this->lastlyChess.isYValid(yPosition)) {
    return PutChessResult::OVER_EDGE;
  } else if (board[yPosition][xPosition] != ChessPiece::EMPTY) {
    return PutChessResult::ALL_RIGHT_ONE;
  } else {
    return PutChessResult::SUCCESS;
  }
}

void Board::resetBoard() {
  for (std::vector<ChessPiece> &line : this->board) {
    for (ChessPiece &c : line) {
      c = ChessPiece::EMPTY;
    }
  }
}

int getHorizaonlDistance(const Board &b1) {
  int distance = 1;
  int leftIndex = b1.lastlyChess.getX() - 1;
  int rightIndex = b1.lastlyChess.getX() + 1;
  int y = b1.lastlyChess.getY();

  while (b1.lastlyChess.isXValid(leftIndex) &&
         b1.board[y][leftIndex] == b1.whoPlay) {
    distance++;
    leftIndex--;
  }

  while (b1.lastlyChess.isXValid(rightIndex) &&
         b1.board[y][rightIndex] == b1.whoPlay) {
    distance++;
    rightIndex++;
  }

  return distance;
}

int getVerticalDistance(const Board &b1) {
  int distance = 1;
  int upIndex = b1.lastlyChess.getY() + 1;
  int downIndex = b1.lastlyChess.getY() - 1;
  int x = b1.lastlyChess.getX();

  while (b1.lastlyChess.isYValid(upIndex) &&
         b1.board[upIndex][x] == b1.whoPlay) {
    distance++;
    upIndex++;
  }

  while (b1.lastlyChess.isYValid(downIndex) &&
         b1.board[downIndex][x] == b1.whoPlay) {
    distance++;
    downIndex--;
  }

  return distance;
}

int getLeftDiagonalDistance(const Board &b1) {
  int distance = 1;
  int leftIndex = b1.lastlyChess.getX() - 1;
  int rightIndex = b1.lastlyChess.getX() + 1;
  int upIndex = b1.lastlyChess.getY() + 1;
  int downIndex = b1.lastlyChess.getY() - 1;

  while (b1.lastlyChess.isXValid(leftIndex) &&
         b1.lastlyChess.isYValid(downIndex) &&
         b1.board[downIndex][leftIndex] == b1.whoPlay) {
    distance++;
    downIndex--;
    leftIndex--;
  }

  while (b1.lastlyChess.isXValid(rightIndex) &&
         b1.lastlyChess.isYValid(upIndex) &&
         b1.board[upIndex][rightIndex] == b1.whoPlay) {
    distance++;
    upIndex++;
    rightIndex++;
  }

  return distance;
}

int getRightDiagonalDistance(const Board &b1) {
  int distance = 1;
  int leftIndex = b1.lastlyChess.getX() - 1;
  int rightIndex = b1.lastlyChess.getX() + 1;
  int upIndex = b1.lastlyChess.getY() + 1;
  int downIndex = b1.lastlyChess.getY() - 1;

  while (b1.lastlyChess.isXValid(rightIndex) &&
         b1.lastlyChess.isYValid(downIndex) &&
         b1.board[downIndex][rightIndex] == b1.whoPlay) {
    distance++;
    downIndex--;
    rightIndex++;
  }

  while (b1.lastlyChess.isXValid(leftIndex) &&
         b1.lastlyChess.isYValid(upIndex) &&
         b1.board[upIndex][leftIndex] == b1.whoPlay) {
    distance++;
    upIndex++;
    leftIndex--;
  }

  return distance;
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

BattleResult Board::calculateBattleState() const {
  // std::cout << "whoPlay:" << whoPlay << std::endl;
  // std::cout << "水平:" << getHorizaonlDistance(*this) << std::endl;
  // std::cout << "垂直:" << getVerticalDistance(*this) << std::endl;
  // std::cout << "左斜:" << getLeftDiagonalDistance(*this) << std::endl;
  // std::cout << "右斜:" << getRightDiagonalDistance(*this) << std::endl;
  if (getHorizaonlDistance(*this) >= 5 || getVerticalDistance(*this) >= 5 ||
      getLeftDiagonalDistance(*this) >= 5 ||
      getRightDiagonalDistance(*this) >= 5) {
    if (whoPlay == ChessPiece::BLACK) {
      return BattleResult::BLACK_WIN;
    } else if (whoPlay == ChessPiece::WHITE) {
      return BattleResult::WHITE_WIN;
    }
  } else if (totalChesses >= ((sizeLimit - 1) * (sizeLimit - 1))) {
    return BattleResult::DRAW;
  }
  return BattleResult::CONTINUE;
}

BattleResult Board::getBattleState() const { return battleState; }