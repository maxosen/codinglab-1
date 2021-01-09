import json
from subprocess import PIPE, run
import itertools

from .models import Tutorial, Assignment, LessonProgress, ExerciseProgress, Lesson, Exercise


'''
UTILITIES FOR RUNNING USER CODE
'''
def run_testcases(code, testcases):
    '''
    Return results of testcases
    Example output: [
        {'isMatch': false, 'userOutput': 0},
        {'isMatch': false, 'userOutput': 0},
        {'isMatch': false, 'userOutput': 0}
    ]
    '''
    command = ["node", "student/node/runTestcases.js", code, testcases]
    output = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    try:
        return json.loads(output.stdout)
    except:
        return {'Error': True}


def is_testcases_pass(results):
    if results == {'Error': True}:
        return False
    else:
        for result in results:
            if not result['isMatch']:
                return False
    return True



'''
UTILITIES FOR ANALYTICS
'''

'''
Get progress of tutorial, ordered by lessons/exercises, and students

Returns a dictionary of following format:
{
    'lesson_id': [
        {'student_id': Completion Status <Boolean>},
        {'student_id': Completion Status <Boolean>},
        ...
    ],
    'lesson_id': [ ],
    ...
}
'''
def getTutorialProgress(tutorial_id):
    tutorial = Tutorial.objects.get(id=tutorial_id)
    assignments = Assignment.objects.filter(tutorial=tutorial)
    student_progresses = {}
    if tutorial.tutorial_type == Tutorial.LESSON:
        lessons = Lesson.objects.filter(tutorial=tutorial)
        for lesson in lessons:
            student_progresses[f'{lesson.id}'] = []
            for assignment in assignments:
                student_progresses[f'{lesson.id}'].append({
                    f'{assignment.student.id}':
                        LessonProgress.objects.get(assignment__id=assignment.id, lesson=lesson).completed
                })
    else:
        exercises = Exercise.objects.filter(tutorial=tutorial)
        for exercise in exercises:
            student_progresses[f'{exercise.id}'] = []
            for assignment in assignments:
                student_progresses[f'{exercise.id}'].append({
                    f'{assignment.student.id}':
                        ExerciseProgress.objects.get(assignment__id=assignment.id, exercise=exercise).completed
                })
    return student_progresses

'''
Receives dictionary by getTutorialProgress(), and returns a dictionary of following format
{
    'lesson_id': Completion Percentage <Float>
}
'''
def getCompletionPercentages(student_progresses):
    lesson_percentages = {}
    for lesson_id, student_progresses in student_progresses.items():
        lesson_percentages[f'{lesson_id}'] = [progress.values() for progress in student_progresses]
        lesson_percentages[f'{lesson_id}'] = list(itertools.chain.from_iterable(lesson_percentages[f'{lesson_id}']))
        lesson_percentages[f'{lesson_id}'] = \
            round((lesson_percentages[f'{lesson_id}'].count(True) / len(lesson_percentages[f'{lesson_id}'])) * 100, 2)
    return lesson_percentages


    