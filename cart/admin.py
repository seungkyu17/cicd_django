from django.contrib import admin
from django.utils.html import format_html

from cart.models import Cart, CartProduct

#StackedInline : 부모 모델에서 자식 모델을 보여 줄때, '세로로 펼쳐진 폼 형태' 로 보여 줍니다.
#TabularInline : 부모 모델에서 자식 모델을 보여 줄때, '표(Table) 형태' 로 보여 줍니다.
class CartProductInline(admin.StackedInline):
    model = CartProduct  #자식 모델의 이름
    extra = 2  #보여줄 비어있는(empty) 입력 양식의 갯수

    def product_image(self, obj):
        # 인라인의 빈 폼일 때
        if obj is None:
            return ''

        # 이미지가 있을 때만 format_html 호출
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" style="width:80px; height:auto;" />',
                obj.product.image.url
            )

        return '이미지 없음'

    product_image.short_description = '상품 이미지'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'member')

    inlines = [CartProductInline]
    search_fields = (
        'member__username',
        'member__email',
    )

    readonly_fields = (
        'member',
    )

    list_filter = (
        'member', # 특정 회원의 장바구니 필터링
    )

    list_per_page = 10
#end class CartAdmin

@admin.register(CartProduct)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'cart',
        'product',
        'product_image',
        'quantity',
    )

    search_fields = (
        'cart__id',
        'product__name',
    )

    readonly_fields = ('product_image',)

    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" style="width:80px; height:auto;" />',
                obj.product.image.url
            )
        return '이미지 없음'

    product_image.short_description = '상품 이미지'
#end class CartAdmin