import tkinter
import random

#CONSTANTS
WIDTH = 640
HEIGHT = 480
BG_COLOR = 'white'
BALL_COLOR = 'lightgreen'
BAD_COLOR = 'red'
BLACK_COLOR = 'black'
COLORS = [BAD_COLOR, 'pink', 'aqua', 'gold', 'yellow', 'fuchsia']
ZERO = 0
BALL_RADIUS = 30
DELAY = 3
NUNBER_OF_BALLS = 3

#balls class
class Ball():
    def __init__(self, x, y, r, color, dx=0, dy=0 ):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy
        
    def draw(self):
        canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.color, outline = self.color if self.color != BAD_COLOR else BLACK_COLOR)
    
    def hide(self):
        canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=BG_COLOR, outline=BG_COLOR)

    def is_collision(self, ball):
        a = abs(self.x + self.dx - ball.x)
        b = abs(self.y +self.dy - ball.y)
        return (a*a + b*b)**0.5 <= self.r + ball.r

    def move(self):
        #colliding with walls
        if(self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= ZERO ):
            self.dx = -self.dx
        if(self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dy <= ZERO ):
            self.dy = -self.dy
        #colliding with balls
        for ball in balls:
            if self.is_collision(ball):
                if ball.color != BAD_COLOR:
                    ball.hide()
                    balls.remove(ball)
                    self.dx = -self.dx
                    self.dy = -self.dy
                else: 
                    self.dx = self.dy = 0
        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()

#mouse events
def mouse_click(event):
    global main_ball
    if event.num == 1:
        if 'main_ball' not in globals():
            main_ball = Ball(event.x, event.y, BALL_RADIUS, BALL_COLOR, 1, 1)
            main_ball.draw()
        else : #turn left
            if main_ball.dx * main_ball.dy > 0 :
                main_ball.dy = - main_ball.dy
            else : 
                main_ball.dx = - main_ball.dx
    elif event.num == 3 : #turn right
        if main_ball.dx * main_ball.dy > 0 :
            main_ball.dx = - main_ball.dx
        else : 
            main_ball.dy = - main_ball.dy
        
#count of bad balls
def count_bad_balls(list):
    res = 0
    for ball in list:
        if ball.color == BAD_COLOR:
            res += 1
    return res
    
#create random list of balls 
def create_list_of_balls(number):
    list = []
    while len(list) < number :
        next_ball = Ball(
                    random.choice(range(ZERO, WIDTH)), 
                    random.choice(range(ZERO, HEIGHT)), 
                    random.choice(range(15, 35)), 
                    random.choice(COLORS))
        next_ball.draw()
        list.append(next_ball)
    return list

#main cicle game
def main():
    if 'main_ball' in globals():
        main_ball.move()  
        if len(balls) - num_of_bad_balls == 0: 
            canvas.create_text(WIDTH/2, HEIGHT/2, text="You are win", font = "Arial 20")
            main_ball.dx = main_ball.dy = 0
        elif main_ball.dx == 0:
            canvas.create_text(WIDTH/2, HEIGHT/2, text="You are lose", font = "Arial 20")
    root.after(DELAY, main)
     

root = tkinter.Tk()
root.title('Colliding balls')
canvas = tkinter.Canvas(root, width = WIDTH, height = HEIGHT, bg = BG_COLOR)
canvas.pack()
canvas.bind('<Button 1>', mouse_click)
canvas.bind('<Button 3>', mouse_click)
if 'main_ball' in globals():
    del main_ball
balls = create_list_of_balls(NUNBER_OF_BALLS)
num_of_bad_balls = count_bad_balls(balls)
main()
root.mainloop()