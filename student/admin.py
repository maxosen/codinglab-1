from django.contrib import admin
from .models import *

admin.site.register(InstructorProfile)
admin.site.register(Class)
admin.site.register(StudentProfile)
admin.site.register(Tutorial)
admin.site.register(Assignment)
admin.site.register(Lesson)
admin.site.register(Exercise)
admin.site.register(LessonProgress)
admin.site.register(ExerciseProgress)