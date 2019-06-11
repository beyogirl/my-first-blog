from django.contrib import admin
from .models import Post

#admin.site.register(모델명)을 입력할 경우 admin 페이지에서 수정 가능! 
#수석처리하면  admin 싸이트에서 post가 사라짐. 
admin.site.register(Post)
