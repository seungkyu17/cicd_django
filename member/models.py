from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
#'Role 상수' 정의.
ROLE_CHOICES = [
    ('USER', '일반 회원'),
    ('ADMIN', '관리자'),
]

#PRAGMA table_info(auth_user);

#'Django' 에는 사용자 (회원)를 위한 'User - 모델 클래스' 가 자동으로 제공 됩니다.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #'User 모델' 과 일대일 관계.
    #'verbose_name' 은 관리자 페이지 등에서 사람에게 보여줄때 사용하는 이름 입니다.
    address = models.CharField(max_length=255, blank=False, verbose_name="주소")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    regdate = models.DateField(default=timezone.now, verbose_name="등록 일자")

    # 추가 유효성 검증 예시
    password_validator = RegexValidator(
        regex=r'^(?=.*[A-Z])(?=.*[!@#$%]).{8,255}$',
        message='비밀번호는 8자리 이상, 대문자 1개 이상, 특수 문자(!@#$%)중 한개를 포함해야 합니다.'
    )

    class Meta:  #'모델 생성' 시 정보를 추가 작성하는 메타 클래스
        db_table = 'profiles'  #'테이블 이름' 을 명시함.

    def __str__(self):  #자바의 'toString() 메소드' 역할과 유사함.
        return f'{self.user.username} - {self.role}'  #예시) hong - USER
#end class