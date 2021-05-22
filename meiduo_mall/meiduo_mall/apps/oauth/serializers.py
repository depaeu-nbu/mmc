from django_redis import get_redis_connection
from rest_framework import serializers

from .models import OAuthUser
from .utils import check_save_user_token
from users.models import User


class QQAuthUserSerializer(serializers.Serializer):
    """QQ登陆创建序列化器"""
    access_token = serializers.CharField(write_only=True, help_text='jwt Token')
    # RegexField设置当前字段需符合正则匹配
    mobile = serializers.RegexField(label='手机号', regex=r'1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')

    def validate_access_token(self, value):
        # attrs是加密后的access-token 因为校验方法检查的是从qq服务器中传回来的access-token

        openid = check_save_user_token(value)
        print(openid)
        # 判断openid是否获取成功
        if openid is None:
            raise serializers.ValidationError({'message': '无效的access_token'})
        return openid

    def validate(self, attrs):
        """校验短信验证码"""
        mobile = attrs['mobile']
        sms_code = attrs['sms_code']
        redis = get_redis_connection('verify')
        # 判断短信验证码是否已过期
        try:
            real_sms_code = redis.get('sms_%s' % mobile)
            real_sms_code = real_sms_code.decode()
        except Exception as e:
            raise serializers.ValidationError({'massage': '无效的短信验证码'})
        # 判断验证码是否输入正确
        if sms_code != real_sms_code:
            raise serializers.ValidationError({'massage': '无效的短信验证码'})

        # 判断用户是否已注册美多账户
        try:
            user = User.objects.get(mobile=mobile)
            attrs['user'] = user
        except User.DoesNotExist:
            # 无美多账号则需要创建美多账户，另写create方法实现，这里不需要处理异常
            pass
        else:
            # 账号存在，判断登录密码是否正确
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({'message': '密码错误！'})
            # 返回用户信息
            return attrs

    def create(self, validated_data):
        """新增账号密码，以手机号作为账号"""
        user = validated_data.get('user')
        if user is None:
            user = User.objects.create(
                username=validated_data['mobile'],
                mobile=validated_data['mobile'],
                password=validated_data['password'],
            )

            # 加密新增的美多账户密码
            user.set_password(validated_data['password'])
            user.save()

        # 将美多账号和qq的openid绑定到auth_QQ表中
        OAuthUser.objects.create(
            openid=validated_data['access_token'],
            user=user,
        )

        return user
