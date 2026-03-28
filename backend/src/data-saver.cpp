#include "data-saver.h"

void DataSaver::putAChess(const int x, const int y) {
  steps.push((std::pair<int, int>{x, y}));
}

std::pair<int, int> DataSaver::takeBackAMove() {
  if (steps.empty()) {
    return std::pair<int, int>{-1, -1};
  }
  auto temp = steps.top();
  steps.pop();
  return temp;
}