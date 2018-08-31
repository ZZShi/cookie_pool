# -*- coding: utf-8 -*-
"""
@Time   : 2018/8/27 18:15
@File   : login.py
@Author : ZZShi
程序作用：
    录入账号并模拟登录
"""
import re
import json
import time
import requests
import hashlib
from bs4 import BeautifulSoup


class Login(object):
    """
    定义模拟登录的基类
    """
    def __init__(self):
        self.session = requests.Session()

    def get_token(self):
        """
        得到登录所需的token
        :return:
        """
        pass

    def login(self, username, password):
        """
        模拟登录
        :return:
        """
        pass

    def good_cookies(self):
        """
        判断cookies是否有效
        :return:
        """
        pass

    def get_cookies(self):
        """
        得到有效的cookies
        :return:
        """
        pass


class LagouLogin(Login):
    """
    拉勾网模拟登录
    """
    def __init__(self):
        """
        初始化
        """
        Login.__init__(self)
        self.login_url = 'https://passport.lagou.com/login/login.html'
        self.post_url = 'https://passport.lagou.com/login/login.json'
        self.ticket_url = 'https://passport.lagou.com/grantServiceTicket/grant.html'
        self.test_url = 'https://www.lagou.com/'
        self.hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                    Chrome/67.0.3396.62 Safari/537.36',
            'Host': 'passport.lagou.com',
            'Referer': 'https://www.lagou.com/'
        }

    def get_token(self):
        """
        获取登录所需的token、code
        :return:
        """
        try:
            r = self.session.get(self.login_url, headers=self.hd)
            html = r.text
            token = re.search(r"window.X_Anti_Forge_Token = '(.*?)';", html).group(1)
            code = re.search(r"window.X_Anti_Forge_Code = '(.*?)'", html).group(1)
            time.sleep(2)
            return token, code
        except Exception as e:
            print('Token获取异常---：', e.args)

    def get_ticket(self):
        """
        登录之后还需要得到服务器认可，得到的cookies才有效
        :return:
        """
        hd = {
            'Host': 'passport.lagou.com',
            'Referer': self.login_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/67.0.3396.62 Safari/537.36'
        }
        try:
            r = self.session.get(self.ticket_url, headers=hd, allow_redirects=False)
            url = r.next.url
            url = re.sub('http://', 'https://', url)
            hd['Host'] = 'www.lagou.com'
            r = self.session.get(url, headers=hd, allow_redirects=False)
        except Exception as e:
            print('Ticket获取异常---：', e.args)

    def login(self, username, password):
        """
        模拟登录,登录前需要拿到token，登录后需要拿到ticket
        :return:
        """
        token, code = self.get_token()
        hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                    Chrome/67.0.3396.62 Safari/537.36',
            'Host': 'passport.lagou.com',
            'Referer': self.login_url,
            'X-Anit-Forge-Token': token,
            'X-Anit-Forge-Code': code,
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 对密码进行了md5双重加密
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        # 'veenike' 这个值是在js文件找到的一个写死的值
        password = 'veenike' + password + 'veenike'
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        data = {
            'isValidate': True,
            'username': username,
            'password': password,
            'request_from_verifyCode': '',
            'submit': ''
        }
        try:
            r = self.session.post(self.post_url, data=data, headers=hd)
            r.raise_for_status()
            # print(r.json())
            state = r.json().get('state')
            if state == 1:
                print('\t%s\t\t登录成功...' % username)
                time.sleep(2)
                self.get_ticket()
                if self.good_cookies():
                    print('\t%s\t\tCookies有效...' % username)
                else:
                    print('\t%s\t\tCookies无效!!!' % username)
            else:
                print('\t%s\t\t登录失败!!!' % username)
        except Exception as e:
            print('\t%s\t\t登录异常---%s' % (username, e.args))

    def good_cookies(self, cookies=None):
        """
        判断当前cookies是否可以使用
        :return:
        """
        hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                                            Chrome/67.0.3396.62 Safari/537.36',
            'Host': 'www.lagou.com'
        }
        if cookies:
            cookies = json.loads(cookies)
        else:
            cookies = self.session.cookies
        r = requests.get(self.test_url, cookies=cookies, headers=hd)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            user = soup.find('span', attrs={'class': 'unick bl'}).text
            # 保存到数据库
            pass
            return True
        except Exception as e:
            print('Cookies无效：', e.args)
            return False

    def get_cookies(self):
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        cookies = json.dumps(cookies)
        return cookies


class GithubLogin(Login):
    """
    github模拟登录
    """
    def __init__(self):
        Login.__init__(self)
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.test_url = 'https://github.com/'
        self.hd = {
            'Host': 'github.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/67.0.3396.62 Safari/537.36'
        }

    def get_token(self):
        try:
            r = self.session.get(self.login_url, headers=self.hd)
            soup = BeautifulSoup(r.text, 'html.parser')
            token = soup.find('input', attrs={'name': 'authenticity_token'})['value']
            return token
        except Exception as e:
            print('Token获取失败：', e.args)

    def login(self, username, password):
        data = {
            'commit': 'Sign in',
            'utf-8': True,
            'authenticity_token': self.get_token(),
            'login': username,
            'password': password

        }
        try:
            r = self.session.post(self.post_url, data=data, headers=self.hd, allow_redirects=False)
            # 登录成功之后会重定向
            if r.status_code == 302:
                print('\t%s\t\t登录成功...' % username)
                if self.good_cookies():
                    print('\t%s\t\tCookies有效...' % username)
                else:
                    print('\t%s\t\tCookies无效...' % username)
            else:
                print('\t%s\t\t登录失败...' % username)
        except Exception as e:
            print('\t{}\t\t登录异常---'.format(username, e.args))

    def good_cookies(self, cookies=None):
        if cookies:
            cookies = json.loads(cookies)
        else:
            cookies = self.session.cookies
        try:
            r = requests.get(self.test_url, cookies=cookies, headers=self.hd)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            user = soup.find('meta', attrs={'name': 'octolytics-actor-login'})['content']
            if user:
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_cookies(self):
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        cookies = json.dumps(cookies)
        return cookies
