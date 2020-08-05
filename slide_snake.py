################################################################
############ Developed by - Rishikesh Sarode ###################
################################################################
# rishisarode99@gmail.com

import tkinter as tk
from tkinter import *
import time
import random
import math


class SlideSnake:

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry('400x700')
        self.root.title('Slide Snake')
        self.root.resizable(0, 0)
        self.ball_queue = []
        self.nballs = 5
        self.r = 10
        self.bally = 350
        self.x = 192
        self.y = self.bally
        self.startCount = 0
        self.stopFlag = False
        self.brick_queue = []
        self.ball_bonus = []
        self.gap = 2001
        self.score = 0
        self.score_ = 0
        self.max_score = 0
        self.frameRate = 15
        self.collision = []
        self.text = 'white'
        self.bg = 'black'
        self.brickcolor = {
            1: 'purple1',
            2: 'purple2',
            3: 'purple3',
            4: 'purple4',
            5: 'chocolate1',
            6: 'chocolate2',
            7: 'chocolate3',
            8: 'red1',
            9: 'red2',
            10: 'red3',
        }
        self.bonus_color = {
            1: 'LightSkyBlue2',
            2: 'RoyalBlue1',
            3: 'SlateBlue4',}
        self.theme_text = StringVar()
        self.theme_text.set('Light Theme')

    def buildGame(self):
        self.prebuild()
        self.root.bind('<Motion>', self.motion)
        self.root.mainloop()

    def prebuild(self):
        self.main_frame = Frame(self.root, relief=SUNKEN, bd=2, bg='grey91').place(x=4, y=90, height=606, width=392)
        self.canvas = self.draw_canvas(self.main_frame)
        self.Button_(self.root, 'start', self.start, 30, 60, 10, 10)
        self.Button_(self.root, 'stop', self.stop, 30, 60, 80, 10)
        self.Button_(self.root, 'Restart', self.restart, 30, 80, 150, 10)
        self.Button_(self.root, self.theme_text.get(), self.changeTheme, 30, 100, 10, 50)
        self.Button_(self.root, 'About', self.info_display, 30, 60, 330, 10)
        self.ball_queue = []
        for x in range(self.nballs):
            ball = Ball()
            ball.x, ball.y = 195, self.bally + 2*x*ball.r
            self.ball_queue.append(ball)
        self.canvas.delete('All')
        self.canvas.create_text(200, 300, fill=self.text, font="Times 20 italic bold",
                                text="Click start to play")


        for ball in self.ball_queue:
            if self.x < ball.r: ball.x = ball.r
            if self.x > 390- ball.r: self.x = 390 - ball.r
            x = 390/2
            self.canvas.create_oval(x - ball.r, ball.y - ball.r, x + ball.r, ball.y + ball.r, fill=self.rgb(ball.color))
        self.canvas.update_idletasks()

    def start(self):
        self.stopFlag = False
        self.updater()

    def changeTheme(self):

        if self.bg == 'white':
            self.theme_text.set('Light Theme')
            self.text = 'white'
            self.bg = 'black'
        else:
            self.theme_text.set('Dark Theme')
            self.text = 'black'
            self.bg = 'white'

        self.stop()
        self.prebuild()


    def setLight(self):
        self.text = 'black'
        self.bg = 'white'
        self.stop()
        self.prebuild()

    def draw_canvas(self,frame):
        c = Canvas(frame, bg=self.bg)
        c.place(x=6, y=92,  height=604, width=390)
        return c


    def Button_(self, root, text, command, h, w, x, y):
        button = Button(master=root, text=text, command=command, fg='grey91')
        button.place(bordermode=OUTSIDE, height=h, width=w, y=y, x=x)
        return button

    def motion(self,event):
        x, y = event.x, event.y
        self.x,self.y = x,y
        # print (self.x,self.y, event.state, event.x_root,event.y_root)

    def update_canvas(self):

        self.canvas.delete("all")
        for ball in self.ball_bonus:
            self.canvas.create_oval(ball.x - ball.r, ball.y - ball.r, ball.x + ball.r, ball.y + ball.r, fill=self.bonus_color[ball.add])
            self.canvas.create_text(ball.x +3, ball.y - 2*ball.r , fill=self.text, font=("Purisa", 15),text=str(ball.add), )

        for ball in self.ball_queue:
            if self.x < ball.r: ball.x = ball.r
            if self.x > 390- ball.r: self.x = 390 - ball.r
            self.canvas.create_oval(ball.x - ball.r, ball.y - ball.r, ball.x + ball.r, ball.y + ball.r, fill=self.rgb(ball.color))

        if self.ball_queue:
            ball0 = self.ball_queue[0]
            self.canvas.create_text(ball0.x + 2*ball0.r, ball0.y, fill=self.text, font=("Purisa", 15),text=str(len(self.ball_queue)), )

        for brick in self.brick_queue:

            self.canvas.create_rectangle(brick.x , brick.y, brick.x + brick.l ,brick.y+ brick.l,fill=self.brickcolor[brick.power])
            self.canvas.create_text(brick.x + brick.l/3 ,brick.y + brick.l/3 ,fill="darkblue",font=("Purisa", 15),text=str(brick.power), )

        temp = []
        for col in self.collision:
            if col.r < 60:
                self.canvas.create_oval(col.x - col.r, col.y - col.r, col.x + col.r, col.y + col.r, outline=self.text)
                col.r *= 2
            else:temp.append(col)

        for x in temp: self.collision.remove(x)

        self.canvas.create_text(4,10, fill=self.text, font=("Purisa", 15),text='score: {}'.format(self.score), anchor='w')
        self.canvas.create_text(4,30, fill=self.text, font=("Purisa", 15),text='High score: {}'.format(self.max_score), anchor='w')
        self.canvas.update_idletasks()

    def update_obj_loc(self):

        tempx = self.x
        for ball in self.ball_queue:
            x_ = ball.x
            ball.x = tempx
            tempx = x_

        if not self.check_collision():
            temp = []
            for brick in self.brick_queue:
                if brick.y >  700:
                    temp.append(brick)
                    continue
                brick.y += self.frameRate
            [self.brick_queue.remove(x) for x in temp]

            temp = []
            for bonus in self.ball_bonus:
                if bonus.y > 700:
                    temp.append(bonus)
                bonus.y += self.frameRate
            [self.ball_bonus.remove(x) for x in temp]
        else:
            if self.ball_queue:
                ball = self.ball_queue[0]
                for brick in self.brick_queue:
                    brick.y -= 2*ball.r
                for b_ in self.ball_bonus:
                    b_.y -= 2*ball.r


    def restart(self):

        self.stop()
        self.prebuild()
        self.start()

    def stop(self):
        self.startCount = 0
        self.score = 0
        self.score_ = 0
        self.ball_queue = []
        self.brick_queue = []
        self.ball_bonus = []
        self.collision = []
        self.stopFlag=True

    def addBricks(self):

        a = list(range(0,8))
        for _ in range(random.randint(0,8)):
            x_ = random.choice(a)
            a.remove(x_)
            brick = Brick()
            brick.x = x_*(390/8)
            brick.l = (390/8)
            brick.y = -1 * brick.l
            brick.power = random.randint(1,10)
            self.brick_queue.append(brick)


    def add_bonus(self):

            flag = random.choice([0,1])
            if flag == 1:
                bonus = Ball()
                bonus.x = random.randint(1, 390)
                bonus.y = -random.randint(1, 200)
                bonus.add = random.randint(1,3)
                self.ball_bonus.append(bonus)

    def check_collision(self):

        ball = self.ball_queue[0]
        prox = []
        for brick in self.brick_queue:
            if (brick.x  < ball.x - ball.r < brick.x + brick.l or brick.x <  ball.x + ball.r < brick.x + brick.l) and brick.y+brick.l > ball.y > brick.y:
                prox.append(brick)

        if len(prox)>1:
                for brick in prox:
                    if brick.x  < ball.x + ball.r < brick.x + brick.l :
                        if brick.power == 1:
                            self.brick_queue.remove(brick)
                        else:
                            brick.power -=1
                        self.remove_ball_from_snake()
                        return True

        elif len(prox)==1:
                brick = prox[0]
                if brick.power == 1:
                    self.brick_queue.remove(brick)
                else:
                    brick.power -= 1
                self.remove_ball_from_snake()
                return True
        return False


    def add_ball_to_snake(self):

        ball = Ball()
        for b_ in self.ball_queue: b_.y += ball.r * 2
        ball.x = self.x
        ball.y = self.bally
        self.ball_queue.insert(0,ball )


    def remove_ball_from_snake(self):

        ball = self.ball_queue.pop(0)
        self.collision.append(ball)
        for b_ in self.ball_queue: b_.y -= ball.r * 2


    def eatBonus(self):

        ball = self.ball_queue[0]
        temp = []
        for bonus in self.ball_bonus:
            if bonus.x - 2*bonus.r <  ball.x < bonus.x + 2*bonus.r and bonus.y - bonus.r <  ball.y < bonus.y + 2*bonus.r:
                bonus.y = self.bally
                for x in range(bonus.add):
                    self.add_ball_to_snake()
                temp.append(bonus)
        [self.ball_bonus.remove(x) for x in temp]


    def start_counter(self):

        self.canvas.delete('all')
        self.canvas.create_text(200, 300, fill=self.text, font="Times 20 italic bold",text="Ready in {}".format(2 - self.startCount + 1))
        if self.ball_queue:
            ball0 = self.ball_queue[0]
            self.canvas.create_text(ball0.x + 2*ball0.r, ball0.y, fill=self.text, font=("Purisa", 15),text=str(len(self.ball_queue)), )
        for ball in self.ball_queue:
            if self.x < ball.r: ball.x = ball.r
            if self.x > 390- ball.r: self.x = 390 - ball.r
            x = 390/2
            self.canvas.create_oval(x - ball.r, ball.y - ball.r, x + ball.r, ball.y + ball.r, fill=self.rgb(ball.color))
        self.canvas.update_idletasks()
        self.startCount += 1



    def frame_update(self):

        if len(self.ball_queue):
            self.gap += 1
            diff = 2 * int(self.score_ / 200)
            if diff > 40: diff = 40
            if self.gap > 50 - diff:
                self.score += 1
                self.gap = 0
                self.addBricks()
                self.add_bonus()
            self.eatBonus()
            self.update_obj_loc()
            self.update_canvas()
            return False
        else:
            if self.score >= self.max_score:
                self.max_score = self.score
                self.canvas.create_text(200, 500, fill=self.text,
                                        font=("Purisa", 25),
                                        text="New Max Score: {}".format(self.score), )
            else:
                self.canvas.create_text(200, 500, fill=self.text,
                                        font=("Purisa", 25),
                                        text="Score: {}".format(self.score), )
            return True


    def updater(self):

        if not self.stopFlag:
            if self.startCount < 3:
                after = 1000
                self.start_counter()
            else:
                exit =  self.frame_update()
                after = 30
                if exit:
                    return
            self.score_ += 1
            self.root.after(after, self.updater)
        else:
            self.stop()
            self.prebuild()


    def rgb(self,color):
       return  "#{0:02x}{1:02x}{2:02x}".format(color[0], color[1], color[2])


    def info_display(self):
        root = Tk()
        root.title('About')
        root.geometry('400x200')
        TextBox = Text(root, relief=SUNKEN, bd=1, height='12', width='54', wrap=WORD, bg='grey91')
        TextBox.insert(END, "Name          : Slide Snake\n")
        TextBox.insert(END, "Version       : v_00.1\n")
        TextBox.insert(END, "Uploaded on   : 06/August/2020\n")
        TextBox.insert(END, "Developer     : Rishikesh Sarode\n")
        TextBox.insert(END, "Contact       : rishisarode99@gmail.com\n")
        TextBox.insert(END, "Github        : https://github.com/rishi-99\n")
        TextBox.place(x=5, y=5)
        TextBox.config(state=DISABLED)
        root.mainloop()


class Ball:

    def __init__(self):
        self.r = 10
        self.x = 0
        self.y = 0
        self.color = (random.randint(50,255),random.randint(50,255),random.randint(50,255))

class Brick:

    def __init__(self):
        self.l = 100
        self.x = 0
        self.y = 0
        self.power = 10



if '__main__' == __name__:

    game = SlideSnake()
    game.buildGame()
