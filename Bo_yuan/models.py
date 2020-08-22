from django.db import models

from django.utils import timezone

# Create your models here.


# 上传图片
class Img(models.Model):
    img = models.ImageField(upload_to='imgs')
    name = models.CharField(max_length=256)
    class Meta:
        db_table = 'By_imgs'


# 上传视频
class Video(models.Model):
    video = models.FileField(upload_to='video')
    name = models.CharField(max_length=256)

    class Meta:
        db_table = 'By_video'




user_type = (
    (0, '个人'),
    (1, '商户'),
)


# 用户
class Users(models.Model):
    wx_name = models.CharField(max_length=256)
    wx_icon = models.ImageField(upload_to="users/icon")
    openid = models.CharField(max_length=255, unique=True)
    # 个人/商户 0/1
    u_property = models.IntegerField(choices=user_type, default=0)
    # 加入时间
    u_time = models.DateTimeField(auto_now_add=True)

    u_name = models.CharField(max_length=128, null=True)
    contacts = models.CharField(max_length=128, null=True)
    u_phone = models.CharField(max_length=128, null=True)
    address = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = "By_users"


# 用户>收藏
class UserLikes(models.Model):
    # 用户id
    uid = models.IntegerField()
    # 收藏
    like_car_id = models.IntegerField()

    # 发布
    # issue_car_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "By_user_likes"


# Banners
class Banners(models.Model):
    img = models.ImageField(upload_to='banners')
    # 车辆编号
    car_id = models.CharField(max_length=128, null=True)
    # 内容
    content = models.TextField(null=True)
    # 查看数
    look = models.IntegerField(default=1)
    # 权重
    weight = models.IntegerField(default=1)
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "By_banners"


# 公司文化
class CorporateCulture(models.Model):
    pass


class Fwb(models.Model):
    content = models.TextField()


# 广告
class News(models.Model):
    new = models.ImageField(upload_to='news')
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=512)

    class Meta:
        db_table = "By_news"


# 品牌
class Brands(models.Model):
    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(upload_to="brands/logo",
                             default='https://sta.guazistatic.com/static/c2c/web/che-logo/dongfengxiaokang.png')
    weight = models.IntegerField(default=1)

    class Meta:
        db_table = "By_brands"


# 车型
class CarsTypes(models.Model):
    name = models.CharField(max_length=64, unique=True)
    weight = models.IntegerField(default=0)
    class Meta:
        db_table = "By_cars_types"


# 车系
class CarsSeries(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # 所属品牌
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'By_cars_series'


status_car = (
    (0, '新上架'),
    (1, '普通车'),
    (2, '严选车'),
    (3, '超值购'),
)

new_status = (
    (0, '准新车'),
    (1, '普通车'),
)

protect_status = (
    (0, '质保'),
    (1, '无质保'),
)

status_issue = (
    (0, '待审核'),
    (1, '审核通过'),
    (2, '审核未通过')
)

status_cars = (
    (0, '上架'),
    (1, '未上架'),
    (2, '已售'),
)


# 车辆
class Cars(models.Model):
    name = models.CharField(max_length=128)
    img1 = models.CharField(max_length=256)
    img2 = models.CharField(max_length=256, null=True)
    img3 = models.CharField(max_length=256, null=True)
    img4 = models.CharField(max_length=256, null=True)
    img5 = models.CharField(max_length=256, null=True)
    img6 = models.CharField(max_length=256, null=True)
    img7 = models.CharField(max_length=256, null=True)
    img8 = models.CharField(max_length=256, null=True)
    img9 = models.CharField(max_length=256, null=True)
    video = models.CharField(max_length=256, null=True)
    video_img = models.CharField(max_length=256, null=True)
    # 上牌时间
    time = models.CharField(max_length=128)
    # 发布时间
    issue_time = models.DateTimeField(max_length=128, default=timezone.now)
    # 里程数
    km = models.FloatField()
    # 排量
    displacement = models.FloatField()
    # 变速箱
    gearbox = models.CharField(max_length=16)
    # 原价
    price = models.FloatField()
    # 现价
    s_price = models.FloatField()
    # 首付
    down_payment = models.FloatField(default=0)
    # # 首付比例
    # ratio = models.FloatField(default=0)
    # 严选/超值
    trait = models.IntegerField(choices=status_car, default=0)
    # 准新车
    new_car = models.IntegerField(choices=new_status, default=0)
    # 有无质保
    protect = models.IntegerField(choices=protect_status, default=0)
    # 过户次数
    transfer = models.IntegerField(default=0)
    # 颜色
    color = models.CharField(max_length=128)

    # 包不包含过户费
    transfer_fee = models.CharField(max_length=64)
    # 排放标准
    emission = models.CharField(max_length=64)
    # 有无重大事故
    accident = models.CharField(max_length=128)
    # 车牌所在地
    license_plate = models.CharField(max_length=128)
    # 维修保养
    maintenance = models.CharField(max_length=128)
    # 用途
    purpose = models.CharField(max_length=128)
    # 年检到期
    yearly_check = models.CharField(max_length=128, null=True)
    # 交强险到期
    compulsory_insurance = models.CharField(max_length=128, null=True)
    # 商业险到期
    commercial_insurance = models.CharField(max_length=128, null=True)

    # 审核是否通过
    is_check = models.IntegerField(choices=status_issue, default=0)
    # 审核失败内容
    failed_content = models.TextField(blank=True, null=True)

    # 车辆状态
    cars_status = models.IntegerField(choices=status_cars, default=0)

    # 车辆描述信息
    info = models.CharField(max_length=256, null=True)
    # 所属车型
    car_type = models.ForeignKey(CarsTypes, on_delete=models.CASCADE)
    # 所属车系
    car_serie = models.ForeignKey(CarsSeries, on_delete=models.CASCADE)

    # 所属用户
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='cars_user')

    # # 被收藏
    # like = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='cars_like', blank=True, null=True)

    class Meta:
        db_table = "By_cars"




status_appointment = (
    (0, '待确认'),
    (1, '已确认'),
    (2, '已取消'),  #用户取消  已取消
    (3, '已失效'),  #商家取消  已失效
)



# 预约看车
class Appointments(models.Model):
    # 预约用户
    uid = models.IntegerField()
    # 预约车辆
    car_id = models.IntegerField()
    # 车辆所属
    car_user = models.IntegerField(default=1)
    # 预约时间
    time = models.DateTimeField(default=timezone.now)
    # 预约姓名
    name = models.CharField(max_length=128)
    # 预约人电话
    phone = models.CharField(max_length=11)
    # 预约状态
    status = models.IntegerField(choices=status_appointment, default=0)

    class Meta:
        db_table = "By_appointments"


status_sell_appointment = (
    (0, '待确认'),
    (1, '已确认'),
    (2, '已取消'),
    (3, '已失效'),
)


# 预约卖车
class SellAppointments(models.Model):
    # 预约用户
    uid = models.IntegerField()
    # 预约时间
    time = models.DateTimeField(default=timezone.now)
    # 预约人电话
    phone = models.CharField(max_length=11, unique=True)
    # 预约人姓名
    name = models.CharField(max_length=128)
    # 预约状态
    status = models.IntegerField(choices=status_sell_appointment, default=0)

    class Meta:
        db_table = "By_sell_appointments"
