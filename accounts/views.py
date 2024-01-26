from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from accounts.serializers import MyUserSerializer,LoginSerializer

def home(request: HttpRequest) -> HttpResponse:
    return redirect('/account/login/')

class AccountCreateAPIView(generics.CreateAPIView):
    # 회원가입, 유저 생성
    serializer_class = MyUserSerializer


class LoginAPIView(generics.GenericAPIView):
    # 로그인
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        res = Response(
            data={
                "userid": serializer.validated_data['user'].email,
                "username": serializer.validated_data['user'].name,
                "message": "로그인 성공",
                "token": {
                    "access": serializer.validated_data['access'],
                    "refresh": serializer.validated_data['refresh'],
                }
            },
            status=status.HTTP_200_OK,
        )

        # jwt 토큰을 쿠키에 저장
        res.set_cookie("access", serializer.validated_data['access'], httponly=True)
        res.set_cookie("refresh", serializer.validated_data['refresh'], httponly=True)

        return res

class RefreshTokenAPIView(generics.GenericAPIView):
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        res = Response(
            {
                "message": "재발급 성공",
                "token": {
                    "access": serializer.validated_data['access'],
                    "refresh": serializer.validated_data['refresh'],
                }
            },
            status=status.HTTP_201_CREATED
        )

        res.set_cookie("access", serializer.validated_data['access'], httponly=True)
        res.set_cookie("refresh", serializer.validated_data['refresh'], httponly=True)

        return res