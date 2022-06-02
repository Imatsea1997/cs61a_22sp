def falling(n, k):
    """Compute the falling factorial of n to depth k.

    >>> falling(6, 3)  # 6 * 5 * 4
    120
    >>> falling(4, 3)  # 4 * 3 * 2
    24
    >>> falling(4, 1)  # 4
    4
    >>> falling(4, 0)
    1
    """
    result = 1
    while k !=0:
        result *= n
        n -= 1
        k -= 1
    return result

def sum_digits(y):
    """Sum all the digits of y.

    >>> sum_digits(10) # 1 + 0 = 1
    1
    >>> sum_digits(4224) # 4 + 2 + 2 + 4 = 12
    12
    >>> sum_digits(1234567890)
    45
    >>> a = sum_digits(123) # make sure that you are using return rather than print
    >>> a
    6
    """
    sum = 0
    "计算每一位值，求和"
    while y !=0:
        digit = y % 10
        sum += digit
        y = y // 10
    return sum

def double_eights(n):
    """Return true if n has two eights in a row.
    >>> double_eights(8)
    False
    >>> double_eights(88)
    True
    >>> double_eights(2882)
    True
    >>> double_eights(880088)
    True
    >>> double_eights(12345)
    False
    >>> double_eights(80808080)
    False
    """
    "一位位验证，当前位和下一位同时为8"
    prev_flag = False
    tmp_flag = False
    while n != 0:
        # 更新tmp_flag
        if n % 10 == 8:
            tmp_flag = True
            # 进一步检查prev_flag
            if prev_flag:
                return True
        else:
            tmp_flag = False
        # 移动，下一轮检查
        prev_flag = tmp_flag
        n = n // 10
            
    return False
    
    prev_eight = False
    while n != 0:
        #检查当前位
        #1:tmp true，prev true
        if n % 10 == 8 and prev_eight:
            return True
        #2:tmp true
        elif n % 10 == 8:
            prev_eight = True
        #3:
        else:
            prev_eight = False
        #移动下一位。prev_eight的状态上面合并的挪动了
        n = n // 10
    return False