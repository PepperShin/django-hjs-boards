from django.test import TestCase, TransactionTestCase
from django.db.models import Count, Sum, Avg, Min, Max
from django.db.models.functions import Length  # Length를 여기에서 임포트
from .models import Question, Answer
from django.utils import timezone


class DatabaseTestCase(TransactionTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.insert_test_data()

    @classmethod
    def insert_test_data(cls):
        Question.objects.all().delete()
        Answer.objects.all().delete()
        """
        Test setup method to create initial data
        """
        # 질문 3개 생성
        q1 = Question.objects.create(
            subject="Python이란?",
            content="Python은 프로그래밍 언어입니다.",
            create_date=timezone.now(),
        )
        q2 = Question.objects.create(
            subject="Django란?",
            content="Django는 Python 웹 프레임워크입니다.",
            create_date=timezone.now(),
        )
        q3 = Question.objects.create(
            subject="Java란?",
            content="Java는 객체 지향 언어입니다.",
            create_date=timezone.now(),
        )

        # 각 질문에 대한 답변 생성
        Answer.objects.create(
            question=q1,
            content="Python은 매우 유용합니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q1,
            content="Python은 쉽고 강력합니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q2,
            content="Django는 빠르고 확장성이 좋습니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q3,
            content="Java는 크로스 플랫폼에서 사용됩니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q3,
            content="Java는 많은 라이브러리와 도구를 지원합니다.",
            create_date=timezone.now(),
        )

    # def test_departments_exist(self):
    #     self.assertEqual(Department.objects.count(), 4)

    # def test_employees_exist(self):
    #     self.assertEqual(Employee.objects.count(), 14)

    # def test_salary_grades_exist(self):
    #     self.assertEqual(SalaryGrade.objects.count(), 5)

    # def test_employee_salary_range(self):
    #     for grade in SalaryGrade.objects.all():
    #         employees = Employee.objects.filter(sal__gte=grade.losal, sal__lte=grade.hisal)
    #         self.assertTrue(employees.exists())


# 아래의 명령어 실행
# python manage.py shell

# from pybo.pybo_tests import DatabaseTestCase
# DatabaseTestCase.insert_test_data()
