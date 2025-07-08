from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q, F
from .models import Post, Comment
from .forms import PostForm

import openai

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

from accounts.models import Profile


def post_list(request):
    query = request.GET.get('q', '')  # 검색어 파라미터 q
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(category__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    profile = None
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)

    context = {
        'posts': posts,
        'query': query,
        'profile': profile,
    }
    return render(request, 'blog/post_list.html', context)



@login_required
def post_create(request):
    """게시글 작성 (로그인 사용자만 가능)"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시글이 작성되었습니다.')
            return redirect('blog:post_list')
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form, 'button_text': '작성'})

def post_detail(request, pk):
    """게시글 상세보기"""
    try:
        post = get_object_or_404(Post, pk=pk)

        # 조회수 증가
        post.views = F('views') + 1
        post.save(update_fields=['views'])
        post.refresh_from_db()

        # 댓글 가져오기
        comments = Comment.objects.filter(post=post, parent=None).order_by('-created_at')
        
        return render(request, 'blog/post_detail.html', {
            'post': post,
            'comments': comments
        })
    except Http404:
        return render(request, 'blog/not_found.html')

@login_required
def post_edit(request, pk):
    """게시글 수정 (작성자만 가능)"""
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, '작성자가 아닙니다.')
        return redirect('blog:post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '게시글이 수정되었습니다.')
            return redirect('blog:post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'button_text': '수정'})

@login_required
def post_delete(request, pk):
    """게시글 삭제 (작성자만 가능)"""
    try:
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            messages.error(request, '사용자가 작성한 게시물이 아닙니다.')
            return redirect('blog:post_detail', pk=pk)

        post.delete()
        messages.success(request, '게시물이 삭제되었습니다.')
        return redirect('blog:post_list')
    except Http404:
        return render(request, 'blog/not_found.html')

def post_search(request):
    """게시글 검색"""
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        ).order_by('-created_at')

    return render(request, 'blog/post_search.html', {
        'query': query,
        'results': results,
    })




# 댓글 관련 뷰들
@login_required
def comment_create(request, post_pk):
    """댓글 작성"""
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
            )
            messages.success(request, '댓글이 작성되었습니다.')
        else:
            messages.error(request, '댓글 내용을 입력하세요.')

    return redirect('blog:post_detail', pk=post_pk)

@login_required
def comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.author != request.user:
        messages.error(request, '권한이 없습니다.')
        return redirect('blog:post_detail', pk=comment.post.pk)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            comment.content = content
            comment.save()
            messages.success(request, '댓글이 수정되었습니다.')
        else:
            messages.error(request, '댓글 내용을 입력하세요.')

    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_delete(request, comment_pk):
    """댓글 삭제"""
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.author != request.user:
        messages.error(request, '권한이 없습니다.')
        return redirect('blog:post_detail', pk=comment.post.pk)
    
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('blog:post_detail', pk=post_pk)


def post_category(request, category_name):
    """카테고리"""
    posts = Post.objects.filter(category__iexact=category_name).order_by('-created_at')
    context = {
        'posts': posts,
        'category_name': category_name,
    }
    return render(request, 'blog/post_list.html', context)



# openai.api_key = os.getenv("OPENAI_API_KEY") 

# @csrf_exempt  
# def generate_intro(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             prompt = data.get("prompt", "")
#             response = openai.ChatCompletion.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "user", "content": f"{prompt}에 어울리는 블로그 도입부를 써줘"},
#                 ],
#                 max_tokens=300,
#             )
#             result_text = response['choices'][0]['message']['content']
#             return JsonResponse({"result": result_text})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "POST 요청만 지원"}, status=405)
    

@csrf_exempt
def generate_intro(request):
    print("generate_intro 함수 호출됨")  # 함수 진입 확인

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(f"요청 데이터: {data}")  # 데이터 출력
            
            prompt = data.get("prompt", "")
            print(f"프롬프트: {prompt}")

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"{prompt}에 어울리는 블로그 도입부를 써줘"}],
                max_tokens=300,
            )
            result_text = response['choices'][0]['message']['content']
            print(f"OpenAI 응답: {result_text}")

            return JsonResponse({"result": result_text})
        except Exception as e:
            print(f"오류 발생: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        print("POST 요청 아님")
        return JsonResponse({"error": "POST 요청만 지원"}, status=405)
