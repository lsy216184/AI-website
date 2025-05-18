
from django import forms
from .models import Writing

class WritingForm(forms.ModelForm):  #ModelForm은 연결된 모델의 데이터를 저장할수있는 폼이다.
    class Meta:
        model = Writing #사용할 모델
        fields = ['subject',  'image']  #Writing모델에서 사용할 속성

