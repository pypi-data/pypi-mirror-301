from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


class AutomationUtils:
    """
    用于自动化测试的工具类
    """

    def __init__(self, driver_path, headless=False):
        """
        初始化方法
        :param driver_path: 浏览器驱动路径
        """
        self.driver_path = driver_path
        options = Options()
        options.use_chromium = True
        if headless:
            options.add_argument('--headless')
        self._driver = webdriver.Edge(service=Service(self.driver_path), options=options)
        self.get_driver()

    def get_driver(self):
        """
        获取驱动
        :return:
        """
        return self._driver

    def get(self, url):
        """
        打开指定url
        :param url:
        :return:
        """
        self._driver.get(url)
        self._driver.maximize_window()

    def find_element_by_xpath(self, xpath):
        """
        根据xpath查找元素，如果有多个元素，只返回第一个
        :param xpath:
        :return:
        """
        return self._driver.find_element(By.XPATH, xpath)

    def find_elements_by_xpath(self, xpath):
        """
        根据xpath查找元素，返回所有元素
        :param xpath:
        :return:
        """
        return self._driver.find_elements(By.XPATH, xpath)

    def find_element(self, id):
        """
        根据id查找元素，如果有多个元素，只返回第一个
        :param id:
        :return:
        """
        return self._driver.find_element(value=id)

    class XpathGenerator:
        """
        XPath生成器
        """

        __xpath = ""

        @staticmethod
        def reset():
            """重置 XPath"""
            AutomationUtils.XpathGenerator.__xpath = ""
            return AutomationUtils.XpathGenerator

        @staticmethod
        def add(path: str):
            """添加路径"""
            AutomationUtils.XpathGenerator.__xpath += path
            return AutomationUtils.XpathGenerator

        @staticmethod
        def descendant_of_all(tag: str = "*"):
            """选择后代元素"""
            AutomationUtils.XpathGenerator.__xpath += f"//{tag}"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def this_descendant(tag: str = "*"):
            """选择当前元素的后代元素"""
            AutomationUtils.XpathGenerator.__xpath += f"./{tag}"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def descendant_from_parent(tag: str = "*"):
            """选择根元素的后代元素"""
            AutomationUtils.XpathGenerator.__xpath += f"/{tag}"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def attribute(name: str, value: str, contains: bool = False):
            """根据属性选择"""
            if contains:
                AutomationUtils.XpathGenerator.__xpath += f"[contains(@{name}, '{value}')]"
            else:
                AutomationUtils.XpathGenerator.__xpath += f"[@{name}='{value}']"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def text(value: str, contains: bool = False):
            """选择包含特定文本的元素"""
            if contains:
                AutomationUtils.XpathGenerator.__xpath += f"[contains(text(), '{value}')]"
            else:
                AutomationUtils.XpathGenerator.__xpath += f"[text()='{value}']"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def index(n: int):
            """选择第n个元素"""
            AutomationUtils.XpathGenerator.__xpath += f"[{n}]"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def parent():
            """选择父元素"""
            AutomationUtils.XpathGenerator.__xpath += "/.."
            return AutomationUtils.XpathGenerator

        @staticmethod
        def or_condition(condition: str):
            """添加 OR 条件"""
            AutomationUtils.XpathGenerator.__xpath += f" | {condition}"
            return AutomationUtils.XpathGenerator

        @staticmethod
        def get() -> str:
            """获取生成的 XPath"""
            xpath = AutomationUtils.XpathGenerator.__xpath
            AutomationUtils.XpathGenerator.reset()  # 自动重置
            return xpath


# 示例使用
if __name__ == '__main__':
    driver = AutomationUtils('D:/msedgedriver.exe')
    driver.get('https://www.baidu.com')
