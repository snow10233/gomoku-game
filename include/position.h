#pragma once
class Position {
private:
  int x, xLeftLimit, xRightLimit;
  int y, yLeftLimit, yRightLimit;

public:
  Position(const int &xPos = 0, const int &yPos = 0) : x(xPos), y(yPos) {}

  int getX() const;

  int getY() const;

  bool setX(const int &xPos);

  bool getY(const int &yPos);

  void setXLimit(const int &left, const int &right);

  void setYLimit(const int &left, const int &right);
};
