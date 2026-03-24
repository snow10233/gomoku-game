#include "position.h"

int Position::getX() const {
	return x;
}

int Position::getY() const {
	return y;
}

bool Position::setX(const int& xPos) {
	if(xLeftLimit <= xPos && xPos <= xRightLimit) {
		x = xPos;
		return true;
	}
	return false;
}

bool Position::getY(const int& yPos) {
	if(yLeftLimit <= yPos && yPos <= yRightLimit) {
		y = yPos;
		return true;
	}
	return false;
}

void Position::setXLimit(const int& left, const int& right) {
	xLeftLimit = left;
	xRightLimit = right;
}

void Position::setYLimit(const int& left, const int& right) {
	yLeftLimit = left;
	yRightLimit = right;
}