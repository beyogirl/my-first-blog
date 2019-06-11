from django.db import models
from django.utils import timezone


class Post(models.Model):
    #author는 auth.User 모델과 연동, auth.User는 admin 계정을 위해 장고에서 자동으로 생성하는 모델명. 
    #createsuperuser 명령어등으로 생성한 계정을 저장한다
    author =models.ForeignKey('auth.User',on_delete=models.CASCADE)
    #제목에 나타내는 부분.charfield는 글자수가 제한된 필드이며 최대 글자수 200글자 
    #max_length 는 소문자여야 함. 만일 대분자로 자동 변경되면 Esc 키를 눌러주면 됨 
    title =models.CharField(max_length=200)
    #본문을 나태내는 부분,  textfield는 굴자수 제한이 없음을 의미함 
    text=models.TextField()
    # 작성시간을 나타내는 부분, timezone 은 django.utils 의 것을 사용함
    #글 최초 작성 시간을 나타내는 부분.  default 는 미 입력시 자동 기입할 자료 
    created_date=models.DateTimeField(default=timezone.now)
    #최종 수정시간을 나타내는 부분. 
    #blank는 공백으로 둬도 되는지,  null 은 입력을 안 해도 되는지를 나타냄 
    published_date=models.DateTimeField(blank=True,null=True)
    
    #글을 수정할 떄 실행할 함수, 사용자가 날짜를 가입하는게 아니라 수정시 매번 호출되는 최종 수정시각을 갱신한다. 
    def publish(self):
        self.published_date=timezone.now()
         #바꾼 시간은 저장까지 해줘야  DB에 반영됨  
        self.save()
     
     # admin 페이지에서  post 모델에 관련된 내용 조회시 글 제목이 나옴.    
    def __str__(self):
        return self.title

    
    
# Create your models here.
