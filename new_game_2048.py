import random

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
    def destroy(self):
        self.game.table[self.y][self.x] = None

class Field:
    def __init__(self):
        self.table = [[None for i in range(4)] for i in range(4)]
        # создание ОДНОЙ рандомной точки (вторая генерируется в модуле self.run)
        self.gen_new_point()
        # self.table[0][0] = Point(self, 0, 0)
        # self.table[0][1] = Point(self, 0, 1)
    def gen_new_point(self):
        while True:
            pos = [random.randint(0,3) for i in range(2)]
            if self.table[pos[0]][pos[1]] == None:
                self.table[pos[0]][pos[1]] = Point(self, *pos)
                break
    def command(self):
        commands = ['right', 'left', 'up', 'down']
        while True:
            user = input('Go: ')
            if user in commands:
                return user
            else:
                print('Incorrect input')
    def show(self):
        for y in range(len(self.table)):
            for x in range(len(self.table[y])):
                print('_____' if self.table[y][x]==None else ' '*(5-len(str(self.table[y][x].points))) +str(self.table[y][x].points), end=' ')
            print()
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

    def run(self):
        end = False
        while not end:
            # каждый ход генерируем новую точку
            self.gen_new_point()

            # показываем игровое поле
            self.show()

            # проверка на проигрыш
            self.lose_cheak()

            # ввод пользователя и работа с полем
            user = self.command()
            self.slide(user)

Game = Field()
Game.run()
