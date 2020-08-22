import datetime
import hashlib
import json
import re
import time

import requests
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import formats
from rest_framework.response import Response
from rest_framework.views import APIView

from Bo_yuan.models import Users, Cars, CarsSeries, CarsTypes, Brands, Banners, Fwb, Appointments, UserLikes, Img, Video
from Bo_yuan.serializers import CarsSerializer, SellAppointmentsSerializer, UserSerializer, \
    BannersSerializer, FwbSerializer, LookAppointmentsSerializer, LikeCarSerializer, \
    BrandsSerializer, CarSerializer, SeriesSerializer, UsersSerializer, UserDetailSerializer, \
    IssueCarsSerializer, CarsTypesSerializer, UserIssueCarsSerializer, CarissueSerializer

"""
获取openid{"data":{"StatusCode":200,"Info":"请求(或处理)成功",
"Data":{"openid":"oWy7F5G3LL0m7_Xp4YVKsbKlH7Wo","session_key":"CHrNOhCux3NMvco5UaoaDw==",
"unionid":null,"errcode":0,"ErrorCodeValue":0,"errmsg":null,"P2PData":null}},
"header":{"Cache-Control":"no-cache","Pragma":"no-cache","Content-Length":"216",
"Content-Type":"application/json; charset=utf-8","Expires":"-1","Server":"Microsoft-IIS/8.5",
"X-AspNet-Version":"4.0.30319","X-Powered-By":"ASP.NET","Date":"Sat, 19 Oct 2019 11:45:17 GMT"},
"statusCode":200,"cookies":[],"errMsg":"request:ok"}
"""


class Code2SessionAPIView(APIView):
    # authentication_classes = (UserAuth, )
    #
    # def get(self, request):
    #     skey = request.query_params.get('skey')
    #
    #     return Response(request.data)

    def post(self, request, *args, **kwargs):
        # appid = 'wxf2c4972a41abe66c'
        # secret = '9895d1f415b19600efabb9ee9b16a45f'
        # js_code = 'ss'
        try:
            appid = request.data.get('appid')
            secret = request.data.get('secret')
            js_code = request.data.get('js_code')

            url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
            response = json.loads(requests.get(url).content)  # 将json数据包转成字典
            # return Response(data={'msg': str(response)})
        except Exception as e:
            return Response(data={'msg': '失败啦', 'data': request.data})

        try:

            # 有错误码
            # 获取成功
            openid = response['openid']
            session_key = response['session_key']
            # 保存openid, 需要先判断数据库中有没有这个openid
            # 生成自定义登录态，返回给前端
            # sha = hashlib.sha1()
            # sha.update(openid.encode())
            # sha.update(session_key.encode())
            # digest = sha.hexdigest()
            # 将自定义登录态保存到缓存中
            #
            # cache.set(digest, u_id)
            data = {'openid': openid, 'session_key': session_key, 'status': 900, 'msg': 'ok'}
            return Response(data)

        except Exception as e:
            response = {'status': 901, 'message': 'openid获取失败，error:{}'.format(str(response))}
            return Response(response)


class UsersAPIView(APIView):
    # authentication_classes = (UserAuth, )

    def get(self, request):
        try:
            response = {'status': 900, 'message': '会员列表获取成功'}
            users_class = Users.objects.all()
            users = UserSerializer(instance=users_class, many=True)

            response['data'] = users.data
            return Response(response)
        except Exception as e:
            response = {'status': 901, 'message': '会员列表获取失败，error:{}'.format(e)}
            return Response(response)

    def post(self, request):
        response = {'status': 900, 'message': '用户添加成功'}
        try:
            wx_name = request.data.get('wx_name')
            wx_icon = request.data.get('wx_icon')
            openid = request.data.get('openid')
            user = Users.objects.filter(openid=openid).first()
            if user:
                user = UserSerializer(user)
                response['message'] = '用户获取成功'
                response['data'] = user.data
                return Response(response)
            else:
                user = Users.objects.create(wx_name=wx_name, wx_icon=wx_icon, openid=openid)
                user = UserSerializer(user)
                response['data'] = user.data
                return Response(response)


        except Exception as e:
            response['status'] = 901
            response['message'] = '用户添加失败'
            return Response(response)


# 商家入驻
class JoinAPIView(APIView):
    def post(self, request):
        response = {'status': 900, 'message': '入驻成功'}
        uid = request.data.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            response['status'] = 901
            response['message'] = "没有找到此用户"
            return Response(response)

        u_name = request.data.get('u_name')
        u_phone = request.data.get('u_phone')
        address = request.data.get('address')
        contacts = request.data.get('contacts')
        user.u_name = u_name
        user.u_phone = u_phone
        user.address = address
        user.contacts = contacts
        user.u_property = 1
        user.save()
        return Response(response)


# 个人信息更改
class UserUpdateAPIView(APIView):
    def post(self, request):
        response = {'status': 900, 'message': '个人信息更改成功'}
        uid = request.data.get('uid')
        try:
            user = Users.objects.get(id=uid)
        except:
            response['status'] = 901
            response['message'] = "没有找到此用户"
            return Response(response)

        u_phone = request.data.get('u_phone')
        address = request.data.get('address')
        contacts = request.data.get('contacts')
        user.u_phone = u_phone
        user.address = address
        user.contacts = contacts
        user.save()
        return Response(response)


