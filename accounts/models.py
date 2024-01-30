import uuid

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group, Permission
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):

        if not email:
            raise ValueError('이메일을 입력해주세요.')

        if not phone:
            raise ValueError('전화번호를 입력해주세요.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
            phone=phone,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):

    MyUser_ROLL_LABEL=[
        ('MEMBER', '멤버'),
        ('MASTER', '마스터'),
    ]
    email = models.EmailField(verbose_name='회사 이메일 혹은 이메일', max_length=50, unique=True, null=False)
    name = models.CharField(verbose_name='회사 이름 혹은 이름', max_length=30)
    phone = models.CharField(verbose_name='회사 번호 혹은 번호', max_length=13, unique=True)
    position = models.CharField(verbose_name='직책', max_length=30, choices=MyUser_ROLL_LABEL, default='NONE')
    is_active = models.BooleanField(verbose_name='로그인 가능', default=True)
    is_superuser = models.BooleanField(verbose_name='최고관리자', default=False)
    is_staff = models.BooleanField(verbose_name='관리자페이지 접근', default=False)
    last_login = models.DateTimeField(verbose_name='로그인 일시', blank=True, null=True)
    created = models.DateTimeField(verbose_name='등록 일시', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='수정 일시', auto_now=True)
    groups = models.ManyToManyField(Group, verbose_name='roll_groups', blank=True, related_name='user_set', related_query_name='user')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    class Meta:
        verbose_name_plural = '사용자'
        db_table = 'user'

    def __str__(self):
        return f'{self.name} - {self.email}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

from rolepermissions.roles import AbstractUserRole

class Teacher(AbstractUserRole):
    available_permissions = {
        'edit_course': True,
    }

class Student(AbstractUserRole):
    available_permissions = {
        'view_course': True,
    }