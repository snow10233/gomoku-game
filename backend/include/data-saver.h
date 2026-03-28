#pragma once
#include <iostream>
#include <stack>
#include <utility>

class DataSaver {
  friend std::ostream &operator<<(std::ostream &os, const DataSaver &Data);

private:
  std::stack<std::pair<int, int>> steps;
public:
  DataSaver();

  void putAChess(const int x, const int y);

  std::pair<int, int> takeBackAMove();
};