from django.urls import path

from .views import RegisterView, LoginView, UserView, LogoutView, \
    create_post_view, take_like_view, get_post_view, post_filter

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', create_post_view, name='create'),
    path('like/', take_like_view, name='like'),
    path('post/<int:pk>', get_post_view, name='like'),
    path('post/', post_filter, name='post'),
]
