openqq
========

OpenQQ SDK for Python

OpenQQ登录的python sdk.


目前支持功能

1. 获取授权登录地址,需要自己跳转.

2.获取access_token,设置access_token

3.获取openid,设置openid,可以在第二步一起完成

4.执行api调用.返回结果为dict对象.

 

使用步骤:

1.获取登录链接

client = OpenQQClient(client_id='your client_id',client_secret='your client_secret',redirect_uri='登录成功后的回调地址')

client.get_auth_url()

2.授权成功后,会跳转至回调地址,并带有code参数.

这时可以通过code获得access_token


client.get_access_token(code) #返回access_token,expires_in


3.接第2步,获得openid

client.request_openid() #返回openid

client.set_openid(openid)

4.执行api调用,默认执行get请求,只需传入api地址,如果要使用POST需传入method和params

client.request_api('user/get_user_info')

 
