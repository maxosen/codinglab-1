import itertools
import numpy as np

from .models import ExerciseFeedback, ExerciseSubmissionEvent, LessonFeedback, LessonSubmissionEvent, LoginEvent, StudentProfile, Tutorial, Assignment, Lesson, Exercise, LessonProgress, ExerciseProgress


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
def get_overall_completion_rate(percentages: dict) -> float:
    overall = 0
    for percent in percentages.values():
        overall += percent
    
    return round(overall / len(percentages), 2)

def get_student_engagement(student: StudentProfile) -> float:
    FEEDBACK_COMPLETION_WEIGHTAGE = 0.3
    TUTORIAL_COMPLETION_WEIGHTAGE = 0.7
    # GET MOST RECENT LOGIN
    # login_events = LoginEvent.objects.filter(student=student) \
    #                 .order_by('-time')
    # try:
    #     last_login = login_events[0]
    # except:
    #     last_login = None

    # GET PERCENTAGES OF FEEDBACK COMPLETION
    number_of_lesson_feedbacks = len(LessonFeedback.objects.filter(assignment__student=student))
    number_of_exercise_feedbacks = len(ExerciseFeedback.objects.filter(assignment__student=student))
    assigned_tutorials = [assignment.tutorial for assignment in Assignment.objects.filter(student=student)]
    number_of_assigned_lessons = len(list(itertools.chain.from_iterable(
        [Lesson.objects.filter(tutorial=tutorial) for tutorial in assigned_tutorials]
    )))
    number_of_assigned_exercises = len(list(itertools.chain.from_iterable(
        [Exercise.objects.filter(tutorial=tutorial) for tutorial in assigned_tutorials]
    )))
    overall_feedback_percentage = (number_of_exercise_feedbacks + number_of_lesson_feedbacks) / (number_of_assigned_exercises + number_of_assigned_lessons)

    # GET LESSON AND EXERCISE COMPLETION PERCENTAGES
    completed_lesson_percentage = len(LessonProgress.objects.filter(completed=True)) / number_of_assigned_lessons
    completed_exercise_percentage = len(ExerciseProgress.objects.filter(completed=True)) / number_of_assigned_exercises
    tutorial_completion_percentage = (completed_lesson_percentage + completed_exercise_percentage) / 2

    # GET AVERAGE LESSON/EXERCISE SUBMISSION FREQUENCY
    # average_lesson_freq = [submission.frequency for submission in LessonSubmissionEvent.objects.filter(assignment__student=student)]
    # average_exercse_freq = [submission.frequency for submission in ExerciseSubmissionEvent.objects.filter(assignment__student=student)]
    score = (overall_feedback_percentage * FEEDBACK_COMPLETION_WEIGHTAGE + \
            tutorial_completion_percentage * TUTORIAL_COMPLETION_WEIGHTAGE) / \
            (FEEDBACK_COMPLETION_WEIGHTAGE + TUTORIAL_COMPLETION_WEIGHTAGE)
    return score

def get_student_skill(student: StudentProfile) -> float:
    # GET AVERAGE LESSON/EXERCISE SUBMISSION FREQUENCY
    average_lesson_freq = [submission.frequency for submission in LessonSubmissionEvent.objects.filter(assignment__student=student)]
    average_lesson_freq = sum(average_lesson_freq) / len(average_lesson_freq)
    average_exercise_freq = [submission.frequency for submission in ExerciseSubmissionEvent.objects.filter(assignment__student=student)]
    average_exercise_freq = sum(average_exercise_freq) / len(average_exercise_freq)
    overall_average = average_exercise_freq + average_lesson_freq
    if overall_average == 1:
        return 1
    elif overall_average < 3:
        return 0.8
    elif overall_average < 5:
        return 0.7
    elif overall_average < 10:
        return 0.6
    elif overall_average < 20:
        return 0.5
    else:
        return 0.2
    

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
        student_scores = {student: get_student_engagement(student) for student in students}
    else:
        student_scores = {student: get_student_skill(student) for student in students}
    scores = student_scores.values()
    overall_average = sum(scores) / len(scores)
    indices = findClosestPermutation(scores, overall_average, len(scores), group_size)
    groups = []
    for group in indices:
        group = []
        for i in group:
            group.append(students[i])
        groups.append(group)
    return groups






