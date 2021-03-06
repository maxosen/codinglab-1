from django.db import models
from django.conf import settings

class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
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
    phone = models.CharField(max_length=50)
    # TODO: specify a default photo
    photo = models.ImageField(upload_to='profile')
    class_enrolled = models.ManyToManyField(Class,
                                        related_name='enrolled_in',
                                        blank=True)
    def __str__(self):
        return f'{self.user.id}: {self.user.username}'


class Tutorial(models.Model):
    '''
    Tutorial is the main content on the platform.
    Created by the instructors, assigned to the students.
    '''
    LESSON = 'LS'
    EXERCISE = 'EX'
    TUTORIAL_TYPE = [
        (LESSON, 'Lesson'),
        (EXERCISE, 'Exercise')
    ]

    title = models.CharField(max_length=400)
    created_by = models.ForeignKey(InstructorProfile,
                                on_delete=models.DO_NOTHING)
    tutorial_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    tutorial_type = models.CharField(max_length=2, choices=TUTORIAL_TYPE)

    # Assigned to which student
    assignment = models.ManyToManyField(StudentProfile,
                                        through='Assignment',
                                        blank=True)
    def __str__(self):
        return f'{self.id}: {self.title}'

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
        return f'ID:{self.id}. Title: {self.title}'


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

    def __str__(self) -> str:
        return f'{self.id}: {self.title}'


class Assignment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE,
                                related_name="tutorial")
    progress = models.IntegerField(default=0)
    is_optional = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}: {self.tutorial.title} to {self.student.user.username}'
    # keep in mind this has a side effect
    # another possible solution might be to use a SAVE signal receiver
    @classmethod
    def create(cls, student, tutorial):
        assignment = cls(student=student, tutorial=tutorial)
        assignment.save()
        if tutorial.tutorial_type == Tutorial.LESSON:
            lessons = Lesson.objects.filter(tutorial=tutorial)
            for lesson in lessons:
                progress = LessonProgress(lesson=lesson, assignment=assignment)
                progress.save()
        else:
            exercises = Exercise.objects.filter(tutorial=tutorial)
            for exercise in exercises:
                progress = ExerciseProgress(exercise=exercise, assignment=assignment)
                progress.save()
        return assignment

    def has_any_lesson(self, lessons):
        for lesson in lessons:
            if self.has_lesson(lesson):
                return True
        return False

    def has_any_exercise(self, exercises):
        for exercise in exercises:
            if self.has_exercise(exercise):
                return True
        False
    
    def has_lesson(self, lesson):
        lessons = Lesson.objects.filter(tutorial=self.tutorial)
        for l in lessons:
            if l == lesson:
                return True
        return False
    
    def has_exercise(self, exercise):
        exercises = Exercise.objects.filter(tutorial=self.tutorial)
        for e in exercises:
            if e == exercise:
                return True
        return False

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
    
    def __str__(self):
        return f'{self.tutorial.title}: {self.student.user.username}'


class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}: {self.lesson.title} by {self.assignment.student.user.username}: {self.completed}'
    


class ExerciseProgress(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}: {self.exercise.title} by {self.assignment.student.user.username}: {self.completed}'


class ExerciseSolution(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    solution = models.TextField()

    def __str__(self):
        return f'{self.id}: {self.exercise.title} by {self.assignment.student.user.username}'



class LessonFeedback(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.id}: {self.lesson.title} by {self.assignment.student.user.username}'



class ExerciseFeedback(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.id}: {self.lesson.title} by {self.assignment.student.user.username}'

    

class LoginEvent(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.student.user.username} on {self.time}'



class ExerciseSubmissionEvent(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    duration = models.FloatField()
    result = models.BooleanField()

    def __str__(self):
        return f'{self.id}: {self.assignment.student.user.username} on {self.exercise.title}'



class LessonSubmissionEvent(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    duration = models.FloatField()
    result = models.BooleanField()

    def __str__(self):
        return f'{self.id}: {self.assignment.student.user.username} on {self.lesson.title}'
