from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name ='register'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('blog/', views.post_list, name='post_list'),
    path('blog/write/', views.post_create, name='post_create'),
    path('blog/<int:pk>/', views.post_detail, name='post_detail'),
    path('blog/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('blog/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('blog/search/<str:tag>/', views.post_search, name='post_search'),


#--프로필 관련 url--#
    path('profile/', views.profile_view, name = 'profile_view'),
    path('profile/edit', views.profile_edit, name = 'profile_edit'),
    path('password-change/', views.password_change, name = 'password_change'),
    

#--댓글 관련 url--#
    path('comment/create/<int:post_pk>/', views.comment_create, name = 'comment_create'),
    path('comment/edit/<int:post_pk>/', views.comment_edit, name = 'comment_edit'),
    path('comment/delete/<int:post_pk>/', views.comment_delete, name = 'comment_delete'),



]