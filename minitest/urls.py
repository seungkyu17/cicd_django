from django.urls import path

from minitest import views

#'app_name' 은 'Template' 파일에서 'NameSpace' 역할을 합니다.
app_name = 'minitest'

#'App url' 파일 : 'minitest App' 에서만 사용하는 'url 경로' 지정 파일 입니다.
urlpatterns = [
    #'name 속성' 은 'Template' 파일의 {% url 구문 %} 에서 참조 합니다.

    path('fruit/', views.fruit, name='fruit'), #http://127.0.0.1:8000/minitest/fruit/
    path('fruit/list', views.fruit_list, name='fruit_list'), #http://127.0.0.1:8000/minitest/fruit/list/
]