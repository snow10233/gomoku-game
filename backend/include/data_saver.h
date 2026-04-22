#pragma once
#include <algorithm>
#include <iostream>
#include <stack>
#include <string>
#include <utility>
#include <vector>

class DataSaver {
  friend std::string &operator<<(std::string &str, DataSaver Data);

private:
  std::stack<std::pair<int, int>> steps;

public:
  void addData(const int x, const int y);

  std::pair<int, int> takeBack();

  std::pair<int, int> getTop() const;

  void reset();
};