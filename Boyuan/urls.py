"""Boyuan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve


import Bo_yuan
from Bo_yuan import views, api
# from Boyuan.settings import STATIC_ROOT
from Boyuan import settings

from Boyuan.settings import MEDIA_ROOT



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('Bo_yuan.urls', namespace='api')),


    # 后台管理
    url(r'^$', views.rindex),
    # 首页
    url(r'^index', views.index, name='index'),







    # 广告管理
    # 首页banner管理
    url(r'^ad/banner$', views.banner, name='banner'),
    # 广告位管理
    url(r'^ad/advertising$', views.advertising, name='advertising'),
    # banner 创建
    url(r'^ad/banner-create$', views.banner_create, name='banner_create'),

    # 二手车管理
    # 品牌管理
    url(r'^car/brand$', views.brand, name='brand'),
    # 车型管理
    url(r'^car/car-type$', views.car_type, name='car_type'),
    url(r'^car/create-type$', views.create_type, name='create_type'),
    # 级别管理
    url(r'^car/car-serie$', views.car_serie, name='car_serie'),
    # 车源管理
    url(r'^car/cars$', views.cars, name='cars'),
    url(r'^car/car-yuan$', views.car_yuan, name='car_yuan'),

    # 车辆审核管理
    url(r'^car-check$', views.car_check, name='car_check'),
    # 预览
    # url(r'^car-look$', views.car_look, name='car_look'),
    # 车辆审核 通过/拒绝
    url(r'^car-operation$', views.car_operation, name='car_operation'),
    # 拒绝
    # url(r'^audit-failed$', views.audit_failed, name='audit_failed'),
    # 预览
    # url(r'^check-look$', views.audit_success, name='check_ok'),
    # 设置级别
    # url(r'^change-type$', views.change_type, name='change-type'),

    # 预约管理
    # 卖车预约管理
    url(r'^appointment/sell-appointment$', views.sell_appointment, name='sell_appointment'),
    # 会员预约买车管理
    url(r'^appointment/vip-appointment$', views.vip_appointment, name='vip_appointment'),

    # 会员管理
    url(r'^vip$', views.vip, name='vip'),
    url(r'^vip-details$', views.vip_details, name='vip_details'),


    # 单页管理
    # 企业文化
    url(r'^corporate-culture$', views.corporate_culture, name='corporate_culture'),

    # 模块管理
    # 车况检测
    url(r'^module/vehicle-inspection$', views.vehicle_inspection, name='vehicle_inspection'),
    # 保养车
    url(r'^module/car-maintenance$', views.car_maintenance, name='car_maintenance'),
    # 保险超市
    url(r'^module/insurance-products$', views.insurance_products, name='insurance_products'),
    # 洗车服务
    url(r'^module/fcwt$', views.fcwt, name='fcwt'),

    # 系统设置
    url(r'^login$', views.login),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^change-passwd$', views.change_passwd, name='change_passwd'),







    # # 品牌
    # url(r'^brands/', views.brands),
    # # 车型
    # url(r'^cars_type/', views.brands),
    # # 级别
    # url(r'^brands/', views.brands),
    # # 车源管理 (总车辆)
    # url(r'^cars/', views.cars),
    # # 会员 (总会员)
    # url(r'^vips/', views.vips),
    # # 今日新增
    # url(r'^daus/', views.daus),
    #
    # # 预约看车
    # url(r'^appointment/', views.appointment),
    # # 预约卖车
    # url(r'^sell_appointment/', views.sell_appointment),
    # 发布
    # url(r'^issue/', api.issue),
    # # 售车
    # url(r'^sellcar/', views.sellcar),
    #
    # url(r'^search_user_car/', views.search_user_car),
    # url(r'^search_car/', views.search_car),
    # url(r'^create_brands/', views.create_brands),




    # static
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    # media
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # url(r'^(?P<path>.*.txt)$', serve, {'document_root': settings.BASE_DIR}),
]

# error处理
handler404 = Bo_yuan.views.page_not_found
handler500 = Bo_yuan.views.server_error