class UserAPIView(APIView):
    # authentication_classes = (UserAuth, )

    def get(self, request, pk):
        response = {'status': 900, 'message': '用户信息获取成功'}
        try:
            user = Users.objects.filter(id=pk).first()
            if user:
                user_class = UserDetailSerializer(user)
                response['data'] = user_class.data
                response['data']['count'] = Cars.objects.filter(user_id=user.id).filter(
                    Q(cars_status=0) & Q(is_check=1)).count()
                return Response(response)
            else:
                response['status'] = 901
                response['message'] = '没有此用户'
                return Response(response)
        except Exception as e:
            response['status'] = 901
            response['message'] = '用户信息获取失败，error:{}'.format(e)
            return Response(response)


# 车辆审核
def check_cars(request):
    if request.method == 'POST':
        pass


# index
class IndexAPIView(APIView):
    def get(self, request):
        brands = Brands.objects.all()[0:10]
        brands = json.loads(serializers.serialize('json', brands))
        cars = Cars.objects.all()[0:10]
        # cars = json.loads(serializers.serialize('json', cars))
        cars = CarsSerializer(instance=cars, many=True)
        banners = Banners.objects.all()
        banners_class = BannersSerializer(instance=banners, many=True)
        data = {
            'banners': banners_class.data,
            'brands': brands,
            'cars': cars.data,

        }
        return Response(data)


# 热门
class HotAPIView(APIView):

    def get(self, request):
        response = {'status': 900, 'message': '获取热门成功'}
        try:
            hot = Brands.objects.all().order_by('-weight')[0:10]
            hot_class = BrandsSerializer(instance=hot, many=True)
            response['data'] = hot_class.data
            return Response(response)
        except:
            response['status'] = 901
            response['message'] = '获取热门失败'
            return Response(response)


# search
class SearchAPIView(APIView):
    def get(self, request):
        response = {'status': 900, 'message': '搜索获取成功'}
        if request.query_params.get('search'):
            search = request.query_params.get('search')
            cars_all = Cars.objects.filter(name__contains=search).order_by('s_price')
            if request.query_params.get('prices'):
                prices = request.query_params.get('prices').split('-')
                if len(prices) == 1:
                    low = prices[0]
                    cars_all = cars_all.filter(s_price__gte=low).order_by('s_price')
                else:
                    low = prices[0]
                    high = prices[1]
                    cars_all = cars_all.filter(Q(s_price__gte=low) & Q(s_price__lte=high)).order_by('s_price')
            cars_all = CarsSerializer(instance=cars_all, many=True)
            response['data'] = cars_all.data
        else:
            response['status'] = 901
            response['message'] = '请输入搜索内容'
        return Response(response)


# 品牌
class BrandsAPIView(APIView):
    def get(self, request):
        # skip = request.query_params.get('skip')
        # limit = request.query_params.get('limit')
        # skipend = int(skip) + int(limit)
        try:
            brands_class = Brands.objects.all()
            response = {'status': 900, 'message': '品牌列表获取成功', 'data': []}
            for brand in brands_class:
                brands_class = BrandsSerializer(brand)
                a = {
                    'brands': brands_class.data,
                    'series': []
                }
                car_series = CarsSeries.objects.filter(brand=brand.id)
                for series in car_series:
                    cars = Cars.objects.filter(car_serie=series.id)
                    count = cars.count()
                    b = {
                        'id': series.id,
                        'name': series.name,
                        'count': count,
                    }
                    a['series'].append(b)
                response['data'].append(a)
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, )
        except:
            response = {'status': 901, 'message': '品牌列表获取失败'}
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, )


# 车型
class CarTypeAPIView(APIView):
    def get(self, request):
        response = {'status': '', 'message': ''}
        try:
            car_type = CarsTypes.objects.all().order_by('id')
            type_class = CarsTypesSerializer(instance=car_type, many=True)
            response['status'] = 900
            response['message'] = '车型获取成功'
            response['data'] = type_class.data
            return Response(response)
        except:
            response['status'] = 901
            response['message'] = '车型获取失败'
            return Response(response)


# class BrandAPIView(APIView):
#     def get(self, request, pk):
#         series_class = CarsSeries.objects.filter(brand__id=pk)
#         # 获取每个车系 及车辆数
#         data = {}
#         for i in series_class:
#             data[i.name] = {
#                 'id': i.id,
#                 'num': Cars.objects.filter(car_serie__name=i.name).count()
#             }
#         data['message'] = '车系及数量获取成功'
#         data['status'] = 900
#         return JsonResponse(data, json_dumps_params={'ensure_ascii':False})


# # 车系-车 cars实现
# class SeriesCarAPIView(APIView):
#     def get(self, request, pk):
#         cars_class = Cars.objects.filter(car_serie__id=pk)
#         cars = CarsSerializer(instance=cars_class, many=True)
#         response = {'status': 900, 'message': '车系车获取成功'}
#         response['data'] = cars.data
#         return Response(response)
#
#     """
#              最新上架 0  NEW_ARRIVAL
#              价格最高 1  PRICE_ASC  　低＞高
#              价格最低 2  PRICE_DESC　　高＞低
#              time车龄最短 3　TIME_SHORT
#              里程最少 4     KM_LESS
#             """


