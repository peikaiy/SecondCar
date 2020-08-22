from rest_framework import serializers

from Bo_yuan.models import Cars, SellAppointments, Users, Banners, Fwb, Appointments, UserLikes, \
    Brands, CarsSeries, CarsTypes


class UserSerializer(serializers.ModelSerializer):
    """用户数据序列化器"""
    u_property = serializers.CharField(source='get_u_property_display')
    wx_icon = serializers.CharField()
    class Meta:
        model = Users

        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """用户数据序列化器"""
    u_property = serializers.CharField(source='get_u_property_display')
    wx_icon = serializers.CharField()

    class Meta:
        model = Users

        fields = '__all__'




class UsersSerializer(serializers.ModelSerializer):
    """用户创建数据序列化器"""

    class Meta:
        model = Users

        fields = '__all__'




class CarSerializer(serializers.ModelSerializer):
    """车详情数据序列化器"""
    user = serializers.CharField(source='user.wx_name')
    # user_id = serializers.CharField(source='user.id')
    car_type = serializers.CharField(source='car_type.name')
    car_serie = serializers.CharField(source='car_serie.name')
    u_property = serializers.CharField(source='user.get_u_property_display')
    new_car = serializers.CharField(source='get_new_car_display')
    protect = serializers.CharField(source='get_protect_display')
    trait = serializers.CharField(source='get_trait_display')
    cars_status = serializers.CharField(source='get_cars_status_display')
    is_check = serializers.CharField(source='get_is_check_display')
    img1 = serializers.CharField()
    img2 = serializers.CharField()
    img3 = serializers.CharField()
    img4 = serializers.CharField()
    img5 = serializers.CharField()

    class Meta:
        model = Cars
        # fields = ('id', 'name', 'km', 'time', 'user', 's_price')
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['failed_content']:
            data['failed_content'] = ""
        if not data['compulsory_insurance']:
            data['compulsory_insurance'] = ""
        if not data['yearly_check']:
            data['yearly_check'] = ""
        if not data['info']:
            data['info'] = ""
        if not data['commercial_insurance']:
            data['commercial_insurance'] = ""
        if not data['img2']:
            data['img2'] = ""
        if not data['img3']:
            data['img3'] = ""
        if not data['img4']:
            data['img4'] = ""
        if not data['img5']:
            data['img5'] = ""
        if not data['img6']:
            data['img6'] = ""
        if not data['img7']:
            data['img7'] = ""
        if not data['img8']:
            data['img8'] = ""
        if not data['img9']:
            data['img9'] = ""
        if not data['video']:
            data['video'] = ""
        if not data['video_img']:
            data['video_img'] = ""
        return data


class CarissueSerializer(serializers.ModelSerializer):
    """编辑车详情数据序列化器"""
    user = serializers.CharField(source='user.wx_name')
    # user_id = serializers.CharField(source='user.id')
    u_property = serializers.CharField(source='user.get_u_property_display')
    new_car = serializers.CharField(source='get_new_car_display')
    trait = serializers.CharField(source='get_trait_display')
    cars_status = serializers.CharField(source='get_cars_status_display')
    is_check = serializers.CharField(source='get_is_check_display')
    img1 = serializers.CharField()
    img2 = serializers.CharField()
    img3 = serializers.CharField()
    img4 = serializers.CharField()
    img5 = serializers.CharField()

    class Meta:
        model = Cars
        # fields = ('id', 'name', 'km', 'time', 'user', 's_price')
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['failed_content']:
            data['failed_content'] = ""
        if not data['compulsory_insurance']:
            data['compulsory_insurance'] = ""
        if not data['yearly_check']:
            data['yearly_check'] = ""
        if not data['info']:
            data['info'] = ""
        if not data['commercial_insurance']:
            data['commercial_insurance'] = ""
        if not data['img2']:
            data['img2'] = ""
        if not data['img3']:
            data['img3'] = ""
        if not data['img4']:
            data['img4'] = ""
        if not data['img5']:
            data['img5'] = ""
        if not data['img6']:
            data['img6'] = ""
        if not data['img7']:
            data['img7'] = ""
        if not data['img8']:
            data['img8'] = ""
        if not data['img9']:
            data['img9'] = ""
        if not data['video']:
            data['video'] = ""

        if not data['video_img']:
            data['video_img'] = ""

        return data



