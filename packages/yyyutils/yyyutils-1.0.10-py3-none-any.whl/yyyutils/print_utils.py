import inspect
import builtins
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=False)  # 将 autoreset 设置为 False，以便手动控制颜色


class PrintUtils:
    """
    自定义print函数，可以添加文件名、类名、函数名、行号、时间，以及手动控制文字颜色
    """
    original_print = print

    def __init__(self, add_line=True, add_file=False, add_class=False, add_func=False, add_time=False):
        self.add_line = add_line
        self.add_file = add_file
        self.add_func = add_func
        self.add_time = add_time
        self.add_class = add_class
        self.__enable = True
        self.__current_color = ''
        self.__replace_print(self.__all_print)

    @staticmethod
    def get_original_print():
        return PrintUtils.original_print

    def __all_print(self, *args, **kwargs):
        string = ""
        frame = inspect.currentframe().f_back

        if self.add_file:
            file_name = frame.f_code.co_filename
            string += f"F--{file_name}, "
        if self.add_class:
            class_name = frame.f_locals.get('self', None).__class__.__name__
            string += f"C--{class_name}, "
        if self.add_func:
            func_name = frame.f_code.co_name
            string += f"Fu--{func_name}, "
        if self.add_line:
            line_number = frame.f_lineno
            string += f"L--{line_number}, "
        if self.add_time:
            import time
            now_time = time.strftime("%H:%M:%S", time.localtime())
            string += f"T--{now_time}, "
        string = string[:-2] + "：" if string else ""

        # 处理 sep 参数
        sep = kwargs.pop('sep', ' ')

        # 构建完整的输出字符串
        output = self.__current_color + string + sep.join(map(str, args))

        # 使用原始的 print 函数打印
        PrintUtils.original_print(output, **kwargs)

    def set_color(self, color):
        """设置文字颜色"""
        if color.lower() == 'red':
            self.__current_color = Fore.RED
        elif color.lower() == 'green':
            self.__current_color = Fore.GREEN
        elif color.lower() == 'blue':
            self.__current_color = Fore.BLUE
        elif color.lower() == 'yellow':
            self.__current_color = Fore.YELLOW
        else:
            self.__current_color = ''
        PrintUtils.original_print(self.__current_color, end='')

    def reset_color(self):
        """重置文字颜色"""
        self.__current_color = ''
        PrintUtils.original_print(Style.RESET_ALL, end='')

    def disable(self):
        self.__enable = False
        self.reset_color()
        self.__replace_print(PrintUtils.original_print)

    def enable(self):
        self.__enable = True
        self.__replace_print(self.__all_print)

    def __replace_print(self, func):
        builtins.print = func
