import pandas as pd
import openpyxl
from app.graphs_path_lib import (
    prima_alg
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

cost_m = load_cost_matrix(file_path)
for m in cost_m:
    print(m)
print("*"*100)
res_Prima = prima_alg(cost_m)
print(res_Prima['value'])
