from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    """메인 환영 페이지"""
    return render(request, 'main/index.html')


def blog_home_view(request):
    """블로그 홈으로 리디렉션"""
    from blog.views import post_list
    return post_list(request)  # 리디렉션 대신 직접 호출

def about(request):
    """About 페이지"""
    return render(request, 'main/about.html')