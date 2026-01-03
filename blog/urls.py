from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
