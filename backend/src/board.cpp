#include "board.h"

std::ostream &operator<<(std::ostream &os, const Board &b) {
  os << "   ";
  for (int y = 0; y < b.board[0].size(); ++y) {
    os << std::setw(2) << y << " ";
  }
  os << std::endl;
  for (int y = 0; y < b.sizeLimit; ++y) {
    os << std::setw(2) << y;
    for (int x = 0; x < b.sizeLimit; ++x) {
      os << "  " << b.board[y][x];
    }
    os << std::endl;
  }
  return os;
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

void Board::changePlayer() {
  if (whoPlay == ChessPiece::BLACK) {
    whoPlay = ChessPiece::WHITE;
  } else {
    whoPlay = ChessPiece::BLACK;
  }
}

PutChessResult Board::isChessPositionValid(const int x, const int y) const {
  if (!this->lastlyChess.isXValid(x) || !this->lastlyChess.isYValid(y)) {
    return PutChessResult::OUT_BOUNDS;
  } else if (board[y][x] != ChessPiece::EMPTY) {
    return PutChessResult::OVERLAPPING;
  } else {
    return PutChessResult::SUCCESS;
  }
}

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

void Board::resetBoard() {
  for (std::vector<ChessPiece> &line : this->board) {
    for (ChessPiece &c : line) {
      c = ChessPiece::EMPTY;
    }
  }
}

PutChessResult Board::putChess(const int x, const int y) {
  PutChessResult result = isChessPositionValid(x, y);

  if (result == PutChessResult::SUCCESS) {
    totalChesses++;
    board[y][x] = whoPlay;
    lastlyChess.setPosition(x, y);
    boardData.putAChess(x, y);
    battleState = calculateBattleState();

    changePlayer();
  }

  return result;
}

std::pair<int, int> Board::takeBackAMove() {
  if (!boardData.takeBackAMove()) {
    return {-1, -1};
  }
  int x = lastlyChess.getX();
  int y = lastlyChess.getY();

  board[y][x] = ChessPiece::EMPTY;

  if (!boardData.steps.empty()) {
    auto last = boardData.steps.top();
    lastlyChess.setPosition(last.first, last.second);
  } else {
    lastlyChess.resetChess();
  }

  changePlayer();
  totalChesses--;
  return {x, y};
}

// 將-1 -1寫入data做為佔位使用 後續進行存檔才不會亂
void Board::overTimeProcess() {
  changePlayer();

  if (boardData.steps.empty()) {
    return;
  }

  boardData.putAChess(-1, -1);
}


int getThisPosScore(Board &b) {
  std::vector<int> lengths;

  lengths.push_back(getHorizontalDistance(b));
  lengths.push_back(getVerticalDistance(b));
  lengths.push_back(getLeftDiagonalDistance(b));
  lengths.push_back(getRightDiagonalDistance(b));

  int score = 0;

  // 1 -> 1, 2 -> 10, ...
  for (int val : lengths) {
    score += std::pow(10, val - 1);
  }

  return score;
}

std::pair<int, int> Board::aiFindBestPos() {
  AICalculatePair aiScore{std::pair<int, int>{0, 0}, 0};
  AICalculatePair playerScore{std::pair<int, int>{0, 0}, 0};

  for (int y = 0; y < sizeLimit; ++y) {
    for (int x = 0; x < sizeLimit; ++x) {
      if (board[y][x] == ChessPiece::EMPTY) {
        int lastlyChessTempX = lastlyChess.getX();
        int lastlyChessTempY = lastlyChess.getY();

        std::pair<int, int> pos{x, y};
        this->lastlyChess.setPosition(x, y);

        board[y][x] = whoPlay;
        int score = getThisPosScore(*this);
        if (score > aiScore.second) {
          aiScore = {pos, score};
        }

        changePlayer();

        board[y][x] = whoPlay;
        score = getThisPosScore(*this);
        if (score > playerScore.second) {
          playerScore = {pos, score};
        }

        changePlayer();
        board[y][x] = ChessPiece::EMPTY;
        this->lastlyChess.setPosition(lastlyChessTempX, lastlyChessTempY);
      }
    }
  }

  // std::cout << "aiScore: " << aiScore.first.first << "," <<
  // aiScore.first.second
  //           << " " << aiScore.second << std::endl;
  // std::cout << "playerScore: " << playerScore.first.first << ","
  //           << playerScore.first.second << " " << playerScore.second
  //           << std::endl;

  if (aiScore.second >= playerScore.second) {
    return aiScore.first;
  }
  return playerScore.first;
}