from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from common.forms import UserForm

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect ('index')

def signup(request):
    if request.method =="POST": 
        form = UserForm(request.POST)
        if form.is_valid(): #유효성 검사
            form.save() #db에 사용자 저장
            username = form.cleaned_data.get('username') #입력된 폼에서 정보 추출
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password) #사용자가 실제로 인증 가능한지 확인
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})
    
    
    
    
    
    