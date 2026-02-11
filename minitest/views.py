from django.shortcuts import render

# Create your views here.
#'과일 1개' 를 보여주는 함수 작성.
def fruit(request):
    bean = {
        "id": "banana",
        "name": "바나나",
        "price": 1000,
    }
    return render(request, 'minitest/fruit.html', {'fruit':bean})

#'여러개의 과일' 을 보여주는 함수 작성.
def fruit_list(request):
    fruits = [
            {"id": "apple", "name": "사과", "price": 1000},
            {"id": "pear", "name": "나주배", "price": 2000},
            {"id": "grape", "name": "포도", "price": 3000},
    ]

    return render(request, 'minitest/fruit_list.html', {'fruit_list':fruits})