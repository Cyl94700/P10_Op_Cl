import pytest
from rest_framework.test import APIClient


# ##############################  FIXTURES  ################################

@pytest.fixture
def client(db):
    return APIClient()


@pytest.fixture
def user1(client: APIClient):
    response = client.post('/signup/',
                           {'username': 'User_1',
                            'first_name': 'Jean',
                            'last_name': 'Dupont',
                            'email': 'jeandupont@test.fr',
                            'password': 'password999',
                            'password2': 'password999'})
    response = client.post('/login/',
                           {'username': 'User_1',
                            'password': 'password999'})
    return response.data['access']


@pytest.fixture
def user2(client: APIClient):
    response = client.post('/signup/',
                           {'username': 'User_2',
                            'first_name': 'Bernard',
                            'last_name': 'Henri',
                            'email': 'bernardhenri@test.fr',
                            'password': 'password999',
                            'password2': 'password999'})
    response = client.post('/login/',
                           {'username': 'User_2',
                            'password': 'password999'})
    return response.data['access']


@pytest.fixture
def user_intruder(client: APIClient):
    response = client.post('/signup/',
                           {'username': 'Intruder',
                            'first_name': 'Intruder',
                            'last_name': 'Intruder',
                            'email': 'intruder@test.fr',
                            'password': 'password999',
                            'password2': 'password999'})
    response = client.post('/login/',
                           {'username': 'Intruder',
                            'password': 'password999'})
    return response.data['access']


@pytest.fixture
def user1_project(client: APIClient, user1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    return client.post('/projects/', {
        'title': 'Projet 1',
        'description': 'Mon test du projet 1',
        'type': 'BACKEND'}, format='json')


@pytest.fixture
def user1_issue_project(client: APIClient, user1, user1_project, user2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    return client.post('/projects/1/issues/',
                       {'title': 'Problème 1',
                        'description': "problème 1 du projet 1",
                        'tag': 'BUG',
                        'priority': 'LOW',
                        'status': 'TODO',
                        'assignee': 'User_2'})


@pytest.fixture
def user1_comment_issue_project(client: APIClient, user1, user1_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    return client.post('/projects/1/issues/1/comments/', {
        'description': "commentaire 1 du problème 1 du projet 1"})

# ############################################################################
# ###########################  Tests PROJECTS  ###############################
# ############################################################################


def test_get_project_list(client, user1, user1_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/')
    assert response.status_code == 200


def test_delete_project_non_authorized(client, user_intruder, user1_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_intruder)
    response = client.delete('/projects/1/')
    assert response.status_code == 404


def test_delete_project_authorized(client, user1, user1_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.delete('/projects/1/')
    assert response.status_code == 204


def test_post_new_project(client, user1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.post('/projects/', {
        'title': 'Projet 1',
        'description': 'Montest du projet 1',
        'type': 'BACKEND'}, format='json')
    assert response.status_code == 201


def test_get_project1(client, user1, user1_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/1/')
    assert response.status_code == 200

# ###########################################################################
# ##########################  Tests ISSUES  #################################
# ###########################################################################


def test_issues_post(client, user1, user1_project, user2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.post('/projects/1/issues/',
                           {'title': 'Premier problème',
                            'description': "problème 1 de l'issue 1",
                            'tag': 'BUG',
                            'priority': 'LOW',
                            'status': 'TODO',
                            'assignee': 'User_2'})
    assert response.status_code == 201


def test_get_issue1_project1(client, user1, user1_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/1/issues/1/')
    assert response.status_code == 200


def test_delete_issue_non_authorized(client, user_intruder, user1_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_intruder)
    response = client.delete('/projects/1/issues/1/')
    assert response.status_code == 403


def test_delete_issue_autjorized(client, user1, user1_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.delete('/projects/1/issues/1/')
    assert response.status_code == 204

# ###########################################################################
# ############################ Tests COMMENTS  ##############################
# ###########################################################################


def test_comment_post(client, user1, user1_issue_project, user2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.post('/projects/1/issues/1/comments/', {
        'description': 'Premier commentaire'})
    assert response.status_code == 201


def test_get_comment1_issue1_project1(client, user1, user1_comment_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/1/issues/1/comments/1/')
    assert response.status_code == 200


def test_delete_comments_non_authorized(client, user_intruder, user1_comment_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_intruder)
    response = client.delete('/projects/1/issues/1/comments/1/')
    assert response.status_code == 403


def test_delete_comments_authorized(client, user1, user1_comment_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.delete('/projects/1/issues/1/comments/1/')
    assert response.status_code == 204

# ###########################################################################
# ############################ Tests COMMENTS  ##############################
# ###########################################################################


def test_get_user1_project1(client, user1, user1_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/1/users/1/')
    assert response.status_code == 200


def test_get_users_project1(client, user1, user1_project, user2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.post('/projects/1/users/',
                           {'role': 'CONTRIBUTOR',
                            'user': 'User_2'})
    assert response.status_code == 201


def test_delete_contributors_non_authorized(client, user_intruder, user1_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_intruder)
    response = client.delete('/projects/1/users/1/')
    assert response.status_code == 403


def test_delete_contributors_authorized(client, user1, user1_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.delete('/projects/1/users/1/')
    assert response.status_code == 204
