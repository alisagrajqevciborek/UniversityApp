from django.contrib import admin
from .models import Faculty, Subject, Administrator, Professor, Student


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "faculty", "professor")
    filter_horizontal = ("students",)


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "faculty")


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("user", "office", "faculty")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "enrollment_number", "year", "faculty")
