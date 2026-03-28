#pragma once
class Chess {
private:
  int x, xLeftLimit, xRightLimit;
  int y, yLeftLimit, yRightLimit;

public:
  Chess(const int &xPosition = -1, const int &yPosition = -1)
      : x(xPosition), y(yPosition) {}

  void resetChess();

  int getX() const;

  int getY() const;

  bool isXValid(const int &xPosition) const;

  bool isYValid(const int &yPosition) const;

  bool setPosition(const int &xPosition, const int &yPosition);

  void setXLimit(const int &left, const int &right);

  void setYLimit(const int &left, const int &right);
};
