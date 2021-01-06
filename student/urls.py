from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('class/<int:id>', views.class_tutorials, name='class_tutorials'),
    path('tutorial/<int:id>', views.tutorial, name='tutorial'),
    path('tutorial/<int:tutorial_id>/lesson/<int:id>', views.lesson, name='lesson'),
    path('tutorial/<int:tutorial_id>/exercise/<int:id>', views.exercise, name='exercise'),
    path('tutorial/<int:tutorial_id>/submit_exercise/<int:id>', views.submit_exercise, name='submit_exercise'),
]
