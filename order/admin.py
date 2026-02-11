from django.contrib import admin
from .models import Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Order 목록 : 주문 ID, 주문자 이메일, 주문 상태(대기/완료/취소), 주문 일자(시간 포함)##
    list_display = (
        'id',
        'member',
        'status',
        'orderdate',
    )

    list_filter = (
        'status',
        'orderdate',
    )

    list_editable = ('status',)

    date_hierarchy = 'orderdate'

    search_fields = (
        'member__username',
        'member__email',
    )

    ordering = ('-orderdate',)  # 최신 주문이 위로

    readonly_fields = (
        'member', 'orderdate',
    )

    inlines = [OrderProductInline]

    list_per_page = 10 # 1페이지에 보여줄 행수
# end class OrderAdmin


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
    )

    search_fields = (
        'order__id',
        'product__name',
    )
