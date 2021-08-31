import pygame
import random
import time
import os
# ----------
# Не забудь, сделать запрет на движение в ту сторону,
# в которую больше двигатся невозможно (безсмысленно)
# ---------
dis_resol = {'height':600, 'width':500}

color = {'2'   :(219,215,210), 'bg'   : (113,89,86),
         '4'   :(201,190,156), 'hole' : (169,120,117),
         '8'   :(244,164,96),
         '16'  :(233,150,122), # 233 150 122
         '32'  :(222,99,133),
         '64'  :(184,59,94),
         '128' :(252,217,117),
         '256' :(218,216,113),
         '512' :(69,206,162),
         '1024':(128,218,235)
         }
total_score = 0
# ----------
pygame.init()
# open the window
window = pygame.display.set_mode((dis_resol['width'], dis_resol['height']))
pygame.display.set_caption('2048')
pygame.display.update()
# ==========
class Point:
    def __init__(self, field, y:int, x:int, score:int=0):
        self.game = field
        self.y:int = y
        self.x:int = x
        self.points:int = random.choice((2,4)) if score==0 else score
    def slide_right(self):
        # пробегаемся по строке до конца
        if self.x==3:
            return

        for x in range(self.x+1, 4):
            inspecting_dot = self.game.table[self.y][x]
            if inspecting_dot == None:
                continue
            if inspecting_dot.points == self.points:
                inspecting_dot.next_score()
                self.destroy()
                break
            else:
                if self.x != x-1:
                    self.game.table[self.y][x-1] = Point(self.game, self.y, x-1, self.points)
                    self.destroy()
                break
        else:
            self.game.table[self.y][3] = Point(self.game, self.y, 3, self.points)
            self.destroy()
    def slide_left(self):
        if self.x==0:
            return

        for x in range(self.x-1, -1, -1):
            inspecting_dot = self.game.table[self.y][x]
            if inspecting_dot == None:
                continue
            if inspecting_dot.points == self.points:
                inspecting_dot.next_score()
                self.destroy()
                break
            else:
                if self.x != x+1:
                    self.game.table[self.y][x+1] = Point(self.game, self.y, x+1, self.points)
                    self.destroy()
                break
        else:
            self.game.table[self.y][0] = Point(self.game, self.y, 0, self.points)
            self.destroy()
    def slide_up(self):
        if self.y == 0:
            return

        for y in range(self.y-1, -1, -1):
            inspecting_dot = self.game.table[y][self.x]
            if inspecting_dot == None:
                continue
            if inspecting_dot.points == self.points:
                inspecting_dot.next_score()
                self.destroy()
                break
            else:
                if self.y != y+1:
                    self.game.table[y+1][self.x] = Point(self.game, y+1, self.x, self.points)
                    self.destroy()
                break
        else:
            self.game.table[0][self.x] = Point(self.game, 0, self.x, self.points)
            self.destroy()
    def slide_down(self):
        if self.y == 3:
            return

        for y in range(self.y+1, 4):
            inspecting_dot = self.game.table[y][self.x]
            if inspecting_dot == None:
                continue
            if inspecting_dot.points == self.points:
                inspecting_dot.next_score()
                self.destroy()
                break
            else:
                if self.y != y-1:
                    self.game.table[y-1][self.x] = Point(self.game, y-1, self.x, self.points)
                    self.destroy()
                break
        else:
            self.game.table[3][self.x] = Point(self.game, 3, self.x, self.points)
            self.destroy()
    def next_score(self):
        self.points *= 2
        global total_score
        total_score += self.points
    def destroy(self):
        self.game.table[self.y][self.x] = None

