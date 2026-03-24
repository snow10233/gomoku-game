#pragma once
#include <iostream>
#include <vector>
#include "position.h"

using dualCharVector = std::vector<std::vector<char>>;

class Board {
	friend std::ostream& operator<<(std::ostream& os, const dualCharVector& board);
private:
	dualCharVector board;
	Position black, white;
	int sizeLimit;
	bool whoPlay; // 0 black 1 white
public:
	Board(const int& size) : sizeLimit(size) {
		whoPlay = 1;
		black.setXLimit(-size, size);
		black.setYLimit(-size, size);
		white.setXLimit(-size, size);
		white.setYLimit(-size, size);
		for(int i = 0; i < size; i++) {
			board.push_back(std::vector<char>{});
			for(int j = 0; j < size; ++j) {
				board[i].push_back('*');
			}
		}
	}

	bool isWhoPlayNow() const;

	bool putChess(const int& xPos, const int& yPos);

	// bool isPosVaild(const int& x, const int& y);
};


