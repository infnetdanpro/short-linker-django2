from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/add_link/', views.add_link),
    path('profile/delete_link/<profile_username>/<int:id>/', views.delete_link),
    path('profile/<profile_username>/', views.profile, name='profile'),
    path('settings/', views.settings_view),
    path('page/<page_id>/', views.page_view),
    path('logout/', views.logout_view)
]