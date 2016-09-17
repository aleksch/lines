import random
import copy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameModel:
    def __init__(self, weight=9, height=9, amount_colors=7):

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
        self.amount_colors = amount_colors
        self.game_board = []
        self.init_board()
        self.score = 0
        self.game_state = 0

    def init_board(self):
        self.game_board = [[0] * self.weight for i in range(self.height)]

    def spawn_balls(self):
        balls_list = [i for i in range(1, self.amount_colors + 1)]
        next_balls = [random.choice(balls_list) for b in range(3)]

        i = 2
        while i >= 0:
            y = random.randrange(self.height)
            x = random.randrange(self.weight)
            if self.game_board[y][x] == 0:
                self.game_board[y][x] = next_balls[i]
                i -= 1
            else:
                continue
        self.game_state = 1

    def check_to_lose(self):
        count_of_empty = 0
        for i in range(self.height):
            count_of_empty = count_of_empty + self.game_board[i].count(0)
        if count_of_empty >= 3:
            return False
        else:
            self.game_state = 2
            return True

    def easy_move(self, from_x, from_y, to_x, to_y):
        if self.check_to_move(from_x, from_y, to_x, to_y):
            self.game_board[to_y][to_x] = self.game_board[from_y][from_x]
            self.game_board[from_y][from_x] = 0
            self.game_state = 0
            if self.check_to_destroy(to_x, to_y):
                self.game_state = 1
                self.update_score()
                self.destroy_balls(self.check_to_destroy(to_x, to_y))

    def make_move(self, from_x, from_y, to_x, to_y):
        if self.check_to_move(from_x, from_y, to_x, to_y):
            self.game_board[to_y][to_x] = self.game_board[from_x][from_y]
            self.game_board[from_x][from_y] = 0
        else:
            return

    def check_to_move(self, from_x, from_y, to_x, to_y):
        # http://accepted.narod.ru/bfs.htm
        di = [-1, 0, 1, 0]
        dj = [0, 1, 0, -1]

        d = [[0] * self.weight for i in range(self.height)]
        d[from_y][from_x] = 1

        queue = [Point(0, 0) for i in range(self.height * self.weight)]
        head = tail = 0
        queue[tail].x = from_x
        queue[tail].y = from_y
        tail += 1

        while head < tail:
            p_point = queue[head]
            head += 1
            for k in range(4):
                new_point = Point(0, 0)
                new_point.x = p_point.x + di[k]
                new_point.y = p_point.y + dj[k]
                if self.arr_in_board(new_point.x, new_point.y):
                    if self.game_board[new_point.y][new_point.x] == 0 and d[new_point.y][new_point.x] == 0:
                        d[new_point.y][new_point.x] = d[p_point.y][p_point.x] + 1
                        queue[tail] = new_point
                        tail += 1
        if d[to_y][to_x]:
            way_list = [[to_x, to_y]]
            current_distance = d[to_y][to_x]
            for i in range(d[to_y][to_x]-1):
                current_distance -= 1
                for k in range(4):
                    way_point = copy.deepcopy(way_list[0])
                    way_point[0] += di[k]
                    way_point[1] += dj[k]
                    if 0 > way_point[1] or way_point[0] > self.weight or 0 > way_point[0] or way_point[1] > self.height:
                        continue
                    if current_distance == d[way_point[1]][way_point[0]]:
                        way_list.insert(0, [way_point[0], way_point[1]])
                        break
            return way_list
        else:
            return []

    # def checkToDestroy(self, X, Y):
    #     '''проверяет на возможность очищения ряда из пяти шаров
    #     (по всем направлениям), возрошает либо пустой list,
    #     либо list с координатами шаров на удаление (в виде tupl'ov)
    #     '''
    #
    #     color = self.gameBoard[Y][X]
    #     t = [[1, 0], [1, 1], [0, 1], [1, -1]]
    #     lines = []
    #     for i in reversed(range(4)):
    #         p = t[i]
    #         line = [(X, Y)]
    #         count = 1
    #         x = X
    #         y = Y
    #         dx = p[0]
    #         dy = p[1]
    #         while(True):
    #             x = x + dx
    #             y = y + dy
    #             if self.arrInBoard(x, y):
    #                 if self.gameBoard[y][x] == color:
    #                     line.append((x, y))
    #                     count += 1
    #             else:
    #                 break
    #         count = 1
    #         x = X
    #         y = Y
    #         dx = -p[0]
    #         dy = -p[1]
    #         while(True):
    #             x = x + dx
    #             y = y + dy
    #             if self.arrInBoard(x, y):
    #                 if self.gameBoard[y][x] == color:
    #                     line.append((x, y))
    #                     count += 1
    #             else:
    #                 break
    #         if len(line) >= 5:
    #             lines.append(line)
    #     return lines[0]

    def check_to_destroy(self, x, y):
        if len(self.check_for_x(x, y)) > len(self.check_for_y(x, y)):
            list_destroy = self.check_for_x(x, y)
        else:
            list_destroy = self.check_for_y(x, y)
        return list_destroy

    def check_for_y(self, x, y):
        list_destroy = []
        color = self.game_board[y][x]
        array_to_check = self.game_board[y]
        array_to_check[x] = color
        for x in range(self.weight):
            if array_to_check[x] == color:
                list_destroy.append(x)
                if len(list_destroy) == 5:
                    return [(x, y) for x in list_destroy]
            else:
                list_destroy.clear()
        return []

    def check_for_x(self, x, y):
        list_destroy = []
        color = self.game_board[y][x]
        array_to_check = []
        for y in range(self.height):
            array_to_check.append(self.game_board[y][x])

        print('checkForX', array_to_check, (x, y))
        array_to_check[x] = color
        for y in range(self.height):
            if array_to_check[y] == color:
                list_destroy.append(y)
                if len(list_destroy) == 5:
                    return [(x, y) for y in list_destroy]
            else:
                    list_destroy.clear()
        return []

    def arr_in_board(self, x, y):
        return self.weight > x and self.height > y and x >= 0 and y >= 0

    def destroy_balls(self, list_balls):
        if len(list_balls) == 0:
            return
        for xy in list_balls:
            self.game_board[xy[1]][xy[0]] = 0

    def update_score(self):
        self.score += 5
