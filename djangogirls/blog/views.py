from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.http.response import HttpResponse
from .models import Post
from django.utils import timezone
from .forms import PostForm 



def post_list(request):
    #print 는 콘솔에, HttpResponse는 웹페이지에 직접 출력해 주는 명령어 
    #HttpResponse는 print()구문처럼 내부에 적은 문자열을 화면에 출력
#    return HttpResponse("Post_list  준비중")
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
     #render 함수는 바로 템플릿 파일을 지정해서 사용할수 있다. 
    return render (request,'blog/post_list.html',{'posts':posts})

'''Post.object. 을 이용해서 다음 조건을 만족시키는  ORM을 사용해보세요. 
1.배포 시간이 현재 시간 이전일것
2.published_date 기준으로 내림차순'''

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    #요청방식이  POST 방식으로 전달되었는지 검증한다
    if request.method == "POST":
        #PostForm양식을 받아오되 POST방식으로 전달된 데이터를 채워넣는다.
        #이렇게 되면title, text, create_date세개의 컬럼에 자료가 채워진다. 
        #단, 아직  author, published_date 에는 자료가 채워지지 않은 상태이다. 
        form = PostForm(request.POST)
        #들어온 자료가 오라바른 자료인지, .is_valid()로 감사한다. 
        #자료가 올바른 (폼을 통해 전달된 자료)라면  is_valid()는 true 이다. 
        if form.is_valid(): 
            #나머지 2개 컬럼에 대해서도 자료를 모두 저장하기 위해서 
            #먼저 핸져 들어와있는 3개 자료에 대해서 임시저장을 한다
            #commit=False 로  save() 함수를 실행하면 임시저장상태. 
            post=form.save(commit=False)
            #author 컬럼에는 요청한 유저를 집어 넣는다
            post.author = request.user
            #published_date  컬럼에는 현재 시간을 집어 넣는다
            post.published_date = timezone.now()
            #모자란 2개 컬럼을 다 채웠기 때문에  DB에 완전 저장
            post.save()
            #자료를 다 집어 넣었다면 올린 글을 확인할 수 있도록 상세페이지로 간다
            #return redirect후 자동완성 -> django.shortcuts  선택
            #redirect 의 'post_detail'은  urls.py의 post_detail 패턴 
            return redirect('post_detail',pk=post.pk)
    else:
        #form양식을 작성할 경우에는 forms.py 내부의 자료를 form 이라는 변수에 저장받는다. 
        form =PostForm()
        #저장한 form을  render 함수를 이용해 템플릿으로 보내준다. 
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request,pk):
    #사용자가 없는 pk로 접속하는것을 방지하기 위해서 404처리. 
    post = get_object_or_404(Post, pk=pk)
    #POST  방식으로 요청받은 경우 (수정 버튼을 눌러서 요청받은 경우)
    if request.method == "POST":
        #instance는 미리 적혀있던 정보를 폼에 저장 
        form = PostForm(request.POST, instance=post)
        #미리 적혀있던 정보가 유효한 정보인지 is_valid() 검증 
        if form.is_valid():
            #수정시에도 역시 published_date와 글쓴이 확인을 해야 함 
            #그래서 임시저장을 먼저 하고  author와 publisehd_date를 다시 입력
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            #정보를 모두 넘겨받으면 다시 최종 저장 
            post.save()
            #최종저장후 Post_detail 주소로 다시 보내서 수정 결과 확인 
        
            return redirect('post_detail', pk=post.pk)
    else:
        #post가 아닌 get방식인 경우 수정 결과 반영이 아닌 수정 창만 보여줌 
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# Create your views here.
