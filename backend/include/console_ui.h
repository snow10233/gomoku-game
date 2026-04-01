#pragma once
#include "game_manager.h"
#include <limits>
#include <string>

namespace CONSOLE_UI {
void showWhichPlayer(const GameManager &gameManager);

void clearConsole();

void pauseConsole();

bool isInputValid();

bool isGameModeInputValid(std::string &gameMode);

bool isGameActionInputValid(std::string &action);

} // namespace CONSOLE_UI