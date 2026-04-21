from enum import Enum

from PySide6.QtWidgets import QStackedWidget, QWidget


class Route(str, Enum):
    HOME = "home"
    SINGLE_CHOOSE_MODE = "single_choose_mode"
    SINGLE_NEW_GAME = "single_new_game"
    SINGLE_GAME = "single_game"
    MULTI_CHOOSE_MODE = "multi_choose_mode"
    MULTI_LOCAL_CHOOSE_MODE = "multi_local_choose_mode"
    MULTI_NEW_GAME = "multi_new_game"
    MULTI_GAME = "multi_game"
    MULTI_REMOTE = "multi_remote"
    REPLAY = "replay"


class Router:
    """Lightweight router for QStackedWidget pages."""

    def __init__(self, stack: QStackedWidget):
        self._stack = stack
        self._route_indexes: dict[Route, int] = {}

    def register(self, route: Route, page: QWidget) -> None:
        if route in self._route_indexes:
            raise ValueError(f"Route already registered: {route}")
        index = self._stack.addWidget(page)
        self._route_indexes[route] = index

    def go(self, route: Route) -> None:
        if route not in self._route_indexes:
            raise KeyError(f"Unknown route: {route}")
        self._stack.setCurrentIndex(self._route_indexes[route])

    def current_route(self) -> Route | None:
        current_index = self._stack.currentIndex()
        for route, index in self._route_indexes.items():
            if index == current_index:
                return route
        return None
