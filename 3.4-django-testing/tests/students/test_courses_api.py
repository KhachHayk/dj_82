import pytest
from django.urls import reverse


@pytest.mark.skip
def test_example():
    assert False, "Just test example"


@pytest.mark.django_db
def test_retrieve_course(course_bakery, client):
    course = course_bakery()
    response = client.get(reverse('courses-detail', args=[course.id]))
    assert response.status_code == 200
    assert response.json()['id'] == course.id


@pytest.mark.django_db
def test_list_courses(course_bakery, client):
    courses = course_bakery(_quantity=20)
    response = client.get(reverse('courses-list'))
    assert response.status_code == 200
    assert len(response.json()) == len(courses)


@pytest.mark.django_db
def test_filter_course_from_id(course_bakery, client):
    courses = course_bakery(_quantity=20)
    for course in courses:
        response = client.get(reverse('courses-list'), data={'id': course.id})
        assert response.status_code == 200
        assert response.json()[0]['id'] == course.id


@pytest.mark.django_db
def test_filter_course_from_name(course_bakery, client):
    courses = course_bakery(_quantity=20)
    for course in courses:
        response = client.get(reverse('courses-list'), data={'name': course.name})
        assert response.status_code == 200
        assert response.json()[0]['name'] == course.name


@pytest.mark.parametrize(
    'num_students, expected', [(2, 201), (10, 400)]
)
@pytest.mark.django_db
def test_create_course(client, student_bakery, num_students, expected):
    students = student_bakery(_quantity=num_students)
    data = {
        'name': "rrrrrrr",
        'students': []
    }
    for student in students:
        data['students'].append(
            student.pk
        )

@pytest.mark.parametrize(
    'num_students1, num_students2, expected', [(2, 5, 400), (2, 2, 200)]
)
@pytest.mark.django_db
def test_update_course(
        num_students1,
        num_students2,
        expected,
        client,
        student_bakery,
        course_bakery
):
    course = course_bakery()
    url = reverse('courses-detail', args=[course.id])
    data = {
        'name': 'name1',
    }
    response = client.put(url, data=data)
    assert response.status_code == 200
    data = {
        'id': course.id,
        'name': 'name2',
        'students': [student.id for student in student_bakery(_quantity=num_students1)]
    }
    response = client.patch(url, data=data)
    assert response.status_code == 200
    assert response.json()['name'] == data['name']
    assert len(response.json()['students']) == num_students1


@pytest.mark.django_db
def test_delete_course(client, course_bakery):
    course = course_bakery()
    url = reverse('courses-detail', args=[course.id])
    response = client.delete(url)
    assert response.status_code == 204