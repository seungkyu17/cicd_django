from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST

from cart.models import CartProduct, Cart
from product.models import Product

#장바구니에 상품 담기.
@require_POST  #이 뷰는 'POST 요청' 만 처리 합니다.
def add_to_cart(request):
    member_id = request.user.id
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))  #1 = 기본 값

    #'get_object_or_404' 함수는 객체를 조회하되, 존재하지 않으면, '404 오류' 를 반환해주는 함수 입니다.
    product = get_object_or_404(Product, id=product_id)

    #'get_or_create' 함수 는 존재하면 가져오고, 없으면 신규 생성 해주는 함수 입니다.
    cart, _ = Cart.objects.get_or_create(member_id=member_id)

    #'Created 변수' 는 신규로 생성이 되면, 'True' 입니다.
    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:  #이미 상품이 담겨 있으면.
        #앞에 담겨져 있던 상품 개수를 누적 합니다.
        cart_product.quantity += quantity
        cart_product.save()

    #'성공 메시지 생성
    messages.success(request, f'장바구니에 상품 "{product.name}"이(가) {quantity} 개 추가 되었습니다.')

    #'상품 목록' 페이지로 이동 합니다.
    #'product_list' 라는 항목은 'product' 앱의 'urls.py' 파일에 정의되어 있습니다.
    return redirect('product:product_list')
#end def add_to_cart

#'특정한 사용자' 의 장바구니 목록 조회하기.
@login_required # 로그인한 사용자만 접근이 가능합니다.
def cart_list(request, member_id):
    # 내 Cart가 없으면 상품 목록 페이지로 이동
    cart = Cart.objects.filter(member_id=member_id).first()

    if not cart:
        return redirect('product:product_list')  # 상품 목록 URL 이름

    cart_products = CartProduct.objects.filter(cart=cart).select_related('product')

    # 장바구니의 총 금액과 각 품목 금액 계산
    cart_total_price = 0
    for item in cart_products:
        item.total_price = item.product.price * item.quantity
        cart_total_price += item.total_price
    # end for

    context = {
        'cart_products': cart_products,
        'cart_total_price': cart_total_price,
    }

    return render(request, 'cart/cart_list.html', context)
# end def cart_list

@login_required
def delete_cart_product(request, item_id):
    #주의사항 - 'Cart 모델' 에서 변수 이름을 'member' 라고 정의 했습니다.
    cart_product = get_object_or_404(CartProduct, id=item_id, cart__member=request.user)

    cart = cart_product.cart  #나의 카트

    cart_product.delete()  #카트 상품 덜어내기

    if not cart.cart_products.exists():  #내 카트에 물건이 없으면.
        #카트도 같이 삭제하고, 상품 목록 페이지로 이동하기
        cart.delete()  #카트도 삭제하기.
        return redirect('product:product_list')
    else:
        #해당 상품을 삭제하고, 다시 나의 장바구니 목록 페이지로 이동
        return redirect('cart:cart_list', member_id=request.user.id)

# end def delete_cart_product


import json

@login_required
@require_POST
def update_cart_product(request, item_id):
    data = json.loads(request.body)
    quantity = int(data.get('quantity', 1))

    if quantity < 1:
        quantity = 1

    cart_product = get_object_or_404(CartProduct, id=item_id, cart__member=request.user)
    cart_product.quantity = quantity
    cart_product.save()

    return redirect('cart:cart_list', member_id=request.user.id)
#end def update_cart_product