from django.shortcuts import render,get_object_or_404, redirect
from . models import Writing
from .forms import WritingForm
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import os
from ultralytics import YOLO
from glob import glob
from django.conf import settings


# Create your views here.

def index(request):
    diary_list = Writing.objects.order_by('-create_date') 
    context = {'diary_list': diary_list} 
    return render(request, 'diary/diary_list.html', context) 

def detail(request, diary_id):
    diary = Writing.objects.get(id=diary_id) 
    context = {'diary':diary}  
    return render(request, 'diary/diary_detail.html', context) 


#일기 검색
def diary_search(request):
    keyword = request.GET.get("keyword", "")  
    diary_list = Writing.objects.all()

    if keyword: 
        diary_list = diary_list.filter(
            Q(subject__icontains=keyword) | 
            Q(content__icontains=keyword)
        )

    context = {'diary_list': diary_list, 'keyword': keyword}  
    return render(request, "diary/diary_list.html", context) 


#일기 생성
@login_required(login_url='common:login')
def diary_create(request):
    
    if request.method =='POST': 
        form = WritingForm(request.POST, request.FILES) 
        
        
        if form.is_valid():      
            diary = form.save(commit=False)  
            diary.author = request.user 
            diary.create_date = timezone.now() 
            diary.save()                            
            return redirect('diary:index')     
        
    else:                    #get요청이라면
        form = WritingForm()

    return render(request, 'diary/diary_form.html', {'form': form})
    
    
#일기 수정  
@login_required(login_url='common:login')
def diary_modify(request, diary_id):
    diary = get_object_or_404(Writing, pk=diary_id)

    if request.user != diary.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('diary:detail', diary_id=diary.id)

    if request.method == 'POST':
        form = WritingForm(request.POST, request.FILES, instance=diary)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.modify_date = timezone.now()
            diary.save()
            # upload_images = request.FILES.getlist('photo')
            return redirect('diary:detail', diary_id=diary.id)
    else:
        form = WritingForm(instance=diary)

    context = {'form': form}
    return render(request, 'diary/diary_form.html', context)
           
           
#일기 삭제          
@login_required(login_url='common:login')
def diary_delete(request, diary_id):
    diary = get_object_or_404(Writing, pk=diary_id)
    if request.user != diary.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('diary:detail', diary_id=diary.id)
    diary.delete()
    return redirect('diary:index')


@login_required(login_url='common:login')
def diary_predict(request, diary_id):
    diary = get_object_or_404(Writing, pk=diary_id)

    if request.user != diary.author:
        messages.error(request, "예측 권한이 없습니다.")
        return redirect("diary:detail", diary_id=diary.id)

    # 유저 업로드 이미지 폴더
    user_dir = os.path.join(settings.MEDIA_ROOT, "diary_images", request.user.username)
    image_files = sorted(glob(os.path.join(user_dir, "*.*")), key=os.path.getmtime, reverse=True)
    if not image_files:
        messages.error(request, "이미지가 없습니다.")
        return redirect("diary:detail", diary_id=diary.id)

    latest_image = image_files[0]

    # YOLO 모델 로딩
    model = YOLO("/root/yolo/weight/yolo11x.pt")

    # 저장할 디렉토리 설정
    name = "predict"
    save_dir = os.path.join(settings.MEDIA_ROOT, "predicted", request.user.username)

    # YOLO 실행
    results = model(
        source=latest_image,
        device=0,
        save=True,
        project=save_dir,
        name=name,
        exist_ok=True
    )

    # 결과 이미지가 저장된 정확한 폴더
    result_dir = os.path.join(save_dir, name)
    result_files = sorted(glob(os.path.join(result_dir, "*.*")), key=os.path.getmtime)

    if not result_files:
        messages.error(request, "예측 결과 파일이 생성되지 않았습니다.")
        return redirect("diary:detail", diary_id=diary.id)

    predicted_path = result_files[-1].replace(settings.MEDIA_ROOT, "").lstrip("/")
    original_path = latest_image.replace(settings.MEDIA_ROOT, "").lstrip("/")

    return render(request, "diary/prediction_result.html", {
        "original": original_path,
        "predicted": predicted_path,
        "diary": diary,
        "MEDIA_URL": settings.MEDIA_URL,  # 👈 이것을 꼭 추가
    })
