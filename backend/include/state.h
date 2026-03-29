#pragma once
#include <iostream>

enum class ChessPiece { EMPTY, BLACK, WHITE };

enum class PutChessResult { SUCCESS, OUT_BOUNDS, OVERLAPPING };

enum class BattleResult { BLACK_WIN, WHITE_WIN, DRAW, CONTINUE };

std::ostream &operator<<(std::ostream &os, const ChessPiece &c);

std::ostream &operator<<(std::ostream &os, const PutChessResult &p);

std::ostream &operator<<(std::ostream &os, const BattleResult &b);