from django.shortcuts import render,get_object_or_404, redirect
from .models import Post
from django.db.models import Q

# -- 메인페이지 --#
def index(request):
    return render(request, 'blog/index.html')

# -- 게시글 리스트  --#
def post_list(request):
    posts = Post.object.order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts':posts})


# -- 게시글 작성하기  --#
def post_create(request):
    if request.method == 'Post':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        Post.objects.create(title=title, content=content, category=category)
        return redirect('blog:post_list')
    return render(request, 'blog/post_form.html')

# -- 게시글 상세보기  --#
def post_detail(request, pk):
    post = get_object_or_404(Post, pk)
    return render(request, 'blog/post_detail.html',{'post':post})


# -- 게시글 수정하기 --#
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.category = request.POST['category']
        post.save()
        return redirect('blog:post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'post':post})



# -- 게시글 삭제하기 --# 
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method =='POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# -- 게시글 검색 --# 
def post_search(request, tag):
    order = request.GET.get('order', 'desc')
    posts = Post.objects.filter(
        Q(title__icontains=tag) | Q(category__icontains=tag)
    ).order_by('-created_at' if order == 'desc' else 'created_at')
    return render(request, 'blog/search_results.html', {'posts':posts, 'tag': tag, 'order':order})



