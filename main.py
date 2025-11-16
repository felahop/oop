class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        avg_grade = self.average_grade()
        return (f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {avg_grade}\n'
                f'Курсы в процессе обучения: {", ".join(self.courses_in_progress)}\nЗавершённые курсы: {", ".join(self.finished_courses)}')

    def average_grade(self):
        if not self.grades:
            return 0.0
        all_grades = []
        for course_grades in self.grades.values():
            all_grades.extend(course_grades)
        return sum(all_grades) / len(list(all_grades))

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __lt__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка'
        return self.average_grade() < other.average_grade()

    def __gt__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка'
        return self.average_grade() > other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка'
        return self.average_grade() == other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = self.average_grade()
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade}'

    def average_grade(self):
        if not self.grades:
            return 0.0
        all_grades = []
        for course_grades in self.grades.values():
            all_grades.extend(course_grades)
        return sum(all_grades) / len(all_grades)

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка'
        return self.average_grade() < other.average_grade()

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка'
        return self.average_grade() > other.average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка'
        return self.average_grade() == other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


def average_homework(students, course):
    all_grades = []
    for student in students:
        if not isinstance(student, Student):
            continue
        if course in student.grades and student.grades[course]:
            all_grades.extend(student.grades[course])
    if not all_grades:
        return 0.0
    return sum(all_grades) / len(all_grades)


def average_grade_lect(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if not isinstance(lecturer, Lecturer):
            continue
        if course in lecturer.grades and lecturer.grades[course]:
            all_grades.extend(lecturer.grades[course])
    if not all_grades:
        return 0.0
    return sum(all_grades) / len(all_grades)


lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Кирилл', 'Епов')
reviewer1 = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Мария', 'Мартин')
student1 = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Максим', 'Костылев', 'М')

print(isinstance(lecturer1, Mentor)) # True
print(isinstance(reviewer1, Mentor)) # True
print(lecturer1.courses_attached)    # []
print(reviewer1.courses_attached)    # []

student1.finished_courses += ['Введение в программирование']
student2.finished_courses += ['Введение в программирование', 'Англиский язык для IT']
student1.courses_in_progress += ['Python', 'Java']
student2.courses_in_progress += ['Python', 'C++']
lecturer1.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Java', 'C++']
reviewer1.courses_attached += ['Python', 'C++']
reviewer2.courses_attached += ['Java', 'C++']

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 7)
reviewer1.rate_hw(student2, 'Python', 9)
print(student1.rate_lecture(lecturer1, 'Python', 7))  # None
print(student2.rate_lecture(lecturer2, 'Java', 9))    # Ошибка
print(student1.rate_lecture(lecturer1, 'Python', 7))   # None
print(student1.rate_lecture(lecturer2, 'Java', 8))     # None
print(student2.rate_lecture(lecturer1, 'С++', 8))      # Ошибка
print(student2.rate_lecture(reviewer2, 'Python', 6))   # Ошибка
print(lecturer1.grades)  # {'Python': [7, 7]}

print(reviewer1)
print(lecturer1)
print(student1)

print(f'Сравнение оценок студентов, student1 > student2: {student1 > student2}')
print(f'Сравнение оценок студентов, student1 < student2: {student1 < student2}')
print(f'Сравнение оценок студентов, student1 == student2: {student1 == student2}')

print(f'Сравнение оценок лекторов, lecturer1 > lecturer2: {lecturer1 > lecturer2}')
print(f'Сравнение оценок лекторов, lecturer1 < lecturer2: {lecturer1 < lecturer2}')
print(f'Сравнение оценок лекторов, lecturer1 == lecturer2: {lecturer1 == lecturer2}')

print(f'Проверка на ошибки: {student1 < lecturer1}')
print(f'Проверка на ошибки: {student1 > 10}')

print(f'Средняя оценка студентов за курс Python - {average_homework([student1, student2], 'Python')}')
print(f'Средняя оценка лекторов за курс Java - {average_grade_lect([lecturer1, lecturer2], 'Java')}')