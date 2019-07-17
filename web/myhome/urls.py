from django.conf.urls import url
from . views import IndexViews,LoginViews,CartViews,PersonalViews


urlpatterns = [
    # 首页
    url(r'^$',IndexViews.myhome_index,name="myhome_index"),
    # 列表
    url(r'^list/(?P<cid>[0-9]+)',IndexViews.myhome_list,name="myhome_list"),
    url(r'^all_list/',IndexViews.myhome_all_list,name="myhome_all_list"),

    # # 详情
    url(r'^info/',IndexViews.myhome_info,name="myhome_info"),

    # 登录
    url(r'^login/',LoginViews.myhome_login,name="myhome_login"),
    url(r'^dologin/',LoginViews.myhome_dologin,name="myhome_dologin"),
    url(r'^isphone/',LoginViews.isphone,name="isphone"),
    # 退出登录
    url(r'^logout/',LoginViews.myhome_logout,name="myhome_logout"),


    # 注册
    url(r'^register/',LoginViews.myhome_register,name="myhome_register"),
    url(r'^doregister/',LoginViews.myhome_doregister,name="myhome_doregister"),

    # 短信发送
    url(r'^sendMsg/',LoginViews.myhome_sendMsg,name="myhome_sendMsg"),

    # 个人中心首页
    url(r'personal/$', PersonalViews.myhome_personal, name="myhome_personal"),
    # 地址管理页面
    url(r'address/$', PersonalViews.myhome_address, name="myhome_address"),
    # 设置为默认地址
    url(r'address/def/$', PersonalViews.myhome_address_def, name="myhome_address_def"),
    # 地址编辑页面
    url(r'address/edit/$', PersonalViews.myhome_address_edit, name="myhome_address_edit"),
    # 执行编辑
    url(r'address/doedit/$', PersonalViews.myhome_address_doedit, name="myhome_address_doedit"),
    # 地址删除
    url(r'address/del/$', PersonalViews.myhome_address_del, name="myhome_address_del"),

    # 购物车  增删改查 
    url(r'^cart/add/',CartViews.myhome_cart_add,name="myhome_cart_add"),
    url(r'^cart/index/',CartViews.myhome_cart_index,name="myhome_cart_index"),
    url(r'^cart/del/',CartViews.myhome_cart_del,name="myhome_cart_del"),
    url(r'^cart/clear/',CartViews.myhome_cart_clear,name="myhome_cart_clear"),
    url(r'^cart/edit/',CartViews.myhome_cart_edit,name="myhome_cart_edit"),
    

    # 订单
]
