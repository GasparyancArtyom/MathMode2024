import pathlib
import typing as tp
from random import randint, choice

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    group = [] # для результата
    for i in range(0, len(values), n):
        mass = [] # создаём подмассив
        for j in range(i, i+n):
            mass.append(values[j])
        group.append(mass) # добавляем в результируюший список
    return group



def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row = []
    for i in grid[pos[0]]: # проходимся по значениям колонки и добавляем в результат
        row.append(i)
    return row

def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = []
    for i in range(len(grid)): # проходимся по значениям столбца и записываем в результат
        col.append(grid[i][pos[1]])
    return col


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    group = []
    for i in range(pos[0] // 3 * 3, pos[0] // 3 * 3 + 3): # проходимся по элементам блоков и добавляем в резёльтат
        for j in range(pos[1] // 3 * 3, pos[1] // 3 * 3 + 3):
            group.append(grid[i][j])
    return group # возвращаем значение



def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    # будем проходиться по матрице (grid) и если найдём пустую позицию, её вернём
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == '.':
                return tuple([i, j])


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    good = {'1', '2', '3', '4', '5', '6', '7', '8', '9'} # "хорошие" начения, которые доотупны
    for i in get_col(grid, pos): # будем удалять из доступных значений те которые есть в колонках столбцах и блоках
        good.discard(i)
    for i in get_row(grid, pos):
        good.discard(i)
    for i in get_block(grid, pos):
        good.discard(i)
    return good


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    # найдём свободную позицию
    pos = find_empty_positions(grid)
    if pos == None: # (завершающая обработка) если вся таблица заполнена - значит судоку решено!
        return grid
    else:
        for val in find_possible_values(grid, pos):
            i, j = pos[0], pos[1]
            grid[i][j] = val
            if solve(grid) != None:
                return grid
            grid[i][j] = '.'


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    good = {'1', '2', '3', '4', '5', '6', '7', '8', '9'} # множество, с которым будем сравнивать
    for i in solution:
        if set(i) != good: return False
    for i in range(9):
        if set(get_col(solution, [i, 0])) != good: return False
    blocks = [[0, 0], [0, 3], [0, 6], [3, 0], [3, 3], [3, 6], [6, 0], [6, 3], [6, 6]] # позиции всех блоков
    for pos in blocks:
        if set(get_block(solution, pos)) != good:
            return False
    return True



def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    N = 81 - N
    good = [['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                ['4', '5', '6', '7', '8', '9', '1', '2', '3'],
                ['7', '8', '9', '1', '2', '3', '4', '5', '6'],
                ['2', '3', '4', '5', '6', '7', '8', '9', '1'],
                ['5', '6', '7', '8', '9', '1', '2', '3', '4'],
                ['8', '9', '1', '2', '3', '4', '5', '6', '7'],
                ['3', '4', '5', '6', '7', '8', '9', '1', '2'],
                ['6', '7', '8', '9', '1', '2', '3', '4', '5'],
                ['9', '1', '2', '3', '4', '5', '6', '7', '8']]

    for i in range(0, 9, 3):
        for _ in range(10):
            a = choice([i, i + 1, i + 2])
            b = choice([i, i + 1, i + 2])
            good[a], good[b] = good[b], good[a]  # мешаем строки внутри блоков
    for i in range(0, 9, 3):  # мешаем столбцы
        for _ in range(10):
            a = choice([i, i + 1, i + 2])
            b = choice([i, i + 1, i + 2])
            for j in range(9):
                good[j][a], good[j][b] = good[j][b], good[j][a]
    used = list()
    while N > 0:
        i, j = randint(0, 8), randint(0, 8)
        if (i, j) not in used:
            good[i][j] = '.'
            N -= 1
            used.append((i, j))
    return good


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
