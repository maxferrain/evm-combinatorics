import csv
from graph import Matrix

from containers_generator import get_variants
from calculation import (
    bound_count, get_groups, optimization_groups, allocation, opt_allocation, weight
)

# with open('data.csv') as file:
with open('test20.csv') as file:
    reader = csv.reader(file)
    matrix = Matrix([list(map(int, row)) for row in reader])


# Задача компоновки
print(' Задача компоновки '.center(80, '*'))
for containers in get_variants(20, [3, 4, 5, 7]):
# for containers in get_variants(250, [30, 45, 55, 70, 80]):

    direct_res = get_groups(matrix, containers)
    direct_bound = bound_count(direct_res)
    opt_res, i = optimization_groups(direct_res)

    print(f"Контейнер = {containers},  связей = "
          f"{direct_bound} (послед), "
          f"и {bound_count(opt_res)} (итерац) =======> ({i} итераций)")

# Задача размещения
print(' Задача размещения '.center(80, '*'))
for shape in [(4, 5), (2, 10)]:
# for shape in [(10, 25), (5, 50)]:

    print('\nДля платы ', shape)

    crystal = allocation(matrix, shape)
    print(f'Начальная позиция (вес = {crystal.sum_distance(weight)}):')
    print(crystal)

    crystal, swap_count = opt_allocation(crystal, matrix)
    print(f'За {swap_count} итераций получено улучшенное расположение')
    print(f'\n Новая позиция (вес = {crystal.sum_distance(weight)})')
    print(crystal)