 # 프로젝트 주제
**Django 기반의 안정적이고 확장 가능한 블로그 시스템 구축**


 # 프로젝트 개요
**이 프로젝트는 Django 프레임워크를 활용한 블로그 시스템 개발입니다. 사용자 인증과 권한 관리를 기본으로 하며, 게시글 작성, 댓글 작성 기능을 포함한 전형적인 블로그 서비스를 구현합니다.**   
**또한, 사용자 프로필 확장과 관리자 활동 로그 기능을 통해 관리 및 사용자 경험을 강화합니다. 데이터베이스 설계는 ERD를 기반으로 하여 사용자, 게시글, 댓글, 권한, 시스템 로그 간의 관계를 명확히 정의하였습니다.**

 # 프로젝트 목표
**Django 기반의 블로그 시스템을 통해 사용자 인증과 권한 관리, 게시글 및 댓글 기능을 안정적으로 구현하고, 사용자 경험과 관리 효율성을 높일 수 있는 확장 가능하고 체계적인 웹 서비스를 완성하는 것입니다.**


> # WBS 작성
![image](https://github.com/user-attachments/assets/137d969a-30ed-4e75-9e5b-88c7e4f70ef8)  

---

> # 프로젝트 구조

```
Django_BlogProject/
├── 🔐 accounts/              
│   ├── migrations/           
│   ├── static/accounts/      
│   ├── templates/accounts/   
│   ├── models.py           
│   ├── views.py             
│   ├── forms.py             
│   └── urls.py              
├── 📝 blog/                 
│   ├── migrations/          
│   ├── migrations_backup/    
│   ├── static/blog/          
│   ├── templates/blog/       
│   ├── models.py           
│   ├── views.py             
│   ├── forms.py            
│   └── urls.py             
├── 🏠 main/                 
│   ├── static/main/        
│   ├── templates/main/     
│   ├── views.py            
│   └── urls.py          
├── ⚙️ config/                
├── ⚡ fastapi_app/         
│   ├── main.py          
│   └── __init__.py         
├── 📦 media/              
├── 📦 staticfiles/      
├── 🌐 locale/               
├── 🔒 .env                
├── ⚙️ manage.py           
├── 📋 requirements.txt      
└── 🧪 test_openapi.py
```
- 이 프로젝트는 Django 기반 블로그 웹앱으로, accounts, blog, main 세 앱으로 구성되어 있습니다.  
- accounts/는 회원가입, 로그인, 프로필 관리 등 사용자 인증 기능을 담당합니다.  
- blog/는 게시글 및 댓글 CRUD, 검색, 카테고리 기능을 포함하며 핵심 콘텐츠를 처리합니다.  
- main/은 메인 페이지와 블로그 홈 진입을 담당하며 간단한 소개 페이지를 포함할 수 있습니다.  
- FastAPI 기능은 fastapi_app/에 별도로 구성되어 있으며, 정적·미디어 파일과 환경 설정도 프로젝트 루트에 정리되어 있습니다.

---

> # ERD
![ERD](https://github.com/user-attachments/assets/374b057e-7541-49f4-b50a-03e12852a809)  

- **AuthUser 테이블**  
  회원가입한 사용자의 기본 정보(아이디, 비밀번호, 이메일 등)를 저장합니다.

- **AccountsProfile**  
  사용자 프로필 정보를 확장해서 저장하는 테이블로, AuthUser 한 명과 1:1 관계입니다.  
  (예: 프로필 사진, 자기소개 등)

- **BlogPost 테이블**  
  블로그 게시글 내용을 저장하며, 게시글 작성자는 AuthUser와 연결됩니다.

- **BlogComment 테이블**  
  게시글에 달린 댓글을 저장하며, 댓글 작성자와 댓글이 달린 게시글을 참조합니다.

- **권한 관리 관련 테이블 (AuthGroup, AuthPermission 등)**  
  사용자가 어떤 권한(기능)을 가졌는지 관리합니다.  
  예를 들어, 일반 사용자와 관리자 권한 구분 등.

- **DjangoContentType**  
  권한이 어떤 모델(게시글, 댓글, 사용자 등)에 적용되는지 정보를 제공합니다.

- **DjangoAdminLog**  
  관리자 활동 내역를 기록하는 테이블입니다.
  
---

> # WireFrame
![WireFrame](https://github.com/user-attachments/assets/82659402-433c-46e6-87d9-7146e7f5df1a)

---

> # URL 패턴 정리

| 앱 이름     | URL 패턴                            | View 함수           | Name               |
|------------|--------------------------------------|---------------------|--------------------|
| accounts   | register/                            | register            | register           |
| accounts   | login/                               | login_view          | login              |
| accounts   | logout/                              | logout_view         | logout             |
| accounts   | profile/                             | profile_view        | profile_view       |
| accounts   | profile/edit/                        | profile_edit        | profile_edit       |
| accounts   | password-change/                     | password_change     | password_change    |
|------------|--------------------------------------|---------------------|--------------------|
| blog       |                         | post_list           | post_list          |
| blog       | write/                               | post_create         | post_create        |
| blog       | <int:pk>/                            | post_detail         | post_detail        |
| blog       | edit/<int:pk>/                       | post_edit           | post_edit          |
| blog       | delete/<int:pk>/                     | post_delete         | post_delete        |
| blog       | search/                              | post_search         | post_search        |
| blog       | comment/create/<int:post_pk>/        | comment_create      | comment_create     |
| blog       | comment/<int:comment_pk>/edit/       | comment_edit        | comment_edit       |
| blog       | comment/delete/<int:comment_pk>/     | comment_delete      | comment_delete     |
| blog       | generate/                            | generate_intro      | generate_intro     |
| blog       | category/<str:category_name>/        | post_category       | post_category      |
|------------|--------------------------------------|---------------------|--------------------|
| main       |                          | index               | index              |
| main       | blog/                                | blog_home_view      | blog_home          |


- 이 프로젝트는 accounts, blog, main 세 개의 앱으로 구성되어 있으며, 각 앱의 URL은 기능별로 나눠 관리하였습니다.   
- accounts 앱은 회원가입(register/), 로그인(login/), 로그아웃(logout/), 프로필 조회 및 수정, 비밀번호 변경 등 사용자 인증 관련 경로를 포함합니다.  
- blog 앱은 글 목록, 글 작성·수정·삭제, 상세 보기 등 게시글 관리 기능과 댓글 작성·수정·삭제, 검색, 카테고리별 조회, 자동 소개글 생성 등 다양한 블로그 기능의 URL을 포함합니다.  
- main 앱은 홈페이지(index)와 블로그로 진입하는 경로(blog/)를 제공합니다.  

---

# ⚠️ 오류가 많이 발생했던 부분

| 기능 영역             | 자주 발생하는 오류/문제 | 원인 또는 실수 | 해결 방법 요약 | 실제 오류 메시지 / 코드 예시 |
|----------------------|--------------------------|----------------|----------------|-------------------------------|
| URL 연결 및 템플릿 링크 | `NoReverseMatch`, 404 오류 | `{% url %}`에 name 틀림, 인자 빠짐 | `urls.py`의 name과 인자 정확히 확인 | ❌ 오류: `NoReverseMatch at /blog/`<br>✅ 수정 전: `{% url 'post_detail' %}`<br>✅ 수정 후: `{% url 'blog:post_detail' post.pk %}` |
| 폼 처리 (POST 요청) | 403 Forbidden, 저장 안 됨 | `csrf_token` 없음, `form.is_valid()` 누락 | `{% csrf_token %}` 추가, 유효성 검사 필수 | ❌ 오류: `403 Forbidden (CSRF token missing)`<br>✅ HTML: `<form method="post">{% csrf_token %}`<br>✅ Python: `if form.is_valid(): form.save()` |
| 댓글 수정/삭제 권한 | 다른 사용자가 수정/삭제 가능 | 작성자 확인 조건 없음 | `request.user == comment.author` 체크 | ❌ 문제: 누구나 댓글 수정 가능<br>✅ 예: `if request.user != comment.author: return HttpResponseForbidden()` |
| 이미지/파일 업로드 | 업로드는 되지만 화면에 출력 안 됨 | 미디어 설정 누락 | `MEDIA_URL`, `MEDIA_ROOT` 설정 및 `urls.py`에 static 처리 | ✅ `settings.py`<br>`MEDIA_URL = '/media/'`<br>`MEDIA_ROOT = BASE_DIR / 'media'`<br>✅ `urls.py`<br>`+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` |
| 검색 / 카테고리 필터 | 빈 페이지, 없는 값 접근 시 오류 | `.get()`으로 찾다가 없는 값 발생 | `.exists()`로 체크, 없으면 404 반환 | ❌ 오류: `DoesNotExist at /category/foo`<br>✅ 예: `get_object_or_404(Post, category__name=name)` |
| 로그인 기능 | 로그인 안 되고 무한 리디렉트 발생 | 로그인 성공 후 `next` URL이 다시 login 페이지 | `LOGIN_REDIRECT_URL` 설정, login 뷰에서 redirect 로직 확인 | ❌ 현상: 로그인 후 다시 로그인 페이지로 계속 이동<br>✅ `settings.py`: `LOGIN_REDIRECT_URL = '/'`<br>✅ login 뷰에서 `return redirect('main:index')` 등으로 수정 |

---

# 느낀점
이번 프로젝트를 진행하면서 기능을 구현하는 것도 중요했지만, 그 기능들을 화면에 제대로 보여주는 작업이 가장 어렵고 힘들었다는 점을 크게 느꼈습니다. 처음에는 HTML과 CSS를 분리해서 관리하려고 노력했지만, 시간이 지나면서 구조가 복잡해지고 몇몇 파일은 HTML과 CSS가 섞인 상태로 작업하게 되었습니다. 정적 파일을 다루는 부분도 익숙하지 않아 시간이 많이 소요되었고, 이 과정에서 프론트엔드 개발자와 협업하는 것이 얼마나 중요한지 깨달았습니다.

API를 연결하는 과정도 쉽지 않았습니다. 한 번은 API가 정상적으로 연결되는 듯했으나, 이후에는 “응답을 받아오지 못했습니다”라는 메시지가 반복해서 나왔습니다. 문제를 파악하기 위해 뷰 함수에서 print 문을 사용해 어디서 문제가 생기는지 직접 확인해보기도 했지만, API 자체의 문제일 가능성도 있었습니다. 최종적으로는 완벽하게 연동하지 못했지만, 브라우저 개발자 도구(F12)를 통해 오류 메시지를 직접 보고 분석하는 방법을 배우면서, 오류를 읽고 이해하는 능력을 키울 수 있었습니다. 수업 시간에 한 번 배웠던 내용을 직접 경험해보니 머리에 훨씬 더 잘 남았습니다.

또 한 가지 어려웠던 점은 로그인 후 무한 루프에 빠지는 문제였습니다. 보통 대댓글 기능에서 발생하는 문제라고 알려져 있지만, 저는 앱을 세 개로 분리하는 과정에서 로그인 후 블로그 홈으로 넘어가지 않고 계속 로그인 페이지로 돌아가는 현상을 겪었습니다. 이 문제는 로그인 후 리디렉션 경로가 자기 자신을 참조하는 설정 때문이었고, 이를 LOGIN_REDIRECT_URL 설정을 확인하고 수정하면서 해결할 수 있었습니다.

이번 프로젝트에서 가장 뿌듯했던 점은, 오류가 발생했을 때 포기하지 않고 직접 오류 메시지를 읽고 원인을 찾기 위해 노력했다는 점입니다. 콘솔과 개발자 도구를 활용해 문제를 하나씩 해결하는 경험을 하면서 개발자로서 성장할 수 있는 값진 시간이 되었습니다. 앞으로도 이런 경험들을 바탕으로 더 나은 코드를 작성하고 문제 해결 능력을 키워 나가고 싶습니다.
