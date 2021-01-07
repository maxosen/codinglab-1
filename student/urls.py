from django.urls import path
from . import views


urlpatterns = [
    path('class/<int:id>', views.class_tutorials, name='class_tutorials'),
    # TODO: prefix these with CLASS Urls later (refer instructor: <int:class_id>)
    path('tutorial/<int:id>', views.tutorial, name='tutorial'),
    path('tutorial/<int:tutorial_id>/lesson/<int:id>', views.lesson, name='lesson'),
    path('tutorial/<int:tutorial_id>/exercise/<int:id>', views.exercise, name='exercise'),
    path('tutorial/<int:tutorial_id>/submit_exercise/<int:id>', views.submit_exercise, name='submit_exercise'),
    # path for instructors
    path('class/<int:class_id>/editor/<int:tutorial_id>/', views.editor, name='editor'),
    path('class/<int:class_id>/tutorial_dir', views.tutorial_dir, name='tutorial_dir'),
    # path for logins
    path('login/', views.login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
