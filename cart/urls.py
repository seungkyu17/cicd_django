from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('insert/', views.add_to_cart, name='add_to_cart'),
    path('list/<int:member_id>', views.cart_list, name='cart_list'),
    path('delete/<int:item_id>', views.delete_cart_product, name='delete_cart_product'),
    path('update_quantity/<int:item_id>', views.update_cart_product, name='update_cart_product'),
]