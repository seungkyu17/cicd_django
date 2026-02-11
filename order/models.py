from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
from django.views.decorators.http import require_http_methods


# Create your models here.
class Order(models.Model):
    class OrderStatus(models.TextChoices):  #'주문 상태' 열거형 상수
        PENDING = 'PENDING', '대기'
        COMPLETED = 'COMPLETED', '완료'
        CANCELED = 'CANCELED', '취소'
    #end class OrderStatus

    id = models.BigAutoField(primary_key=True)

    #'회원 1명' 은 여러개의 주문을 할 수 있습니다.(회원 - '1 : N' 주문)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    # 정렬을 위하여 DateTimeField이 좋을 듯함
    # orderdate = models.DateField(default=timezone.now)
    orderdate = models.DateTimeField(auto_now_add=True)

    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING, max_length=10)

    #주문 목록 페이지에서 사용하는 'Helper' 메소드로, 'order_list.html' 문서에서 사용 됨.
    def is_completed(self):
        return self.status == self.OrderStatus.COMPLETED

    def __str__(self):
        return f'Order {self.id}({self.status})'

    class Meta:
        db_table = 'orders'
#end class Order

from product.models import Product

class OrderProduct(models.Model):
    id = models.BigAutoField(primary_key=True)

    #주문과 다대일 관계
    #'related_name' 매개 변수에는 'db_table' 속성 값과 동일한 값을 입력해 줍니다.
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')

    #상품과 다대일 관계
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')

    quantity = models.PositiveIntegerField(default=1)  #주문 수량

    def __str__(self):
        return f'Order {self.product.name} * {self.quantity}'

    class Meta:
        db_table = 'order_products'
#end class OrderProduct