# 最新上架
NEW_ARRIVAL = 0
# 价格最高
PRICE_ASC = 1
# 价格最低
PRICE_DESC = 2
# 车龄最短
TIME_SHORT = 3
# 里程最少
KM_LESS = 4


# 智能筛选
class ZNSearchAPIView(APIView):
    def get(self, request):
        response = {'status': 900, 'message': '智能筛选获取成功'}
        try:
            search = request.query_params.get('search')
            cars_all = Cars.objects.filter(name__contains=search)
            search_type = int(request.query_params.get('search-type'))
            if search_type == NEW_ARRIVAL:

                # 当前日期
                date_now = datetime.date.today()
                # 查询天数
                da = datetime.timedelta(2)
                end = date_now - da

                cars_all = cars_all.filter(issue_time__range=(end, date_now)).order_by('-issue_time')
                response['message'] = '最新上架'
            elif search_type == PRICE_ASC:
                cars_all = cars_all.order_by('s_price')
                response['message'] = '价格升序'

            elif search_type == PRICE_DESC:
                cars_all = cars_all.order_by('-s_price')
                response['message'] = '价格降序'
            elif search_type == TIME_SHORT:
                cars_all = cars_all.order_by('time')
                response['message'] = '车龄最短'
            elif search_type == KM_LESS:
                cars_all = cars_all.order_by('km')
                response['message'] = '里程最短'

            cars_all = CarsSerializer(instance=cars_all, many=True)
            response['data'] = cars_all.data
            return Response(response)
        except Exception as e:
            response['status'] = 901
            response['message'] = '智能筛选获取失败'
            return Response(response)


# Banners
class BannersAPIView(APIView):
    def get(self, request):
        banners = Banners.objects.all()
        response = {'status': 900, 'message': 'banner列表获取成功'}
        banners_class = BannersSerializer(instance=banners, many=True)
        response['data'] = banners_class.data
        return Response(response)

    def post(self, request):
        banner_data = BannersSerializer(data=request.data)
        response = {'status': 900, 'message': 'banner添加成功'}
        if banner_data.is_valid():
            banner_data.save()
            return Response(response)
        else:
            response['status'] = 901
            response['message'] = 'banner添加失败'
            response['errors'] = banner_data.errors
            return Response(response)


# 筛选carid
def not_empty(s):
    return s and s.strip()


# banner
class BannerAPIView(APIView):
    def get(self, request, pk):
        banners = Banners.objects.filter(id=pk).first()
        response = {'status': 900, 'message': '获取banner成功'}
        banners_class = BannersSerializer(banners)
        response['data'] = banners_class.data
        car_id = banners.car_id.replace('，', ',')
        if len(car_id) >= 1:
            car_id_list = car_id.split(',')
            cars_list = list(filter(not_empty, car_id_list))
            cars = Cars.objects.filter(id__in=cars_list).filter(Q(is_check=1) & Q(cars_status=0))
            cars = CarsSerializer(instance=cars, many=True)
            response['data']['car'] = cars.data
        return Response(response)


# 车型筛选
def models(model, modelscars, price, skip, skipend, sort):
    if model == 0:
        cars = modelscars

        prices_cars = prices(cars, price)

        cars_data = sorts(sort, skip, skipend, prices_cars)
    else:
        cars = modelscars.filter(car_type=model)
        prices_cars = prices(cars, price)
        cars_data = sorts(sort, skip, skipend, prices_cars)

    return cars_data


# 排序
def sorts(sort, skip, skipend, prices_cars):
    # 超值购 > 严选车 > 二手车
    if sort == 0:
        cars_all = prices_cars.order_by('-trait')[int(skip):skipend]
    # 最新上架
    elif sort == 1:
        cars_all = prices_cars.filter(trait=0)[int(skip):skipend]
    # 价格最低
    elif sort == 2:
        cars_all = prices_cars.order_by('s_price')[int(skip):skipend]
    # 价格最高
    elif sort == 3:
        cars_all = prices_cars.order_by('-s_price')[int(skip):skipend]
    # 车龄最短
    elif sort == 4:
        cars_all = prices_cars.order_by('-time')[int(skip):skipend]
    # 里程最少
    else:
        cars_all = prices_cars.order_by('km')[int(skip):skipend]

    return cars_all


# 价格筛选
def prices(cars, price):
    if price == 0:
        cars = cars
    elif price == 1:
        cars = cars.filter(s_price__lte=5)

    elif price == 2:
        cars = cars.filter(Q(s_price__gte=5) & Q(s_price__lte=10))
    elif price == 3:
        cars = cars.filter(Q(s_price__gte=10) & Q(s_price__lte=15))
    elif price == 4:
        cars = cars.filter(Q(s_price__gte=15) & Q(s_price__lte=20))
    elif price == 5:
        cars = cars.filter(Q(s_price__gte=20) & Q(s_price__lte=30))
    elif price == 6:
        cars = cars.filter(Q(s_price__gte=30) & Q(s_price__lte=50))
    else:
        cars = cars.filter(Q(s_price__gte=50))

    return cars


