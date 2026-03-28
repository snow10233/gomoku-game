#pragma once
#include "board.h"
#include <limits>
#include <string>

namespace CONSOLE_UI {
void showBoard(const Board &board);

void showWhichPlayer(const Board &board);

void clearConsole();

void pauseConsole();

bool isChessInputValid();

bool isGameModeInputValid(std::string &gameMode);
} // namespace CONSOLE_UI