from itertools import product, chain, combinations
from operator import sub
from collections import namedtuple

Position = namedtuple('Position', ('row', 'col'))


class Crystal(object):
    """
    Класс кристала (платы). Создаем кристалл заданного размера,
    а дальше постепенно добалвяем туда наши элементы
    """
    def __init__(self, rows, cols):

        # Собственно сама матрица для хранения размещенных элементов
        self.mat = [[None] * cols for _ in range(rows)]
        #  Список всех позиций. Автоматически корректируется при добавлении элемента
        self.all_positions = [
            Position(row, col) for row, col in product(range(rows), range(cols))]

        # Свободные для размещения позиции
        self.free_positions = self.all_positions[:]

    def __repr__(self):
        """
        Это чтобы красиво печатать табличку
        """
        # Смотрим, сколько требуется строк для самого "жирного" элемента
        width = max(len(str(x)) for x in chain(*self.mat)) + 2

        # А дальше просто возвращаем строку в виде таблички (лучше не пытаться понять)
        return '\n'.join('|'.join(
            map(lambda x: str(x or "x").center(width), row)) for row in self.mat)

    @property
    def busy_position(self):
        """
        Занятые позиции

        :return: [Position(row=0, col=2), Position(row=4, col=6), ... ]
        """
        return list(set(self.all_positions) - set(self.free_positions))

    def get(self, position):
        """
        Возвращает элемент по позиции

        :param position: Position(row=...)
        :return: value in position
        """
        return self.mat[position.row][position.col]

    def __getitem__(self, pos):
        return self.mat[pos.row][pos.col]

    def __iter__(self):
        return iter(self.busy_position)

    def add(self, pos, value):
        """
        ДОбавление элемента

        :param pos: Position(row=...)
        :param value: value
        """
        self.free_positions.remove(pos)
        self.mat[pos.row][pos.col] = value

    def swap(self, pos_1, pos_2):
        """
        Меняет два элемента на кристале

        :param pos_1: Position(row=...)
        :param pos_2: Position(row=...)
        """
        self.mat[pos_2.row][pos_2.col], self.mat[pos_1.row][pos_1.col] = \
            self.mat[pos_1.row][pos_1.col], self.mat[pos_2.row][pos_2.col]

    def distance(self, pos_1, pos_2, w=lambda first, second: 1, split=False):
        """
        Возвращает количество клеток между двумя соседними (по вертикали и горизонтали)

        :param pos_1: Position(row=...)
        :param pos_2: Position(row=...)
        :param w: весовая функция
        :param split: разбить результат по row, col
        :return: int distance
        """
        weight = w(self.get(pos_1), self.get(pos_2))
        if split:
            return [abs(x) * weight for x in (pos_1.row - pos_2.row, pos_1.col - pos_2.col)]

        return sum(map(abs, (map(sub, pos_1, pos_2)))) * weight

    def sum_distance(self, w=lambda first, second: 1):
        """
        Взвешанная сумма связей

        :param w: весовая функция
        :return: int
        """
        positions = combinations(self.busy_position, 2)
        return sum(
            self.distance(*items) * w(*map(self.get, items)) for items in positions)

    def weight_center(self, pos,  w=lambda first, second: 1):
        """
        Взвешенный центр масс

        :param pos: позиция элемента
        :param w: Весовая функция (для сравнения с другими элементами)
        :return: x, y
        """

        distances = [self.distance(pos, x, w, split=True) for x in self.busy_position]
        return list(map(sum, zip(*distances)))