# 所有车辆
class CarsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            skip = int(request.query_params.get('skip'))
            limit = int(request.query_params.get('limit'))
            skipend = skip + limit
            response = {'status': 900, 'message': '获取在售车辆成功'}
            # key
            key = request.query_params.get('key')
            # 价格区间
            price = int(request.query_params.get('price'))
            # 排序规则
            sort = int((request.query_params.get('sort')))
            # 车型
            model = int((request.query_params.get('model')))
            # 品牌
            brand = int(request.query_params.get('brand'))
            # 车系
            series = int(request.query_params.get('series'))
            # trait 严选 超值 2是严选车
            trait = int(request.query_params.get('trait'))
            if trait == 2:
                cars = Cars.objects.filter(Q(is_check=1) & Q(cars_status=0) & Q(trait=2))
                if brand:
                    cars = cars.filter(car_serie__brand_id=int(brand))
                    if series:

                        cars = cars.filter(car_serie=int(series))
                        cars = models(model, cars, price, skip, skipend, sort)

                    else:
                        cars = models(model, cars, price, skip, skipend, sort)

                else:
                    cars = models(model, cars, price, skip, skipend, sort)

                cars_all = CarsSerializer(instance=cars, many=True)
                response['data'] = cars_all.data
                return Response(response)
            else:
                cars = Cars.objects.filter(Q(is_check=1) & Q(cars_status=0))
                if key:
                    cars = cars.filter(name__contains=key)

                    cars = models(model, cars, price, skip, skipend, sort)

                else:
                    if brand:

                        cars = cars.filter(car_serie__brand_id=int(brand))
                        if series:

                            cars = cars.filter(car_serie=int(series))
                            cars = models(model, cars, price, skip, skipend, sort)

                        else:
                            cars = models(model, cars, price, skip, skipend, sort)

                    else:
                        cars = models(model, cars, price, skip, skipend, sort)

                cars_all = CarsSerializer(instance=cars, many=True)
                response['data'] = cars_all.data
                return Response(response)
        except Exception as e:
            response = {'status': 900, 'message': '获取失败'}
            response['errors'] = str(e)
            return Response(response)

    def post(self, request, *args, **kwargs):
        car = CarSerializer(data=request.data)
        response = {'status': 900, 'message': '添加在售车辆成功'}
        if car.is_valid():
            car.save()
            return Response(response)
        else:
            response['status'] = 901
            response['message'] = '添加在售车辆失败'
            response['errors'] = car.errors
            return Response(response)


# 单个车辆
class CarAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        cars = Cars.objects.filter(id=pk).first()
        today = datetime.date.today()
        try:
            yearly_check = cars.yearly_check
            yearly_check_date = datetime.date(*map(int, yearly_check.split('-')))
            if today > yearly_check_date:
                yearly_check = '已过期'
            else:
                yearly_check = yearly_check
            compulsory_insurance = cars.compulsory_insurance
            compulsory_insurance_date = datetime.date(*map(int, compulsory_insurance.split('-')))
            if today > compulsory_insurance_date:
                compulsory_insurance = '已过期'
            else:
                compulsory_insurance = compulsory_insurance
            commercial_insurance = cars.commercial_insurance
            commercial_insurance_date = datetime.date(*map(int, commercial_insurance.split('-')))
            if today > commercial_insurance_date:
                commercial_insurance = '已过期'
            else:
                commercial_insurance = commercial_insurance
        except:
            yearly_check = cars.yearly_check
            compulsory_insurance = cars.compulsory_insurance
            commercial_insurance = cars.commercial_insurance

        response = {'status': 900, 'message': '获取单个车成功'}
        cars_all = CarSerializer(cars)
        response['data'] = cars_all.data
        response['data']['user'] = cars.user.id
        response['data']['yearly_check'] = yearly_check
        response['data']['compulsory_insurance'] = compulsory_insurance
        response['data']['commercial_insurance'] = commercial_insurance
        return Response(response)

    def delete(self, request, pk, *args, **kwargs):
        pass

    def patch(self, request, pk, *args, **kwargs):
        pass


# 快速卖车
class SellCarAPIView(APIView):

    def post(self, request, *args, **kwargs):
        Appointment = SellAppointmentsSerializer(data=request.data)
        response = {'status': 900, 'message': '卖车预约成功'}
        if Appointment.is_valid():
            Appointment.save()
            return Response(response)
        else:
            response['status'] = 901
            response['message'] = '卖车预约失败'
            response['errors'] = Appointment.errors
            return Response(response)


# # 个人信息
# class UserAPIView(APIView):
#     def get(self, request):
#         phone = rds.get('phone')
#         user = Users.objects.filter(phone=phone)
#         response = {'status': 900, 'message': '获取个人信息成功'}
#         user = UserSerializer(instance=user, many=True)
#         response['data'] = user.data
#         return Response(response)


