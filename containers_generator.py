from itertools import combinations_with_replacement


def reduce_lst(lst, n):
    """
    Берет список и удаляет из него по элементу, пока сумма элементов не будет равна n
    Если сумма не будет равна n, то вернет None

    :param lst: Список контейнеров [3, 3, 3, 5, ...]
    :param n: Значение, до которого происходит урезание
    :return: lst or None
    """
    while lst:
        if sum(lst) == n:
            return lst
        lst.pop()

    return None


def get_variants(size, base_variants):
    """
    Решение "комбинаторной задачи". По факту делает перебов всех возможных вариантов и
    отбирает по условию sum(variant) == size. Реализация избыточная, но если я правильно понял,
    это np-полная задача. Такая задача элегантно не решается

    :param size:
    :param base_variants:
    :return: [[3, 3, 3, ...], [3, 4, 4, ...], ... ]
    """
    all_var = combinations_with_replacement(base_variants, size // min(base_variants))
    return iter(set(
        tuple(x) for x in (reduce_lst(list(x), size) for x in all_var) if x is not None
    ))
