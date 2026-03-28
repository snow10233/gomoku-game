#pragma once
#include "board.h"
#include <limits>
#include <string>

namespace CONSOLE_UI {
void showBoard(const Board &board);

void showWhichPlayer(const Board &board);

void clearConsole();

void pauseConsole();

bool isInputValid();

bool isGameModeInputValid(std::string &gameMode);

bool isGameActionInputValid(std::string& action);
} // namespace CONSOLE_UI