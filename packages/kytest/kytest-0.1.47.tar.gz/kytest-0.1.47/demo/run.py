"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest

from data.login_data import get_headers


if __name__ == '__main__':
    hosts = {
        'api': 'https://app-test.qizhidao.com/',
        'web': 'https://www-test.qizhidao.com/'
    }
    kytest.main(
        path="tests/test_adr.py",
        pkg="com.qizhidao.clientapp",  # 针对IOS和安卓
        host=hosts,
        headers=get_headers()
    )

