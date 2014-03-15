# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import time

try:
    import urllib.parse as urllib_parse  # py3
except ImportError:
    import urlpase as urllib_parse  # py2


class QQMixin(object):
    """
    腾讯的开放平台的员工们，你们像屎一样的api设计还有文档，你们老板知道的吗？？？
    """
    _WEB_BASE_URL = "https://graph.qq.com"
    _API_VERSION = "oauth2.0"
    _WEB_OAUTH_AUTHORIZE_URL = "%s/%s/%s" % (_WEB_BASE_URL, _API_VERSION, "authorize")
    _WEB_OAUTH_ACCESS_TOKEN_URL = "%s/%s/%s" % (_WEB_BASE_URL,_API_VERSION, "token")

    def __init__(self, client_id, client_secret,
                 redirect_uri=None, response_type='code', display='', state='CSRF_Protection'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        #desplay 用于展示的样式。不传则默认展示为PC下的样式。 如果传入“mobile”，则展示为mobile端下的样式。
        self.display = display
        self.state = state
        self.access_token = None
        self.openid = None
        self.expires = 0.0

    def set_access_token(self, access_token, expires_in):
        """
            设置access_token
        """
        self.access_token = access_token
        self.expires = expires_in

    def get_auth_url(self, redirect_uri=None,):
        """
            获取登录的url。需要跳转至该url,让用户进行QQ授权登录
        """
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        params = {'client_id': self.client_id,
                  'response_type': self.response_type,
                  'redirect_uri': redirect,
                  'state': self.state,
                  }
        return '%s?%s' % (self._WEB_OAUTH_AUTHORIZE_URL, urllib.urlencode(params))

    def get_access_token(self, code, get_openid=True):
        """
            获得access_token
        """
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'code': code,
                  'redirect_uri': self.redirect_uri,
                  }
        url = '%s?%s' % (self._WEB_OAUTH_ACCESS_TOKEN_URL, urllib.urlencode(params))
        resp = urllib2.urlopen(url)

        url_parts = urllib_parse(resp.read())
        access_token = str(urllib_parse.parse_qs['access_token'][0])
        expires_in = float(int(url_parts['expires_in'][0]) + int(time.time()))

        if get_openid:
            self.get_openid()
        return {'access_token':access_token, 'expires_in': expires_in}

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def get_openid(self):
        """
            获得openid,(腾讯返回的内容用了callback()包含)...这种东西应该让开发者去决定要不要好吧
            callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );
        """
        params = {'access_token': self.access_token}
        url = '%s/%s/%s?%s' % (self._WEB_BASE_URL,self._API_VERSION, 'me',(params))
        resp = urllib2.urlopen(url)
        callback_str = resp.read()
        json_content = callback_str[9:-3]
        client_id_open_id = json.loads(json_content)
        self.openid = client_id_open_id['openid']
        return self.openid

    def get_user_info(self):
        return self.request_api_info("user/get_user_info")


    def request_api_info(self,method="GET", dest_api="", data={}):
        params = {'access_token': self.access_token,
                  'oauth_consumer_key': self.client_id,
                  'openid': self.openid}
        url = '%s/%s?%s' % (self._WEB_BASE_URL, dest_api, (params))
        if method.upper() == "GET":
            resp = urllib2.urlopen(url)
        elif method.upper() == "POST":
            data = urllib.urlencode(data)
            resp = urllib2.urlopen(url, data=data)
        else:
            raise "Error!! Bad http request method"
        return json.loads(resp)