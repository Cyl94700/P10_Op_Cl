from django.conf import settings
from django.db import models
from users.models import User


class Project(models.Model):

    TYPES = [('BACKEND', 'Back-end'), ('FRONTEND', 'Front-end'), ('IOS', 'iOS'), ('ANDROID', 'Android')]

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=2000)
    type = models.CharField(choices=TYPES, max_length=9)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    objects = models.Manager()

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        """
        Save a new project during creation. Call the Contributor method : save_author_as_contributor()
        """
        super(Project, self).save(*args, **kwargs)
        Contributor.save_author_as_contributor(self)


class Contributor(models.Model):

    ROLES = [('AUTHOR', 'Auteur'), ('CONTRIBUTOR', 'Contributeur')]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributors')
    role = models.CharField(max_length=12, choices=ROLES, default='CONTRIBUTOR')

    objects = models.Manager()

    class Meta:
        ordering = ['id']

    @classmethod
    def save_author_as_contributor(cls, project):
        """
        Author is saved as contributor.
        get_or_create method distinct create and update

        Arguments:
        project {Project Object} -- Project object
        """
        cls.objects.get_or_create(role='AUTHOR',
                                  user=project.author,
                                  project=project)

    @classmethod
    def save_assignee_issue_as_contributor(cls, issue):
        """Save the contributor as an assignee_user.
        get_or_create method distinct create and update
        Arguments:
        project {Project Object} -- Project object
        """
        cls.objects.get_or_create(role='CONTRIBUTOR',
                                  user=issue.assignee_user,
                                  project=issue.project)


class Issue(models.Model):

    TAGS = [('BUG', 'Bug'), ('TASK', 'Tâche'), ('IMPROVEMENTS', 'Améliorations')]
    PRIORITIES = [('LOW', 'Faible'), ('MEDIUM', 'Moyenne'), ('HIGH', 'Haute')]
    STATUS = [("TODO", "A faire"), ("IN PROGRESS", "En cours"), ("DONE", "Terminé")]

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=2000)
    tag = models.CharField(choices=TAGS, max_length=12)
    priority = models.CharField(choices=PRIORITIES, max_length=7, default='LOW')
    status = models.CharField(choices=STATUS, max_length=11, default='TODO')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.TextField(max_length=2000)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
