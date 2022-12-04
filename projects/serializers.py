from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from .models import Project, Contributor, Issue, Comment
from users.models import User


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    issue = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']


class IssueSerializer(serializers.ModelSerializer):

    comments = StringRelatedField(many=True, read_only=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    assignee = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    project = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project', 'status', 'author', 'assignee',
                  'created_time', 'comments']


class ContributorsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    project = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Contributor
        fields = ['id', 'role', 'user', 'project']


class ProjectSerializer(serializers.ModelSerializer):
    issues = StringRelatedField(many=True, read_only=True)
    contributors = ContributorsSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'contributors', 'issues']
