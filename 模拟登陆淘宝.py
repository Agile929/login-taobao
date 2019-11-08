# -*- coding:utf-8 -*-
import re
import os
import json
import requests

"""
获取详细教程、获取代码帮助、提出意见建议
关注微信公众号「裸睡的猪」与猪哥联系
@Author  :   猪哥,
@Version :   2.0"
"""

s = requests.Session()
# cookies序列化文件
COOKIES_FILE_PATH = 'taobao_login_cookies.txt'


class UsernameLogin:

    def __init__(self, username, ua, TPL_password2):
        """
        账号登录对象
        :param username: 用户名
        :param ua: 淘宝的ua参数
        :param TPL_password2: 加密后的密码
        """
        # 检测是否需要验证码的URL
        self.user_check_url = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
        # 验证淘宝用户名密码URL
        self.verify_password_url = "https://login.taobao.com/member/login.jhtml"
        # 访问st码URL
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'
        # 淘宝个人 主页
        self.my_taobao_url = 'https://i.taobao.com/my_taobao.htm'

        # 淘宝用户名
        self.username = "17322316272"
        # 淘宝关键参数，包含用户浏览器等一些信息，很多地方会使用，从浏览器或抓包工具中复制，可重复使用
        self.ua = "121#fWolkqEmjLwlVlhiG8X/lAX+ec+tKuD4ltCYecwkDvu1sQFV5GDdVYmmmc8dK5jVllKY+zPIDMlSAQOZZLQPll9YAcWZKujVVyeH4FJ5KM9lOlrJEGiIlMLYAcfdK5jVlmuY+zpIxM9VO3rnEkDIll9YOc8dKkjVlwr7HzHO/MQVBkbvsbcSMtFPD0rjXxFbbZ3glWfopCibkZeT83Smbgi0CeIAFtZfkQWXnjxSpqLbCZeTM35O3piDkeHXmo60bZienqC9pCibCZ0T83BhbZs0keHaF9FbbZsbnjxSpXsbMqAA5dBLUbi0Ze16Fmibg6bXN4xVEIK0KuuRMc/hCQSbCeIabMwAGXGyt5c5aPa370YKQE/1DqB8vU3iYwBeXoWgqO13faWqBGu7gHMKQgI4l1fQR8ZEpI7olpn3D3cx1rARTqgONwvU7S5iiqMyn3hRmQyNKNHOUPdJovyJSL+8bul0qFcALNOrXs9GfqA7R592JWEmTvzXs4e/LPCGefzQJnz/VG09Ig/zWEIJbwxOZXZMzequlvWNYHGzBhaTDPj3CnHIpbHvLfJB88No0eyj6K2+DMia+UlZHYblFZ20hJYXIPBWWJN8rug4IAFwCRtOdnP36iPskV7wrNOBfQuxSbl1od64UxUcFnE0xpT5W2sUdsvP8oC1qMjFY6zddF/0x2CqDIydQdv4x8YIgXODhNCMYmFDMSNPrPxTY3k8z8gvhU2hMB04QHfUALDwMlCQapd9CnlqIVcMnMEGmEhYgXUqOCMB9xnMDxJh3VyCKqSXpAD5odKh9XYGKkvsICljNfzG/wvx6K8Bi0TkbaTCs/Iby1tSbsEzmFJwHGICorkJWUDqo5EHKvYmnA1K+I0zr6jbWGQVkZpC/OoKaqkvM4AldfAZ/FrfuWgr/KRstDYI22W7rK8BS4Au5P8Z6a3KPo77r5e4PIUy6WwMwFLiBpc2TZeouF/Jfc8Y0+nF4lPSQjLdqwvN2ZV1zSnsU0vJxRAnklLWbdyUUB6Hh5Ir9kVMWolfHBQ3dxx9mN8Jiaii49FpXKN2qyblGD+S8QGuT/hG8VV+wB87vgzkK/h7HddXtxOvSDn5bpn2g+d9MUvGRjQPHKuu3Qe0wVvpDLS7McqvoIaBz8pqyrfiOKYGOqpb9MD4qldiv7SP3XTEX1aPplLzbGj6IVY81G8acZX/iw=="
        # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
        self.TPL_password2 = "84dda97ee855eefb71764c2f1524aaff1caf6dc753d1b242bd8eb125dfc0499549ea8251cba930fc7cb73f9fbba41184fc9d5e60ce143a7f0995c102c1830a50b78ef1178659aaad15a2bb3d70bdff338a87f627c21d676151bc2140255320d71a39d510a4b76e69ff1ee417eb5ae82a187d372ba590dbea7d295e1b6d7d34de"

        # 请求超时时间
        self.timeout = 3

    def _user_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        data = {
            'username': self.username,
            'ua': self.ua
        }
        try:
            response = s.post(self.user_check_url, data=data, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print('检测是否需要验证码请求失败，原因：')
            raise e
        needcode = response.json()['needcode']
        print('是否需要滑块验证：{}'.format(needcode))
        return needcode

    def _verify_password(self):
        """
        验证用户名密码，并获取st码申请URL
        :return: 验证成功返回st码申请地址
        """
        verify_password_headers = {
            # 'Connection': 'keep-alive',
            # ':authority': 'login.taobao.com',
            # ':method': 'POST',
            # ':path': '/member/login.jhtml?redirectURL=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm%3Fspm%3Da2d00.7723416.754894437.1.61531fc917M0p9%26ad_id%3D%26am_id%3D%26cm_id%3D%26pm_id%3D1501036000a02c5c3739',
            # ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'content-length': '2858',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://login.taobao.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm%3Fspm%3Da2d00.7723416.754894437.1.61531fc917M0p9%26ad_id%3D%26am_id%3D%26cm_id%3D%26pm_id%3D1501036000a02c5c3739',
        }
        # 登录toabao.com提交的数据，如果登录失败，可以从浏览器复制你的form data
        verify_password_data = {
            'TPL_username': self.username,
            'ncoToken': '1f1389fac2a670101d8a09de4c99795e8023b341',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://i.taobao.com/my_taobao.htm?spm=a2d00.7723416.754894437.1.61531fc917M0p9&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c3739',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            # 'gvfdcre': '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D613231626F2E323031372E3735343839343433372E372E356166393131643970714B52693126663D746F70266F75743D7472756526726564697265637455524C3D68747470732533412532462532467777772E74616F62616F2E636F6D253246',
            'TPL_password_2': self.TPL_password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1920*1080',
            # 'osVer': 'macos|10.145',
            'naviVer': 'chrome|78.039047',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'osPF': 'Win32',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://i.taobao.com/my_taobao.htm?spm=a2d00.7723416.754894437.1.61531fc917M0p9&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c3739&useMobile=true',
            'showAssistantLink': 'false',
            'um_token': 'T274D86E0BEB4F2F2F527C889BADD92868CE10177BFF895DE67CFE2D52A',
            'ua': self.ua
        }
        try:
            response = s.post(self.verify_password_url, headers=verify_password_headers, data=verify_password_data,
                              timeout=self.timeout)
            response.raise_for_status()
            # 从返回的页面中提取申请st码地址
        except Exception as e:
            print('验证用户名和密码请求失败，原因：')
            raise e
        # 提取申请st码url
        apply_st_url_match = re.search(r'<script src="(.*?)"></script>', response.text)
        # 存在则返回
        if apply_st_url_match:
            print('验证用户名密码成功，st码申请地址：{}'.format(apply_st_url_match.group(1)))
            return apply_st_url_match.group(1)
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _apply_st(self):
        """
        申请st码
        :return: st码
        """
        apply_st_url = self._verify_password()
        try:
            response = s.get(apply_st_url)
            # response.raise_for_status()
        except Exception as e:
            print('申请st码请求失败，原因：')
            raise e
        st_match = re.search(r'"data":{"st":"(.*?)"}', response.text)
        if st_match:
            print('获取st码成功，st码：{}'.format(st_match.group(1)))
            return st_match.group(1)
        else:
            raise RuntimeError('获取st码失败！response：{}'.format(response.text))
            # raise RuntimeError('获取st码失败！')

    def login(self):
        """
        使用st码登录
        :return:
        """
        # 加载cookies文件
        if self._load_cookies():
            return True
        # 判断是否需要滑块验证
        self._user_check()
        st = self._apply_st()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        try:
            response = s.get(self.vst_url.format(st), headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('st码登录请求，原因：')
            raise e
        # 登录成功，提取跳转淘宝用户主页url
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            print('登录淘宝成功，跳转链接：{}'.format(my_taobao_match.group(1)))
            self._serialization_cookies()
            return True
        else:
            raise RuntimeError('登录失败！response：{}'.format(response.text))

    def _load_cookies(self):
        # 1、判断cookies序列化文件是否存在
        if not os.path.exists(COOKIES_FILE_PATH):
            return False
        # 2、加载cookies
        s.cookies = self._deserialization_cookies()
        # 3、判断cookies是否过期
        try:
            self.get_taobao_nick_name()
        except Exception as e:
            os.remove(COOKIES_FILE_PATH)
            print('cookies过期，删除cookies文件！')
            return False
        print('加载淘宝登录cookies成功!!!')
        return True

    def _serialization_cookies(self):
        """
        序列化cookies
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(s.cookies)
        with open(COOKIES_FILE_PATH, 'w+', encoding='utf-8') as file:
            json.dump(cookies_dict, file)
            print('保存cookies文件成功！')

    def _deserialization_cookies(self):
        """
        反序列化cookies
        :return:
        """
        with open(COOKIES_FILE_PATH, 'r+', encoding='utf-8') as file:
            cookies_dict = json.load(file)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            return cookies

    def get_taobao_nick_name(self):
        """
        获取淘宝昵称
        :return: 淘宝昵称
        """
        headers = {
            'User-Agent': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        try:
            response = s.get(self.my_taobao_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页请求失败！原因：')
            raise e
        # 提取淘宝昵称
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            print('登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            raise RuntimeError('获取淘宝昵称失败！response：{}'.format(response.text))


if __name__ == '__main__':
    # 淘宝用户名
    username = '17322316272'
    # 淘宝重要参数，从浏览器或抓包工具中复制，可重复使用
    ua = '121#fWolkqEmjLwlVlhiG8X/lAX+ec+tKuD4ltCYecwkDvu1sQFV5GDdVYmmmc8dK5jVllKY+zPIDMlSAQOZZLQPll9YAcWZKujVVyeH4FJ5KM9lOlrJEGiIlMLYAcfdK5jVlmuY+zpIxM9VO3rnEkDIll9YOc8dKkjVlwr7HzHO/MQVBkbvsbcSMtFPD0rjXxFbbZ3glWfopCibkZeT83Smbgi0CeIAFtZfkQWXnjxSpqLbCZeTM35O3piDkeHXmo60bZienqC9pCibCZ0T83BhbZs0keHaF9FbbZsbnjxSpXsbMqAA5dBLUbi0Ze16Fmibg6bXN4xVEIK0KuuRMc/hCQSbCeIabMwAGXGyt5c5aPa370YKQE/1DqB8vU3iYwBeXoWgqO13faWqBGu7gHMKQgI4l1fQR8ZEpI7olpn3D3cx1rARTqgONwvU7S5iiqMyn3hRmQyNKNHOUPdJovyJSL+8bul0qFcALNOrXs9GfqA7R592JWEmTvzXs4e/LPCGefzQJnz/VG09Ig/zWEIJbwxOZXZMzequlvWNYHGzBhaTDPj3CnHIpbHvLfJB88No0eyj6K2+DMia+UlZHYblFZ20hJYXIPBWWJN8rug4IAFwCRtOdnP36iPskV7wrNOBfQuxSbl1od64UxUcFnE0xpT5W2sUdsvP8oC1qMjFY6zddF/0x2CqDIydQdv4x8YIgXODhNCMYmFDMSNPrPxTY3k8z8gvhU2hMB04QHfUALDwMlCQapd9CnlqIVcMnMEGmEhYgXUqOCMB9xnMDxJh3VyCKqSXpAD5odKh9XYGKkvsICljNfzG/wvx6K8Bi0TkbaTCs/Iby1tSbsEzmFJwHGICorkJWUDqo5EHKvYmnA1K+I0zr6jbWGQVkZpC/OoKaqkvM4AldfAZ/FrfuWgr/KRstDYI22W7rK8BS4Au5P8Z6a3KPo77r5e4PIUy6WwMwFLiBpc2TZeouF/Jfc8Y0+nF4lPSQjLdqwvN2ZV1zSnsU0vJxRAnklLWbdyUUB6Hh5Ir9kVMWolfHBQ3dxx9mN8Jiaii49FpXKN2qyblGD+S8QGuT/hG8VV+wB87vgzkK/h7HddXtxOvSDn5bpn2g+d9MUvGRjQPHKuu3Qe0wVvpDLS7McqvoIaBz8pqyrfiOKYGOqpb9MD4qldiv7SP3XTEX1aPplLzbGj6IVY81G8acZX/iw=='
    # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
    TPL_password2 = '84dda97ee855eefb71764c2f1524aaff1caf6dc753d1b242bd8eb125dfc0499549ea8251cba930fc7cb73f9fbba41184fc9d5e60ce143a7f0995c102c1830a50b78ef1178659aaad15a2bb3d70bdff338a87f627c21d676151bc2140255320d71a39d510a4b76e69ff1ee417eb5ae82a187d372ba590dbea7d295e1b6d7d34de'
    ul = UsernameLogin(username, ua, TPL_password2)
    ul.login()
