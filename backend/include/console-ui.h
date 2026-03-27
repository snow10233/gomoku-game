#pragma once
#include "board.h"
#include <limits> // 需要引入這個才能使用 numeric_limits

namespace CONSOLE_UI {
void showBoard(const Board &board);

void showWhichPlayer(const Board &board);

void clearConsole();

void pauseConsole();
} // namespace CONSOLE_UI