# 个人预约车辆
class UserAppointmentAPIView(APIView):

    def get(self, request):

        response = {'status': 900, 'message': '个人预约信息获取成功', 'data': {'my_appointment': [], 'appointment_me': []}}
        try:
            uid = int(request.query_params.get('uid'))
            # 预约我的车的表单
            appt = Appointments.objects.filter(car_user=uid).filter(Q(status=0) | Q(status=1))
            for i in appt:
                # 格式时间
                formatted_datetime = formats.date_format(i.time, 'SHORT_DATETIME_FORMAT')
                # 预约的人
                user = Users.objects.get(id=i.uid)
                car = Cars.objects.get(id=i.car_id)
                if user.u_property == 0:
                    u_property = '个人'
                    u_name = user.wx_name
                else:
                    u_property = '商家'
                    u_name = user.contacts
                if i.status == 0:
                    status = '待确认'
                else:
                    status = '已确认'
                car = CarsSerializer(car)
                b = car.data
                b['u_name'] = u_name
                b['u_property'] = u_property
                # 预约电话
                b['phone'] = i.phone
                b['status'] = i.status
                b['appointment'] = i.id
                b['appointment_time'] = formatted_datetime
                b['status'] = status

                response['data']['appointment_me'].append(b)

            # 我预约的表单
            apit = Appointments.objects.filter(uid=uid).exclude(status=2)
            for i in apit:
                car_user = i.car_user
                car = Cars.objects.get(id=i.car_id)
                formatted_datetime = formats.date_format(i.time, 'SHORT_DATETIME_FORMAT')
                if car.user.u_property == 0:
                    u_property = '个人'
                    u_name = car.user.wx_name
                else:
                    u_property = '商户'
                    u_name = car.user.u_name

                if i.status == 0:
                    status = '待确认'
                elif i.status == 1:
                    status = '已确认'
                else:
                    status = '已失效'
                car = CarsSerializer(car)
                a = car.data
                a['appointment'] = i.id
                a['u_property'] = u_property
                a['u_name'] = u_name
                a['appointment_time'] = formatted_datetime
                a['status'] = status

                response['data']['my_appointment'].append(a)
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, )
        except Exception:
            response = {'status': 901, 'message': '个人预约信息获取失败'}
            return Response(response)

    def post(self, request, *args, **kwargs):
        # lookAppointment = LookAppointmentsSerializer(data=request.data)
        response = {'status': 900, 'message': '预约看车成功'}
        try:
            uid = int(request.data.get('uid'))
            car_id = int(request.data.get('car_id'))
            try:
                userapit = Appointments.objects.get(uid=uid, car_id=car_id)
                response['message'] = '您已经预约过啦'
                return Response(response)
            except:
                car = Cars.objects.get(id=car_id)
                if uid == car.user_id:
                    response['status'] = 901
                    response['message'] = '不能预约自己发布车辆'
                    return Response(response)
                else:
                    apit = Appointments()
                    apit.uid = uid
                    car_id = car_id
                    apit.car_id = car_id
                    apit.car_user = Cars.objects.get(id=car_id).user_id
                    apit.phone = request.data.get('phone')
                    apit.time = request.data.get('time')
                    apit.name = request.data.get('name')
                    apit.save()
                    return Response(response)



        except Exception as e:
            response['status'] = 901
            response['message'] = '预约看车失败'
            print(e)
            return Response(response)


'''
更改状态操作
    action  0  用户取消预约
    action  1  发布者取消预约
    action  2  取消关注
    action  3  上架车
    action  4  下驾车
    action  5  已售
'''


class UserCancelAppointmentAPIView(APIView):
    def get(self, request):
        response = {'status': '', 'message': ''}
        try:
            action = int(request.query_params.get('action'))
        except:
            response['status'] = 901
            response['message'] = '请输入你想要进行的操作'
            return Response(response)
        # 用户取消预约
        if action == 0:
            appointment_id = request.query_params.get('appointment')
            try:
                Appointments.objects.get(id=appointment_id).delete()
            except:
                response['status'] = 901
                response['message'] = '未找到此预约记录'
                return Response(response)
            response['status'] = 900
            response['message'] = '取消成功'
            return Response(response)
        # 发布者取消预约
        if action == 1:
            appointment_id = request.query_params.get('appointment')
            try:
                apit = Appointments.objects.get(id=appointment_id)
                apit.status = 3
                apit.save()
            except:
                response['status'] = 901
                response['message'] = '未找到此预约记录'
                return Response(response)
            response['status'] = 900
            response['message'] = '取消成功'
            return Response(response)
        # 取消关注
        elif action == 2:
            uid = request.query_params.get('uid')
            car_id = request.query_params.get('car_id')
            try:
                Appointments.objects.get(Q(uid=uid) & Q(car_id=car_id)).delete()
            except:
                response['status'] = 901
                response['message'] = '未找到此关注记录'
                return Response(response)
            response['status'] = 900
            response['message'] = '取消成功'
            return Response(response)
        # 上架车
        elif action == 3:
            uid = request.query_params.get('uid')
            car_id = request.query_params.get('car_id')
            try:
                car = Cars.objects.get(Q(id=car_id) & Q(user_id=uid))
                car.cars_status = 0
                car.save()
            except:
                response['status'] = 901
                response['message'] = '上架失败'
                return Response(response)
            response['status'] = 900
            response['message'] = '上架成功'
            return Response(response)
        # 下架车
        elif action == 4:
            uid = request.query_params.get('uid')
            car_id = request.query_params.get('car_id')
            try:
                car = Cars.objects.get(Q(id=car_id) & Q(user_id=uid))
                car.cars_status = 1
                car.save()
            except:
                response['status'] = 901
                response['message'] = '下架失败'
                return Response(response)
            response['status'] = 900
            response['message'] = '下架成功'
            return Response(response)
        # 已售
        elif action == 5:
            uid = request.query_params.get('uid')
            car_id = request.query_params.get('car_id')
            try:
                car = Cars.objects.get(Q(id=car_id) & Q(user_id=uid))
                car.cars_status = 2
                car.save()
            except:
                response['status'] = 901
                response['message'] = '更为已售失败'
                return Response(response)
            response['status'] = 900
            response['message'] = '更为已售成功'
            return Response(response)
        # 已确认
        elif action == 6:
            appointment_id = request.query_params.get('appointment')
            try:
                apit = Appointments.objects.get(id=appointment_id)
                apit.status = 1
            except:
                response['status'] = 901
                response['message'] = '未找到此预约记录'
                return Response(response)
            response['status'] = 900
            response['message'] = '已确认'
            return Response(response)

