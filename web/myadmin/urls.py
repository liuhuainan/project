from django.conf.urls import url
from . views import views,userviews,typesviews,goodsviews,ordersviews,authviews

urlpatterns = [
    # 后台首页
    url(r'^$', views.index,name='myadmin_index'),

    # 后台权限管理
    # 后台用户添加
    url(r'^auth/user/add$', authviews.useradd,name='auth_user_add'),    
    # 后台用户列表
    url(r'^auth/user/list$', authviews.userlist,name='auth_user_list'),    
    url(r'^auth/group/del/(?P<uid>[0-9]+)$', authviews.userdel,name='auth_user_del'),      
    
    # 后台组添加
    url(r'^auth/group/add$', authviews.groupadd,name='auth_group_add'),    
    # 后台组列表
    url(r'^auth/group/list$', authviews.grouplist,name='auth_group_list'),
    url(r'^auth/group/edit/(?P<gid>[0-9]+)$', authviews.groupedit,name='auth_group_edit'),      
    
    # 会员管理
    url(r'^user/add/$', userviews.add,name='myadmin_user_add'),
    url(r'^user/index/$', userviews.index,name='myadmin_user_list'),
    url(r'^user/delete/$', userviews.delete,name='myadmin_user_delete'),
    url(r'^user/edit/$', userviews.edit,name='myadmin_user_edit'),
    
    # 商品分类管理
    url(r'^types/add/$', typesviews.add,name='myadmin_types_add'),
    url(r'^types/index/$', typesviews.index,name='myadmin_types_list'),
    url(r'^types/delete/$',typesviews.delete,name='myadmin_types_delete'),
    url(r'^types/edit/$', typesviews.edit,name='myadmin_types_edit'),  
   
    # 商品管理
    url(r'^goods/add/$', goodsviews.add,name='myadmin_goods_add'),
    url(r'^goods/index/$', goodsviews.index,name='myadmin_goods_list'),
    url(r'^goods/delete/$',goodsviews.delete,name='myadmin_goods_delete'),
    url(r'^goods/edit/$', goodsviews.edit,name='myadmin_goods_edit'),
    # 商品订单
    url(r'^orders/index$', ordersviews.index,name='myadmin_orders_index'),
    url(r'^orders/edit$', ordersviews.edit,name='myadmin_orders_edit'),
    # 后台登录和登录验证
    url(r'^login/', authviews.mylogin,name='myadmin_login'),
    url(r'^logout/', authviews.mylogout,name='myadmin_logout'),         
                
]
