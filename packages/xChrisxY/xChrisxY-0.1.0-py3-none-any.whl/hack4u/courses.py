class Course:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link
    
    def __repr__(self):
        return f"{self.name} [{self.duration}] ({self.link})"

courses = [
    
        Course("Introdución a Linux", 15, ""),
        Course("Personalización de Linux", 3, ""),
        Course("Introducción al Hacking", 55, "")

]

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in couses:
        if course.name == name:
            return course

    return None
    
