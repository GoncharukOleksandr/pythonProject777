from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)  ## бали гравця

    ## Відпригування кульки при колізії с панелькою гравця
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1

            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    # Швидкість ругу нашої кульки по двох осях
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # Створюємо умовний вектор
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Змушуємо кульку рухатися
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)  # це буде наший зв'язок з об'єктом кульки
    player1 = ObjectProperty(None)  # Гравець 1
    player2 = ObjectProperty(None)  # Гравець 2

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(vel[0], vel[1]).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()  # передвигаємо кульку в кажному обновленні екрану

        # перевірка відюивання кульки від панельок гравців
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # відбиття кульки по осі Y
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1  # інверсуємо дану швидкість по осі Y

        # відбиття кульки по осі X
        # тут якщо кулька змогла вийти за панельку гравця, то виходить гравець невстиг відбити кульку
        # то це значить що він програв і ми добавимо +1 бал противнику
        if self.ball.x < self.x:
            # Перший гравець програв, добавляемо 1 бал другому гравцю
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))  # заново генеруємо кульку в центрі

        if self.ball.x > self.width:
            # Другий гравець програв, добавляемо 1 бал першому гравцю
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))  # заново генеруємо кульку в центрі

    # подія доторкання до екрану
    def on_touch_move(self, touch):
        # перший гравець може доторкатися тільки своєї частини екрану (лівої)
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

        # другий гравець може доторкатися тільки своєї частини екрану (правої)
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60)  # 60 FPS
        return game


if __name__ == '__main__':
    PongApp().run()
