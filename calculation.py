from graph import SegGraph, Graph
from crystal import Crystal, Position
from operator import add
from functools import partial
from itertools import product, count, combinations, chain


def bound_count(groups_lst):
    """
    Принимает список подграфов и возращает количество внешних связей

    :param groups_lst: [graph_1, graph_2 ... ]
    :return: Количество внешних связей
    """
    res = 0

    # не надо вдаваться в подробности, главное, что получаем одномерный список со всеми вершинами
    all_vertex = list(chain(*map(list, groups_lst)))

    for c_group in groups_lst:
        # Выделяем вершини, которых нет в данной подгруппе
        vertex_lst = [x for x in all_vertex if x not in c_group]
        res += sum(a.distance(b) for a, b in product(vertex_lst, c_group))

    return res // 2  # Сумму получается по всем связям. Сответсвенно каждая из них дублируется


def get_groups(matrix, containers):

    """
    Прямой алгоритм компановки

    :param matrix: Матрица смежности
    :param containers: Контейнеры для компановлке (sum(containers) == len(matrix))
    :return: [graph_1, graph_2 ... ]
    """

    # Вообще матрица для всех подграфом дожна быть единой, поэтому можно передавать эту матрицу
    # как аргумент по-умолчанию
    get_graph = partial(SegGraph, matrix)

    # Изначально полный граф, далее его будем постепенно урезать
    main_graph = get_graph()
    groups = []

    for c_size in containers:

        # Среди графа ищем вершину с минимальным локальным p и берем связанные с ней вершины
        # key=lambda - функция, по которой будет инди сравнение в функции min,
        # Так как Graph - итерируемый (по своим вершинам) объект min вернет объект вершины
        group = get_graph(main_graph.bound(min(main_graph, key=lambda x: main_graph.p(x))))

        while len(group) != c_size:  # подгоняем под размер контейнера
            if len(group) > c_size:
                group.pop(max(group, key=lambda v: main_graph.p(v) - group.delta(v)))
            else:
                group.add(min(
                    main_graph - group, key=lambda v: main_graph.p(v)
                ))

        groups.append(group)
        main_graph = main_graph - group

    return groups


def optimization_groups(groups, max_steps=None):
    """
    Итерационный алгоритм компоновки

    :param groups: [graph_1, graph_2, ... ]
    :param max_steps: максимальное количество итераций (включая неудачные)
    :return: [graph_1, graph_2, ... ], step_count
    """
    step_count = 0

    for group_1, group_2 in combinations(groups, 2):

        beta = 1

        while beta > 0:

            # пар вершин двух подграфов  вычислим bi и храним в виде списка (а не таблицы)
            lst = []
            # это пригодится далее
            # а вообще next(counter) вовращает новое число на 1 больше предыдущего
            counter = count()

            # итерация по всем парам
            for x1, x2 in product(group_1, group_2):
                # По факту значение bi, которое равно alpha(x1) + alpha(x2) - 2r
                # но вот почему-то я, негодяй такой, назвал alpha
                alpha = \
                    group_1.alpha(group_2, x1) + group_1.alpha(group_2, x2) - 2 * x1.distance(x2)

                # Сохраняем кортеж с результатом и уникальным числом
                # Если alpha одного элемета списка будет равно alpha дрогому,
                # то без counter будет идти сравнение по вершинам, которые это не поддреживают
                lst.append((alpha, next(counter), x1, x2))

            beta, ig, x1, x2 = max(lst)
            if beta > 0:  # свопаем вершины
                group_1.add(group_2.pop(x2))
                group_2.add(group_1.pop(x1))

            step_count += 1
            if max_steps and max_steps < step_count:
                return groups, step_count

    return groups, step_count


def allocation(matrix, shape):
    """
        Размещение элементов на плате
    """
    crystal = Crystal(*shape)

    vertex, *other = list(Graph(matrix))
    crystal.add(Position(0, 0), vertex)

    old_graph = Graph(matrix, other)  # Это неразмещенные элементы
    new_graph = Graph(matrix, [vertex])  # Это размещенные

    while len(old_graph) != 0:

        # Ищем элемент, который максимально связан с остальными
        vertex = max(old_graph, key=lambda v: sum(v.distance(x) for x in new_graph) - sum(
            v.distance(x) for x in old_graph
        ))

        # Ищем позицию, где сумма его весов с размещенными минимальна
        # Если по какой-то причине у вас идет слишком хорошее размещение и итерационный алгоритм
        # не может ничего улучшить а в отчете хочется показать его работу
        # то просто, удалите vertex.distance(crystal[x])
        n_pos = min(crystal.free_positions, key=lambda pos: sum(
            crystal.distance(x, pos) * vertex.distance(crystal[x]) for x in crystal
        ))

        crystal.add(n_pos, new_graph.add(old_graph.pop(vertex)))

    return crystal


def weight(vertex_1, vertex_2):
    """
    Используется для вычисления целевой функции при расмещении
    """
    return vertex_1.distance(vertex_2)


def normal_weight(normalize_p):
    """
    Используется для нахождении центра масс, возращает функцию веса
    """
    def wrap(vertex_1, vertex_2):
        return vertex_1.distance(vertex_2) / normalize_p
    return wrap


def district_position(position):
    """
    :param position: some_positions
    :return: [position_1, position_2, ...]
    """
    movies = (-1, 0, 1)
    return (Position(*map(add, position, x)) for x in product(movies, movies))


def opt_allocation(crystal, matrix):
    """
    Оптимизация размещения
    """
    count_swaps = 0
    graph = SegGraph(matrix)  # По сути используется для нахождения локального p

    while True:

        current_distance = crystal.sum_distance(weight)  # значение целефой функции

        # Поиск элемента с самым неудачным положением
        elem_pos = max(crystal, key=lambda pos: sum(
            crystal.distance(x, pos, normal_weight(graph.p(crystal[pos]))) for x in crystal
        ))

        # Поиск его центра масс
        center_pos = Position(*(map(int, crystal.weight_center(
            elem_pos, normal_weight(graph.p(crystal[elem_pos]))
        ))))

        best_pos = None
        # district_position может вернуть элементы, которые находятся за границей,
        # поэтому делаем set
        for variant in set(district_position(center_pos)) & set(crystal):

            # Делаем своп и вычисляем значение целевой функции
            # Я знаю, что такое вычисление не оптимально. Хотел написать нормально, но что-то лень
            crystal.swap(elem_pos, variant)
            if crystal.sum_distance(weight) < current_distance:
                current_distance = crystal.sum_distance(weight)
                best_pos = variant

            # обязательно свопаем обратно
            crystal.swap(elem_pos, variant)

        if not best_pos:
            return crystal, count_swaps

        crystal.swap(best_pos, elem_pos)
        count_swaps += 1
