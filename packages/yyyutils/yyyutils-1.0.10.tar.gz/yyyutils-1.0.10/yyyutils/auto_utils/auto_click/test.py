from yyyutils.auto_utils.auto_click.new_acbi_utils import AutoClickGenerator
from yyyutils.window_utils import WindowUtils
from yyyutils.auto_utils.auto_press import AutoPressUtils
from yyyutils.auto_utils.mouse_utils import MouseUtils

if __name__ == '__main__':
    auto_press_utils = AutoPressUtils()
    generator = AutoClickGenerator()
    name = '86'
    while True:
        generator.add_icon(
            r"D:\Python\Python38\Lib\site-packages\mytools\yyyutils\auto_utils\image\Snipaste_2024-10-11_10-13-22.png")
        generator.click()
        auto_press_utils.press_keys_continuously(list(name), interval=0)
        generator.add_icon(
            r"D:\Python\Python38\Lib\site-packages\mytools\yyyutils\auto_utils\image\Snipaste_2024-10-11_10-13-49.png").click()
        if generator.click_res:
            generator.add_icon(
                r"D:\Python\Python38\Lib\site-packages\mytools\yyyutils\auto_utils\image\Snipaste_2024-10-11_10-47-21.png").click()
            if not generator.click_res:
                MouseUtils.set_cursor_pos(1680, 680)
            name = str(int(name) + 1)
            MouseUtils.click_mouse('left', 344, 822)
