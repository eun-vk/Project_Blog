from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('write/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('search/', views.post_search, name='post_search'),
    
    # 댓글 관련 URL
    path('comment/create/<int:post_pk>/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),

    path('generate/', views.generate_intro, name='generate_intro'),

    path('category/<str:category_name>/', views.post_category, name='post_category'),
]