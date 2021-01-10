import itertools

from .models import Tutorial, Assignment, Lesson, Exercise, LessonProgress, ExerciseProgress


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
def getTutorialProgress(tutorial_id) -> dict:
    tutorial = Tutorial.objects.get(id=tutorial_id)
    assignments = Assignment.objects.filter(tutorial=tutorial)
    student_progresses = {}
    if tutorial.tutorial_type == Tutorial.LESSON:
        lessons = Lesson.objects.filter(tutorial=tutorial)
        for lesson in lessons:
            student_progresses[lesson] = []
            for assignment in assignments:
                student_progresses[lesson].append({
                    f'{assignment.student.id}':
                        LessonProgress.objects.get(assignment__id=assignment.id, lesson=lesson).completed
                })
    else:
        exercises = Exercise.objects.filter(tutorial=tutorial)
        for exercise in exercises:
            student_progresses[exercise] = []
            for assignment in assignments:
                student_progresses[exercise].append({
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
def getCompletionPercentages(student_progresses: dict) -> dict:
    lesson_percentages = {}
    for lesson, student_progresses in student_progresses.items():
        lesson_percentages[lesson] = [progress.values() for progress in student_progresses]
        lesson_percentages[lesson] = list(itertools.chain.from_iterable(lesson_percentages[lesson]))
        lesson_percentages[lesson] = \
            round((lesson_percentages[lesson].count(True) / len(lesson_percentages[lesson])) * 100, 2)
    return lesson_percentages

'''
Receives output from `getCompletionPercentages`
and returns total completion rate in Percentages

Example: getOverallCompletionRate(lessonPercentages) -> 87.22
'''
def getOverallCompletionRate(percentages: dict) -> float:
    overall = 0
    for percent in percentages.values():
        overall += percent
    
    return round(overall / len(percentages), 2)


    