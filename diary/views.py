from django.shortcuts import render,get_object_or_404, redirect
from . models import Writing
from .forms import WritingForm
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import os
import shutil
from ultralytics import YOLO
from glob import glob
from django.conf import settings

#모델용 함수 가져오기
from .vit_classifier import classify_image 


# YOLO 모델 로딩(모델이 무거워서 최상단에서 한번만 로드)
model = YOLO("/root/yolo/weight/yolo11x.pt")

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
    
    # 1) 업로드된 이미지 파일 삭제
    if diary.image:
        diary.image.delete(save=False)

    # 2) 예측 결과 폴더 삭제
    import os, shutil
    from django.conf import settings

    pred_dir = os.path.join(
        settings.MEDIA_ROOT,
        'predicted',
        request.user.username,
        str(diary.id)
    )
    if os.path.isdir(pred_dir):
        shutil.rmtree(pred_dir)
    
    
    diary.delete()
    return redirect('diary:index')



#이미지 예측
@login_required(login_url='common:login')
def image_predict(request, diary_id):
    # 1) 일기 객체 가져오기 + 권한 체크
    diary = get_object_or_404(Writing, pk=diary_id)
    if request.user != diary.author:
        messages.error(request, "예측 권한이 없습니다.")
        return redirect("diary:detail", diary_id=diary.id)

    # 2) 이 일기의 이미지 경로
    if not diary.image:
        messages.error(request, "업로드된 이미지가 없습니다.")
        return redirect("diary:detail", diary_id=diary.id)
    source_path = diary.image.path

    # 3) 예측 결과를 저장할 디렉터리: media/predicted/<username>/<diary_id>/
    save_root = os.path.join(settings.MEDIA_ROOT, "predicted", request.user.username)
    result_dir = os.path.join(save_root, str(diary.id))

    # 3-1) 이전 예측물이 남아 있으면 초기화
    if os.path.isdir(result_dir):
        shutil.rmtree(result_dir)
    os.makedirs(result_dir, exist_ok=True)

    # 4) YOLO 예측 실행
    #    - project=save_root, name=str(diary.id) 이면
    #      save_root/<diary.id>/ 으로 결과가 저장됩니다.
    model(
        source=source_path,
        device=0,
        save=True,
        project=save_root,
        name=str(diary.id),
        exist_ok=True
    )

    # 5) 결과 파일 목록을 모아서 가장 최신 하나를 선택
    out_files = sorted(
        glob(os.path.join(result_dir, "*.*")),
        key=os.path.getmtime
    )
    if not out_files:
        messages.error(request, "예측 결과가 생성되지 않았습니다.")
        return redirect("diary:detail", diary_id=diary.id)

    # 6) 템플릿엔 media 설정이 있을 테지만, 안전을 위해 전달
    #    URL로 쓸 수 있게 '/predicted/.../파일명' 로 만듭니다.
    predicted_rel = out_files[-1].replace(settings.MEDIA_ROOT, "").lstrip("/")
    original_rel  = source_path     .replace(settings.MEDIA_ROOT, "").lstrip("/")

    return render(request, "diary/prediction_result.html", {
        "original": original_rel,
        "predicted": predicted_rel,
        "diary": diary,
        "MEDIA_URL": settings.MEDIA_URL,
    })
 



 #이미지 분류
@login_required(login_url='common:login')
#모델용 함수(classify_image) 와 뷰 함수(classify_image_view)의 이름이 겹치지 않게 정의!
def classify_image_view(request, diary_id):  
    diary = get_object_or_404(Writing, pk=diary_id)

    if request.user != diary.author:
        messages.error(request, "분류 권한이 없습니다.")
        return redirect("diary:detail", diary_id=diary.id)

    if not diary.image:
        messages.error(request, "이미지가 없습니다.")
        return redirect("diary:detail", diary_id=diary.id)

    # 함수 호출만으로 분류 수행
    predictions = classify_image(diary.image.path)

    return render(request, 'diary/classify_image_res.html', {
        'diary': diary,
        'predictions': predictions,
        'image_url': diary.image.url
    })