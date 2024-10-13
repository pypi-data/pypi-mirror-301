"""
功能：将十进制数转换为任意进制数
"""


def decimal_to_any(decimal, base):
    if base < 2 or base > 36:
        return "Error: Base should be between 2 and 36"
    if decimal == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while decimal > 0:
        decimal, remainder = divmod(decimal, base)
        result += digits[remainder]
    return result[::-1]


def any_to_decimal(any):
    """
    TODO: 实现任意进制数到十进制数的转换
    :param any:
    :return:
    """
    # 以下是代码实现
    digits = "0123456789"
    decimal = 0
    base = 1
    for digit in str(any):
        decimal += digits.index(digit) * base
        base *= 10
    return decimal


# 示例
if __name__ == '__main__':
    decimal = 123456789
    base = 16
    print(decimal_to_any(decimal, base))  # Output: 75BCD15
