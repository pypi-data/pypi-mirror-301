"""
@Author: kang.yang
@Date: 2023/10/26 09:48
"""
import time
import json
import os

import allure
from urllib import parse

from .driver import Driver
from .element import Elem

from kytest.core.api.request import HttpReq
from kytest.utils.log import logger
from kytest.utils.config import kconfig


class TestCase(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    dr: Driver = None

    # ---------------------初始化-------------------------------
    @classmethod
    def start_class(cls):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    @classmethod
    def end_class(cls):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        browserName = kconfig["browser"]
        headless = kconfig["headless"]
        maximized = kconfig["full"]
        window_size = kconfig["size"]
        state_file = kconfig["state"]
        if not state_file:
            try:
                cookies = kconfig["cookies"]
                if cookies:
                    if not os.path.exists("data"):
                        os.makedirs("data")
                    state_file = os.path.join("data", "state.json")
                    state_json = {
                        "cookies": cookies
                    }
                    with open(state_file, "w") as f:
                        f.write(json.dumps(state_json))
            except Exception as e:
                print(e)
                state_file = None

        cls.dr = Driver(
            browserName=browserName,
            headless=headless,
            state=state_file,
            maximized=maximized,
            window_size=window_size
        )
        cls.context = cls.dr.context
        cls.page = cls.dr.page

        cls.start_class()

    @classmethod
    def teardown_class(cls):
        cls.end_class()
        cls.dr.close()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        project_name = kconfig['project']
        if project_name:
            allure.dynamic.feature(project_name)

        self.start()

    def teardown_method(self):
        self.end()

    # 公共方法
    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    def shot(self, name: str, delay=0):
        """截图"""
        if delay:
            self.sleep(delay)
        self.dr.shot(name)

    # UI方法
    def elem(self, xpath=None, css=None):
        _kwargs = {}
        if xpath is not None:
            _kwargs['xpath'] = xpath
        if css is not None:
            _kwargs['css'] = css

        return Elem(self.dr, **_kwargs)

    # web方法
    def assert_title(self, title: str, timeout: int = 5):
        """断言页面标题"""
        self.dr.assert_title(title, timeout)

    @staticmethod
    def is_url_has_http(url):
        """针对为空和只有路径的情况，使用默认host进行补全"""
        web_host = kconfig["web_url"]
        if web_host:
            host = web_host
        else:
            host = kconfig["base_url"]
        if url is None:
            url = host
        if 'http' not in url:
            url = parse.urljoin(host, url)
        return url

    def assert_url(self, url: str = None, timeout: int = 10):
        """断言页面url"""
        url = self.is_url_has_http(url)
        self.dr.assert_url(url, timeout)

    def goto(self, url):
        """打开页面"""
        url = self.is_url_has_http(url)
        self.dr.goto(url)


