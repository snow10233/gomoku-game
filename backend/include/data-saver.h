#pragma once
#include <iostream>
#include <stack>
#include <utility>

class Board;

class DataSaver {
  friend std::ostream &operator<<(std::ostream &os, const DataSaver &Data);
  friend Board;

private:
  std::stack<std::pair<int, int>> steps;

public:
  void putAChess(const int x, const int y);

  bool takeBackAMove();
};