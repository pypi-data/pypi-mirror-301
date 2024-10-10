"""
@Author: kang.yang
@Date: 2024/10/8 15:12
"""
from kytest.core.hm import TC
from page.hm_page import HmPage


class TestHmDemo(TC):

    def start(self):
        self.start_app()
        self.hm_page = HmPage(self.dr)

    def end(self):
        self.stop_app()

    def test_hm(self):
        self.dr.click(630, 2050)
        self.hm_page.my_entry.click()
        self.hm_page.login_entry.click()
        assert self.hm_page.pwd_login.exists()



