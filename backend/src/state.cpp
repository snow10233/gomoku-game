#include "state.h"

std::ostream &operator<<(std::ostream &os, const ChessPiece &c) {
  if (c == ChessPiece::BLACK) {
    os << "●";
  } else if (c == ChessPiece::WHITE) {
    os << "○";
  } else {
    os << ".";
  }
  return os;
}

std::ostream &operator<<(std::ostream &os, const PutChessResult &p) {
  if (p == PutChessResult::OVERLAPPING) {
    os << "OVERLAPPING";
  } else if (p == PutChessResult::OUT_BOUNDS) {
    os << "OUT_BOUNDS";
  } else {
    os << "SUCCESS";
  }
  return os;
}

std::ostream &operator<<(std::ostream &os, const BattleResult &b) {
  if (b == BattleResult::BLACK_WIN) {
    os << "BLACK_WIN";
  } else if (b == BattleResult::WHITE_WIN) {
    os << "WHITE_WIN";
  } else if (b == BattleResult::DRAW) {
    os << "DRAW";
  } else {
    os << "CONTINUE";
  }
  return os;
}