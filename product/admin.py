from django.contrib import admin
from django.utils.html import format_html

from product.models import Product


#'Product' 앱을 'Admin' 페이지에서 관리하기 위해 등록을 하겠습니다.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image_preview',
        'name',
        'price',
        'category',
        'stock',
        'inputdate',
    )

    list_display_links = ('id', 'name')

    list_per_page = 10

    list_filter = ('category', 'inputdate',)

    search_fields = ('name', 'description',)

    # 읽기 전용 필드
    readonly_fields = ('image_preview',)

    # 상세 페이지 레이아웃
    # fieldsets는 관리자(Admin)에서 "상세(등록/수정) 화면의 필드를 그룹으로 나누고, 제목을 붙여서 배치하는 옵션"입니다.
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'price', 'category', 'stock')
        }),
        ('상품 설명', {
            'fields': ('description',)
        }),
        ('상품 이미지', {
            'fields': ('image', 'image_preview',)
        }),
        ('날짜 정보', {
            'fields': ('inputdate',)
        }),
    )

    # 이미지 미리 보기 함수
    # obj는 “현재 admin 화면에서 한 줄(row)에 해당하는 모델 객체 1개” 입니다.
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:100px; height:auto; border:1px solid #ccc;" />',
                obj.image.url
            )
        return '이미지 없음'
    # end def image_preview

    #목록에서 보여지는 열(column) 의 이름을 지정.
    image_preview.short_description = '상품 이미지'

#end class ProductAdmin