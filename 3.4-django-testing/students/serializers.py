from rest_framework import serializers
from django.conf import settings

from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")
