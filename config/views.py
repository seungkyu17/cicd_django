from django.shortcuts import render

#임시로 사용할 홈페이지를 위한 'View'
def home_view(request):
    return render(request, 'home.html')