
"""
A very minimal console UI for the snake engine.
This is optional and not used in tests or CI.
Controls: W/A/S/D + Enter for moves, Q to quit.
"""
from __future__ import annotations
from .game import Game, Direction, GameOver, Cell

def render(game: Game) -> None:
    grid = game.grid()
    lines = []
    for y in range(game.height):
        row = ""
        for x in range(game.width):
            c = grid[y][x]
            if c is Cell.EMPTY:
                row += " ."
            elif c is Cell.SNAKE:
                row += " S"
            else:
                row += " F"
        lines.append(row)
    print("\n".join(lines))
    print(f"Score: {game.score}\n")

def main():
    g = Game(10, 10)
    print("Controls: W/A/S/D + Enter. Q to quit.\n")
    render(g)
    while True:
        move = input("Move> ").strip().lower()
        if not move:
            continue
        if move[0] == 'q':
            print("Bye!")
            return
        
        if move[0] == 'w':
            g.change_direction(Direction.UP)
        
        if move[0] == 'i':
            g.change_direction(Direction.UP)

        if move[0] == 'p':
            g.change_direction(Direction.UP)    

        elif move[0] == 's':
            g.change_direction(Direction.DOWN)
        elif move[0] == 'a':
            g.change_direction(Direction.LEFT)
        elif move[0] == 'd':
            g.change_direction(Direction.RIGHT)
        try:
            g.step()
        except GameOver as e:
            render(g)
            print(f"Game Over: {e}")
            return
        render(g)

if __name__ == "__main__":
    main()
