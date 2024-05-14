from django.urls import path
from  . import views


app_name='accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='profile_detail'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('following/<int:user_id>', views.userfollowingView.as_view(), name='following_page'),
    path('unfollowing/<int:user_id>', views.userunfollowingView.as_view(), name='unfollowing_page'),
    path('reset/', views.userpasswordresetView.as_view(), name='pass_reset'),
    path('reset/done', views.userpasswordresetdoneview.as_view(), name='pass_reset_done'),
    path('confirm/<uidb64>/<token>', views.userpasswordresetconfirmview.as_view(), name='pass_reset_confirm'),
    path('confirm/complete', views.userpasswordresetcompleteview.as_view(), name='pass_reset_complete'),
    
]
