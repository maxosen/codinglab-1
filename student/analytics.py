import itertools
import numpy as np

from .models import StudentProfile, Tutorial, Assignment, Lesson, Exercise, LessonProgress, ExerciseProgress


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



def getStudentEngagement() -> float:
    return 5

def getStudentSkill() -> float:
    return 5


def shuffledSSD(scores: list, target: int, length: int, split_size: int):
    indices = np.arange(length)
    np.random.shuffle(indices)
    scores = np.array(scores)[indices]
    scores = np.array_split(scores, length / split_size)
    averages = [np.sum(score) for score in scores]
    SSE = np.square(np.array(averages) - np.array(target))
    SSE = np.sum(SSE)
    return {indices: SSE}

'''
return the permutations of closest sub-array average to target
'''
def findClosestPermutation(scores: list, target: int, length: int, split_size: int, iterations: int=100):
    permutations = {}
    for i in range(iterations):
        permutations.append(shuffledSSD(scores, target, length, split_size))
    index = min(permutations.values())
    indices = permutations.keys[index]
    return indices


'''
Return an array of subarrays of StudentProfile:

size of subarrays: group_size
group_by: must be either "EN" (Engagement) or "SK" (Skill)

Engagement will measure 


Example:
[
    [Student 1, Student 2, Student 3],
    [Student 1, Student 2, Student 3],
    ...
    ...
]
'''
def groupStudents(students: StudentProfile, group_size: int, group_by: str):
    if group_by == "EN":
        student_scores = {student: getStudentSkill(student) for student in students}
    else:
        student_scores = {student: getStudentEngagement(student) for student in students}
    scores = student_scores.values()
    overall_average = sum(scores) / len(scores)
    indices = findClosestPermutation(scores, overall_average, len(scores), group_size)

    # correctly shuffled scores
    scores = np.array(scores)[indices]
    scores = np.array_split(scores, len(scores) / group_size)
    return scores.tolist()





