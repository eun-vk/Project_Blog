from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from .models import Post

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

# -- 로그아웃 --#
def logout_view(request):
    logout(request)
    return redirect('index')

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

        Post.objects.create(
            title=title,
            content=content,
            category=category,
            author=request.user
        )
        return redirect('post_list')

    return render(request, 'blog/post_form.html')

# -- 게시글 상세보기 --#
def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})
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
