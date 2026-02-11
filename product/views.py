from django.shortcuts import render

from product.models import Product

# Create your views here.
def product_carousel(request):  #상품 목록 페이지
    products = Product.objects.filter(image__icontains='bigs')

    return render(request, 'product/product_carousel.html',
     {'products': products})
#end def product_carousel

from math import ceil

def product_list(request):  #상품 목록 페이지
    #'Get' 파라미터 처리
    page_number =int(request.GET.get('pageNumber', 0))
    page_size =int(request.GET.get('pageSize', 6))
    
    searchDataType = request.GET.get('searchDataType','all')  #검색 기간
    category = request.GET.get('category','All')  #카테고리
    searchMode = request.GET.get('searchMode','All')  #검색 모드('이름' 또는 '설명' 중, 택일.)
    searchKeyword = request.GET.get('searchKeyword','')  #검색 키워드

    #상품 목록 가져오기
    products = Product.objects.all().order_by('-id')  #앞에 '-' 는 내림차순 정렬

    #카테고리 필터
    if category != 'All':  #예를 들어, '빵' 만 필터링 해봄.
        products = products.filter(category='category')
    #end if

    #검색 필터
    if searchKeyword:
        if searchMode == 'name':
            products = products.filter(name__icontains=searchKeyword)

        elif searchMode == 'description':
            products = products.filter(description__icontains=searchKeyword)

        else:
            products = products.filter(
                name__icontains=searchKeyword
            ) | products.filter(
                description__icontains=searchKeyword
            )
        #end if
    #end if

    #페이징 처리
    total = products.count()
    total_pages = ceil(total / page_size)

    start = page_number * page_size
    end = start + page_size

    #'현재 페이지' 에서 보여줄 상품들
    paged_products = products[start:end]

    #페이지 번호 리스트
    page_range = range(0, total_pages)

    #넘겨지는 데이터.
    context = {
        'products': paged_products,
        'page_range': page_range,

        'total': total,
        'total_pages': total_pages,

        'page_number' : page_number,
        'page_size' : page_size,
        
        'searchDataType' : searchDataType,
        'category' : category,
        'searchMode' : searchMode,
        'searchKeyword' : searchKeyword,
    }

    return render(request, 'product/product_list.html', context)
#end def product_list

#특정 상품에 대한 상세보기 페이지로 이동.
def product_detail(request, id):
    #ID = 넘겨받은 상품의 아이디
    try:
        product = Product.objects.get(id=id)

        context = {'product': product}
        return render(request, 'product/product_detail.html', context)

    except Product.DoesNotExist:  #'해당 상품' 이 없으면.
        return render(request, 'product/product_not_found.html', status=404)
    #end try
#end def product_detail