class Field:
    def __init__(self):
        self.table = [[None for i in range(4)] for i in range(4)]
        # создание ОДНОЙ рандомной точки (вторая генерируется в модуле self.run)
        self.gen_new_point()
    def gen_new_point(self):
        while True:
            pos = [random.randint(0,3) for i in range(2)]
            if self.table[pos[0]][pos[1]] == None:
                self.table[pos[0]][pos[1]] = Point(self, *pos)
                break
    def show(self):
        # os.system('cls||clear')
        # for y in range(len(self.table)):
        #     for x in range(len(self.table[y])):
        #         print('_____' if self.table[y][x]==None else ' '*(5-len(str(self.table[y][x].points))) +str(self.table[y][x].points), end=' ')
        #     print()
        # ----
        # Фон
        window.fill(color['bg'])
        # интерфейс
        f2 = pygame.font.SysFont('serif', 50)
        text2 = f2.render('Score: ' + str(total_score), 1, (225, 225, 225))
        window.blit(text2, (dis_resol['width']/2-80, 20))
        # игровое поле
        x_pos = 0
        y_pos = 100
        side_of_window = dis_resol['width']
        numb_of_side_blocks = 4
        a = (5*side_of_window)/(6*numb_of_side_blocks+1)
        b = side_of_window/(6*numb_of_side_blocks+1)
        for y in range(len(self.table)):
            y_pos += b
            x_pos = 0
            for x in range(len(self.table[y])):
                x_pos += b
                if self.table[y][x] != None:
                    pygame.draw.rect(window, color[str(self.table[y][x].points)], (x_pos, y_pos, a, a))
                else:
                    pygame.draw.rect(window, color['hole'], (x_pos, y_pos, a, a))
                x_pos += a
            y_pos += a

        pygame.display.update()
    def slide(self, der:str):
        if der == 'right':
            for x in range(3,-1,-1):
                for y in range(4):
                    if self.table[y][x] != None:
                        self.table[y][x].slide_right()
        elif der == 'left':
            for x in range(4):
                for y in range(4):
                    if self.table[y][x] != None:
                        self.table[y][x].slide_left()
        elif der == 'up':
            for y in range(3, -1, -1):
                for x in range(4):
                    if self.table[y][x] != None:
                        self.table[y][x].slide_up()
        elif der == 'down':
            for y in range(3, -1, -1):
                for x in range(4):
                    if self.table[y][x] != None:
                        self.table[y][x].slide_down()
    def lose_cheak(self):
        # иначе проверяем, есть ли по соседству две одинаковые клетки
        for y in range(len(self.table)):
            for x in range(len(self.table)):
                inspecting_dot = self.table[y][x]
                if inspecting_dot == None:
                    return False
                # слева клетки
                if x != 0 and inspecting_dot.points == self.table[y][x-1].points:
                    return False
                # сверху клетки
                if y != 0 and inspecting_dot.points == self.table[y-1][x].points:
                    return False
                # справа клетки
                if x != 3 and inspecting_dot.points == self.table[y][x+1]:
                    return False
                # снизу клетки
                if y != 3 and inspecting_dot.points == self.table[y+1][x]:
                    return False
        else:
            return True
    def win_cheak(self):
        def f(lst:list):
            for y in lst:
                for x in y:
                    yield x
        for i in f(self.table):
            if i != None:
                if i.points == 2048:
                    return True
        else:
            return False
    def is_holes_here(self):
        def f(lst:list):
            for y in lst:
                for x in y:
                    yield x
        for i in f(self.table):
            if i == None:
                return True
        else:
            return False
    def run(self):
        game_end = False
        user = 1
        while not game_end:
            # каждый ход генерируем новую точку
            if user != None and self.is_holes_here():
                self.gen_new_point()

            user = None
            # показываем игровое поле
            self.show()

            # проверка на выигрыш
            if self.win_cheak():
                print('-----------------')
                print('You won')
                print('-----------------')
                time.sleep(5)
                game_end = True

            # проверка на проигрыш
            if self.lose_cheak():
                print('-----------------')
                print('You lost')
                print('-----------------')
                time.sleep(5)
                game_end = True

            # ввод пользователя и работа с полем
            # user = self.command()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        user = 'up'
                    elif event.key == pygame.K_LEFT:
                        user = 'left'
                    elif event.key == pygame.K_RIGHT:
                        user = 'right'
                    elif event.key == pygame.K_DOWN:
                        user = 'down'
            if user != None:
                self.slide(user)
            time.sleep(0.01)

Game = Field()
Game.run()
