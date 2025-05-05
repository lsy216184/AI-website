from django.db import models
from django.contrib.auth.models import User


#글쓰기 모델 정의 
class Writing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200) #글자 수 제한 있는 텍스트
    content = models.TextField() #본문의 내용 /글자 수 제한 없는 텍스트
    create_date = models.DateTimeField() 
    modify_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='dairy_images/', blank=True, null=True) #이미지 첨부는 선택사항
    
    def __str__(self):
        return self.subject #제목을 반환하도록 설정
    

