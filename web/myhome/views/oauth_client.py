import json
import urllib
import re

class OAuth_Base(object):    #基类，将相同的方法写入到此类中
    def __init__(self,client_id,client_key,redirect_url):   #初始化，载入对应的应用id、秘钥和回调地址
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def _get(self,url,data):      #get方法
        request_url = '%s?%s' % (url,urllib.parse.urlencode(data))
        response = urllib.request.urlopen(request_url)
        return response.read()

    def _post(self,url,data):    #post方法
        request = urllib.request.Request(url,data = urllib.parse.urlencode(data).encode(encoding='UTF8'))     #1
        response = urllib.request.urlopen(request)
        return response.read()

# github类
class OAuth_GITHUB(OAuth_Base):
    def get_auth_url(self):
        params = {
            'client_id':self.client_id,
            'response_type':'code',
            'redirect_uri':self.redirect_url,
            'scope':'user:email',
            'state':1
        }
        url = 'https://github.com/login/oauth/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self,code):
        params = {
            'grant_type':'authorization_code',
            'client_id':self.client_id,
            'client_secret':self.client_key,
            'code':code,
            'redirect_url':self.redirect_url
        }
        response = self._post('https://github.com/login/oauth/access_token',params)  #此处为post方法
        result = urllib.parse.parse_qs(response,True)
        self.access_token = result[b'access_token'][0]
        return self.access_token

#github不需要获取openid，因此不需要get_open_id()方法

    def get_user_info(self):
        params ={'access_token':self.access_token}
        response = self._get('https://api.github.com/user',params)
        result = json.loads(response.decode('utf-8'))
        self.openid = result.get('id','')
        return result

    def get_email(self):
        params ={'access_token':self.access_token}
        response = self._get('https://api.github.com/user/emails',params)
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']

# qq类
class OAuth_QQ(OAuth_Base):
    def get_auth_url(self):
        params = {
            'client_id':self.client_id,
            'response_type':'code',
            'redirect_uri':self.redirect_url,
            'scope':'get_user_info',
            'state':1
        }
        url = 'https://graph.qq.com/oauth2.0/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self,code):
        params = {
            'grant_type':'authorization_code',
            'client_id':self.client_id,
            'client_secret':self.client_key,
            'code':code,
            'redirect_uri':self.redirect_url
        }
        response = self._get('https://graph.qq.com/oauth2.0/token',params)
        result = urllib.parse.parse_qs(response,True)
        self.access_token = result[b'access_token'][0]
        return self.access_token

    def get_open_id(self):
        params ={'access_token':self.access_token}
        response = self._get('https://graph.qq.com/oauth2.0/me',params)
        response = re.split("[()]",response.decode('utf-8'))[1]   #将回应中的callback前缀去掉
        result = json.loads(response)
        self.openid = result.get('openid','')
        return self.openid

    def get_user_info(self):
        params ={
            'access_token':self.access_token,
            'openid':self.openid,
            'oauth_consumer_key':self.client_id,
        }
        response = self._get('https://graph.qq.com/user/get_user_info',params)
        result = json.loads(response.decode('utf-8'))
        return result

#因为QQ没有开放获取qq邮箱的接口，因此不需要重写get_email（）

# 微博类
class OAuth_WEIBO(OAuth_Base):
    def get_auth_url(self):
        params = {
            'client_id':self.client_id,
            'response_type':'code',
            'redirect_uri':self.redirect_url,
            'scope':'email',
            'state':1
        }
        url = 'https://api.weibo.com/oauth2/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self,code):
        params = {
            'grant_type':'authorization_code',
            'client_id':self.client_id,
            'client_secret':self.client_key,
            'code':code,
            'redirect_uri':self.redirect_url
        }
        response = self._post('https://api.weibo.com/oauth2/access_token',params)
        result = json.loads(response.decode('utf-8'))
        self.access_token = result["access_token"]
        self.openid = result["uid"]
        return self.access_token

    def get_open_id(self):    #新浪的openid在之前get_access_token（）方法中已经获得
        return self.openid

    def get_user_info(self):
        params ={
            'access_token':self.access_token,
            'uid':self.openid,
        }
        response = self._get('https://api.weibo.com/2/users/show.json',params)
        result = json.loads(response.decode('utf-8'))
        return result

    def get_email(self):
        params ={'access_token':self.access_token}
        response = self._get('https://api.weibo.com/2/account/profile/email.json',params)
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']

