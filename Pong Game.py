"""
Pong Game - Using Turtle Graphics
A classic Pong game implementation using object-oriented programming principles.
"""
import turtle
import time
import random
from typing import Tuple, Optional


class GameObject:
    """Base class for all game objects."""

    def __init__(self, shape: str, color: str, position: Optional[Tuple[int, int]] = (0, 0)):
        """Initialize a game object with shape, color, and position."""
        self.sprite = turtle.Turtle()
        self.sprite.speed(0)  # Animation speed (0 = fastest)
        self.sprite.shape(shape)
        self.sprite.color(color)
        self.sprite.penup()
        self.sprite.goto(position)

    def set_position(self, x: float, y: float) -> None:
        """Set the position of the game object."""
        self.sprite.goto(x, y)

    def get_position(self) -> Tuple[float, float]:
        """Get the current position of the game object."""
        return self.sprite.xcor(), self.sprite.ycor()


class Paddle(GameObject):
    """Paddle class for player controls."""

    def __init__(self, color: str, position: Optional[Tuple[int, int]] = (0, 0), width: int = 5, height: int = 1):
        """Initialize a paddle with specified color, position, and dimensions."""
        super().__init__("square", color, position)
        self.sprite.shapesize(stretch_wid=height, stretch_len=width)
        self.speed = 20
        self.width = width * 20  # Convert turtle units to pixels
        self.height = height * 20  # Convert turtle units to pixels

    def move_up(self, boundary: int) -> None:
        """Move the paddle up within the specified boundary."""
        y = self.sprite.ycor()
        if y < boundary:
            y += self.speed
            self.sprite.sety(y)

    def move_down(self, boundary: int) -> None:
        """Move the paddle down within the specified boundary."""
        y = self.sprite.ycor()
        if y > boundary:
            y -= self.speed
            self.sprite.sety(y)

    def move_left(self, boundary: int) -> None:
        """Move the paddle left within the specified boundary."""
        x = self.sprite.xcor()
        if x > boundary:
            x -= self.speed
            self.sprite.setx(x)

    def move_right(self, boundary: int) -> None:
        """Move the paddle right within the specified boundary."""
        x = self.sprite.xcor()
        if x < boundary:
            x += self.speed
            self.sprite.setx(x)


class Ball(GameObject):
    """Ball class for the game."""

    def __init__(self, color: str, position: Optional[Tuple[int, int]] = (0, 0)):
        """Initialize a ball with specified color and position."""
        super().__init__("circle", color, position)
        self.dx = 0.5  # Initial horizontal speed
        self.dy = 0.5  # Initial vertical speed
        self.radius = 10  # Ball radius in pixels
        self.colors = ["red", "blue", "green", "yellow", "orange", "purple", "white"]

    def move(self) -> None:
        """Move the ball according to its current velocity."""
        self.sprite.setx(self.sprite.xcor() + self.dx)
        self.sprite.sety(self.sprite.ycor() + self.dy)

    def bounce_y(self) -> None:
        """Reverse the vertical direction of the ball."""
        self.dy *= -1

    def bounce_x(self) -> None:
        """Reverse the horizontal direction of the ball."""
        self.dx *= -1

    def reset_position(self) -> None:
        """Reset the ball to the center of the screen."""
        self.set_position(0, 0)
        # Randomize the direction after reset
        self.dx = 0.5 * random.choice([-1, 1])
        self.dy = 0.5 * random.choice([-1, 1])

    def change_color(self) -> None:
        """Change the ball's color randomly."""
        self.sprite.color(random.choice(self.colors))

    def increase_speed(self, factor: float = 1.1) -> None:
        """Increase the ball's speed by the given factor."""
        self.dx *= factor
        self.dy *= factor


