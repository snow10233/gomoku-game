#pragma once
#include "board.h"
#include <limits> // 需要引入這個才能使用 numeric_limits

namespace UI {
void everyRoundStartMessage(const Board &b);

void clearConsole();

void pauseConsole();
} // namespace UI