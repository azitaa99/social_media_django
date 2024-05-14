from django.urls import path
from  . import views


app_name='home'

urlpatterns = [
    path('', views.mainpageView.as_view(), name='main_page'),
    path('createpost/', views.CreatpostView.as_view(), name='create_post'),
    path('postdetail/<int:post_id>', views.PostdetailView.as_view(), name='post_detail'),
    path('updatepost/<int:post_id>', views.updatepostView.as_view(), name='post_update'),
    path('reply/<int:post_id>/<int:comment_id>', views.replycommentView.as_view(), name='reply_page'),
    path('deletepost/<int:post_id>', views.deletpostView.as_view(), name='delete_post'),
    path('like/<int:post_id>/', views.postlikeView.as_view(), name='post_like')
    
]
