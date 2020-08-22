from django.conf.urls import url, include


from Bo_yuan import api


urlpatterns = [
    # API
    # 对接微信登陆 返回openid session_key
    url(r'^code2session$', api.Code2SessionAPIView.as_view()),

    # 用户信息
    url(r'^users$', api.UsersAPIView.as_view()),
    url(r'^users/(?P<pk>\d+)/$', api.UserAPIView.as_view()),
    # 商家入驻
    url(r'^join$', api.JoinAPIView.as_view()),
    # 个人信息更改
    url(r'^user/update$', api.UserUpdateAPIView.as_view()),
    # 我的预约
    url(r'^user/appointment$', api.UserAppointmentAPIView.as_view()),
    # 更改状态操作
    url(r'^user/cancel$', api.UserCancelAppointmentAPIView.as_view()),
    # 我的发布
    url(r'^user/issue$', api.UserIssueAPIView.as_view()),
    url(r'^user/issue/(?P<pk>\d+)/$', api.UserIssueDAPIView.as_view()),
    # 编辑
    url(r'^user/issue-edit$', api.UserIssueEditAPIView.as_view()),
    # 我的关注
    url(r'^user/likes$', api.UserLikeAPIView.as_view()),

    url(r'^update-data$', api.year),



    # 导入数据
    url(r'^create-brands$', api.create_brands),

    # 首页数据
    url(r'^index$', api.IndexAPIView.as_view()),
    # 热门
    url(r'^hot$', api.HotAPIView.as_view()),


    # banner
    url(r'^banners$', api.BannersAPIView.as_view()),
    url(r'^banners/(?P<pk>\d+)/$', api.BannerAPIView.as_view()),

    # search search prices 价格筛选 格式 0-8  5>
    url(r'^search$', api.SearchAPIView.as_view()),

    # 二手车 添加
    url(r'^cars$', api.CarsAPIView.as_view()),
    url(r'^cars/(?P<pk>\d+)/$', api.CarAPIView.as_view()),
    # 品牌 / 车系 brand
    url(r'^brands$', api.BrandsAPIView.as_view()),
    # 车型
    url(r'^car-type$', api.CarTypeAPIView.as_view()),

    # # 品牌下车系
    # url(r'^brands/(?P<pk>\d+)/$', api.BrandAPIView.as_view()),

    # # 车系>车 series cars接口
    # url(r'^series-car/(?P<pk>\d+)/$', api.SeriesCarAPIView.as_view()),


    # 快速卖车(预约卖车)
    url(r'^sell-car$', api.SellCarAPIView.as_view()),







    # # 品牌下车系
    # url(r'^brands/(?P<pk>\d+)/$', api.BrandAPIView.as_view()),

    # # 车系>车 series cars接口
    # url(r'^series-car/(?P<pk>\d+)/$', api.SeriesCarAPIView.as_view()),


    # 智能排序  最新上架 价格最高 价格最低 time车龄最短 里程最少
    url(r'^intelligent-search$', api.ZNSearchAPIView.as_view()),


    # 筛选   车型 变速箱 排量 里程 颜色




    url(r'^fwb$', api.FwbAPIView.as_view()),

    # 图片上传
    url(r'^upload-img$', api.uploadimg),
    url(r'^upload-imgn$', api.uploadimgn),
    # 视频上传
    url(r'^upload-video$', api.uploadvideo),




]


