from django.urls import path

from product import views

app_name = 'product'

urlpatterns = [
    path('list/', views.product_list, name='product_list'),

    #http://127.0.0.1:8000/product/detail/10
    path('detail/<int:id>', views.product_detail, name='detail'),
]