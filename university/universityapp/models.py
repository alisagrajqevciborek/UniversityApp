from django.db import models
from django.contrib.auth.models import User


class Faculty(models.Model):
    COMPUTER_SCIENCE = "CS"
    ENGLISH = "EN"
    DEPARTMENT_CHOICES = [
        (COMPUTER_SCIENCE, "Computer Science"),
        (ENGLISH, "English"),
    ]

    name = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, unique=True)

    def __str__(self):
        return dict(self.DEPARTMENT_CHOICES).get(self.name, self.name)


class Profile(models.Model):
    """Abstract base profile to keep common fields DRY."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Administrator(Profile):
    title = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Administrator: {self.user.get_full_name() or self.user.username}"


class Professor(Profile):
    office = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Professor: {self.user.get_full_name() or self.user.username}"


class Student(Profile):
    enrollment_number = models.CharField(max_length=30, unique=True)
    year = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"Student: {self.user.get_full_name() or self.user.username}"


class Subject(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, related_name="subjects")
    students = models.ManyToManyField(Student, related_name="subjects", blank=True)

    def __str__(self):
        return f"{self.code} - {self.title}"
