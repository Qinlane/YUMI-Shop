from django.conf.urls import url
from . views import IndexViews,UsersViews,CatesViews,GoodsViews,CenterViews

urlpatterns = [
    url(r'^index/$',IndexViews.index,name="myadmin_index"),

    # 权限管理
    # 管理员管理
    url(r'^auth/user/index/$',IndexViews.myadmin_authuser_index,name="myadmin_authuser_index"),
    url(r'^auth/user/add/$',IndexViews.myadmin_authuser_add,name="myadmin_authuser_add"),
    url(r'^auth/user/insert/$',IndexViews.myadmin_authuser_insert,name="myadmin_authuser_insert"),
    url(r'^auth/user/edit/$',IndexViews.myadmin_authuser_edit,name="myadmin_authuser_edit"),

    # 权限管理组
    url(r'^auth/group/index/$',IndexViews.myadmin_authgroup_index,name="myadmin_authgroup_index"),
    url(r'^auth/group/add/$',IndexViews.myadmin_authgroup_add,name="myadmin_authgroup_add"),
    url(r'^auth/group/insert/$',IndexViews.myadmin_authgroup_insert,name="myadmin_authgroup_insert"),
    url(r'^auth/group/edit/$',IndexViews.myadmin_authgroup_edit,name="myadmin_authgroup_edit"),
 

    # 登录页
    url(r'^login/$',IndexViews.myadmin_login,name="myadmin_login"),
    url(r'^dologin/$',IndexViews.myadmin_dologin,name="myadmin_dologin"),
    url(r'^logout/$',IndexViews.myadmin_logout,name="myadmin_logout"),
    url(r'^verifycode/$',IndexViews.verifycode,name="myadmin_vcode"),

    # 会员管理
    url(r'^user/add/$', UsersViews.user_add,name="myadmin_user_add"),
    url(r'^user/insert/$', UsersViews.user_insert,name="myadmin_user_insert"),
    url(r'^user/index/$', UsersViews.user_index,name="myadmin_user_index"),
    url(r'^user/edit/$',UsersViews.user_edit,name="myadmin_user_edit"),
    url(r'^user/setstutus/$', UsersViews.user_set_status,name="myadmin_user_set_status"),

    # 分类管理
    url(r'^cate/add/$',CatesViews.cate_add,name="myadmin_cate_add"),
    url(r'^cate/index/$',CatesViews.cate_list,name="myadmin_cate_index"),
    url(r'^cate/del/$',CatesViews.cate_del,name="myadmin_cate_del"),
    url(r'^cate/edit/$',CatesViews.cate_edit,name="myadmin_cate_edit"),

    # 商品管理
    url(r'^goods/add/$',GoodsViews.goods_add,name="myadmin_goods_add"),
    url(r'^goods/index/$', GoodsViews.goods_index,name="myadmin_goods_index"),
    url(r'^goods/insert/$',GoodsViews.goods_insert,name="myadmin_goods_insert"),
    url(r'^goods/edit/$',GoodsViews.goods_edit,name="myadmin_goods_edit"),
    url(r'^goods/del/$',GoodsViews.goods_del,name="myadmin_goods_del"),

    # 订单管理
    url(r'^center/index/$',CenterViews.center_index,name="myadmin_center_index"),
    url(r'^center/erit/$',CenterViews.center_edit,name="myadmin_center_edit"),
  

    
]   
