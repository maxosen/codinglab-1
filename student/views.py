from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import TutorialForm, LessonForm, LoginForm, RegistrationForm, StudentProfileForm, InstructorProfileForm, ExerciseForm
from .models import Tutorial, Lesson, Exercise, StudentProfile, InstructorProfile, Class
from .utils import run_testcases

import json

# Create your views here.
# @login_required
def class_tutorials(request, id):
    tutorials = Tutorial.objects.filter(tutorial_class__id=id)
    context = {
        'tutorials': tutorials,
    }
    return render(request, 'class.html', context)


def tutorial(request, id):
    tutorial = Tutorial.objects.get(id=id)
    lessons = Lesson.objects.filter(tutorial__id=id).order_by('order')
    exercises = Exercise.objects.filter(tutorial__id=id).order_by('order')

    context = {
        'tutorial': tutorial,
        'lessons': lessons,
        'exercises': exercises,
    }
    return render(request, 'tutorial.html', context)


def lesson(request, id, tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    lesson = Lesson.objects.get(id=id)
    next_lesson = tutorial.get_next_lesson(id=lesson.id)
    prev_lesson = tutorial.get_prev_lesson(id=lesson.id)

    context = {
        'lesson': lesson,
        'next': next_lesson,
        'prev': prev_lesson
    }
    return render(request, 'lesson.html', context)


def exercise(request, id, tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    exercise = Exercise.objects.get(id=id)
    testcases = json.loads(exercise.testcases)
    context = {
        'exercise': exercise,
        'testcases': testcases
    }
    return render(request, 'exercise.html', context)

@require_POST
def submit_exercise(request, id, tutorial_id):
    data = json.loads(request.body.decode("utf-8"))
    code = data['code']
    testcases = Exercise.objects.get(id=id).testcases
    results = run_testcases(code, testcases)
    return JsonResponse(results, safe=False)

'''
INSTRUCTOR VIEWS
'''

def editor(request, class_id, tutorial_id):
    '''
    2. Display list of lessons or exercises at the side
    3. 
    3. 
    '''
    '''
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            # TODO: how to get the tutorial (using hidden form field or URL?)
            # TODO: configure the tutorial creation
            new_lesson.tutorial = tutorial
            new_lesson.save()
            return HttpResponse('Successfully created')
    else:
        form = LessonForm()
    '''
    tutorial = Tutorial.objects.get(id=tutorial_id)
    if request.method == 'POST':
        if request.POST['tutorial_type'] == Tutorial.LESSON:
            # New lesson
            lesson_form = LessonForm(request.POST)
            if request.POST.get('content_id', None) == None:
                new_lesson = lesson_form.save(commit=False)
                new_lesson.tutorial = tutorial
                new_lesson.save()
            # Update old lesson
            else:
                if lesson_form.is_valid():
                    lesson = Lesson.objects.get(id=request.POST.get('content_id'))
                    cd = lesson_form.cleaned_data
                    lesson.title = cd['title']
                    lesson.order = cd['order']
                    lesson.markdown = cd['markdown']
                    lesson.exercise_question = cd['exercise_question']
                    lesson.exercise_ans = cd['exercise_ans']
                    lesson.save()

        else:
            # New exercise
            exercise_form = ExerciseForm(request.POST)
            if request.POST.get('content_id', None) == None:
                new_exercise = exercise_form.save(commit=False)
                new_exercise.tutorial = tutorial
                new_exercise.save()
            else: # update old exercise
                if exercise_form.is_valid():
                    exercise = Exercise.objects.get(id=request.POST.get('content_id'))
                    cd = exercise_form.cleaned_data
                    exercise.title = cd['title']
                    exercise.order = cd['order']
                    exercise.question = cd['question']
                    exercise.testcases = cd['testcases']
                    exercise.save()

    if tutorial.tutorial_type == Tutorial.LESSON:
        form = LessonForm()
        materials = Lesson.objects.filter(tutorial=tutorial)
        if request.GET.get('content_id', None) != None:
            lesson = get_object_or_404(Lesson, id=request.GET['content_id'])
            data = {
                'title': lesson.title,
                'order': lesson.order,
                'markdown': lesson.markdown,
                'exercise_question': lesson.exercise_question,
                'exercise_ans': lesson.exercise_ans
            }
            form = LessonForm(initial=data)
    else:
        form = ExerciseForm()
        materials = Exercise.objects.filter(tutorial=tutorial)
        if request.GET.get('content_id', None) != None:
            exercise = get_object_or_404(Exercise, id=request.GET['content_id'])
            data = {
                'title': exercise.title,
                'order': exercise.order,
                'question': exercise.question,
                'testcases': exercise.testcases,
            }
            form = ExerciseForm(initial=data)

    context = {
        'form': form,
        'materials': materials,
    }
    return render(request, 'editor.html', context)


def tutorial_dir(request, class_id):
    '''
    * retrieve all tutorial objects from database
    * display as cards
    * allows instructor to assign tutorials to students by clicking \
    on cards.
        1. instructor click on assign
        2. popup a list of students
            * CONTENT:
            * students already assigned with this tutorial
                * how? filter all assignments with this tutorial
                * retrieve their student ids (using array comprehension?)
                * match with all students
                * matched students appear as ady assigneed
            * students not assigned appear as checkboxes
            * a shortcut button to assign to all students not assigned
    * Show button to Editor view as 'Create tutorial'
    '''
    if request.method == 'POST':
        tutorial_form = TutorialForm(request.POST)
        new_tutorial = tutorial_form.save(commit=False)
        new_tutorial.created_by = InstructorProfile.objects.get(user=request.user)
        new_tutorial.tutorial_class = Class.objects.get(id=class_id)
        new_tutorial.save()
        return redirect(f'/class/{class_id}/editor/{new_tutorial.id}', permanent=True)

    the_class = get_object_or_404(Class, id=class_id)
    tutorials = Tutorial.objects.filter(tutorial_class__id=class_id)
    tutorial_form = TutorialForm()

    context = {
        'tutorials': tutorials,
        'tutorial_form': tutorial_form
    }
    return render(request, 'tutorial_dir.html', context)


def assigned_students(request, class_id, assignment_id, tutorial_id):
    
    return JsonResponse()


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    # get user profile
                    role_matching = True
                    try:
                        role = cd['role']
                        if role == 'S':
                            StudentProfile.objects.get(user=user)
                        else:
                            InstructorProfile.objects.get(user=user)
                    except:
                        role_matching = False

                    if role_matching:
                        login(request, user)
                        return render(request, 'class/2')
                    else:
                        return HttpResponse('Invalid Login')
                        
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        instructor_form = InstructorProfileForm()
        student_form = StudentProfileForm()
        if request.POST['role'] == 'student':
            profile_form = StudentProfileForm(request.POST, request.FILES)
        else:
            profile_form = InstructorProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            # TODO: Correct these redirect URLs
            if request.POST['role'] == 'student':
                return redirect('/class/2')
            else:
                return redirect('/class/2')
        else:
            context = {
                'user_form': user_form,
                'instructor_form': instructor_form,
                'student_form': student_form,
                'profile_form': profile_form
            }
            return render(request, 'register.html', context)


    else:
        user_form = RegistrationForm()
        instructor_form = InstructorProfileForm()
        student_form = StudentProfileForm()

    context = {
        'user_form': user_form,
        'instructor_form': instructor_form,
        'student_form': student_form,
    }
    return render(request, 'register.html', context)

# HANDLING AJAX REQUESTS FOR ASSIGNMENT POPUP
