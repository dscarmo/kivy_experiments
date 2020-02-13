from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            y_offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            if bounced.distance(Vector(0, 0)) < ball.max_speed:
                vel = bounced * 1.1
            else:
                vel = bounced
            ball.velocity = vel.x, vel.y + y_offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    max_speed = 30

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class MiddleLine(Widget):
    pass


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    prt = ObjectProperty(None)
    print_obj = ObjectProperty(None)
    mid_line = ObjectProperty(None)

    def start(self, dt=None):
        self.prt = ""
        self.ball.size = (50, 50)
        self.mid_line.size = 10, self.height
        self.player1.center_y = self.height / 2
        self.player2.center_y = self.height / 2
        self.player1.score = 0
        self.player2.score = 0
        self.serve_ball()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def serve_ball(self, vel=(5, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        winner = None
        if self.player1.score >= 1:
            winner = '1'
        elif self.player2.score >= 1:
            winner = '2'

        if winner is not None:
            self.ball.size = (0, 0)
            self.mid_line.size = (0, 0)
            self.prt = "Player {} wins!".format(winner)
            Clock.unschedule(self.update)
            Clock.schedule_once(self.start, 3)

        # self.prt = "Vx: {}, Vy: {}".format(round(self.ball.velocity_x, 2), round(self.ball.velocity_y, 2))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.start()
        return game


if __name__ == '__main__':
    PongApp().run()
