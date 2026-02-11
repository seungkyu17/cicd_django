from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from member.models import Profile

#Signal : 어떠한 사건이 발생함을 알려주는 신호.
# 예시)
# 신규 회원이 가입했을 때
# 사용자가 상품을 주문했을 때

#Decorator : 기존 함수의 코드를 수정하지 않고, 기능을 덧 붙이거나 변경하기 위한 동작.
#'@receiver' 는 'signal' 과 해당 함수를 연결합니다.

#회원 가입 : 'User' 객체 생성 --> 'Profile' 객체 생성
# 'User' 객체에 대해, 'post_save' 라는 'signal' 이 입력되면,
# 'create_user_profile' 함수가 실행된다.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    #sender : 'signal' 을 생성한 객체(User 객체)
    #instance : 데이터베이스에 방금 생성된 'User' 객체
    #created : 신규 생성인지를 판단하는 'boolean' - True/False
    #**kwargs : 추가 정보 (사전 형식)

    if created : #회원 가입 직후, 실행에 해당하는 어떤 로직
        Profile.objects.create(user=instance)
#end def create_user_profile

#회원 정보 수정 : 'User' 객체 수정 --> 'Profile' 객체 수정
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    #'instance.profile' 은 'User' 객체와 연결된 'Profile' 객체
    instance.profile.save()
#end def save_user_profile