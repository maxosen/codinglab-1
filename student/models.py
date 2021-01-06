from django.db import models
from django.conf import settings


class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    # TODO: specify a default photo
    photo = models.ImageField(upload_to='profile')



class Class(models.Model):
    '''
    Class is a collection of students, instructors, and tutorials
    Represents a class in real-life.
    '''
    title = models.CharField(max_length=400)

    # Introduction in Markdown
    introduction = models.TextField()

    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)



class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    # TODO: specify a default photo
    photo = models.ImageField(upload_to='profile')

    class_enrolled = models.ManyToManyField(Class,
                                        related_name='enrolled_in',
                                        blank=True)


class Tutorial(models.Model):
    '''
    Tutorial is the main content on the platform.
    Created by the instructors, assigned to the students.
    '''
    title = models.CharField(max_length=400)
    created_by = models.ForeignKey(InstructorProfile,
                                on_delete=models.DO_NOTHING)
    date_created = models.DateField(auto_now_add=True)

    # Assigned to which student
    assignment = models.ManyToManyField(StudentProfile,
                                        through='Assignment',
                                        blank=True)
    tutorial_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def get_next_lesson(self, id):
        lessons = Lesson.objects.filter(tutorial=self)
        lessons_size = len(lessons)
        for i in range(lessons_size):
            if lessons[i].id == id:
                # last lesson
                if i == lessons_size - 1:
                    return None
                return lessons[i + 1]
        return None

    def get_prev_lesson(self, id):
        lessons = Exercise.objects.filter(tutorial=self)
        lessons_size = len(lessons)
        for i in range(lessons_size):
            if lessons[i].id == id:
                # last lesson
                if i == 0:
                    return None
                return lessons[i - 1]
        return None

    def get_next_exercise(self, id):
        exercises = Exercise.objects.filter(tutorial=self)
        exercises_size = len(exercises)
        for i in range(exercises_size):
            if exercises[i].id == id:
                # last lesson
                if i == exercises_size - 1:
                    return None
                return exercises[i + 1]
        return None

    def get_prev_exercise(self, id):
        exercises = Exercise.objects.filter(tutorial=self)
        exercises_size = len(exercises)
        for i in range(exercises_size):
            if exercises[i].id == id:
                # last exercise
                if i == 0:
                    return None
                return exercises[i - 1]
        return None


class Lesson(models.Model):
    '''
    Lesson is a sub-unit of Tutorial. It stores a read-only content,
    with an optional quick exercise.
    '''

    # Parent tutorial
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)

    title = models.CharField(max_length=400)

    # The order of this exercise in the tutorial
    order = models.IntegerField()

    # The content in Markdown
    markdown = models.TextField()

    # Optional question and answer for quick exercise
    exercise_question = models.TextField(blank=True)
    exercise_ans = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Tutorial.ID:<{self.id}>({self.title})Order:{self.order}'


class Exercise(models.Model):
    '''
    Exercise is a sub-unit of Tutorial. It stores the programming exercise.
    '''

    # Parent Tutorial    
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)

    # Title of this exercise
    title = models.CharField(max_length=400)

    # The order of this exercise in the tutorial
    order = models.IntegerField()

    # The question in Markdown
    question = models.TextField()

    # Testcases in JSON
    testcases = models.TextField()

    # Date Exercise is created
    date_created = models.DateField(auto_now_add=True)


class Assignment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE,
                                related_name="tutorial")
    progress = models.IntegerField(default=0)
    is_optional = models.BooleanField(default=False)

    @classmethod
    def create(cls, student, tutorial):
        assignment = cls(student=student, tutorial=tutorial)
        return assignment


    def create_exercises_progress(self):
        exercises = Exercise.objects.filter(tutorial=self.tutorial)
        progresses = [ExerciseProgress(exercise=exercise, assignment=self)
                    for exercise in exercises]
        return progresses


    def create_lessons_progress(self):
        lessons = Lesson.objects.filter(tutorial=self.tutorial)
        progresses = [LessonProgress(lesson=lesson, assignment=self)
                    for lesson in lessons]
        return progresses


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    progress = models.BooleanField(default=False)


class ExerciseProgress(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    progress = models.BooleanField(default=False)