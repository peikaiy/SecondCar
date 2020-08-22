import datetime
import json
import re

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.response import Response

from Bo_yuan.models import Users, Cars, Brands, CarsSeries, CarsTypes, UserLikes, Appointments, \
    SellAppointments, Banners, Fwb
from django.core import serializers
# 全部
from Bo_yuan.serializers import CarSerializer

ALL = '0'
# 审核通过
AUDIT_SUCCESS = 1
# 审核失败
AUDIT_FAILED = 2

# 后台管理
def rindex(request):
    return redirect(index)


def index(request):
    # 当前日期
    date_now = datetime.date.today()
    # 查询天数
    da = datetime.timedelta(1)
    end = date_now + da
    cars = Cars.objects.all()
    users = Users.objects.all()
    # 今日新增会员
    add_vips = users.filter(u_time__range=(date_now, end))
    add_vip = add_vips.count()
    # 今日新增车辆
    add_cars = cars.filter(issue_time__range=(date_now, end))
    add_car = add_cars.count()
    # 今日新增卖车
    # add_sell_cars = Cars.objects.filter(sell_time__range=(date_now, end))
    # add_sell = add_sell_cars.count()
    # 今日新增预约
    add_users = Appointments.objects.filter(time__range=(date_now, end))
    add_aimt = add_users.count
    # 待审核
    wait_check = Cars.objects.filter(is_check=0)
    wait_check = wait_check.count()
    # 待预约卖车
    # 车辆管理-总车辆
    car_count = cars.count()
    # 会员管理-总会员
    vip_count = users.count()
    # 卖车预约
    sell_aimts = SellAppointments.objects.all()

    data = {
        "add_vip": add_vip,
        "add_car": add_car,
        # "add_sell": add_sell,
        "add_aimt": add_aimt,
        "wait_check": wait_check,
        "car_count": car_count,
        "vip_count": vip_count,
        "sell_aimts": sell_aimts,
    }
    return render(request, 'index/index.html', context=data)



# banner
def banner(request):
    return render(request, 'advertising/banner.html')


def banner_create(request):
    img = request.FILES.get('img')
    car_id = request.POST.get('car_id')
    text = request.POST.get('text')
    Banners.objects.create(img=img, car_id=car_id, content=text)


    return render(request, 'advertising/banner-create.html')


# 广告管理
def advertising(request):
    return render(request, 'advertising/advertising.html')


# 品牌
def brand(request):
    brands = Brands.objects.all()
    brand_count = brands.count
    # 分页
    paginator = Paginator(brands, 15)
    try:
        num = request.GET.get('page', '1')
    except:
        num = 1
    number = paginator.page(num)

    data = {
        'brands': brands,
        'paginator': paginator,
        'page': number,
        'num': int(num),
        'brand_count': brand_count,
    }
    return render(request, 'second_car/brand.html', context=data)


# 车型
def car_type(request):

    return render(request, 'second_car/car-type.html')

# 创建车型
def create_type(request):
    action = request.GET.get('action')
    car_id = request.GET.get('car_list')

    if action == '0':
        type = request.GET.get('type')


        if len(car_id) >= 1:
                car_id = car_id.split('#')
                car_type = CarsTypes.objects.get(id=car_id[-1])

                car_type.name = type
                car_type.save()

                data = {
                    'msg': '编辑成功',
                    'status': 900,
                }
                return JsonResponse(data)
        else:

                car_type = CarsTypes()
                car_type.name = type
                car_type.save()
                data = {
                    'msg': '创建成功',
                    'status': 900,
                }
                return JsonResponse(data)
    elif action == '1':
        weight1 = request.GET.get('weight1')

        car_id = car_id.split('#')
        car_type = CarsTypes.objects.get(id=car_id[-1])
        try:
            car_type.weight = int(weight1)
            car_type.save()
            data = {
                'msg': '设置权重成功',
                'status': 900,
            }
            return JsonResponse(data)
        except:
            data = {
                'msg': '设置权重失败',
                'status': 901,
            }
            return JsonResponse(data)
    return JsonResponse({'msg': ''})

# 级别(车系)
def car_serie(request):
    car_types = CarsTypes.objects.all().order_by('-weight')
    data = {
        'car_types': car_types
    }
    return render(request, 'second_car/car-serie.html', context=data)


