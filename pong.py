import turtle as tl
import winsound
import random
import tkinter as tk


class PONG:
    def __init__(self):
        self.create_window()
        self.leftpaddle()
        self.rightpaddle()
        self.create_ball()
        self.create_score()
        self.create_powerup()
        self.keys()
        self.game_paused = False
        self.play_background_music()
        self.game()

    def create_window(self):
        self.root = tl.Screen()
        self.root.title("PONG GAME")
        self.root.bgcolor("black")
        self.root.setup(width=800, height=600)
        self.root.tracer(0)

    def leftpaddle(self):
        self.left_paddle = tl.Turtle()
        self.left_paddle.speed(0)
        self.left_paddle.shape('square')
        self.left_paddle.color('blue')
        self.left_paddle.shapesize(stretch_wid=6, stretch_len=1)
        self.left_paddle.penup()
        self.left_paddle.goto(-350, 0)

    def rightpaddle(self):
        self.right_paddle = tl.Turtle()
        self.right_paddle.speed(0)
        self.right_paddle.shape('square')
        self.right_paddle.color('red')
        self.right_paddle.shapesize(stretch_wid=6, stretch_len=1)
        self.right_paddle.penup()
        self.right_paddle.goto(350, 0)

    def create_ball(self):
        self.ball = tl.Turtle()
        self.ball.speed(1)
        self.ball.shape('square')
        self.ball.color('white')
        self.ball.penup()
        self.reset_ball_position()

    def reset_ball_position(self):
        self.ball.goto(random.randint(-200, 200), random.randint(-150, 150))
        self.ball_direction_x = random.choice([0.15, -0.15])
        self.ball_direction_y = random.choice([0.15, -0.15])

    def create_score(self):
        self.left_score = 0
        self.right_score = 0
        self.score_display = tl.Turtle()
        self.score_display.speed(0)
        self.score_display.color('white')
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(0, 260)
        self.update_score()

    def update_score(self):
        self.score_display.clear()
        self.score_display.write("Player 1: {}  Player 2: {}".format(self.left_score, self.right_score), align="center", font=("Courier", 24, "normal"))

    def left_paddle_up(self):
        y = self.left_paddle.ycor()
        if y < 250:
            y += 20
        self.left_paddle.sety(y)

    def left_paddle_down(self):
        y = self.left_paddle.ycor()
        if y > -240:
            y -= 20
        self.left_paddle.sety(y)

    def right_paddle_up(self):
        y = self.right_paddle.ycor()
        if y < 250:
            y += 20
        self.right_paddle.sety(y)

    def right_paddle_down(self):
        y = self.right_paddle.ycor()
        if y > -240:
            y -= 20
        self.right_paddle.sety(y)

    def toggle_pause(self):
        self.game_paused = not self.game_paused

    def keys(self):
        self.root.listen()
        self.root.onkeypress(self.left_paddle_up, "w")
        self.root.onkeypress(self.left_paddle_down, "s")
        self.root.onkeypress(self.right_paddle_up, "o")
        self.root.onkeypress(self.right_paddle_down, "k")
        self.root.onkeypress(self.toggle_pause, "p")

    def play_sound(self, sound):
        winsound.PlaySound(sound, winsound.SND_ASYNC)

    def play_background_music(self):
        winsound.PlaySound("background.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

    def create_powerup(self):
        self.powerup = tl.Turtle()
        self.powerup.speed(0)
        self.powerup.shape('triangle')
        self.powerup.color('yellow')
        self.powerup.penup()
        self.powerup.shapesize(stretch_wid=1.5, stretch_len=1.5)
        self.powerup.goto(1000, 1000)  # Initially place it off-screen
        self.powerup_active = False

    def spawn_powerup(self):
        if not self.powerup_active:
            self.powerup_active = True
            self.powerup.goto(random.randint(-350, 350), random.randint(-250, 250))

    def check_powerup_collision(self):
        if self.ball.distance(self.powerup) < 20:
            self.powerup.goto(1000, 1000)  # Move the power-up off-screen after collision
            self.powerup_active = False
            self.apply_powerup_effect()

    def apply_powerup_effect(self):
        effect = random.choice(['increase_paddle_left', 'increase_paddle_right', 'decrease_paddle_left', 'decrease_paddle_right', 'speed_boost', 'speed_slow'])
        if effect == 'increase_paddle_left':
            self.left_paddle.shapesize(stretch_wid=8, stretch_len=1)
        elif effect == 'increase_paddle_right':
            self.right_paddle.shapesize(stretch_wid=8, stretch_len=1)
        elif effect == 'decrease_paddle_left':
            self.left_paddle.shapesize(stretch_wid=4, stretch_len=1)
        elif effect == 'decrease_paddle_right':
            self.right_paddle.shapesize(stretch_wid=4, stretch_len=1)
        elif effect == 'speed_boost':
            self.ball_direction_x *= 1.5
            self.ball_direction_y *= 1.5
        elif effect == 'speed_slow':
            self.ball_direction_x *= 0.5
            self.ball_direction_y *= 0.5

    def game(self):
        powerup_timer = 0
        speed_increase_timer = 0
        while True:
            self.root.update()
            if not self.game_paused:
                self.ball.setx(self.ball.xcor() + self.ball_direction_x)
                self.ball.sety(self.ball.ycor() + self.ball_direction_y)

                # Border collision check for y-axis
                if self.ball.ycor() > 290:
                    self.ball.sety(290)
                    self.ball_direction_y *= -1
                    self.play_sound("bounce.wav")

                if self.ball.ycor() < -290:
                    self.ball.sety(-290)
                    self.ball_direction_y *= -1
                    self.play_sound("bounce.wav")

                # Border collision check for x-axis (scoring)
                if self.ball.xcor() > 390:
                    self.reset_ball_position()
                    self.ball_direction_x *= -1
                    self.left_score += 1
                    self.update_score()
                    self.play_sound("score.wav")
                    self.reset_ball_speed()

                if self.ball.xcor() < -390:
                    self.ball.goto(0, 0)
                    self.ball_direction_x *= -1
                    self.right_score += 1
                    self.update_score()
                    self.play_sound("score.wav")
                    self.reset_ball_speed()

                # Paddle collision check
                if (340 < self.ball.xcor() < 350) and (self.right_paddle.ycor() - 50 < self.ball.ycor() < self.right_paddle.ycor() + 50):
                    self.ball.setx(340)
                    self.ball_direction_x *= -1
                    self.play_sound("bounce.wav")

                if (-350 < self.ball.xcor() < -340) and (self.left_paddle.ycor() - 50 < self.ball.ycor() < self.left_paddle.ycor() + 50):
                    self.ball.setx(-340)
                    self.ball_direction_x *= -1
                    self.play_sound("bounce.wav")

                # Powerup spawning and collision check
                powerup_timer += 1
                if powerup_timer > 500:
                    self.spawn_powerup()
                    powerup_timer = 0
                self.check_powerup_collision()

                # Gradually increase ball speed
                speed_increase_timer += 1
                if speed_increase_timer > 1000:  # Adjust this value to control speed increase frequency
                    self.ball_direction_x *= 1.01
                    self.ball_direction_y *= 1.01
                    speed_increase_timer = 0

                # Check for game over
                if self.left_score >= 10 or self.right_score >= 10:
                    self.end_game()

    def reset_ball_speed(self):
        self.ball_direction_x = 0.15 if self.ball_direction_x > 0 else -0.15
        self.ball_direction_y = 0.15 if self.ball_direction_y > 0 else -0.15

    def end_game(self):
        self.ball.goto(0, 0)
        self.ball_direction_x = 0
        self.ball_direction_y = 0
        self.score_display.goto(0, 0)
        if self.left_score >= 10:
            winner = "Player 1 Wins!"
        else:
            winner = "Player 2 Wins!"
        self.score_display.write(winner, align="center", font=("Courier", 36, "normal"))
        self.play_sound("gameover.wav")
        self.root.update()
        self.root.bye()

def main():
    PONG()

if __name__ == '__main__':
    main()
