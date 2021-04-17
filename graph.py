from functools import reduce


class Matrix(list):
    """
    По своей сути обычный список с дополнительной проверкой в конструкторе и методом
    """
    def __init__(self, matrix):
        if len(matrix) != len(matrix[0]):
            raise ValueError('Идиот, матрица должна быть квадратной')
        super().__init__(matrix)

    def pos_vertex(self, vertex):
        """
        По объекту vertex возвращает число, соотвествующее позиции в matrix

        :param vertex: int или vertex
        :return: int
        """
        if isinstance(vertex, Vertex):
            vertex = vertex.pos

        if vertex < 0 or vertex >= super().__len__():
            raise ValueError('Вершина не принадлежат базовому графу')

        return vertex


class Vertex(object):

    def __init__(self, matrix: Matrix, pos: int):
        self.matrix = matrix
        self.pos = pos

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = self.matrix.pos_vertex(value)

    def __eq__(self, other):
        # Это нужно, чтобы можно было сравнивать вершини как vertex_1 == vertex_2
        return self.matrix is other.matrix and self.pos == other.pos

    def distance(self, vertex):
        if vertex.matrix is not self.matrix:
            raise ValueError('Вершины должны принадлежать одному графу')
        return self.matrix[self.pos][vertex.pos]

    def __repr__(self):
        return f"V(matrix=<matrix at {id(self.matrix)}>, pos={self.pos})"

    def __str__(self):
        return f"V = {self.pos:>3}"


class Graph(object):
    """
    По своей сути подграф какого-то графа (сам граф представлется матрицей смежности).
    Если в контсруктор не передать списков вершин этого подграфа, то будет считаться, что подграф.
    является полным графом и будет содержать все вершины. Для внуртеннего предстваления вершин
    используется списков целых чисел, однако большинство методов поддерживают как и объекты вершин,
    так и целые цисла, которые их характеризуют
    """
    def __init__(self, matrix: Matrix, vertex_lst=None):
        self.matrix = matrix
        self.vertex_lst = vertex_lst or list(range(len(matrix)))

    def __getitem__(self, vertex):
        # Обращаемся к графу graph[4] и получаем объект 4 вершини. Если она есть в этом графе
        return Vertex(self.matrix, self.pos_vertex(vertex))

    @property
    def raw_vertex_lst(self):
        """
        Возращает внутреннее представление вершин (int).
        И даже не пытайтесь из поменять. Не получится, вахахаха

        :return: (0, 1, 4, 5 ... )
        """
        return tuple(self._vertex_lst)

    @property
    def vertex_lst(self):
        """
        Возращает список объектов вершит

        :return: [vertex_0, vertex_1, ... ]
        """
        return [Vertex(self.matrix, x) for x in self._vertex_lst]

    @vertex_lst.setter
    def vertex_lst(self, vertex_lst):
        """
        Для установки новых вершин graph.vertex_lst = [1, 3, 5]
        или  graph.vertex_lst = [vertex_1, vertex_2, ...]

        :param vertex_lst:
        :return: None
        """
        if not isinstance(vertex_lst, list):
            raise TypeError('Список вершин должен быть списком')

        self._vertex_lst = [self.matrix.pos_vertex(x) for x in vertex_lst]

    def pop(self, vertex):
        """
        Удаляет из подграфа вершину

        :param vertex: int или vertex
        :return: vertex
        """
        del self._vertex_lst[self._vertex_lst.index(self.pos_vertex(vertex))]
        return Vertex(self.matrix, vertex)

    def add(self, vertex):
        """
        ДОбавляет в подграф вершину

        :param vertex: int или vertex
        :return: vertex
        """
        self._vertex_lst = sorted(self._vertex_lst + [self.matrix.pos_vertex(vertex)])
        return Vertex(self.matrix, vertex)

    def pos_vertex(self, vertex):
        """
        Возвращает число, для внутреннего представления вершины и делает проверку на принадлежность

        :param vertex: int или vertex
        :return: int
        """
        if isinstance(vertex, Vertex):
            vertex = vertex.pos

        if vertex not in self.raw_vertex_lst:
            raise ValueError('Данная вершина не принадлежить этому графу')

        return vertex

    def __iter__(self):
        """
        Это, чтобы было удобно итерароваться по вершинам подграфа через for
        """
        return (Vertex(self.matrix, x) for x in self._vertex_lst)

    def __len__(self):
        return len(self._vertex_lst)

    def __repr__(self):
        """
        Красивая печать подграфа

        :return: str
        """
        matrix = "\n".join(map(lambda x: f"\t{str(x)}", self.matrix))
        return f'Graph(matrix=[\n{matrix}\n], vertex_lst={self._vertex_lst})'

    def __sub__(self, other):
        """
        Вычитание одного подграфа из другого

        :param other: graph
        :return: graph
        """
        vertex_lst = [x for x in self._vertex_lst if x not in other.raw_vertex_lst]
        return self.__class__(self.matrix, vertex_lst)


class SegGraph(Graph):
    """
    Это Конкретная реализация графа с прикладными методами для решения задачи компановки
    """
    def delta(self, vertex):
        """
        показывает, насколько уменьшится число внешних связей куска графа
        если из него удалить вершину vertex
        """
        pos = self.pos_vertex(vertex)
        return 2 * sum(
            self.matrix[pos][x] for x in self.raw_vertex_lst
        )

    def p(self, vertex):
        """
        Локальное значение p
        """
        pos = self.pos_vertex(vertex)
        return sum(self.matrix[x][pos] for x in self.raw_vertex_lst)

    def bound(self, vertex):
        """
        Возвращает связанные вершины подграфа

        :param vertex: vertex or int
        :return: [vertex_1, vertex_2, ... ]
        """
        pos = self.pos_vertex(vertex)
        row = self.matrix[pos]
        return [
            Vertex(self.matrix, x) for x in self.raw_vertex_lst if row[x] != 0 or x == pos
        ]

    def alpha(self, other, vertex):
        """
        Для итерационной компановки

        :param other: graph
        :param vertex: vertex or int
        :return: int
        """
        return sum(
            reduce(lambda a, x: a + (
                -vertex.distance(x) if vertex in graph else vertex.distance(x)), graph, 0)
            for graph in (self, other)
        )
