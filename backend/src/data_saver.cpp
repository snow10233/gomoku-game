#include "data_saver.h"

std::string &operator<<(std::string &str, DataSaver Data) {
  std::vector<std::pair<char, int>> temp;

  // 抓出資料 因為是反的要做reverse
  while (!Data.steps.empty()) {
    temp.push_back(Data.steps.top());
    Data.steps.pop();
  }

  std::reverse(temp.begin(), temp.end());

  for (auto p : temp) {
    if (p.first == -2) {
      str += "OT ";
      continue;
    }

    p.first += 'A';
    str += p.first;
    str += std::to_string(p.second) += " ";
  }

  return str;
}

void DataSaver::addData(const int x, const int y) { steps.push({x, y}); }

std::pair<int, int> DataSaver::takeBack() {
  if (steps.empty()) {
    return {-1, -1};
  }

  auto temp = steps.top();
  steps.pop();

  return temp;
}

void DataSaver::reset() {
  while (!steps.empty()) {
    steps.pop();
  }
}

std::pair<int, int> DataSaver::getTop() const {
  if (steps.empty()) {
    return {-1, -1};
  }

  return steps.top();
}