# 个人发布车辆
class UserIssueAPIView(APIView):
    def get(self, request):
        try:
            skip = int(request.query_params.get('skip'))
            limit = int(request.query_params.get('limit'))
            skipend = skip + limit
            # 用户id
            u_id = int(request.query_params.get('uid'))
            try:
                u = Users.objects.get(id=u_id)
            except:
                response = {'status': 901, 'message': '没有找到此用户'}
                return Response(response)
        except:
            response = {'status': 901, 'message': '缺少必要参数'}
            return Response(response)

        # 发布成功的车
        cars = Cars.objects.filter(user=u_id)[skip:skipend]
        response = {'status': 900, 'message': '获取个人发布车辆成功'}
        # 发布成功的车
        cars = UserIssueCarsSerializer(instance=cars, many=True)
        response['data'] = cars.data

        return Response(response)

    def post(self, request):
        # # 更改querydict
        # _mutable = request.data._mutable
        #
        # # set to mutable
        # request.data._mutable = True
        #
        # # сhange the values you want
        # request.data['down_payment'] = 2
        #
        # # set mutable flag back
        # request.data._mutable = _mutable

        car = IssueCarsSerializer(data=request.data)
        response = {'status': 900, 'message': '发布车辆成功'}
        if car.is_valid():
            car.save()

            return Response(response)
        else:
            response['status'] = 901
            response['message'] = '发布车辆失败'
            response['errors'] = car.errors
            return Response(response)


class UserIssueDAPIView(APIView):
    def get(self, request, pk):
        try:
            car = Cars.objects.get(id=pk)
            car_brand = car.car_serie.brand_id
            car = CarissueSerializer(car)
            response = {'status': 900, 'message': '个人单个车辆成功'}
            response['data'] = car.data
            response['data']['car_brand'] = car_brand
            return Response(response)
        except:
            response = {'status': 901, 'message': '个人单个车辆失败'}
            return Response(response)


# 编辑发布内容
class UserIssueEditAPIView(APIView):

    def post(self, request):
        try:
            request_data = request.data
            car_id = request.data.get('car_id')
            old_car = Cars.objects.get(id=car_id)
            old_car.is_check = 0
            old_car.save()
            car_ser = IssueCarsSerializer(instance=old_car, data=request_data, partial=False)
            response = {'status': 900, 'message': '编辑车辆成功'}
            if car_ser.is_valid(raise_exception=True):
                old_car = car_ser.save()
                rt = UserIssueCarsSerializer(Cars.objects.get(id=car_id))
                response['data'] = rt.data
                return Response(response)
        except:
            response = {'status': 901, 'message': '编辑车辆失败'}
            return Response(response)


# 个人关注车辆
class UserLikeAPIView(APIView):

    def get(self, request):
        response = {'status': 900, 'message': '获取个人关注车辆成功'}

        try:
            u_id = int(request.query_params.get('uid'))
            # 关注表单 UserLikes
            like = UserLikes.objects.filter(uid=u_id)
            like_car_list = []
            for i in like:
                like_car_list.append(i.like_car_id)

            # 关注的所有车
            cars = Cars.objects.filter(id__in=like_car_list)
            cars = CarsSerializer(instance=cars, many=True)
            response['cars'] = cars.data
            return Response(response)
        except:
            response['status'] = 901
            response['message'] = '获取个人关注失败,可能缺少必要参数'
            return Response(response)

    def post(self, request):
        response = {'status': 900, 'message': '关注成功'}
        like = LikeCarSerializer(data=request.data)
        if like.is_valid():
            like.save()
            return Response(response)
        else:
            response['status'] = 901
            response['message'] = '关注失败'
            response['errors'] = like.errors
            return Response(response)


