from django.shortcuts import render,get_object_or_404, redirect
from . models import Writing
from .forms import WritingForm
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def index(request):
    diary_list = Writing.objects.order_by('-create_date')  # 생성일 기준으로 일기목록을 가져온다
    context = {'diary_list': diary_list} #내용은 일기목록
    return render(request, 'diary/diary_list.html', context) #내용을 html템플릿에 담아서 반환한다
    
# Q1. 어차피 같은 내용인데 변수가 왜 다를까?
# model에서의 content는 글 내용 자체 / views에서의 context는 템플릿에 전달할 "데이터박스"를 의미
# Q2. context는 왜 딕셔너리로 담을까?
# render함수는 데이터를 템플릿으로 넘길때 딕셔너리(키-값) 형태로 전달해야 템플릿을 사용할수있다.
#즉, 내용을 context라는 디렉터리에 담음 => 템플릿에서 {{diary.subject}}같은 방식으로 데이터 접근이 가능하다

def detail(request, diary_id):
    diary = Writing.objects.get(id=diary_id) #Writing 모델에서 id가 diary_id인 객체를 불러온다
    context = {'diary':diary}  
    return render(request, 'diary/diary_detail.html', context) 


#일기 검색
def diary_search(request):
    keyword = request.GET.get("keyword", "")  # GET방식으로 들어온 검색어 가져오기, 검색어 없으면 ""으로 대체 
    diary_list = Writing.objects.all()  # 기본적으로 전체 리스트 가져오기

    if keyword:  # 검색어가 있으면 필터링, if문이 조건을 만족하지 않아도 diarys = Writing.objects.all() 값은 항상 존재함
        diary_list = diary_list.filter(
            Q(subject__icontains=keyword) | #icontains=>키워드가 포함된
            Q(content__icontains=keyword)
        )

    context = {'diary_list': diary_list, 'keyword': keyword}  #템플릿에 전달할 데이터는 일기와 검색어
    return render(request, "diary/diary_list.html", context) # render는 템플릿에 데이터를 넘길때 딕셔너리 형태를 원함.


#일기 생성
@login_required(login_url='common:login')
def diary_create(request):
    
    if request.method =='POST': #불러오는 방식이라면
        form = WritingForm(request.POST, request.FILES) #폼은 글쓰기폼(post요청)
        
        
        if form.is_valid():      
            diary = form.save(commit=False)  #임시저장으로 diary객체 값을 입력받는다.
            diary.author = request.user #author 속성에 로그인 게정 저장
            diary.create_date = timezone.now() #실제 저장을 위해 작성일시 설정
            diary.save()                       #데이터 실제 저장            
            return redirect('diary:index')     #일기 목록 화면으로 돌아감
        
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
        form = WritingForm(request.POST, request.FILES, instance=diary) #수정 기능에서 request.FILES를 전달하지 않으면 이미지가 저장되지 않음
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