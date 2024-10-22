import openpyxl
import os

USERNAME = os.getlogin()
BASE_DIR = f'C:/Users/{USERNAME}/Documents/Social_capital'
CACHE_FILE = f'C:/Users/{USERNAME}/Documents/Social_capital/CACHE.xlsx'
# Необходимо заменить значение переменной REPORT_NAME на имя анализируемого результата анкетирования
REPORT_NAME = '2024-10-01 MAOU SOSh 131'
WORKBOOK = openpyxl.open(f'{BASE_DIR}/{REPORT_NAME}.xlsx')
WORKSHEET = WORKBOOK['Sheet']


def create_cache(filename):
    '''Функция создания кэша, где хранятся имена отчетов, уже проанализированных'''
    cache = openpyxl.Workbook(filename)
    cache.save(filename)
    return


def check_cache(filename, reportname):
    '''Функция проверки записи в кэше, если отчет уже подвергался анализу, повторное выполнение не будет выполнено.'''
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
    '''Создание списка преподавателей'''
    teachers_list = []
    rows = WORKSHEET.max_row
    for current_row in range(2, rows+1):
        if WORKSHEET.cell(row=current_row, column=1).value not in teachers_list:
            teachers_list.append(WORKSHEET.cell(row=current_row, column=1).value)
        else:
            pass
    return sorted(list(set(teachers_list)))

def teatchers_dict(teachers_list):
    '''Создание словаря для вычисления индексов преподавателей в матрице'''
    teachers_dict = {}
    for index in range(len(teachers_list)):
        teachers_dict[teachers_list[index]]=index+2
    return teachers_dict

def create_matrix(teachers, amount, workbook):
    '''Создание матрицы выбора лучшего преподавателя'''
    workbook.create_sheet('matrix_best_teacher')
    worksheet = workbook['matrix_best_teacher']
    for current_cell in range(2, amount+2):
        worksheet.cell(row=current_cell, column=1).value = teachers[current_cell-2]
        worksheet.cell(row=1, column=current_cell).value = teachers[current_cell-2]
    workbook.save(f'{BASE_DIR}/{REPORT_NAME}.xlsx')
    return worksheet

def fill_the_matrix(matrix, data, amount, workbook, teachers_indexes):
    for current_row in range(2, amount+3):
        for current_column in range(40, 40+amount):
            if data.cell(row=current_row, column=current_column).value is not None:
                matrix_row = teachers_indexes[data.cell(row=current_row, column=1).value]
                matrix_column = teachers_indexes[data.cell(row=current_row, column=current_column).value]
                matrix.cell(row=matrix_row, column=matrix_column).value = 1
            else:
                matrix_row = teachers_indexes[data.cell(row=current_row, column=1).value]
                matrix_column = teachers_indexes[data.cell(row=1, column=current_column).value[133:]]
                matrix.cell(row=matrix_row, column=matrix_column).value = 0
    workbook.save(f'{BASE_DIR}/{REPORT_NAME}.xlsx')
    return


# def choosing_the_best_teacher(amount, workbook, w):
#     '''Функция создания списка пар ВЫБРАВШИЙ-ВЫБРАННЫЙ по кртиерию ЛУЧШИЙ ПРЕПОДАВАТЕЛЬ.'''
#     rows = amount
#     columns = 40 + amount
#     matrixsheet = workbook.create_sheet('best_teacher_matrix')
#     best_teacher = []
#     for current_row in range(2, rows+1):
#         for current_column in range(40, columns+1):
#             if
#             matrixsheet.cell(row=current_row-1, column=current_column-columns).value
#     return best_teacher



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
    fill_the_matrix(matrix, WORKSHEET, teachers_amount, WORKBOOK, teachers_indexes)
    # best_teacher = choosing_the_best_teacher(teachers_amount, WORKBOOK)
    # print(best_teacher)