class ScoreBoard:
    """Score display for the game."""

    def __init__(self):
        """Initialize the scoreboard."""
        self.player1_score = 0
        self.player2_score = 0
        self.display = turtle.Turtle()
        self.display.speed(0)
        self.display.color("white")
        self.display.penup()
        self.display.hideturtle()
        self.display.goto(0, 260)
        self.update()

    def update(self) -> None:
        """Update the score display."""
        self.display.clear()
        self.display.write(f"Player 1: {self.player1_score}  Player 2: {self.player2_score}",
                          align="center", font=("Arial", 24, "normal"))

    def player1_scores(self) -> None:
        """Increment player 1's score and update the display."""
        self.player1_score += 1
        self.update()

    def player2_scores(self) -> None:
        """Increment player 2's score and update the display."""
        self.player2_score += 1
        self.update()

    def reset(self) -> None:
        """Reset both scores to zero."""
        self.player1_score = 0
        self.player2_score = 0
        self.update()


class PongGame:
    """Main game class that manages the game state and objects."""

    def __init__(self):
        """Initialize the game, screen, and game objects."""
        # Set up the game window
        self.window = turtle.Screen()
        self.window.title("Pong Game")
        self.window.bgcolor("black")
        self.window.setup(width=800, height=600)
        self.window.tracer(0)  # Turn off automatic screen updates

        # Game boundaries
        self.width = 800
        self.height = 600
        self.top_boundary = self.height / 2 - 10
        self.bottom_boundary = -self.height / 2 + 10
        self.left_boundary = -self.width / 2 + 10
        self.right_boundary = self.width / 2 - 10

        # Create game objects
        self.paddle1 = Paddle("white", (0, int(-self.height / 2 + 50)))
        self.paddle2 = Paddle("white", (0, int(self.height / 2 - 50)))
        self.ball = Ball("red")
        self.scoreboard = ScoreBoard()

        # Game state
        self.is_paused = False
        self.game_over = False
        self.winning_score = 7

        # Set up keyboard bindings
        self.setup_controls()

        # Create a message display
        self.message = turtle.Turtle()
        self.message.speed(0)
        self.message.color("white")
        self.message.penup()
        self.message.hideturtle()
        self.message.goto(0, 0)

        # Draw the center line
        self.draw_center_line()

    def draw_center_line(self) -> None:
        """Draw a dashed line in the center of the screen."""
        # Create a turtle for drawing the center line
        line = turtle.Turtle()
        line.speed(0)  # Fastest drawing speed
        line.color("white")
        line.penup()
        line.goto(-self.width / 2, 0)

        # Set the pen size to make the line more visible but not interfere with ball
        line.pensize(1)
        line.pendown()

        # Draw a dashed line
        for _ in range(40):
            line.forward(20)
            line.penup()
            line.forward(20)
            line.pendown()

        # Make sure the line doesn't interfere with the ball's movement
        line.hideturtle()
        line.penup()

    def setup_controls(self) -> None:
        """Set up keyboard controls for the game."""
        self.window.listen()

        # Player 1 controls (bottom paddle)
        self.window.onkeypress(lambda: self.paddle1.move_left(int(self.left_boundary)), "a")
        self.window.onkeypress(lambda: self.paddle1.move_right(int(self.right_boundary)), "d")

        # Player 2 controls (top paddle)
        self.window.onkeypress(lambda: self.paddle2.move_left(int(self.left_boundary)), "Left")
        self.window.onkeypress(lambda: self.paddle2.move_right(int(self.right_boundary)), "Right")

        # Game controls
        self.window.onkeypress(self.toggle_pause, "p")
        self.window.onkeypress(self.reset_game, "r")
        self.window.onkeypress(self.quit_game, "q")

    def toggle_pause(self) -> None:
        """Toggle the game's pause state."""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.show_message("Game Paused - Press 'P' to continue")
        else:
            self.message.clear()

    def reset_game(self) -> None:
        """Reset the game to its initial state."""
        self.ball.reset_position()
        self.scoreboard.reset()
        self.game_over = False
        self.is_paused = False
        self.message.clear()

    def quit_game(self) -> None:
        """Exit the game."""
        self.window.bye()

    def show_message(self, text: str) -> None:
        """Display a message on the screen."""
        self.message.clear()
        self.message.write(text, align="center", font=("Arial", 24, "normal"))

    def check_collision(self) -> None:
        """Check for collisions between the ball and other game objects."""
        # Check for collisions with paddles
        self.check_paddle_collision(self.paddle1, is_bottom=True)
        self.check_paddle_collision(self.paddle2, is_bottom=False)

        # Check for collisions with side walls (bounce without scoring)
        if self.ball.sprite.xcor() > self.right_boundary:
            self.ball.sprite.setx(self.right_boundary)
            self.ball.bounce_x()
            self.ball.change_color()

        if self.ball.sprite.xcor() < self.left_boundary:
            self.ball.sprite.setx(self.left_boundary)
            self.ball.bounce_x()
            self.ball.change_color()

        # Check for collisions with top and bottom walls (scoring)
        # When the ball hits the top wall, player 1 (bottom) scores
        if self.ball.sprite.ycor() > self.top_boundary:
            self.ball.reset_position()
            self.scoreboard.player1_scores()
            self.check_winner()
            return  # Skip other collision checks after scoring

        # When the ball hits the bottom wall, player 2 (top) scores
        if self.ball.sprite.ycor() < self.bottom_boundary:
            self.ball.reset_position()
            self.scoreboard.player2_scores()
            self.check_winner()
            return  # Skip other collision checks after scoring

    def check_paddle_collision(self, paddle, is_bottom: bool) -> None:
        """Check for collision between the ball and a paddle.

        Args:
            paddle: The paddle to check collision with
            is_bottom: True if this is the bottom paddle, False if it's the top paddle
        """
        # Check if ball and paddle rectangles overlap
        paddle_collision = (
            self.ball.sprite.xcor() + self.ball.radius > paddle.sprite.xcor() - paddle.width / 2 and
            self.ball.sprite.xcor() - self.ball.radius < paddle.sprite.xcor() + paddle.width / 2 and
            self.ball.sprite.ycor() - self.ball.radius < paddle.sprite.ycor() + paddle.height / 2 and
            self.ball.sprite.ycor() + self.ball.radius > paddle.sprite.ycor() - paddle.height / 2
        )

        if paddle_collision:
            # Determine if this is primarily a vertical or horizontal collision
            # For vertical collisions, we bounce the ball vertically
            # For horizontal collisions, we would bounce the ball horizontally (not implemented)

            # Vertical collision with bottom paddle
            if is_bottom and self.ball.dy < 0:
                self.ball.sprite.sety(paddle.sprite.ycor() + paddle.height / 2 + self.ball.radius)
                self.ball.bounce_y()
                self.ball.change_color()
                self.ball.increase_speed(1.7)
            # Vertical collision with top paddle
            elif not is_bottom and self.ball.dy > 0:
                self.ball.sprite.sety(paddle.sprite.ycor() - paddle.height / 2 - self.ball.radius)
                self.ball.bounce_y()
                self.ball.change_color()
                self.ball.increase_speed(1.7)

    def check_winner(self) -> None:
        """Check if either player has reached the winning score."""
        if self.scoreboard.player1_score >= self.winning_score:
            self.game_over = True
            self.show_message("Player 1 Wins! Press 'R' to restart")

        if self.scoreboard.player2_score >= self.winning_score:
            self.game_over = True
            self.show_message("Player 2 Wins! Press 'R' to restart")

    def run(self) -> None:
        """Main game loop."""
        try:
            while True:
                self.window.update()

                # Skip game logic if paused or game over
                if self.is_paused or self.game_over:
                    time.sleep(0.01)  # Reduce CPU usage while paused
                    continue

                # Move the ball
                self.ball.move()

                # Check for collisions
                self.check_collision()

                # Small delay to control game speed
                time.sleep(0.005)

        except turtle.Terminator:
            # Handle the case when the window is closed
            print("Game window was closed.")
        except KeyboardInterrupt:
            print("Game was interrupted by user.")
        except Exception as err:
            print(f"An unexpected error occurred: {err}")


if __name__ == "__main__":
    try:
        game = PongGame()
        game.show_message("Pong Game - Press any key to start")
        time.sleep(2)
        game.message.clear()
        game.run()
    except turtle.TurtleGraphicsError as e:
        print(f"Turtle graphics error: {e}")
    except KeyboardInterrupt:
        print("Game startup was interrupted by user.")
    except Exception as err:
        print(f"Error starting the game: {err}")
        import traceback
        traceback.print_exc()
