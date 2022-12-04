from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContributorsViewSet, IssueViewSet, CommentViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')


contributor_list = ContributorsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

contributor_detail = ContributorsViewSet.as_view({
    'delete': 'destroy',
    'get': 'retrieve'
})
issue_list = IssueViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

issue_detail = IssueViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
urlpatterns = [
    path('', include(router.urls)),

    path('projects/<int:project_id>/users/',
         contributor_list,
         name='contributor_list'),
    path('projects/<int:project_id>/users/<int:pk>/',
         contributor_detail,
         name='contributor_detail'),
    path('projects/<int:project_id>/issues/',
         issue_list,
         name='issue_list'),
    path('projects/<int:project_id>/issues/<int:pk>/',
         issue_detail,
         name='issue_detail'),

    path('projects/<int:project_id>/issues/<int:issue_id>/comments/',
         comment_list,
         name='comment_list'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/',
         comment_detail,
         name='comment_detail'),
]
