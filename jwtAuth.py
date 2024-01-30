"""
모듈
====
사용자에게 받은 jwt코드를 검사 하는 모듈 입니다.

Todo:
    * cookie에 저장되고 있는 jwt 값 또한 처리 할 수 있는 코드  작성

Attributes:
    현재는 header에 Authorization를 통해 받은 jwt를 decode하여 반환합니다.
"""
import os
import jwt
from rest_framework import exceptions

from django.conf import settings

def jwt_decoder(access_token):
    '''
    jwt를 매개변수로 입력받아
    Decode해서 반환 하는 함수

    Args:
        access_token (str) : client에서 header Authorization 값

    Returns:
        str
    '''
    if(access_token == None):
        raise exceptions.ValidationError('access_token NoneType Value')
    try:
        token = access_token.split(' ')[1]
        payload = jwt.decode(
            token, getattr(settings, 'SECRET_KEY'), algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('access_token expired')
    except IndexError:
        raise exceptions.AuthenticationFailed('Token prefix missing')

    return payload