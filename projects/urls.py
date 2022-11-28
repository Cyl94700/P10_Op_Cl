from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContributorsViewSet

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
urlpatterns = [
    path('', include(router.urls)),

    path('projects/<int:project_id>/users/',
         contributor_list,
         name='contributor_list'),
    path('projects/<int:project_id>/users/<int:pk>/',
         contributor_detail,
         name='contributor_detail'),
]
