#include "board.h"

bool Board::isWhoPlayNow() const {
    return whoPlay;
}

bool Board::putChess(const int& xPos, const int& yPos) {
    return true;
}

std::ostream& operator<<(std::ostream& os, const dualCharVector& board) {
    for(std::vector<char> line : board) {
        for(char c : line) {
            os << board;
        }
        os << std::endl;
    }
    return os;
}