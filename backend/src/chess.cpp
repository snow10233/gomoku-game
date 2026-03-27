#include "chess.h"

int Chess::getX() const { return x; }

int Chess::getY() const { return y; }

bool Chess::isXValid(const int &xPosition) const {
  return xLeftLimit <= xPosition && xPosition <= xRightLimit;
}

bool Chess::isYValid(const int &yPosition) const {
  return yLeftLimit <= yPosition && yPosition <= yRightLimit;
}

bool Chess::setPosition(const int &xPosition, const int &yPosition) {
  if (isXValid(xPosition) && isYValid(yPosition)) {
    x = xPosition;
    y = yPosition;
    return true;
  }
  return false;
}

void Chess::setXLimit(const int &left, const int &right) {
  xLeftLimit = left;
  xRightLimit = right;
}

void Chess::setYLimit(const int &left, const int &right) {
  yLeftLimit = left;
  yRightLimit = right;
}