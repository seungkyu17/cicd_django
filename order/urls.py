from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('', views.create_order, name='create_order'),  #상품 상세 페이지에서 주문하기
    path('list/', views.order_list, name='order_list'),  #주문 목록 조회
    path('add/', views.add_to_order, name='add_to_order'),  #주문하기 (장바구니 목록)
    path('update/status/<int:order_id>', views.update_status, name='update_status'),  #주문 상태 변경(COMPLETED)
    path('order/cancel/<int:order_id>', views.order_cancel, name='order_cancel'),  #주문 취소
]