# 车源
def cars(request):
    if request.method == 'POST':

        if request.method == 'POST':
            search = request.POST.get('search')
            ischeck = request.POST.get('ischeck')
            print(ischeck)
            print(type(ischeck))
            if ischeck == '0':
                cars = Cars.objects.filter(name__contains=search).order_by('id')
            elif ischeck == '1':
                cars = Cars.objects.filter(Q(is_check=1) & Q(name__contains=search)).order_by('id')
            cars_count = cars.count()
            # 分页
            paginator = Paginator(cars, 15)
            try:
                num = request.GET.get('page', '1')
            except:
                num = 1
            number = paginator.page(num)

            data = {
                'cars': cars,
                'page': number,
                'paginator': paginator,
                'num': int(num),
                'cars_count': cars_count,
            }

            return render(request, 'second_car/cars.html', context=data)
    cars = Cars.objects.all()[0:90]
    cars_count = cars.count()
    # 分页
    paginator = Paginator(cars, 15)
    try:
        num = request.GET.get('page', '1')
    except:
        num = 1
    number = paginator.page(num)

    data = {
        'cars': cars,
        'page': number,
        'paginator': paginator,
        'num': int(num),
        'cars_count': cars_count,
    }

    return render(request, 'second_car/cars.html', context=data)


def car_yuan(request):



    if request.method == 'GET':
        car_id = request.GET.get('car_id')
        car = Cars.objects.get(id=car_id)
        cars = Cars.objects.filter(id=car_id)
        cars = json.loads(serializers.serialize('json', cars))
        if car.user.u_property == 0:
            u_name = car.user.wx_name
            u_phone = car.user.u_phone
        else:
            u_name = car.user.u_name
            u_phone = car.user.u_phone
        data = {
            'status': 200,
            'msg': 'look-ok',
            'issue_car': cars,
            'user_name': u_name,
            'user_phone': u_phone,
        }

        return JsonResponse(data)




