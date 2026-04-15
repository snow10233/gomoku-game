#include "distance_calculator.h"

int Distance_calculator::getHorizontalDistance(const Board &gameBoard,
                                               const ChessPiece player,
                                               const int x, const int y) const {
  int distance = 1;
  int leftIndex = x - 1;
  int rightIndex = x + 1;

  while (gameBoard.isXValid(leftIndex) &&
         gameBoard.getChess(leftIndex, y) == player) {
    distance++;
    leftIndex--;
  }

  while (gameBoard.isXValid(rightIndex) &&
         gameBoard.getChess(rightIndex, y) == player) {
    distance++;
    rightIndex++;
  }

  return distance;
}

int Distance_calculator::getVerticalDistance(const Board &gameBoard,
                                             const ChessPiece player,
                                             const int x, const int y) const {
  int distance = 1;
  int upIndex = y + 1;
  int downIndex = y - 1;

  while (gameBoard.isYValid(upIndex) &&
         gameBoard.getChess(x, upIndex) == player) {
    distance++;
    upIndex++;
  }

  while (gameBoard.isYValid(downIndex) &&
         gameBoard.getChess(x, downIndex) == player) {
    distance++;
    downIndex--;
  }

  return distance;
}

int Distance_calculator::getLeftDiagonalDistance(const Board &gameBoard,
                                                 const ChessPiece player,
                                                 const int x,
                                                 const int y) const {
  int distance = 1;
  int leftIndex = x - 1;
  int rightIndex = x + 1;
  int upIndex = y + 1;
  int downIndex = y - 1;

  while (gameBoard.isXValid(leftIndex) && gameBoard.isYValid(downIndex) &&
         gameBoard.getChess(leftIndex, downIndex) == player) {
    distance++;
    downIndex--;
    leftIndex--;
  }

  while (gameBoard.isXValid(rightIndex) && gameBoard.isYValid(upIndex) &&
         gameBoard.getChess(rightIndex, upIndex) == player) {
    distance++;
    upIndex++;
    rightIndex++;
  }

  return distance;
}

int Distance_calculator::getRightDiagonalDistance(const Board &gameBoard,
                                                  const ChessPiece player,
                                                  const int x,
                                                  const int y) const {
  int distance = 1;
  int leftIndex = x - 1;
  int rightIndex = x + 1;
  int upIndex = y + 1;
  int downIndex = y - 1;

  while (gameBoard.isXValid(rightIndex) && gameBoard.isYValid(downIndex) &&
         gameBoard.getChess(rightIndex, downIndex) == player) {
    distance++;
    downIndex--;
    rightIndex++;
  }

  while (gameBoard.isXValid(leftIndex) && gameBoard.isYValid(upIndex) &&
         gameBoard.getChess(leftIndex, upIndex) == player) {
    distance++;
    upIndex++;
    leftIndex--;
  }

  return distance;
}

int Distance_calculator::getlongestDistance(const Board &gameBoard,
                                              const ChessPiece player,
                                              const int x, const int y) const {
  return std::max(
      {getHorizontalDistance(gameBoard, player, x, y),
       getVerticalDistance(gameBoard, player, x, y),
       getLeftDiagonalDistance(gameBoard, player, x, y),
       getRightDiagonalDistance(gameBoard, player, x, y)});
}