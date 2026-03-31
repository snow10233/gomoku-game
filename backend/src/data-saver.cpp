#include "data-saver.h"

void DataSaver::putAChess(const int x, const int y) {
  steps.push((std::pair<int, int>{x, y}));
}

bool DataSaver::takeBackAMove() {
  if (steps.empty()) {
    return false;
  }
  steps.pop();
  return true;
}

void DataSaver::resetDataSaver() {
  while (!steps.empty()) {
    steps.pop();
  }
}