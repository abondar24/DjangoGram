from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin,name='signin'),
    path('logout', views.signin, name='logout'),
    path('settings',views.settings,name='settings'),
    path('upload',views.upload,name='upload'),
    path('like-post', views.like_post, name='like-post'),
    path('delete-post',views.delete_post, name='delete-post'),
    path('edit-caption', views.edit_caption, name='edit-caption'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('add-comment',views.add_comment, name='add-comment'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),

]
