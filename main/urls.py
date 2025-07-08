from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog_home_view, name='blog_home'),
    path('about/', views.about, name='about'),
]