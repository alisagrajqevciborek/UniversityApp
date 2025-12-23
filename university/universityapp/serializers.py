from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Faculty, Administrator, Professor, Student, Subject


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ("id", "name")


class AdministratorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administrator
        fields = ("id", "user", "phone", "faculty", "title")


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Professor
        fields = ("id", "user", "phone", "faculty", "office")


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ("id", "user", "phone", "faculty", "enrollment_number", "year")


class SubjectSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    students = StudentSerializer(read_only=True, many=True)

    class Meta:
        model = Subject
        fields = ("id", "title", "code", "faculty", "professor", "students")
