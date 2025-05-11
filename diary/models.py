from django.db import models
from django.contrib.auth.models import User
import os


# 사용자별 디렉토리에 이미지 저장
# =>django의 ImageField나 ImageField에서 upload_to인자에 문자열을 넣으면 지정된 경로에 저장된다.
# =>함수를 넣으면 동적으로 경로를 생성할수있다.이때 함수는 주로 models.py에 정의한다.
# 이유=>upload_to에 전달되는 함수는 모델 인스턴스(self)에 접근 할수있어야 함으로 모델가 가까운 위치에 두는것이 자연스럽다(종속성 최소화, 유지수 편의성)
def user_directory_path(instance, filename):
    # → /media/diary_images/username/파일명 형식으로 저장됨
    return f'diary_images/{instance.author.username}/{filename}'

#글쓰기 모델 정의 
class Writing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200) #글자 수 제한 있는 텍스트
    content = models.TextField() #본문의 내용 /글자 수 제한 없는 텍스트
    create_date = models.DateTimeField() 
    modify_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True) #이미지 첨부는 선택사항
    def __str__(self):
        return self.subject #제목을 반환하도록 설정
    

