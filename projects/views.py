from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .permissions import IsAuthorProject, IsContributorProject, CanManageContributors


from .serializers import (
    ProjectSerializer,
    ContributorsSerializer,
    IssueSerializer,
    CommentSerializer
)


class ProjectViewSet(ModelViewSet):
    """
    The endpoint [project list](/projects/) is the main entry point of the API
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorProject]

    def perform_create(self, serializer):
        """
        Author is saved as the authenticated user
        Arguments:
        serializer  -- ProjectSerializer
        """
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Return only projects where authenticated user is author or contributor.
        """
        user_projects = []
        is_author_or_contributor = Contributor.objects.filter(
            user=self.request.user).values()
        for user in is_author_or_contributor:
            user_projects.append(user['project_id'])
        return Project.objects.filter(id__in=user_projects)


class ContributorsViewSet(ModelViewSet):

    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated, CanManageContributors]

    def get_queryset(self):
        """
        Return a list of contributors project
        """
        project = self.kwargs['project_id']
        return Contributor.objects.filter(project=project)

    def perform_create(self, serializer):
        """
        Add a contributor in a project and put the project-id in url.
        Arguments:
        serializer  -- CommentSerializer
        """
        project = self.kwargs['project_id']
        project = Project.objects.get(id=project)
        serializer.save(project=project)


class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributorProject]

    def perform_create(self, serializer):
        """The author is automaticaly saved as the authenticated user.
        The project_id is authomaticaly saved using the project_id in the url
        endpoint.

        Arguments:
            serializer  -- CommentSerializer
        """
        project = self.kwargs['project_id']
        project = Project.objects.get(id=project)
        serializer.save(author=self.request.user, project=project)

    def get_queryset(self):
        """
        This view should return a list of all the issues
        as determined by the project_id portion of the URL.
        """
        project = self.kwargs['project_id']
        return Issue.objects.filter(project=project)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributorProject]

    def perform_create(self, serializer):
        """The author is automaticaly saved as the authenticated user.
        The issue_id is authomaticaly saved using the issue_id in the url
        endpoint.

        Arguments:
            serializer  -- CommentSerializer
        """
        issue = self.kwargs['issue_id']
        issue = Issue.objects.get(id=issue)
        serializer.save(author=self.request.user, issue=issue)

    def get_queryset(self):
        """
        This view should return a list of all the comments
        as determined by the issue_id portion of the URL.
        """
        issue = self.kwargs['issue_id']
        return Comment.objects.filter(issue=issue)
