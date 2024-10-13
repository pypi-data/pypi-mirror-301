from .courses import courses

def total_duraction():
    return sum(course.duration for course in courses)
