#장고 form 양식을 사용하기 위해 forms 호출
from django import forms
#Post 모델에 자룔르 보내줄것임 
from .models import Post

#Post에 대한  form이기 때문에 이름은 PostForm
#forms.ModelForm을 괄호 사이에 집어 넣어야  form 구현 가능 
class PostForm(forms.ModelForm):

#PostForm 내부에 Meta라는 이름으로 작성할 경우
#타켓 모델은 model=모델이름 형식으로 사용자에게 입력 받을 부분은 fields =('1번컬럼','2번 컬럼'.....)형식으로 작성 할 수 있다. 
    class Meta:
        model = Post
        fields = ('title', 'text',)
