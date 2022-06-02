HW_SOURCE_FILE = __file__


def summation(n, term):
    """Return the sum of numbers 1 through n (including n) wíth term applied to each number.
    Implement using recursion!

    >>> summation(5, lambda x: x * x * x) # 1^3 + 2^3 + 3^3 + 4^3 + 5^3
    225
    >>> summation(9, lambda x: x + 1) # 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10
    54
    >>> summation(5, lambda x: 2**x) # 2^1 + 2^2 + 2^3 + 2^4 + 2^5
    62
    >>> # Do not use while/for loops!
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'summation',
    ...       ['While', 'For'])
    True
    """
    assert n >= 1
    # base case
    if n == 1:
        return term(n)
    # recursive case: 最后一项 + 前面所有
    return term(n) + summation(n - 1, term)



def paths(m, n):
    """Return the number of paths from one corner of an
    M by N grid to the opposite corner.

    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """
    # base case1: 完成任务
    if m == 1 and n == 1:
        return 1
    # base case2: 往右走不了了
    if m == -1:
        return 0
    # base case3: 往上走不了了
    if n == -1:
        return 0
    # recursive case:当前点路径和 = 向右走一步路径和 + 向上走一步路径和
    return paths(m - 1, n) + paths(m, n - 1)



def pascal(row, column):
    """Returns the value of the item in Pascal's Triangle
    whose position is specified by row and column.
    >>> pascal(0, 0)
    1
    >>> pascal(0, 5)	# Empty entry; outside of Pascal's Triangle
    0
    >>> pascal(3, 2)	# Row 3 (1 3 3 1), Column 2
    3
    >>> pascal(4, 2)     # Row 4 (1 4 6 4 1), Column 2
    6
    """
    "0。 pascal外的元素为0"
    "1。 在pascal里的任何一个item等于上方item + 上左方item"
    "2。 特殊位置(0,0)为起始点 返回1"

    # base case1: 起始点
    if row == 0 and column == 0:
        return 1
    # base case2: 出界情况
    if row < 0 or column < 0 or row < column:
        return 0

    # recursive case
    return pascal(row - 1, column) + pascal(row - 1, column - 1)