#include "ai_player.h"

int AiPlayer::getThisPosScore(const ChessPiece player, const Board &gameBoard,
                              const int x, const int y) const {
  std::vector<int> lengths;

  lengths.push_back(gameBoard.getHorizontalDistance(player, x, y));
  lengths.push_back(gameBoard.getVerticalDistance(player, x, y));
  lengths.push_back(gameBoard.getLeftDiagonalDistance(player, x, y));
  lengths.push_back(gameBoard.getRightDiagonalDistance(player, x, y));

  int score = 0;

  // 1 -> 1, 2 -> 10, ...
  for (int val : lengths) {
    score += std::pow(10, val - 1);
  }

  return score;
}

std::pair<int, int> AiPlayer::aiFindBestPos(const ChessPiece player,
                                            Board &gameBoard, const int x,
                                            const int y) const {
  AICalculatePair aiScore{{0, 0}, 0};
  AICalculatePair playerScore{{0, 0}, 0};

  for (int y = 0; gameBoard.isYValid(y); ++y) {
    for (int x = 0; gameBoard.isXValid(x); ++x) {
      if (gameBoard.putChess(player, x, y) == PutChessResult::SUCCESS) {
        std::pair<int, int> pos{x, y};

        int score = getThisPosScore(player, gameBoard, x, y);
        if (score > aiScore.second) {
          aiScore = {pos, score};
        }
        gameBoard.takeBack(x, y);

        // 預留擴充性 怕我哪天想不開想要開放讓玩家選擇顏色：）
        ChessPiece people = ChessPiece::BLACK;
        if (player == ChessPiece::BLACK) {
          people = ChessPiece::WHITE;
        }

        gameBoard.putChess(people, x, y);
        score = getThisPosScore(people, gameBoard, x, y);
        if (score > playerScore.second) {
          playerScore = {pos, score};
        }
        gameBoard.takeBack(x, y);
      }
    }
  }

  if (aiScore.second >= playerScore.second) {
    return aiScore.first;
  }
  return playerScore.first;
}