from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from product.models import Product


#한명의 회원은 하나의 'Cart' 를 가집니다.
class Cart(models.Model):
    #'related_name' 속성이 없으면, 자동으로 'cart_set' 이라는 이름으로 생성이 됩니다.
    #'user.set.xxx' 형식으로 사용하기 위해, 설정 했습니다.
    # member = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    #AUTH_USER_MODEL = 'auth.user' 가 기본 값 입니다.
    #차후, '확장성' 을 고려해, 'User' 대신 'AUTH_USER_MODEL' 키워드를 사용 합니다.
    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        db_table = 'carts'  #'Developer' 가 테이블 이름을 지정.

    def __str__(self):
        return f'Cart(id={self.id}, member={self.member.username})'
#end class Cart

#'Cart' 에 담길 상품(Product) 1개를 나타내고자 하는 모델 클래스.
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_products'
        #동일한 상품 정보를 동일한 카트에 중복 담기 방지.
        unique_together = (('cart', 'product'),)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
#end class CartProduct