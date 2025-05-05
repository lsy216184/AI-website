from django.urls import path #url 패턴을 정의하는데 사용되는 함수. /path(url경로, 뷰함수, 해당 패턴의 이름지정)
from django.contrib.auth import views as auth_views
from . import views # .은 현재위치인 common앱을 의미 

app_name='common'


urlpatterns=[
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
]