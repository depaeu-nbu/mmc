import re

from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    # 序列化字段
    access_token = serializers.CharField(write_only=True, help_text='jwt Token')
    password2 = serializers.CharField(label="确认密码", write_only=True)
    sms_code = serializers.CharField(label="短信验证码", write_only=True)
    allow = serializers.CharField(label="同意协议", write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'password2', 'sms_code', 'mobile', 'allow', 'id', 'mobile'
        ]

        extra_kwards = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户字符需在5-20个之间',
                    'max_length': '用户字符需在5-20个之间',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户字符需在8-20个之间',
                    'max_length': '用户字符需在8-20个之间',
            }
        }
    }

    def validate_allow(self, value):
        """检查是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请勾选同意协议')
        # 返回原值
        return value

    def validate_mobile(self, value):
        """检查手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        count = User.objects.filter(mobile=value).count()
        # 检查手机号是否已经注册
        if count > 0:
            raise serializers.ValidationError('手机号已经注册')
        return value

    def validate(self, attrs):
        """用户名唯一性检查"""
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError('两次输入密码不一致')
        # 检查验证码是否正确
        sms_code = attrs.get("sms_code")
        mobile = attrs.get("mobile")
        redis = get_redis_connection("verify")
        real_code = redis.get("sms_%s" % mobile)

        # 检查短信验证码是否已过期
        try:
            real_code = real_code.decode()
        except Exception as e:
            raise serializers.ValidationError('短信验证码不存在或已过期')
        # 判断验证码是否输入正确
        if real_code != sms_code:
            raise serializers.ValidationError('短信验证码错误')
        return attrs

    def create(self, validated_data):
        """重写create和update方法,删除多余字段"""

        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        # 使用模型create保存数据
        user = super().create(validated_data)

        # 通过模型设置密码加密
        user.set_password(validated_data['password'])
        user.save()

        # 使用jwt保存登陆状态
        from rest_framework_jwt.settings import api_settings
        # 获取 生成载荷的函数
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

        # 获取 生成token的函数
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        # 返回模型
        return user


class EmailSerializer(serializers.ModelSerializer):
    """用户邮箱信息的序列化器"""
    class Meta:
        model = User
        fields = ['id', 'email']
        extra_kwargs = {
            'email': {
                'required': True,
            }
        }

    # def update(self, instance, validated_data):
    #     instance.email = validated_data['email']
    #     instance.save()
    #
    #     # 生成验证邮箱的链接，instance指代的是当前已登陆的用户
    #     verify_url = generate