class UserDefineCookie:
    @staticmethod
    def get_xueqiu_cookie():
        # 因为泄漏了自己的个人信息，所以需要填写自己的
        # 通过浏览器开发者工具或者抓包拿到雪球cookie填写
        cookie = open('cookie_xueqiu.txt').read()
        print('xueqiu cookie:' + cookie)
        return cookie

    @staticmethod
    def get_guoren_cookie():
        # 因为泄漏了自己的个人信息，所以需要填写自己的
        # 通过浏览器开发者工具或者抓包拿到果仁cookie填写
        cookie = open('cookie_guoren.txt').read()
        print('guoren cookie:' + cookie)
        return cookie
