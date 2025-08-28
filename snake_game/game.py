
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import random

class Cell(Enum):
    EMPTY = 0
    SNAKE = 1
    FOOD = 2

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

class GameOver(Exception):
    pass

class Game:
    """
    Pure-logic Snake engine.
    Grid is width x height, origin (0,0) at top-left.
    """
    def __init__(self, width: int = 10, height: int = 10, seed: int | None = None):
        if width < 4 or height < 4:
            raise ValueError("Grid too small")
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
        self.snake: list[Point] = [Point(width // 2, height // 2)]
        self.direction = Direction.RIGHT
        self.grow_pending = 0
        self.score = 0
        self.food = self._spawn_food()

    def _spawn_food(self) -> Point:
        empty = {Point(x, y) for x in range(self.width) for y in range(self.height)} - set(self.snake)
        if not empty:
            # Victory: filled grid
            raise GameOver("You win! Board filled.")
        return self.rng.choice(list(empty))

    def change_direction(self, direction: Direction) -> None:
        # Prevent 180-turns
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        if direction is opposite[self.direction]:
            return
        self.direction = direction

    def step(self) -> None:
        head = self.snake[0]
        new_head = Point(head.x + self.direction.dx, head.y + self.direction.dy)

        # Wall collision
        if not (0 <= new_head.x < self.width and 0 <= new_head.y < self.height):
            raise GameOver("Hit the wall")

        # Self collision
        if new_head in self.snake:
            raise GameOver("Ate yourself")

        self.snake.insert(0, new_head)

        # Food?
        if new_head == self.food:
            self.score += 1
            self.grow_pending += 1
            self.food = self._spawn_food()

        # Tail trim
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.snake.pop()

    def grid(self) -> list[list[Cell]]:
        grid = [[Cell.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        for p in self.snake:
            grid[p.y][p.x] = Cell.SNAKE
        grid[self.food.y][self.food.x] = Cell.FOOD
        return grid
