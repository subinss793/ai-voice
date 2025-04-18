from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("",views.user_login,name='login'),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # Dashboard & Features
    path("dashboard/", views.dashboard, name="dashboard"),
    path("check_pronunciation/", views.check_pronunciation, name="check_pronunciation"),
    path("record/", views.record_audio, name="record_audio"),
    path("progress/", views.view_progress, name="progress"),
    path("translate/", views.translate_text, name="translate"),
    path('test/', views.test_view, name='test'),  # Add this!
    path('test/next_question/', views.get_question, name='next_question'),


    path('test/progress/', views.get_test_progress, name='get_test_progress'),
    path('test/progress/update/', views.update_progress, name='update_progress'),
    path('test/progress/check_answer/', views.check_answer, name='check_answer'),


    # API Endpoint for Live Progress Updates
    path("get_progress/", views.get_progress, name="get_progress"),
]
