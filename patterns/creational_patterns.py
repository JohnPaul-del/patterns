import copy
import quopri


class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class UsersFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type):
        return cls.types[type]()


class CoursePrototype:
    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class Category:

    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def count_courses(self):
        result = len(self.courses)
        if self.category:
            result += self.category.count_courses()
        return result


class CoursesFactory:

    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
    }

    @classmethod
    def create(cls, type, name, category):
        return cls.types[type](name, category)


class Engine:

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type):
        return UsersFactory.create(type)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_id(self, id):
        for el in self.categories:
            print('item', el.id)
            if el.id == id:
                return el
        raise Exception(f'There is no id category: {id}')

    @staticmethod
    def create_course(type, name, category):
        return CoursesFactory.create(type, name, category)

    def get_course(self, name):
        for el in self.cources:
            if el.name == name:
                return el
        return None

    @staticmethod
    def decode_value(value):
        result = bytes(value.replace('%', '=').replace('+', ' '), 'UTF-8')
        result_str = quopri.decodestring(result)
        return result_str.decode('UTF-8')


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('Log Info: ', text)
