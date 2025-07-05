from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q, F
from .models import Post, Profile, Comment

# -- 메인페이지 --#
def index(request):
    return render(request, 'blog/index.html')

# -- 회원가입 --#
def register(request):
    if request.method == 'POST':
        user_id = request.POST['id']
        password = request.POST['password']

        # 사용자 중복 확인
        if User.objects.filter(username=user_id).exists():
            messages.error(request, '이미 존재하는 사용자명입니다.')
            return render(request, 'blog/register.html')

        # 사용자 생성
        user = User.objects.create_user(username=user_id, password=password)
        messages.success(request, '회원가입이 완료되었습니다.')
        return redirect('login')
    return render(request, 'blog/register.html')

# -- 로그인 --#
def login_view(request):
    if request.method == 'POST':
        user_id = request.POST['id']
        password = request.POST['password']

        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    return render(request, 'blog/login.html')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호가 변경되었습니다.')
            return redirect('profile_view')
        else:
            messages.error(request, '비밀번호 변경에 실패했습니다.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'blog/password_change.html', {'form':form})

# -- 로그아웃 --#
def logout_view(request):
    logout(request)
    return redirect('index')

#--프로필--#
@login_required
def profile_view(request):
    profile, created= Profile.objects.get_or_create(user=request.user)
    return render(request, 'blog/profile.html', {'profile': profile})


#--프로필 수정하기--#
@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method =='POST':
        profile.nickname = request.POST.get('nickname', '')
        profile.bio = request.POST.get('bio', '')

        if 'profile_image' in request.FILES:
            profile.profile_image= request.FILES['profile_image']

        profile.save()
        messages.success(request, '프로필이 수정되었습니다.')
        return redirect('profile_view')
    
    return render(request, 'blog/profile_edit.html', {'profile': profile})



# -- 게시글 리스트 --#
def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

# -- 게시글 작성 (로그인 사용자만 가능) --#
@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        image = request.FILES.get('image') #이미지 추가 

        Post.objects.create(
            title=title,
            content=content,
            category=category,
            author=request.user,
            image=image
        )
        messages.success(request, '게시글이 작성되었습니다.')
        return redirect('post_list')

    return render(request, 'blog/post_form.html')

# -- 게시글 상세보기 --#
def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)


        # 조회수 기능 추가 #
        post.views = F('views') +1
        post.save(update_fields=['views'])

        '''최신 데이터로 새로고침'''
        post.refresh_from_db() 

        # 댓글 가져오기 
        comments = Comment.objects.filter(post=post, parent=None).order_by('-created_at')
        
        return render(request, 'blog/post_detail.html', {
            'post': post,
            'comments' : comments
        })
    except Http404:
        return render(request, 'blog/not_found.html')

# -- 게시글 수정 (작성자만 가능) --#
@login_required
def post_edit(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            messages.error(request, '사용자가 작성한 게시물이 아닙니다.')
            return redirect('post_detail', pk=pk)

        if request.method == 'POST':
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.category = request.POST['category']
            

            if 'image' in request.FILES:
                post.image = request.FILES['image']

            post.save()
            messages.success(request, '게시글이 수정되었습니다.')
            return redirect('post_detail', pk=pk)

        return render(request, 'blog/post_form.html', {'post': post})
    except Http404:
        return render(request, 'blog/not_found.html')

# -- 게시글 삭제 (작성자만 가능) --#
@login_required
def post_delete(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            messages.error(request, '사용자가 작성한 게시물이 아닙니다.')
            return redirect('post_detail', pk=pk)

        post.delete()
        messages.success(request, '게시물이 삭제되었습니다.')
        return redirect('post_list')
    except Http404:
        return render(request, 'blog/not_found.html')

# -- 게시글 검색 --#
def post_search(request, tag):
    posts = Post.objects.filter(
        Q(title__icontains=tag) |
        Q(content__icontains=tag) |
        Q(category__icontains=tag)
    ).order_by('-created_at')

    return render(request, 'blog/post_search.html', {
        'posts': posts,
        'search_tag': tag
    })


#--댓글 작성 --#
@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        if content:
            comment = Comment.objects.create(
                post=post,
                author = request.user,
                content = content, 
                parent_id = parent_id if parent_id else None
            )
            messages.success(request, '댓글이 작성되었습니다.')
    return redirect('post_detail', pk=post_pk)

#--댓글 수정 --#
@login_required
def comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.author != request.user:
        messages.error(request, '권한이 없습니다.')
        return redirect(*'post_detail', pk=comment.post.pk)
    
    if request.mothod =='POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
            messages.success(request, '댓글이 수정되었습니다.')

    return redirect('post_detail', pk=comment.post.pk)

#--댓글 삭제 --#
@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk = comment_pk)

    if comment.authoer != request.user:
        messages.error(request, '권한이 없습니다.')
        return redirect('post_detail', pk=comment.post.pk)
    
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('post_detail', pk=post_pk)

