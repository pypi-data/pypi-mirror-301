import pandas as pd
import openpyxl
from app.graphs_path_lib import (
    prima_alg, kruskal_alg, floyd_alg, dejkstra_alg
)


def load_cost_matrix(path_input: str):
    """
    Загрузка матрицы смежности ориентированного графа
    """

    try:
        # Загрузка файла XLS в датафрейм
        data_frame = pd.read_excel(path_input, header=None)

        # Проверка формата матрицы
        if not data_frame.applymap(lambda x: isinstance(x, (int, float))).values.all():
            raise ValueError('Ошибка: Матрица должна содержать только числа')

        # Преобразование датафрейма в список списков
        matrix_out = data_frame.values.tolist()

        # Проверка квадратности матрицы
        n = len(matrix_out)
        if any(len(row) != n for row in matrix_out):
            raise ValueError('Ошибка: Матрица должна быть квадратной')

        return matrix_out
    except ValueError as e:
        print(e)
        return None


file_path = 'matrix.xlsx'

matrix = load_cost_matrix(file_path)
print('matrix:')
print(matrix)

start_node = 1
end_node = 5

algs = ['Прима', 'Краскала', 'Дейкстры', 'Флойда']


prima_res = prima_alg(matrix)
print(f'\nАлгоритм Прима:')
print(prima_res)

kruskal_res = kruskal_alg(matrix)
print(f'\nАлгоритм Краскала:')
print(kruskal_res)

floyd_res = floyd_alg(matrix)
print(f'\nАлгоритм Флойда:')
print(floyd_res)

dejkstra_res = dejkstra_alg(matrix, start_node, end_node)
print(f'\nАлгоритм Дейкстры:')
print(dejkstra_res)