class FwbAPIView(APIView):
    def get(self, request):
        response = {'status': '', 'message': ''}
        action = int(request.query_params.get('action'))
        print(action)
        try:
            if action == 1:
                fwb = Fwb.objects.get(id=action)
                fwb = FwbSerializer(fwb)
                response['status'] = 900
                response['message'] = '获取公司文化成功'
                response['data'] = fwb.data
                return Response(response)
            if action == 2:
                fwb = Fwb.objects.get(id=action)
                fwb = FwbSerializer(fwb)
                response['status'] = 900
                response['message'] = '获取车况检测成功'
                response['data'] = fwb.data
                return Response(response)
            if action == 3:
                fwb = Fwb.objects.get(id=action)
                fwb = FwbSerializer(fwb)
                response['status'] = 900
                response['message'] = '获取保养车成功'
                response['data'] = fwb.data
                return Response(response)
            if action == 4:
                fwb = Fwb.objects.get(id=action)
                fwb = FwbSerializer(fwb)
                response['status'] = 900
                response['message'] = '获取保险超市成功'
                response['data'] = fwb.data
                return Response(response)
            if action == 5:
                fwb = Fwb.objects.get(id=action)
                fwb = FwbSerializer(fwb)
                response['status'] = 900
                response['message'] = '获取洗车服务成功'
                response['data'] = fwb.data
                return Response(response)
        except Exception as e:
            response['status'] = 901
            response['message'] = '获取服务失败'

            return Response(response)


# 上传图片
def uploadimg(request):
    if request.method == 'POST':
        response = {'status': '', 'message': ''}
        new_img = Img(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name
        )
        new_img.save()
        response['status'] = 900
        response['message'] = 'upload-success'
        response['img_url'] = 'https://api.ershouche.jney.net' + new_img.img.url
        # response['img_url'] = '127.0.0.1' + new_img.img.url
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, )
    response = {'status': 900, 'message': 'get-ok'}
    return JsonResponse(response)


# 上传多张图片
def uploadimgn(request):
    if request.method == 'POST':
        response = {'status': '', 'message': ''}
        try:
            files = request.FILES.getlist('img')
            imgurl=[]
            for i in files:
                    new_img = Img(
                        img=i,
                        name=i.name
                    )
                    new_img.save()
                    imgurl.append('https://api.ershouche.jney.net' + new_img.img.url)
            response['status'] = 900
            response['message'] = 'upload-success'
            response['img_url'] = imgurl
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, )
        except Exception as e:
            response['status'] = 901
            response['message'] = '上传图片失败'
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, )
    response = {'status': 900, 'message': 'get-ok'}
    return JsonResponse(response)


# 上传视频
def uploadvideo(request):
    if request.method == 'POST':
        response = {'status': '', 'message': ''}
        try:

            new_video = Video(
                video=request.FILES.get('video'),
                name=request.FILES.get('video').name,
            )

            new_video.save()
            response['status'] = 900
            response['message'] = 'upload-success'
            response['video_url'] = 'https://api.ershouche.jney.net' + new_video.video.url
            # response['video_url'] = 'http://127.0.0.1:9001' + new_video.video.url
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, )
        except Exception as e:
            response['status'] = 901
            response['message'] = '上传视频失败'
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, )
    response = {'status': 900, 'message': 'get-ok'}
    return JsonResponse(response)


# 导入数据
def create_brands(request):
    with open('Bo_yuan/datails.txt', 'r', encoding='utf8') as f:
        # 按行读 品牌名不存在添加 车型车系如上
        # print(f.readlines())
        # 品牌名
        b_names = {}
        # 车型名
        c_names = {}
        # 车系名
        s_names = {}

        for i in f.readlines():
            try:
                i = eval(i)
                brand = i['brand']
                if brand in b_names:
                    b_names[brand] += 1
                else:
                    b_names[brand] = 1
                vehicle_model = i['vehicle_model']
                if vehicle_model in c_names:
                    c_names[vehicle_model] += 1
                else:
                    c_names[vehicle_model] = 1
                car_series = i['car series']
                if car_series in s_names:
                    s_names[car_series] += 1
                else:
                    s_names[car_series] = 1

                sell_car_name = i['sell_car_name']
                sell_car_name = re.findall(r".*", sell_car_name)[0]
                img1 = i['img1']
                img2 = i['img2']
                img3 = i['img3']
                img4 = i['img4']
                img5 = i['img5']
                # 上牌时间
                car_license = i['car_license']
                # 里程数
                table_show_mileage = i['Table_show_mileage']
                table_show_mileage = re.findall(r"\d+\.?\d*", table_show_mileage)[0]
                # 排量
                displacement = i['displacement']
                if displacement == '潍坊':
                    displacement = 0.0
                # 变速箱
                speed_changing_box = i['speed_changing_box']
                # 原价
                original_price = i['original_price']

                original_price = re.findall(r"\d+\.?\d*", original_price)[0]

                # 现价
                current_price = i['current_price']
                current_price = re.findall(r"\d+\.?\d*", current_price)[0]

                brands = Brands()
                cars_type = CarsTypes()
                cars_serie = CarsSeries()
                # 品牌
                if b_names[brand] == 1:
                    brands.name = brand
                    brands.save()
                # 车型
                if c_names[vehicle_model] == 1:
                    cars_type.name = vehicle_model
                    cars_type.save()
                # 车系
                if s_names[car_series] == 1:
                    cars_serie.name = car_series
                    cars_serie.brand = Brands.objects.filter(name=brand).last()
                    cars_serie.save()
                cars = Cars()
                cars.name = sell_car_name
                cars.img1 = img1
                cars.img2 = img2
                cars.img3 = img3
                cars.img4 = img4
                cars.img5 = img5

                cars.time = car_license
                cars.km = table_show_mileage
                cars.displacement = displacement
                cars.gearbox = speed_changing_box
                cars.price = original_price
                cars.s_price = current_price
                # 所属车系
                cars.car_serie = CarsSeries.objects.all().last()
                cars.car_type = CarsTypes.objects.filter(name=vehicle_model).last()
                cars.user = Users.objects.last()
                cars.save()

                # 收藏
                # u_l = UserLikes()
                # u_l.user_id = Users.objects.last().id
                # u_l.like_car_id = 1
            except:
                pass
    return HttpResponse("ok")
