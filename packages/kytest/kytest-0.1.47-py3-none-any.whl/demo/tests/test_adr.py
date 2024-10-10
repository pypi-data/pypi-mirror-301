import kytest
from kytest.core.adr import TC
from page.adr_page import AdrPage


@kytest.story('测试demo')
class TestAdrDemo(TC):
    def start(self):
        self.start_app()
        self.adr_page = AdrPage(self.dr)

    @kytest.title('进入设置页')
    def test_go_setting(self):
        if self.adr_page.adBtn.exists():
            self.adr_page.adBtn.click()
        self.adr_page.myTab.click()
        self.adr_page.setBtn.click()
        self.adr_page.page_title.assert_text_eq('设置')





