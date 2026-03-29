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

BattleResult Board::getBattleState() const { return battleState; }

int getHorizontalDistance(const Board &b1) {
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

void Board::changePlayer() {
  if (whoPlay == ChessPiece::BLACK) {
    whoPlay = ChessPiece::WHITE;
  } else {
    whoPlay = ChessPiece::BLACK;
  }
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

BattleResult Board::calculateBattleState() const {
  // std::cout << whoPlay << std::endl;
  // std::cout << getHorizontalDistance(*this) << " ";
  // std::cout << getVerticalDistance(*this) << " ";
  // std::cout << getLeftDiagonalDistance(*this) << " ";
  // std::cout << getRightDiagonalDistance(*this) << std::endl;

  if (getHorizontalDistance(*this) >= 5 || getVerticalDistance(*this) >= 5 ||
      getLeftDiagonalDistance(*this) >= 5 ||
      getRightDiagonalDistance(*this) >= 5) {
    if (whoPlay == ChessPiece::BLACK) {
      return BattleResult::BLACK_WIN;
    } else if (whoPlay == ChessPiece::WHITE) {
      return BattleResult::WHITE_WIN;
    }
  } else if (totalChesses >= sizeLimit * sizeLimit) {
    return BattleResult::DRAW;
  }

  return BattleResult::CONTINUE;
}

PutChessResult Board::putChess(const int &xPosition, const int &yPosition) {
  PutChessResult result = isChessPositionValid(xPosition, yPosition);

  if (result == PutChessResult::SUCCESS) {
    totalChesses++;
    board[yPosition][xPosition] = whoPlay;
    this->lastlyChess.setPosition(xPosition, yPosition);
    boardData.putAChess(xPosition, yPosition);

    battleState = calculateBattleState();

    changePlayer();
  }

  return result;
}

bool Board::takeBackAMove() {
  if (!boardData.takeBackAMove()) {
    return false;
  }

  board[lastlyChess.getY()][lastlyChess.getX()] = ChessPiece::EMPTY;

  if (!boardData.steps.empty()) {
    auto temp = boardData.steps.top();
    lastlyChess.setPosition(temp.first, temp.second);
  } else {
    lastlyChess.resetChess();
  }

  changePlayer();
  totalChesses--;
  return true;
}

// 將-1 -1寫入data做為佔位使用 後續進行存檔才不會亂
void Board::overTimeProcess() {
  changePlayer();

  if (boardData.steps.empty()) {
    return;
  }

  boardData.putAChess(-1, -1);
}

// std::pair<int, int> findBestChessPos(dualChessPieceVector vec, ChessPiece
// player) {
//   std::pair<int, int> pos, score;
//   for(std::vector<ChessPiece>& v : vec) {
//     for(ChessPiece c : v) {
//       if(c == ChessPiece::EMPTY) {
//         c = player;
//
//       }
//     }
//   }
// }
//
// void Board::AIPutChess() {
// }

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

std::ostream &operator<<(std::ostream &os, const PutChessResult &p) {
  if (p == PutChessResult::ALL_RIGHT_ONE) {
    os << "OVERIAPPING";
  } else if (p == PutChessResult::OVER_EDGE) {
    os << "OVER_EDGE";
  } else {
    os << "SUCCESS";
  }
  return os;
}

std::ostream &operator<<(std::ostream &os, const BattleResult &b) {
  if (b == BattleResult::BLACK_WIN) {
    os << "BLACK";
  } else if (b == BattleResult::WHITE_WIN) {
    os << "WHITE";
  } else if (b == BattleResult::DRAW) {
    os << "DRAW";
  } else {
    os << "CONTINUE";
  }
  return os;
}