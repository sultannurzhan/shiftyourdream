from django.urls import path
from . import views

urlpatterns = [
    path('', views.Default.as_view(), name="default"),
    path('home', views.Home.as_view(), name="home"),
    path('login/', views.LoginUser.as_view(), name="login"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('create_note/', views.create_note, name='create_note'),
    path('delete-note/<int:pk>/', views.delete_note, name='delete_note'),
    path('edit_note/<int:pk>/', views.edit_note, name='edit_note'),
    path('get_note_details/<int:note_id>/', views.get_note_details, name='get_note_details'),

    path('dreams/', views.Dreams.as_view(), name="dreams"),
    
    path('about/', views.About.as_view(), name="about"),
    path('dashboard/', views.Dashboard.as_view(), name="dashboard")
]