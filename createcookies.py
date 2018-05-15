# !/usr/bin/python3
# -*- coding: utf-8 -*-

from redisdatabase import Redis
from settings import LOGIN_URL, LOGINSUCCESS_URL, VERIFY_URL
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import requests
import json


class DoubanCreateCookies(object):
    def __init__(self):
        self.account_db = Redis('account')
        self.cookies_db = Redis('cookies')
        self.login_url = LOGIN_URL
        self.loginsuccess_url = LOGINSUCCESS_URL
        self.verify_url = VERIFY_URL
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable--gpu')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def run(self):
        for pair in self.account_db.key_valued_pairs().items():
            username, password = pair
            if not self.cookies_db.read(username):
                self.execute(username.decode(), password.decode())
        self.driver.close()

    def execute(self, username, password):
        self.driver.delete_all_cookies()
        self.login(username, password)
        if self.login_successfully():
            print('Login was successful!')
            self.process_cookies(username)
        elif self.password_error(username):
            print('PasswordError, this username:{} was deleted'.format(username))
        elif self.vercode_error():
            print('VercodeError, login again')
            self.execute(username, password)
        else:
            print('Login failed because of unknown reason')

    def login(self, username, password):
        """
        Send username, password [,vercode] to input tags and click the login button
        """
        print('Now creating cookies of:{}'.format(username))
        self.driver.get(self.login_url)
        username_input = self.driver.find_element_by_xpath('//input[@id="email"]')
        username_input.clear()
        username_input.send_keys(username)
        password_input = self.driver.find_element_by_xpath('//input[@id="password"]')
        password_input.clear()
        password_input.send_keys(password)
        try:
            self.driver.find_element_by_xpath('//img[@id="captcha_image"]').get_attribute('src')
            self.process_vercode()
        except NoSuchElementException:
            pass
        login_button = self.driver.find_element_by_xpath('//form[@id="lzform"]//input[@class="btn-submit"]')
        login_button.click()
        time.sleep(5)
        print('URL after login:{}'.format(self.driver.current_url))

    def process_vercode(self):
        """
        Manually find the verification code image, read the vercode and input it
        """
        vercode_url = self.driver.find_element_by_xpath('//img[@id="captcha_image"]').get_attribute('src')
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(vercode_url, headers=headers)
        with open('vercode/image.jpg', 'wb') as f:
            f.write(response.content)
        vercode = input('please input vercode from image.jpg in folder "vercode":')
        vercode_input = self.driver.find_element_by_xpath('//input[@id="captcha_field"]')
        vercode_input.clear()
        vercode_input.send_keys(vercode)

    def login_successfully(self):
        if self.driver.current_url == self.loginsuccess_url:
            return True
        else:
            return False

    def process_cookies(self, username):
        """
        Fetch cookies after login successfully and write it in Redis
        """
        self.driver.get(self.verify_url)
        list_cookies = self.driver.get_cookies()
        cookies = {}
        for cookie in list_cookies:
            cookies[cookie['name']] = cookie['value']
        self.cookies_db.write(username, json.dumps(cookies))
        print('Cookies of {} was successfully wrote in Redis'.format(username))

    def password_error(self, username):
        """
        Delete the username if password is incorrect
        """
        try:
            self.driver.find_element_by_xpath('//*[@id="item-error"]/p')
            self.account_db.delete(username)
            return True
        except NoSuchElementException:
            return False

    def vercode_error(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="captcha-solution_err"]')
            return True
        except NoSuchElementException:
            return False


if __name__ == '__main__':
    DoubanCreateCookies().run()




