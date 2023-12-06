# articles/urls.py
from django.urls import path
from .views import user_login, user_register, dashboard,article_detail,edit_article,delete_article,user_logout


urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('edit/<int:article_id>/', edit_article, name='edit_article'),
    path('delete/<int:article_id>/', delete_article, name='delete_article'),
    path('logout/', user_logout, name='logout'),
    path('',user_login,name="default")
    # Add other URLs as needed
]