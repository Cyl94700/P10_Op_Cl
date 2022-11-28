from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from .models import Project, Contributor
from users.models import User


class ContributorsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    project = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Contributor
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    issues = StringRelatedField(many=True, read_only=True)
    contributors = ContributorsSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Project
        fields = '__all__'
