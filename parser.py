import openpyxl
import os
from graphs import graph_define

USERNAME = os.getlogin()
BASE_DIR = f'C:/Users/{USERNAME}/Documents/Social_capital'
CACHE_FILE = f'C:/Users/{USERNAME}/Documents/Social_capital/CACHE.xlsx'
# Необходимо заменить значение переменной REPORT_NAME на имя анализируемого результата анкетирования
REPORT_NAME = '2024-10-01 MAOU SOSh 131'
WORKBOOK = openpyxl.open(f'{BASE_DIR}/{REPORT_NAME}.xlsx')
WORKSHEET = WORKBOOK['Sheet']
FIRST_MATRIX_QUESTION = '«Кто из коллег, по вашему мнению, являются лучшими педагогами (преподавателями, воспитателями) вашей образовательной организации?»'


def create_cache(filename):
    """Функция создания кэша, где хранятся имена отчетов, уже проанализированных"""
    cache = openpyxl.Workbook(filename)
    cache.save(filename)
    return


def check_cache(filename, reportname):
    """Функция проверки записи в кэше, если отчет уже подвергался анализу, повторное выполнение не будет выполнено."""
    cachebook = openpyxl.open(filename)
    cachesheet = cachebook['Sheet']
    rows = cachesheet.max_row
    for current_row in range(1, rows+1):
        if cachesheet.cell(row = current_row, column=1).value == reportname:
            print('the record of the report already exists')
            return
    cachesheet.cell(row = rows, column=1).value = reportname
    cachebook.save(filename)
    print('A new entry has been added')
    return


def get_teachers_list(WORKSHEET):
    """Создание списка преподавателей"""
    teachers_list = []
    rows = WORKSHEET.max_row
    for current_row in range(2, rows+1):
        if WORKSHEET.cell(row=current_row, column=1).value not in teachers_list:
            teachers_list.append(WORKSHEET.cell(row=current_row, column=1).value)
        else:
            pass
    return sorted(list(set(teachers_list)))


def teatchers_dict(teachers_list):
    """Создание словаря для вычисления индексов преподавателей в матрице"""
    teachers_dict = {}
    for index in range(len(teachers_list)):
        teachers_dict[teachers_list[index]]=index+2
    return teachers_dict


def create_matrix(teachers, amount, workbook):
    """Создание матрицы выбора лучшего преподавателя"""
    workbook.create_sheet('matrix_best_teacher')
    worksheet = workbook['matrix_best_teacher']
    for current_cell in range(2, amount+2):
        worksheet.cell(row=current_cell, column=1).value = teachers[current_cell-2]
        worksheet.cell(row=1, column=current_cell).value = teachers[current_cell-2]
    workbook.save(f'{BASE_DIR}/{REPORT_NAME}.xlsx')
    return worksheet


def first_matrix_start(question, data):
    """Поиск начала первой матрицы по вопросу"""
    columns = data.max_column
    for current_column in range(1, columns+1):
        if question in data.cell(row=1, column=current_column).value:
            return current_column
        else:
            pass


def fill_the_matrix(matrix, start, data, amount, workbook, teachers_indexes):
    """Заполнение матрицы данными"""
    for current_row in range(2, amount+3):
        for current_column in range(start, start+amount):
            if data.cell(row=current_row, column=current_column).value is not None:
                matrix_row = teachers_indexes[data.cell(row=current_row, column=1).value]
                matrix_column = teachers_indexes[data.cell(row=current_row, column=current_column).value]
                matrix.cell(row=matrix_row, column=matrix_column).value = 1
            else:
                matrix_row = teachers_indexes[data.cell(row=current_row, column=1).value]
                matrix_column = teachers_indexes[data.cell(row=1, column=current_column).value[133:]]
                matrix.cell(row=matrix_row, column=matrix_column).value = 0
    workbook.save(f'{BASE_DIR}/{REPORT_NAME}.xlsx')
    return workbook['matrix_best_teacher']


def get_edges(matrix, teachers_indexes, amount, workbook):
    """Создание массива ребер для построения графа"""
    edges = []
    nodes = []
    workbook.create_sheet('edges')
    worksheet = WORKBOOK['edges']
    start_row = 1
    for current_row in range(2, amount+3):
        for current_column in range(2, amount+3):
            if matrix.cell(row=current_row, column=current_column).value == 1:
                edges.append(
                    (
                        teachers_indexes[matrix.cell(row=current_row, column=1).value],
                        teachers_indexes[matrix.cell(row=1, column=current_column).value]
                    )
                )
                nodes.append(teachers_indexes[matrix.cell(row=current_row, column=1).value])
                nodes.append(teachers_indexes[matrix.cell(row=1, column=current_column).value])
                worksheet.cell(row=start_row, column=1).value = teachers_indexes[matrix.cell(row=current_row, column=1).value]
                worksheet.cell(row=start_row, column=2).value = teachers_indexes[matrix.cell(row=1, column=current_column).value]
                start_row += 1
            else:
                pass
    nodes = list(set(nodes))
    workbook.save(f'{BASE_DIR}/{REPORT_NAME}.xlsx')
    return edges, nodes


def get_titles(teachers_indexes):
    """Получение заголовков для построения графа"""
    return list(teachers_indexes.keys())


if __name__ == '__main__':
    if os.path.exists(BASE_DIR):
        if os.path.exists(CACHE_FILE):
            print('the cache file exists')
            pass
        else:
            print('the cache file has been created')
            create_cache(CACHE_FILE)
    else:
        os.mkdir(BASE_DIR)
        create_cache(CACHE_FILE)
        print('the directory has been created, the cache file has been created')
    # check_cache(CACHE_FILE, REPORT_NAME)
    teachers_list = get_teachers_list(WORKSHEET)
    teachers_amount = len(teachers_list)
    teachers_indexes = teatchers_dict(teachers_list)
    matrix = create_matrix(teachers_list, teachers_amount, WORKBOOK)
    first_matrix_pivot = first_matrix_start(FIRST_MATRIX_QUESTION, WORKSHEET)
    filled_matrix = fill_the_matrix(matrix, first_matrix_pivot, WORKSHEET, teachers_amount, WORKBOOK, teachers_indexes)
    edges, nodes = get_edges(filled_matrix, teachers_indexes, teachers_amount, WORKBOOK)
    titles = get_titles(teachers_indexes)
    graph_define(nodes, edges, titles)





