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
    # Read nested, write via pk
    professor = ProfessorSerializer(read_only=True)
    professor_id = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all(), write_only=True, required=False, allow_null=True)
    students = StudentSerializer(read_only=True, many=True)
    student_ids = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True, many=True, required=False)

    class Meta:
        model = Subject
        fields = ("id", "title", "code", "faculty", "professor", "professor_id", "students", "student_ids")

    def create(self, validated_data):
        prof = validated_data.pop('professor_id', None)
        student_ids = validated_data.pop('student_ids', [])
        subj = Subject.objects.create(**validated_data)
        if prof is not None:
            subj.professor = prof
            subj.save()
        if student_ids:
            subj.students.set(student_ids)
        return subj

    def update(self, instance, validated_data):
        prof = validated_data.pop('professor_id', None)
        student_ids = validated_data.pop('student_ids', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if prof is not None:
            instance.professor = prof
        if student_ids is not None:
            instance.students.set(student_ids)
        instance.save()
        return instance
