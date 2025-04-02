from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .auth import AuthManager
from .course import CourseManager
from .models import Course

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('routes.courses'))
    return redirect(url_for('routes.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']          # Get the role from the form
        if AuthManager.register(username, email, password, role=role):
            return redirect(url_for('routes.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if AuthManager.login(username, password):
            return redirect(url_for('routes.courses'))
    return render_template('login.html')

@bp.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    if request.method == 'POST' and current_user.role == 'instructor':
        title = request.form['title']
        description = request.form['description']
        CourseManager.create_course(title, description)
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@bp.route('/course/<int:course_id>/enroll')
@login_required
def enroll(course_id):
    CourseManager.enroll_student(course_id)
    return redirect(url_for('routes.courses'))

@bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)

@bp.route('/logout')
@login_required
def logout():
    from flask_login import logout_user
    logout_user()
    return redirect(url_for('routes.login'))

@bp.route('/api/courses', methods=['GET'])
@login_required
def get_courses():
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'title': c.title, 'description': c.description} for c in courses])