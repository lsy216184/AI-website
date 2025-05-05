"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views

app_name='diary'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:diary_id>/',views.detail, name='detail'),
    path('search/', views.diary_search, name='diary_search'),
    path('create/', views.diary_create, name='diary_create'),
    path('modify/<int:diary_id>/', views.diary_modify, name='diary_modify'),
    path('delete/<int:diary_id>/', views.diary_delete, name='diary_delete'),
]
