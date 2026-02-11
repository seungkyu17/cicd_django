"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from config import views

from django.views.generic import RedirectView
from product.views import product_carousel
from django.conf import settings
from django.conf.urls.static import static

#'Root url' 파일 : 일반 'App' 에 들어있는 'Url' 과 구분 짓기 위해 붙이는 용어 입니다.
#CF) 'App url' 파일
urlpatterns = [
    path('admin/', admin.site.urls),
    path('minitest/', include('minitest.urls')),
    path('member/', include('member.urls')),

    #'홈 페이지' 의 경로를 지정.
    path('home/', views.home_view, name='home'),

    #상품의 'Carousel' 페이지로 구현할 예정
    path('', RedirectView.as_view(pattern_name='product_carousel', permanent=False)),
    path('homepage/', product_carousel, name='product_carousel'),

    path('product/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)