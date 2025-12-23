from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Faculty, Administrator, Professor, Student, Subject
from .serializers import (
    FacultySerializer,
    AdministratorSerializer,
    ProfessorSerializer,
    StudentSerializer,
    SubjectSerializer,
)


class FacultyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.select_related("user", "faculty").all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("user", "faculty").all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related("faculty", "professor").prefetch_related("students").all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class DashboardView(APIView):
    """Return different payloads depending on the authenticated user's role."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        # Administrator
        if hasattr(user, "administrator"):
            # Admin can see all professors, students and subjects
            professors = Professor.objects.count()
            students = Student.objects.count()
            subjects = Subject.objects.count()
            return Response({"role": "administrator", "professors": professors, "students": students, "subjects": subjects})

        # Professor
        if hasattr(user, "professor"):
            prof = user.professor
            subjects = Subject.objects.filter(professor=prof)
            serializer = SubjectSerializer(subjects, many=True, context={"request": request})
            return Response({"role": "professor", "subjects": serializer.data})

        # Student
        if hasattr(user, "student"):
            stud = user.student
            subjects = stud.subjects.all()
            serializer = SubjectSerializer(subjects, many=True, context={"request": request})
            return Response({"role": "student", "subjects": serializer.data})

        return Response({"detail": "No role/profile associated with this user."}, status=status.HTTP_404_NOT_FOUND)
