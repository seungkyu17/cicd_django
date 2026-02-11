from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from cart.models import CartProduct
from order.models import Order, OrderProduct
from product.models import Product


@login_required
@require_http_methods(['POST'])
def create_order(request): # 주문하기(Post)
    user = request.user # 로그인한 사용자

    # 상품 상세 보기 페이지에서 "상품id:주문수량"의 형식으로 데이터가 넘어 옵니다.
    # 참조 : 자바스크립트 함수 prepareOrderItems()
    order_products = request.POST.getlist('order_products')

    if not order_products: # 주문한 상품이 없으면
        # return redirect('product:product_list')
        return redirect('order:order_list') # 아직 미구현
    # end if

    # 주문(Order) 객체 생성
    order = Order.objects.create(member=user, status='PENDING', orderdate=timezone.now())

    # 주문 상품(OrderProduct) 객체 생성
    for product in order_products:
        # map 함수가 모든 요소들을 반복하면서 정수로 변환해 줍니다.
        product_id, quantity = map(int, product.split(':'))

        OrderProduct.objects.create(
            order=order,
            product_id=product_id,
            quantity=quantity
        )

        # 재고 수량 차감
        product = Product.objects.get(id=product_id)
        product.stock -= quantity
        product.save() # DB에 반영하기
    # end for

    # return redirect('product:product_list')
    return redirect('order:order_list') # 아직 미구현
# end def create_order

@login_required
def order_list(request): # 주문 목록 조회(GET)
    user = request.user
    role = user.profile.role # ADMIN 또는 USER

    status_filter = [
        Order.OrderStatus.PENDING,
        Order.OrderStatus.COMPLETED,
    ]

    if role == 'ADMIN': # 모든 주문 내역 보기
        orders = Order.objects.filter(
            status__in=status_filter
        ).order_by('-orderdate')

    else: # 일반인은 나의 주문 내역만 보기
        orders = Order.objects.filter(
            member=user,
            status__in=status_filter
        ).order_by('-orderdate')
    # end if

    context = {
        'orders': orders,
        'role': role,
    }

    return render(request, 'order/order_list.html', context)
# end def order_list

@login_required
@transaction.atomic
def add_to_order(request): # 장바구니 목록에서 주문하기
    if request.method != 'POST':
        return redirect('cart:cart_list', member_id=request.user.id)

    # 선택이 된 장바구니 상품의 id 목록
    # <input> 태그의 name="selected_products"인 항목들의 value 정보가 넘어옵니다.
    # selected_products는 체크된 상품들의 id 정보를 저장하고 있는 리스트
    selected_products = request.POST.getlist('selected_products')

    if not selected_products: # 선택된 품목이 존재하지 않으면 ...
        return redirect('cart:cart_list', member_id=request.user.id)

    # 주문 생성
    order = Order.objects.create(
        member=request.user,
        status='PENDING',
        orderdate=timezone.now()
    )

    # 선택된 상품들을 사용하여 주문 상품으로 변환
    for product_id in selected_products:
        cart_product = CartProduct.objects.filter(
            id=product_id,
            cart__member=request.user
        ).first()

        if not cart_product:
            continue

        # html 문서에서 수량 변경 입력란의 name 속성은 "quantity_상품번호" 형식으로 만들었습니다.
        quantity = int(request.POST.get(f'quantity_{product_id}', cart_product.quantity))

        #시작
        product = cart_product.product
        
        #재고 부족 체크 (중요)
        if product.stock < quantity:
            raise ValueError(f'{product.name} 재고 부족')

        #끝
        OrderProduct.objects.create(  #주문 상품 생성
            order=order,
            product=cart_product.product,
            quantity=quantity
        )

        #시작
        #재고 차감
        product.stock -= quantity
        product.save()
        #끝

        # 주문된 상품은 장바구니 목록에서 제거
        cart_product.delete()
    # end for

    return redirect('order:order_list')
# end def add_to_order

# 주문 상태 선택지
ORDER_STATUS_CHOICES = ['PENDING', 'COMPLETED', 'CANCELLED']

# 주문 상태 변경
@login_required
@require_http_methods(['POST'])
def update_status(request, order_id):
    new_status = request.POST.get('status')
    if new_status not in ORDER_STATUS_CHOICES:
        return redirect('order:order_list')

    order = get_object_or_404(Order, id=order_id)
    order.status = new_status # 주문 상태 변경
    order.save() # 데이터 베이스에 저장
    return redirect('order:order_list')
# end class update_status

# 주문 취소
@login_required
@require_http_methods(['POST'])
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    with transaction.atomic() : # 트랜잭션 처리
        # 재고 수량은 다시 원래대로 복원합니다.
        for item in order.order_products.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        # end for

        order.delete() # 주문 삭제
    # end with

    return redirect('order:order_list')
# end class order_cancel







