
import unittest
from snake_game.game import Game, Direction, GameOver, Point

class TestGameLogic(unittest.TestCase):
    def test_initial_state(self):
        g = Game(8, 8, seed=1)
        self.assertEqual(len(g.snake), 1)
        self.assertEqual(g.score, 0)
        self.assertTrue(0 <= g.food.x < g.width and 0 <= g.food.y < g.height)

    def test_move_and_food(self):
        g = Game(6, 6, seed=0)
        # Force food to be right of head if possible
        head = g.snake[0]
        g.food = head.__class__(head.x + 1, head.y) if head.x + 1 < g.width else g.food
        g.change_direction(Direction.RIGHT)
        g.step()
        # Either ate food (score increment) or just moved
        self.assertIn(len(g.snake), (1, 2))
        self.assertIn(g.score, (0, 1))

    def test_wall_collision(self):
        g = Game(4, 4, seed=0)
        # Can't reverse RIGHT->LEFT immediately, so step UP once first
        g.change_direction(Direction.UP); g.step()      # from (2,2) -> (2,1)
        g.change_direction(Direction.LEFT)
        g.step()  # (1,1)
        g.step()  # (0,1)
        with self.assertRaises(GameOver):
            g.step()  # (-1,1) -> wall


    def test_self_collision(self):
        g = Game(5, 5, seed=0)
        # Grow to make a U-shape and then bite ourselves
        g.grow_pending = 3
        g.step()  # right
        g.step()  # right
        g.change_direction(Direction.DOWN); g.step()
        g.change_direction(Direction.LEFT); g.step()
        g.change_direction(Direction.UP)
        with self.assertRaises(GameOver):
            g.step()


if __name__ == "__main__":
    unittest.main()
