from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Faculty, Administrator, Professor, Student, Subject


class UniversityTests(TestCase):
    def setUp(self):
        # setup faculties (created by data migration already)
        self.cs, _ = Faculty.objects.get_or_create(name='CS')
        self.en, _ = Faculty.objects.get_or_create(name='EN')

        # users
        self.admin_user = User.objects.create_user('admin', password='adminpass')
        Administrator.objects.create(user=self.admin_user, faculty=self.cs)

        self.prof_user = User.objects.create_user('prof1', password='profpass')
        self.prof = Professor.objects.create(user=self.prof_user, faculty=self.cs)

        self.stud_user = User.objects.create_user('student1', password='studentpass')
        self.stud = Student.objects.create(user=self.stud_user, faculty=self.cs, enrollment_number='ENR001')

        self.subject = Subject.objects.create(code='CS101', title='Intro', faculty=self.cs, professor=self.prof)
        self.subject.students.add(self.stud)

        self.client = APIClient()

    def test_faculties_exist(self):
        self.assertEqual(Faculty.objects.count(), 2)

    def test_admin_dashboard(self):
        self.client.login(username='admin', password='adminpass')
        # get token
        resp = self.client.post('/api/auth/token/', {'username': 'admin', 'password': 'adminpass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        r = self.client.get('/api/dashboard/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['role'], 'administrator')

    def test_professor_dashboard(self):
        resp = self.client.post('/api/auth/token/', {'username': 'prof1', 'password': 'profpass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        r = self.client.get('/api/dashboard/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['role'], 'professor')
        self.assertTrue(len(r.data['subjects']) >= 1)

    def test_student_dashboard(self):
        resp = self.client.post('/api/auth/token/', {'username': 'student1', 'password': 'studentpass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        r = self.client.get('/api/dashboard/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['role'], 'student')
        self.assertTrue(len(r.data['subjects']) >= 1)
