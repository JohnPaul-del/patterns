import os
from datetime import datetime

from frameworks.templates import _render
from patterns.creational_patterns import Engine, Logger
from patterns.urls_patterns import Routes, Debugging

site = Engine()
logger = Logger('main')
routes = {}


@Routes(routes=routes, url='/')
class Index:
    @Debugging(name='Index')
    def __call__(self, request):
        return '200 OK', _render('index.html', objects_list=site.categories)


@Routes(routes=routes, url='/about/')
class About:
    @Debugging(name='About')
    def __call__(self, request):
        return '200 OK', _render('about.html')


@Routes(routes=routes, url='/contact/')
class ContactUs:
    @Debugging(name='ContactUs')
    def __call__(self, request):
        return '200 OK', _render('contact_us.html')


# class StudyPrograms:
#     def __call__(self, request):
#         return '200 OK', _render('study-programs.html', data=date.today())


class NotFound404:
    def __call__(self, request):
        return '404 Not found', '404 PAGE Not Found'


@Routes(routes=routes, url='/courses-list/')
class CoursesList:
    @Debugging(name='CoursesList')
    def __call__(self, request):
        logger.log('Courses List')
        try:
            category = site.find_category_id(int(request['request_params']['id']))
            return '200 OK', _render('course-list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@Routes(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debugging(name='Create course')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', _render('course-list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_id(int(self.category_id))

                return '200 OK', _render('create-course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@Routes(routes=routes, url='/create-category/')
class CreateCategory:

    @Debugging(name='Create Category')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', _render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', _render('create-category.html', categories=categories)


@Routes(routes=routes, url='/category-list/')
class CategoryList:

    @Debugging(name='Category list')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', _render('category-list.html', objects_list=site.categories)


@Routes(routes=routes, url='/category-copy/')
class CopyCourse:

    @Debugging(name='Category Copy')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', _render('course-list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
