from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment

@receiver(post_save, sender=Assignment, dispatch_uid="create_new_assignment")
def create_progress(sender, instance, **kwargs):
    lesson_progresses = instance.create_lesson_progress()
    exercise_progresses = instance.create_exercises_progress()
    for i in lesson_progresses:
        i.save()
    for i in exercise_progresses:
        i.save()