class IssueCarsSerializer(serializers.ModelSerializer):
    """编辑车发布详情数据序列化器"""
    class Meta:
        model = Cars
        fields = '__all__'


class CarsSerializer(serializers.ModelSerializer):
    """车数据序列化器"""

    u_property = serializers.CharField(source='user.get_u_property_display')
    new_car = serializers.CharField(source='get_new_car_display')
    protect = serializers.CharField(source='get_protect_display')
    trait = serializers.CharField(source='get_trait_display')
    cars_status = serializers.CharField(source='get_cars_status_display')
    is_check = serializers.CharField(source='get_is_check_display')
    issue_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    img1 = serializers.CharField()

    class Meta:
        model = Cars
        fields = ('id', 'name', 'km',  's_price', 'is_check', 'transfer', 'time', 'img1', 'u_property', 'issue_time', 'trait', 'new_car', 'transfer_fee', 'cars_status', 'protect')
        # fields = '__all__'


class UserIssueCarsSerializer(serializers.ModelSerializer):
    """个人发布车车数据序列化器"""

    u_property = serializers.CharField(source='user.get_u_property_display')
    new_car = serializers.CharField(source='get_new_car_display')
    protect = serializers.CharField(source='get_protect_display')
    trait = serializers.CharField(source='get_trait_display')
    cars_status = serializers.CharField(source='get_cars_status_display')
    is_check = serializers.CharField(source='get_is_check_display')
    issue_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    img1 = serializers.CharField()

    class Meta:
        model = Cars
        fields = ('id', 'name', 'km', 'price',  's_price', 'failed_content',  'is_check', 'transfer', 'time', 'img1', 'u_property', 'issue_time', 'trait', 'new_car', 'transfer_fee', 'cars_status', 'protect')
        # fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['failed_content']:
            data['failed_content'] = ""

        return data


class BrandsSerializer(serializers.ModelSerializer):
    """车品牌数据序列化器"""
    logo = serializers.CharField()
    class Meta:
        model = Brands

        fields = '__all__'


class SeriesSerializer(serializers.ModelSerializer):
    """车系数据序列化器"""

    class Meta:
        model = CarsSeries

        # fields = '__all__'

        exclude = ('brand',)


class CarsTypesSerializer(serializers.ModelSerializer):
    """车型数据序列化器"""

    class Meta:
        model = CarsTypes

        fields = '__all__'



class BannersSerializer(serializers.ModelSerializer):
    """Banners序列化器"""
    img = serializers.CharField()
    content = serializers.CharField()
    class Meta:
        model = Banners
        fields = '__all__'



class FwbSerializer(serializers.ModelSerializer):
    """fwb序列化器"""

    class Meta:
        model = Fwb
        fields = '__all__'





class SellAppointmentsSerializer(serializers.ModelSerializer):
    """快速卖车数据序列化器"""
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=['%Y-%m-%d %H:%M', ])
    class Meta:
        model = SellAppointments
        fields = '__all__'


class LookAppointmentsSerializer(serializers.ModelSerializer):
    """预约看车数据序列化器"""
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=['%Y-%m-%d %H:%M', ])
    class Meta:
        model = Appointments
        fields = '__all__'

#
# class UserSerializer(serializers.ModelSerializer):
#     """用户数据序列化器"""
#     u_property = serializers.CharField(source='get_u_property_display')
#
#     class Meta:
#         model = Users
#         fields = '__all__'





class LikeCarSerializer(serializers.ModelSerializer):
    """关注车辆数据序列化器"""

    class Meta:
        model = UserLikes
        fields = '__all__'
