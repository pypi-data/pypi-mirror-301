import pandas as pd
import sys


def replace_0_to_inf(graph_matrix_out: pd.DataFrame):
    # Заменяем 0 на значение максимального элемента в матрице + 1000
    max_el = graph_matrix_out.max().max()  # Находим максимальный элемент всей матрицы
    max_el = max_el + 1000 if max_el > 0 else 1000  # Обрабатываем случай, когда max_el = 0
    graph_matrix_df = graph_matrix_out.replace(0, max_el)  # Заменяем 0 на max_el
    return graph_matrix_df, max_el


# Функция поиска постоянной пометки
def pp_search(temp_vp: list):
    # Добавляем в список вес дуги от начальной вершины к следующей минимальной по весу среди оставшихся непросмотренных вершин
    min_vp = []
    min_vp.append(min(i for i in temp_vp if i != 0))
    # print(min_vp)

    # Добавляем в список номер вершины
    for i in range(len(temp_vp)):
        if temp_vp[i] == min_vp[0]:
            min_vp.append(i + 1)
            # print('sx',min_vp)
        else:
            continue
            # print('Error')

    # Если вершина, к которой ведет дуга одна, то возвращаем список элементов (вес дуги, номер вершины), иначе добавляем в список первую вершину из списка
    if len(min_vp) == 2:
        return min_vp
    else:
        temp_lst = []
        # print(min_vp[0],min_vp[1],min_vp[2])
        temp_lst.append(min_vp[0])
        temp_lst.append(min_vp[1])
        min_vp = temp_lst
        return min_vp


# Функция поиска кратчайшего пути
def dejkstra_alg(graph_matrix_df: list,
                 start_node: int,
                 end_node: int):
    start = start_node
    end = end_node
    # Заменяем 0 в матрице на максимальный элемент + 1000
    # graph_matrix_df_inf[0] = матрица с замененными 0, а graph_matrix_df_inf[1] = максимальный элемент+1000
    graph_matrix_df = pd.DataFrame(graph_matrix_df)  # Преобразование списка в DataFrame
    graph_matrix_df_inf = replace_0_to_inf(graph_matrix_df)

    # Присвоим каждой вершине пометку
    # pp - список номеров вершин с постоянными пометками
    pp = []
    # Включаем в список pp номер начальной вершины
    pp.append(start_node)
    # c_pp - лист весов ребер, инцидентных вершинам с постоянными пометками
    c_pp = []
    # vp - лист временных пометок
    vp = []
    # c_vp - лист весов ребер, инцидентных вершинам с временными пометками и с постоянными пометками
    c_vp = []
    # Устанавливаем начальные значения весов ребер, инцидентных вершинам с временными пометками, = максимальному элементу+1000
    for i in range(len(graph_matrix_df)):
        c_vp.append(graph_matrix_df_inf[1])
    # print(c_vp)
    # Определяем индекс начальной вершины
    start_index = start_node - 1
    # Полагаем значение в списке c_vp веса ребра, инцидентного начальной вершине с постоянной пометкой = 0
    c_vp[start_index] = 0
    # print(c_vp)

    # Создаем список для фиксации результатов итераций
    df_lst = []
    df_lst.append(c_vp.copy())
    # Проверка, чтобы все вершины имели постоянную пометку до конечной
    # print(pp[-1],end_node)
    while pp[-1] != end_node:
        # while len(pp) < len(graph_matrix_df_inf[0]):
        # print('1', c_vp)

        # Изменяем значения временных пометок
        for i in range(len(c_vp)):
            df = graph_matrix_df_inf[0]
            temp_l = c_vp[pp[-1] - 1] + df[pp[-1] - 1][i]
            # print(temp_l)
            if c_vp[i] < temp_l:
                c_vp[i] = c_vp[i]
            else:
                c_vp[i] = temp_l
                # print(c_vp[i])

        max_el = graph_matrix_df_inf[1]
        # Запрещаем вершины, добавленные в список постоянных вершин
        for i in pp:
            c_vp[i - 1] = max_el

        d = c_vp.copy()
        # Вносим в df_lst результаты итераций
        df_lst.append(d)
        # print('h',df_lst)

        c = []
        # Определяем постоянную пометку (вес ребра, номер вершины)
        c = pp_search(c_vp)
        # Добавляем постоянную пометку в список постоянных пометок
        pp.append(c[1])
        # Добавляем вес ребра в список весов ребер, инцидентных вершинам с временными и постоянными пометками
        c_pp.append(c[0])

    # Конвертируем список в DataFrame
    df = pd.DataFrame(df_lst).transpose()

    n_col = len(df.columns)
    # print(n_col)
    while (n_col < len(df)):
        col = []
        for i in range(len(df)):
            col.append(max_el)
        df.insert(loc=len(df.columns), column=len(df.columns), value=col)
        # df[n_col] = [col]
        n_col += 1

    weight_total = min(c_vp)

    dejkstra_dict = {'title': 'Алгоритм Дейкстры',
                     'pp': pp,
                     'weight_total': weight_total,
                     'df': df,
                     'max_el': max_el,
                     'start': start,
                     'end': end
                     }

    return dejkstra_dict
