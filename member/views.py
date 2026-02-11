from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

from member.forms import LoginForm
from member.models import Profile


# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        #1. 유효성 검사
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        address = request.POST.get('address', '').strip()

        errors = {}  #오류를 저장할 사전
        if not name :
            errors['name'] = '이름을 입력해 주세요.'

        if not name :
            errors['email'] = '이메일을 입력해 주세요.'
        elif User.objects.filter(username=email).exists():
            errors['email'] = '이미 존재하는 회원 입니다.'
        #end if

        if not name :
            errors['password'] = '비밀 번호를 입력해 주세요.'

        if not name :
            errors['address'] = '주소를 입력해 주세요.'

        #2. 폼 양식에 문제가 있으면, 다시 폼으로 이동하기
        if errors:
            return render(request, 'member/signup.html', {
                'errors' :errors,
                'name' :name,
                'email' :email,
                'address' :address
            })

        #3. 회원 생성(User 저장)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        #4. 'Profile 정보' 를 이용해, 부가 정보 저장.(User 저장)
        profile = Profile.objects.get(user=user)
        profile.address = address
        profile.save()


        messages.success(request, '회원 가입 성공~, 로그인 해주세요.')

        return redirect('member:login')  #수정 예정

    else:  #'GET' 방식
        return render(request, 'member/signup.html')
    #end if
#end def signup_view

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():  #'유효성 검사' 를 통과 했으면
            #'cleaned_data' 사전 : '폼 유효성 검사' 를 통과한 입력 값을 정제된 데이터로 담고있는 사전.
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            #'authenticate' 는 인증 관련 함수
            #'username 컬럼' 에 실제 이메일 정보를 저장 합니다.
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                # return redirect('/home')  #로그인 성공
                return redirect('product:product_list')  #로그인 성공
            else:
                messages.error(request, '이메일 또는 비밀 번호가 잘못 되었습니다.')
            #end if

    else:
        form = LoginForm()
    #end if

    return render(request, 'member/login.html', {'form': form})
#end def login_view

def logout_view(request):
    logout(request)  #세션 정보 삭제 + 로그 아웃 처리
    messages.success(request, '로그 아웃 되었습니다.')
    return redirect('member:login')
# end def logout_view