# 车辆审核数据展示
def car_check(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        car_user = request.POST.get('car_user')
        car_name = request.POST.get('car_name')

        check_cars_all = Cars.objects.filter(is_check=0).order_by("id")
        # 用户
        if car_user == ALL:
            # 车型名
            if car_name == ALL:
                check_cars = Cars.objects.filter(is_check=0).filter(
                    Q(name__contains=search)).order_by("id")
            else:
                check_cars = Cars.objects.filter(is_check=0, car_type_id=car_name).filter(
                    Q(name__contains=search)).order_by("id")
        else:
            if car_name == ALL:
                check_cars = Cars.objects.filter(is_check=0, user=car_user).filter(
                    Q(name__contains=search)).order_by("id")
            else:
                check_cars = Cars.objects.filter(is_check=0, user=car_user, car_type_id=car_name).filter(
                    Q(name__contains=search)).order_by("id")
        # 只显示90
        check_carsp = check_cars[0:90]
        # 分页
        paginator = Paginator(check_carsp, 15)
        try:
            num = request.GET.get('page', '1')
        except:
            num = 1
        number = paginator.page(num)
        # 数量统计
        d = {}
        for i in check_cars_all:
            key = i.user_id

            if key in d:
                d[key][1] += 1
            else:
                if i.user.u_property == 0:
                    d[key] = [i.user.wx_name, 1]
                else:
                    d[key] = [i.user.u_name, 1]
        car_types = CarsTypes.objects.all()
        data = {
            'check_cars_all': check_cars_all.count(),
            'check_cars': check_carsp,
            'car_types': car_types,
            'paginator': paginator,
            'page': number,
            'num': int(num),
            'd': d,
        }
        return render(request, 'car_check/car-check.html', context=data)
    elif request.method == 'GET':
        check_cars_all = Cars.objects.filter(is_check=0).order_by("id")
        # 只显示90
        check_carsp = check_cars_all[0:90]
        # 分页
        paginator = Paginator(check_carsp, 15)
        try:
            num = request.GET.get('page', '1')
        except:
            num = 1
        number = paginator.page(num)
        # 数量统计
        d = {}
        for i in check_cars_all:
            key = i.user_id

            if key in d:
                d[key][1] += 1
            else:
                d[key] = [i.user.wx_name, 1]

        car_types = CarsTypes.objects.all()
        data = {
            'check_cars': check_carsp,
            'check_cars_all': check_cars_all.count(),
            'car_types': car_types,
            'd': d,
            'paginator': paginator,
            'page': number,
            'num': int(num),

        }

        return render(request, 'car_check/car-check.html', context=data)


# 车辆信息预览
# def car_look(request):
#     car_id = request.GET.get('car_id')
#     issue_cars = Issue_Cars.objects.filter(id=car_id)
#     issue_cars = json.loads(serializers.serialize('json', issue_cars))
#     data = {
#         'status': 200,
#         'msg': 'look-ok',
#         'issue_car': issue_cars,
#     }
#
#     return JsonResponse(data)


# 车辆操作
def car_operation(request):

    msg = request.GET.get('msg')
    car_list = request.GET.get('car_id')
    car_id_list = car_list.split('#')
    # 批量创建
    if msg == 'success':
        for i in car_id_list:
            issue_car = Cars.objects.get(id=i)
            issue_car.is_check = AUDIT_SUCCESS
            issue_car.save()
        data = {
            'status': 200,
            'msg': 'audit_success'
        }
        return JsonResponse(data)
    elif msg == 'failed':
        failed_content = request.GET.get('failed_content')
        issue_car = Cars.objects.get(id=car_id_list[0])
        issue_car.is_check = AUDIT_FAILED
        issue_car.failed_content = failed_content
        issue_car.save()
        data = {
            'status': 200,
            'msg': 'audit_failed'
        }
        return JsonResponse(data)
    elif msg == 'look':

        issue_cars = Cars.objects.filter(id=car_id_list[0])
        car = Cars.objects.get(id=int(car_id_list[0]))
        issue_cars = json.loads(serializers.serialize('json', issue_cars))
        if car.user.u_property == 0:
            u_name = car.user.wx_name
            u_phone = car.user.u_phone
        else:
            u_name = car.user.u_name
            u_phone = car.user.u_phone
        data = {
            'status': 200,
            'msg': 'look-ok',
            'issue_car': issue_cars,
            'user_name': u_name,
            'user_phone': u_phone,
        }

        return JsonResponse(data)
    elif msg == 'changetype':
        car_type = CarsTypes.objects.get(id=car_list[0])
        data = {

        }
        return JsonResponse(data)

        # issue_car.car_serie =


# 获取车型
def check_types(request):
    u_id = request.GET.get('u_id')

    if u_id == ALL:
        check_cars = Cars.objects.filter(is_check=0)
        d = {}
        for i in check_cars:
            d[i.car_serie.car_type.name] = i.car_serie.car_type.id
    else:
        check_cars = Cars.objects.filter(is_check=0, issue_user_id=u_id)
        d = {}
        for i in check_cars:

            d[i.car_serie.car_type.name] = i.car_serie.car_type.id

    return JsonResponse(d)


# 卖车预约
def sell_appointment(request):
    return render(request, 'appointment/sell-appointment.html')


# 会员预约买车
def vip_appointment(request):
    return render(request, 'appointment/vip-appointment.html')


# 会员管理
def vip(request):

    return render(request, 'vip/vip.html')


# 会员详情
def vip_details(request):
    return render(request, 'vip/vip-details.html')


# 企业文化
def corporate_culture(request):
    if request.method == 'POST':
        editor = request.POST.get('content')
        fwb = Fwb.objects.get(id=1)
        fwb.content = editor
        fwb.save()
    return render(request, 'page/corporate-culture.html')


# 车检
def vehicle_inspection(request):
    if request.method == 'POST':
        editor = request.POST.get('content')
        fwb = Fwb.objects.get(id=2)
        fwb.content = editor
        fwb.save()
    return render(request, 'module/vehicle-inspection.html')


# 汽车保养
def car_maintenance(request):
    if request.method == 'POST':
        editor = request.POST.get('content')
        fwb = Fwb.objects.get(id=3)
        fwb.content = editor
        fwb.save()
    return render(request, 'module/car-maintenance.html')


# 保险超市
def insurance_products(request):
    if request.method == 'POST':
        editor = request.POST.get('content')
        fwb = Fwb.objects.get(id=4)
        fwb.content = editor
        fwb.save()
    return render(request, 'module/insurance-products.html')


# 洗车服务
def fcwt(request):
    if request.method == 'POST':
        editor = request.POST.get('content')
        fwb = Fwb.objects.get(id=5)
        fwb.content = editor
        fwb.save()
    return render(request, 'module/fcwt.html')


# 更改密码
def change_passwd(request):
    return render(request, 'system/change_passwd.html')


# 登陆
def login(request):
    return render(request, 'system/login.html')


def logout(request):
    return





# error 404
def page_not_found(request, *args):
    return render(request, "errors/404.html")


# error 500
def server_error(request, *args):
    return render(request, "errors/404.html")


