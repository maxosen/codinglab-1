from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Tutorial, Lesson, Exercise

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
    # data = json.loads(request.body.decode("utf-8"))
    print(request.body.decode("utf-8"))
    # print(data)
    # usercode = data.code
    testcases = json.loads(Exercise.objects.get(id=id).testcases)
    # print(usercode)
    return JsonResponse({'fuck': 1})

