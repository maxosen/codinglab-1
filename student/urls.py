from django.urls import path
from . import views


urlpatterns = [
    # path for logins
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('account', views.account, name='account'),
    path('', views.home, name='home'),
    path('classes', views.my_classes, name='classes'),
    path('class/<int:id>', views.class_tutorials, name='class_tutorials'),
    path('tutorial/<int:id>', views.tutorial, name='tutorial'),
    path('tutorial/<int:assignment_id>/lesson/<int:id>', views.lesson, name='lesson'),
    path('tutorial/<int:assignment_id>/exercise/<int:id>', views.exercise, name='exercise'),
    # POST path for submitting exercises / lessons
    path('tutorial/<int:assignment_id>/submit_exercise/<int:id>', views.submit_exercise, name='submit_exercise'),
    path('tutorial/<int:assignment_id>/submit_lesson/<int:id>', views.submit_lesson, name='submit_lesson'),
    path('feedback/<int:assignment_id>/<int:id>', views.feedback, name='feedback'),
    # GET path for getting solutions
    path('get_solutions/<int:assignment_id>/<int:id>', views.get_solutions, name='get_solutions'),
    # path for instructors
    path('class/<int:class_id>/editor/<int:tutorial_id>', views.editor, name='editor'),
    path('class/<int:class_id>/tutorial_dir', views.tutorial_dir, name='tutorial_dir'),
    path('class/<int:class_id>/tutorial/<int:tutorial_id>/assignment_status', views.assigned_students, name='assignment_status'),
    # path for instructors: ANALYTICS
    path('class/<int:class_id>/tutorial_statistics/<int:tutorial_id>', views.tutorial_statistics, name='tutorial_statistics'),
    # path for instructors that require POST
    path('assign/<int:class_id>/<int:tutorial_id>', views.assign, name='assign'),
]
