from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import MyUser

# 회원가입
class MyUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=MyUser.objects.all())], # 이메일 중복인증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password] # 비밀번호 유효성 검사
    )
    password2 = serializers.CharField(write_only=True, required=True) # 비밀번호 확인

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password2', 'name', 'phone', 'position']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        if('position' not in data):
            raise serializers.ValidationError({"position":"직책을 입력해주세요"})
        return data

    def create(self, validated_data):
        # create 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성함.
        user = MyUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data['phone'],
            position=validated_data['position']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)

        print(attrs)
        print(user)

        if user:
            data = super().validate(attrs)
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError("아이디 혹은 비밀번호가 일치하지 않습니다.")