from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from universityapp.models import Faculty, Administrator, Professor, Student, Subject


class Command(BaseCommand):
    help = 'Create sample users, profiles, faculties and subjects for testing.'

    def handle(self, *args, **options):
        cs = Faculty.objects.filter(name='CS').first()
        en = Faculty.objects.filter(name='EN').first()

        # Admin / superuser
        admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True})
        if created:
            admin_user.set_password('adminpass')
            admin_user.save()
        Administrator.objects.get_or_create(user=admin_user, defaults={'phone': '000000000', 'faculty': cs, 'title': 'Principal'})

        # Professor
        prof_user, _ = User.objects.get_or_create(username='prof1', defaults={'first_name': 'Ada', 'last_name': 'Lovelace', 'email': 'ada@example.com'})
        prof_user.set_password('profpass')
        prof_user.save()
        prof, _ = Professor.objects.get_or_create(user=prof_user, defaults={'phone': '111111111', 'faculty': cs, 'office': 'A-101'})

        # Student
        stud_user, _ = User.objects.get_or_create(username='student1', defaults={'first_name': 'Alan', 'last_name': 'Turing', 'email': 'alan@example.com'})
        stud_user.set_password('studentpass')
        stud_user.save()
        stud, _ = Student.objects.get_or_create(user=stud_user, defaults={'phone': '222222222', 'faculty': cs, 'enrollment_number': 'ENR001', 'year': 1})

        # Subject linking professor and student
        subj, _ = Subject.objects.get_or_create(code='CS101', defaults={'title': 'Intro to CS', 'faculty': cs, 'professor': prof})
        subj.students.add(stud)

        self.stdout.write(self.style.SUCCESS('Sample data created. Users: admin/adminpass, prof1/profpass, student1/studentpass'))