from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Contributor


class IsAuthorProject(BasePermission):
    message = "Seul l'auteur d'un projet peut modifier et/ou supprimer son projet."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsContributorProject(BasePermission):
    message = "Seuls les contributeurs d'un projet peuvent lire les \
problèmes et commentaires de ce projet et en créer de nouveaux. Seuls les \
auteurs peuvent modifier et supprimer les problèmes ou commentaires."

    def has_permission(self, request, view):
        """
        Allow to read list project, issue or comment and add one of them
        Arguments:
        request {[type]} -- contain post data
        view {[type]} -- current view
        Returns:
        [bool] -- true if permission is ok
        """
        project = view.kwargs['project_id']
        is_author = Contributor.objects.filter(
            project=project,
            user=request.user,
            role="AUTHOR").exists()
        is_contributor = Contributor.objects.filter(
            project=project,
            user=request.user,
            role="CONTRIBUTOR").exists()

        if request.method in SAFE_METHODS or request.method == 'POST':
            return is_author or is_contributor
        if request.method == 'PUT' or request.method == 'DELETE':
            return is_author or is_contributor

    def has_object_permission(self, request, view, obj):
        """
        allow to read, update or delete project, issue or comment.
        Arguments:
        request {[type]} -- contain post data
        view {[type]} -- current view
        obj -- current model object
        Returns:
        [bool] -- true if permission is ok
        """
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE' or request.method == 'PUT':
            return obj.author == request.user


class CanManageContributors(BasePermission):
    message = "Seuls les auteurs et contributeurs d'un projet peuvent ajouter de \
nouveaux contributeurs."

    def has_permission(self, request, view):
        """
        allow to view list contributors and create or delete contributor.
        Arguments:
            request {[type]} -- contain post data
            view {[type]} -- current view
        Returns:
            [bool] -- true if permission is ok
        """
        project = view.kwargs['project_id']
        is_author = Contributor.objects.filter(
            project=project,
            user=request.user,
            role="AUTHOR").exists()
        is_contributor = Contributor.objects.filter(
            project=project,
            user=request.user,
            role="CONTRIBUTOR").exists()

        if request.method in SAFE_METHODS or request.method == 'POST':
            return is_author or is_contributor
        if request.method == 'DELETE':
            return is_author or is_contributor

    def has_object_permission(self, request, view, obj):
        """
        allow to delete contributor
        """
        project = view.kwargs['project_id']
        can_manage_contributors = Contributor.objects.filter(
            project=project,
            user=request.user).exists()

        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return can_manage_contributors
