from . import views
from django.urls import path


urlpatterns = [
     
    path('', views.PostList.as_view(), name='home'),
  
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('<slug:slug>/delete_comment/<int:comment_id>/',views.delete_comment,name='delete_comment'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),


]
