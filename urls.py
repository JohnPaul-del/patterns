from datetime import date
from views import Index, About,  CoursesList, CreateCourse, CreateCategory, CategoryList, CopyCourse, ContactUs

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': ContactUs(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-course/': CopyCourse(),
}

def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
