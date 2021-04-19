from django.urls import path
from app_post import views
from django.contrib.auth.decorators import login_required


app_name = 'post'

urlpatterns = [
    path('createPost/', login_required(views.createPost.as_view()), name='createPost'),

    path('viewPost/', views.viewPost.as_view(), name='viewPost'),

    path('viewPost/author=<author>', views.filterPost, name='filterPost'),

    path('fullPost/<int:pk>/<slug>', views.fullPost.as_view(), name='fullPost'),
    
    path('postUpdate/<int:pk>/<slug>', login_required(views.postUpdate.as_view()), name='postUpdate'),

    path('postDelete/<int:pk>/<slug>', login_required(views.postDelete.as_view()), name='postDelete'),

    path('my_post', login_required(views.my_post.as_view()), name='my_post'),

    path('publish_post/<int:pk>/<slug>', login_required(views.publish_post), name='publish_post'),

    path('all_not_publish_post', login_required(views.notPublishd), name='all_not_publish_post'),

    path('all_publish_post', login_required(views.Publishd), name='all_publish_post'),
    
    path('addComment/<int:pk>', views.addComment, name='addComment'),
]
