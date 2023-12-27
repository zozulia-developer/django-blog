from django.urls import path

from blog.views import (PostCreate, PostDelete, PostDetail, PostUpdate,
                        StartHereView, TagCreate, TagDelete, TagDetail,
                        TagUpdate, posts_list)

urlpatterns = [
    path('', posts_list, name="posts_list_url"),
    path('post/create/', PostCreate.as_view(), name="post_create_url"),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
    path('start-here/', StartHereView.as_view(), name='start_here_url')
]
