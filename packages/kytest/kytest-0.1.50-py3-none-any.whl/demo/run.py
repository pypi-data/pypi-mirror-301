"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from kytest.core.web import BrowserConfig

from data.login_data import get_headers


if __name__ == '__main__':
    # 不常用的浏览器参数设置
    BrowserConfig.headless = True

    hosts = {
        'api': 'https://app-test.qizhidao.com/',
        'web': 'https://www-test.qizhidao.com/'
    }
    kytest.main(
        path="tests/test_web.py",  # 测试脚本目录
        pkg="com.qizhidao.clientapp",  # 应用包名，针对IOS、安卓、鸿蒙
        host=hosts,  # 域名，针对接口和web测试
        headers=get_headers(),  # 请求头信息，针对接口测试
        # xdist=True  # 并发执行，针对接口和web测试
    )

