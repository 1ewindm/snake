import tkinter
from random import randint, random

SIDE = 700
SNAKE_SIZE = 25


class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.circle = None
        self.create()

    def create(self):
        number_of_columns = SIDE // SNAKE_SIZE
        x = randint(0, number_of_columns-1) * SNAKE_SIZE
        y = randint(0, number_of_columns-1) * SNAKE_SIZE

        food_color = randint(1, 4)
        if food_color == 1:
            food_color = 'red'
        elif food_color == 2:
            food_color = 'blue'
        elif food_color == 3:
            food_color = 'yellow'
        elif food_color == 4:
            food_color = 'brown'
        self.circle = self.canvas.create_rectangle(
            x, y,
            x + SNAKE_SIZE, y + SNAKE_SIZE,

            fill=food_color,
            tag='food'
        )


    def recreate(self):
        self.canvas.delete("food")
        self.create()


class Snake:
    def __init__(self, window, canvas):
        self.window = window
        self.canvas = canvas
        self.body = [
            self.canvas.create_rectangle(
                (SIDE//2 - SNAKE_SIZE, SIDE//2 - SNAKE_SIZE),
                (SIDE//2, SIDE//2),
                fill='#00FF00'
            )
        ]
        self.direction = 'space'  # pause
        self.direction_x = 0
        self.direction_y = 0

    def move(self, food):

        global score
        for i in range (len(self.body) - 1, 0, -1):
            prev_x, prev_y, _, _ = self.canvas.coords(self.body[i-1])
            curr_x, curr_y, _, _ = self.canvas.coords(self.body[i])
            self.canvas.move(self.body[i], prev_x - curr_x, prev_y - curr_y)
        self.canvas.move(self.body[0], self.direction_x, self.direction_y)
        if self.collide_food(food):
            score += 1
            self.grow(food)
            label.config(text=f"Score{score}")
            food.recreate()
        self.fix_overflow()
        self.window.after(251, self.move, food)

    def fix_overflow(self):
        for part in self.body:
            x0, y0, x1, y1 = self.canvas.coords(part)
            if self.direction == 'Up' and y0 < 0:
                self.canvas.move(part, 0, SIDE)
            elif self.direction == 'Down' and y1 > SIDE:
                self.canvas.move(part, 0, -SIDE)
            if self.direction == 'Left' and x0 < 0:
                self.canvas.move(part, SIDE, 0)
            if self.direction == 'Right' and x1 > SIDE:
                self.canvas.move(part, -SIDE, 0)

    def turn(self, event):
        if event.keysym == 'Up' and self.direction != 'Down':
            self.direction_x = 0
            self.direction_y = -SNAKE_SIZE
            self.direction = event.keysym
        elif event.keysym == 'Down' and self.direction != 'Up':
            self.direction_x = 0
            self.direction_y = SNAKE_SIZE
            self.direction = event.keysym
        elif event.keysym == 'Left' and self.direction != 'Right':
            self.direction_x = -SNAKE_SIZE
            self.direction_y = 0
            self.direction = event.keysym
        elif event.keysym == 'Right' and self.direction != 'Left':
            self.direction_x = SNAKE_SIZE
            self.direction_y = 0
            self.direction = event.keysym
        elif event.keysym == 'space':
            self.direction_x = 0
            self.direction_y = 0
            self.direction = event.keysym

    def collide_food(self, food):
        head_x, head_y, _, _ = self.canvas.coords(self.body[0])
        food_x, food_y, _, _ = self.canvas.coords(food.circle)
        if head_x == food_x and head_y == food_y:
            return True
        return False

    def grow(self, food):

        x0, y0, x1, y1 = self.canvas.coords(self.body[-1])
        new_part = self.canvas.create_rectangle(
            (x0 + self.direction_x, y0 + self.direction_y),
            (x1 + self.direction_x, y1 + self.direction_y),
            fill='#00FF00'

        )
        self.body.append(new_part)


score = 0
window = tkinter.Tk()
canvas = tkinter.Canvas(window, bg='black', height=SIDE, width=SIDE)
label = tkinter.Label(window, text=f'Score = {score}')
snake = Snake(window, canvas)
food = Food(canvas)
label.pack()
canvas.pack()

window.bind('<KeyPress>', snake.turn)
snake.move(food)
window.mainloop()
