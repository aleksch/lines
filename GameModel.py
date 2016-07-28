import sys
import random


class GameModel:
    '''класс в котором происходят изменения с игровым полем
    в класс передаётся ширина и высота доски,
    колличество цветов для игры,
    поле предстовляется двумерным масивом в котором 0 - пустая ячеика,
    от 1 до amountColors различные цвета шаров
    '''
    def __init__(self, weight=9, height=9, amountColors=5):
        '''инициализация класса
        weight - ширина поля,
        height - высота поля,
        (индексация weight и height с нуля)
        amountColors - колличество играюших цветов
        '''

        # индексация игрового поля начинается с левого верхнего угла,
        # т.е. поле размером 9х9 будет представлено как:
        # 0 1 2 3 5 6 7 8
        # 1
        # 2
        # 3   M
        # 4
        # 5
        # 6
        # 7
        # 8
        # и шар M будет иметь координаты [3][2]
        #

        self.weight = weight
        self.height = height
        self.amountColors = amountColors
        self.gameBoard = [[0] * self.weight for i in range(self.height)]
        self.score = 0
        print(type(self.gameBoard))

    def initBoard(self):
        '''создание новой доски'''
        self.gameBoard = [[0] * self.weight for i in range(self.height)]

    def spawnBalls(self):
        '''случаиное появление трёх новых шаров'''
        balls_list = [i for i in range(1, amountColors + 1)]
        next_balls = [random.choice(balls_list) for b in range(3)]

        i = 2
        while i >= 0:
            y = random.randrange(9)
            x = random.randrange(9)
            if self.gameBoard[y][x] == 0:
                self.gameBoard[y][x] = next_balls[i]
                i -= 1
            else:
                continue

    def checkToLose(self):
        '''проверка на конец игры(окончание возможных ходов)'''
        countOfEmpty = 0
        for i in range(self.height):
            countOfEmpty = countOfEmpty + self.gameBoard[i].count(0)
        if countOfEmpty >= 3:
            return False
        else:
            return True

    def makeMove(self, fromX, fromY, toX, toY):
        '''перемешает шар из координаты (fromX, fromY)
        в координату (toX, toY)
        '''
        if checkToMove():
            self.gameBoard[toY][toX] = self.gameBoard[fromX][fromY]
            self.gameBoard[fromX][fromY] = 0
        else:
            return

    def checkToMove(self, fromX, fromY, toX, toY):
        '''проверят на способность сделать ход одним
        из алгоритмов поиска пути, возрошает True or False
        '''
        di = [-1, 0, 1,  0]
        dj = [0, 1, 0, -1]

        d = [[0] * self.weight for i in range(self.height)]
        d[fromY][fromX] = 1;

        queue = [Point(0, 0) for i in range(self.height*self.weight)]
        head = tail = 0
        queue[tail].x = fromX
        queue[tail].y = fromY
        tail += 1

        while head < tail:
            p_point = queue[head]
            head += 1
            for k in range(4):
                new_point = Point(0, 0)
                new_point.x = p_point.x + di[k];
                new_point.y = p_point.y + dj[k];
                if 0 <= new_point.x and new_point.x < self.weight and 0 <= new_point.y and new_point.y < self.height:
                    if self.gameBoard[new_point.y][new_point.x] == 0 and d[new_point.y][new_point.x] == 0:
                        d[new_point.y][new_point.x] = d[p_point.y][p_point.x] + 1
                        queue[tail] = new_point;
                        tail += 1
        for kek in d:
                print(kek)
        print()
        if d[toY][toX]:
            # way_list = [Point(fromY,fromX)]
            way_list = [[toX, toY]]
            current_distance = 8
            for i in range(d[toY][toX]-1):
                current_distance -= 1
                print(way_list)
                for k in range(4):
                    way_point = copy.deepcopy(way_list[0])
                    way_point[0] += di[k];
                    way_point[1] += dj[k];
                    print(way_point)
                    if 0 > way_point[1] or way_point[0] > self.weight or 0 > way_point[0] or way_point[1] > self.height:
                        continue
                    if current_distance == d[way_point[1]][way_point[0]]:
                        way_list.insert(0, [way_point[0],way_point[1]])
                        break
            print(way_list)
        else:
            return []

    def checkToDestroy(self, X, Y):
        '''проверяет на возможность очищения ряда из пяти шаров
        (по всем направлениям), возрошает либо пустой list,
        либо list с координатами шаров на удаление (в виде tupl'ov)
        '''
        listDestroy = []
        # [y, x]
        color = self.gameBoard[Y][X]
        return self.checkForX(X, Y)
        self.checkForY(X, Y)

    def checkForY(self, X, Y):
        listDestroy = []
        color = self.gameBoard[Y][X]
        arrayToCheck = self.gameBoard[Y]
        print('checkForY', arrayToCheck, (X, Y))
        arrayToCheck[X] = color
        for x in range(self.weight):
            if arrayToCheck[x] == color:
                listDestroy.append(x)
                if len(listDestroy) == 5:
                    return [(x, Y) for x in listDestroy]
            else:
                listDestroy.clear()
        return []

    def checkForX(self, X, Y):
        listDestroy = []
        color = self.gameBoard[Y][X]
        arrayToCheck = []
        for y in range(self.height):
            arrayToCheck.append(self.gameBoard[y][X])

        print('checkForX', arrayToCheck, (X, Y))
        arrayToCheck[X] = color
        for y in range(self.height):
            if arrayToCheck[y] == color:
                listDestroy.append(y)
                if len(listDestroy) == 5:
                    return [(X, y) for y in listDestroy]
            else:
                    listDestroy.clear()
        return []

    # def checkForDiagonal(self, X, Y):
    #     listDestroy = []
    #     color = self.gameBoard[Y][X]
    #     arrayToCheck = []
    #
    #     if X < 4 or self.weight - X < 4 or Y < 4 or self.height - Y:
    #         return []
    #     arrrr = [-1, -2, -3, -4]
    #     for x in range(1, 5):
    #         for y in arrrr:

    def destroyBalls(self, listBalls):
        '''удаляет шары координаты которых в листе'''
        if len(listBalls) == 0:
            return

    def updateScore(self):
        '''обновляет счёт (например вызывается при удаление линии)'''
        pass