#
#
# ''' {'brand': '奥迪', 'vehicle_model': '三厢轿车', 'car series': '奥迪A6L', 'sell_car_name': '奥迪A6L 2009款 2.4L 舒适型\n                                            降价急售', 'img1': 'https://image.guazistatic.com/gz01190929/15/57/7a01b2265dd813978efd24704d4ecd88.jpg@base@tag=imgScale&w=600&h=400&c=1&m=2&q=88', 'img2': 'https://image.guazistatic.com/gz01190929/15/57/cb965556b72c88ca6191c65a7016995b.jpg@base@tag=imgScale&w=600&h=400&c=1&m=2&q=88', 'img3': 'https://image.guazistatic.com/gz01190929/15/57/b38c1459a8ce3fae28d692034d09787a.jpg@base@tag=imgScale&w=600&h=400&c=1&m=2&q=88', 'img4': 'https://image.guazistatic.com/gz01190929/15/57/5eb2ae862544bf08b549593760b66a87.jpg@base@tag=imgScale&w=600&h=400&c=1&m=2&q=88', 'img5': 'https://image.guazistatic.com/gz01190929/15/57/00ce25239f08dbb9d9196c8ec997c7e9.jpg@base@tag=imgScale&w=600&h=400&c=1&m=2&q=88', 'car_license': '2010-07', 'Table_show_mileage': '8.4万公里', 'displacement': '2.4', 'speed_changing_box': '自动', 'original_price': '新车指导价50.90万(含税)', 'current_price': '¥9.80                万'}
#  '''
#
#
# def brands(request):
#     if request.method == 'GET':
#         brands = Brands.objects.all()
#         brands = json.loads(serializers.serialize('json', brands))
#         data = {
#             'brands': brands
#         }
#         return JsonResponse(data)
#
#
# # 车辆
# def cars(request):
#     cars = Cars.objects.all()
#     # 数量
#     c_count = cars.count()
#     data = {
#         "c_count": c_count
#     }
#     return JsonResponse(data)
#
#
# # 会员
# def vips(request):
#     vips = Users.objects.all()
#     v_count = vips.count()
#     data = {
#         'v_count': v_count
#     }
#     return JsonResponse(data)
#
#
# # 日新增
# def daus(request):
#     # 当前日期
#     date_now = datetime.date.today()
#     # 查询天数
#     da = datetime.timedelta(1)
#     end = date_now + da
#
#     users = Users.objects.filter(u_time__range=(date_now, end))
#     daus = users.count()
#     data = {
#         'daus': daus
#     }
#     return JsonResponse(data)
#
#
#
#
#
#
# # 车辆售卖
# def sellcar(request):
#     if request.method == 'POST':
#         car_id = request.POST.get('car_id')
#         car = Cars.objects.filter(id=car_id).first()
#         sell_car = SellCars()
#         sell_car.name = car.name
#         sell_car.img = car.img
#         sell_car.time = car.time
#         sell_car.km = car.km
#         sell_car.displacement = car.displacement
#         sell_car.gearbox = car.gearbox
#         sell_car.price = car.price
#         sell_car.s_price = car.s_price
#         sell_car.issue_time = car.issue_time
#         sell_car.car_serie = car.car_serie
#         sell_car.sell_user = car.user
#
#         sell_car.save()
#         car.delete()
#         return HttpResponse('sell_name%s'%sell_car.name)
#
#
# def sell_appointment(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         sellaimt = SellAppointments()
#         sellaimt.name = name
#         sellaimt.phone = phone
#         sellaimt.user = 3
#         sellaimt.save()
#         return HttpResponse("预约已提交")
def year(request):
    yearly_check = Cars.objects.filter(yearly_check='Null').update(yearly_check='2019-12-20')
    compulsory_insurance = Cars.objects.filter(compulsory_insurance=' ').update(compulsory_insurance='2019-12-20')
    commercial_insurance = Cars.objects.filter(commercial_insurance=' ').update(commercial_insurance='2019-12-20')



    return HttpResponse('更新成功')
