from flask_login import current_user
from .models import Course, Enrollment, db

class CourseManager:
    @staticmethod
    def create_course(title, description):
        if current_user.role != 'instructor':
            return None
        course = Course(title=title, description=description, instructor_id=current_user.id)
        db.session.add(course)
        db.session.commit()
        return course

    @staticmethod
    def enroll_student(course_id):
        if current_user.role != 'student':
            return False
        enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return True
