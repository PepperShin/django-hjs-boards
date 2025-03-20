from django.test import TestCase
from django.db.models import Count, Sum, Avg, Min, Max
from django.db.models.functions import Length  # Length를 여기에서 임포트

from django.utils import timezone
from regex import F
from pybo.models import Answer, Question
from django.db.models import F


class AggregateTestCase(TestCase):

    def setUp(self):
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

    def test_sum_answer_ids(self):
        """
        Test for Sum aggregation on answer ids
        """
        result = Answer.objects.aggregate(Sum("id"))
        # SQL 쿼리:
        # SELECT SUM(id) FROM Answer;
        print(result)
        self.assertEqual(result["id__sum"], 15)  # AssertionError: 15 != 16

    def test_annotate(self):
        # 🎯 annotate() 정리
        # ✔ annotate()는 개별 객체(레코드)에 대해 추가 필드를 생성하여 값을 포함한 QuerySet 반환
        # ✔ GROUP BY를 자동으로 처리하여 집계 함수(Aggregate Functions) 적용 가능
        # ✔ Count, Sum, Avg, Min, Max, Length 등 다양한 집계 연산을 활용 가능
        # ✔ Case-When을 사용하여 조건부 필드 추가 가능
        # 🔹 즉, annotate()는 개별 항목에 대해 추가 정보를 붙이는 강력한 기능! 🚀

        # 부서별 사람수  select count(*), deptno from emp group by deptno
        # 부서별 월급 총합
        # select max(sal) as sal, deptno, ename from emp group by deptno
        # 3000 10
        # 2000 20
        # 500  50

        # 각 질문별 최신 답변의 날짜 가져오기
        # SQL 로 표현하면

        # SELECT q.id,  MAX(a.create_date) AS latest_answer_date
        # FROM question q
        # LEFT JOIN answer a
        #     ON q.id = a.question_id
        # GROUP BY q.id

        # group by 절을 기본적으로 만듦
        questions = Question.objects.annotate(
            latest_answer_date=Max("answer__create_date")
        )

        # for q in questions:
        #    print(q.subject, q.latest_answer_date)

        # 각 문제별, 대답들 갯수

        # SELECT q.id, COUNT(a.id) AS answer_count
        # FROM Question q
        # LEFT JOIN Answer a ON q.id = a.question_id
        # GROUP BY q.id,

        questions = Question.objects.annotate(answer_count=Count("answer__id"))

        # for q in questions:
        #    print(f"질문: {q.subject}, 답변 개수: {q.answer_count}")

    # def test_value(self):
    #     ## SQL 쿼리:
    #     ## SELECT subject, content  FROM Answer;
    #     # SELECT *  FROM Answer; => queryset
    #     ## 딕셔너리 형태로 반환
    #     result = Question.objects.values("subject", "content")
    #     result = Question.objects.all().values()  # 딕셔너리
    #     result = Question.objects.all().values_list()  # 튜플

    #     # 관련 테입즐 필드 조회(포오린키 조회)

    #     # SELECT Answer.id, Question.subject, Answer.content
    #     # FROM Answer
    #     # JOIN Question ON Answer.question_id = Question.id;

    #     #SELECT "pybo_answer"."id", "pybo_question"."subject", "pybo_answer"."content"
    #     #FROM "pybo_answer" INNER JOIN "pybo_question" ON ("pybo_answer"."question_id" = "pybo_question"."id")

    #     query_set = Answer.objects.values("id", "question__subject", "content")
    #     print(query_set.query)

    def test_filter(self):

        # SELECT * FROM Question WHERE id = 1;

        # 1. 특정 ID의 질문 조회
        query = Question.objects.filter(id=1)
        # print(query.query)

        # 2. 특정 제목을 가진 질문 조회
        # SELECT * FROM Question WHERE subject = 'Django란?';
        query = Question.objects.filter(subject="Django란?")
        # print(query)

        # 3. 특정 내용이 포함된 질문 조회 (icontains)
        # SELECT * FROM Question WHERE content LIKE '%Python%';
        query = Question.objects.filter(content__icontains="Python").values()
        # print(query)

        # 4. 날짜 형 조회

        # query = Question.objects.filter(create_date__gt=datetime(2024, 1, 1))
        # print(query)

        # 5. 숫자 필터링
        # lt < 5 , lte <=5 , gt > 5,gte >=5
        # SELECT * FROM Question WHERE id < 5;

        query = Question.objects.filter(id__lt=5)  # id < 5
        # print(query)

        # 특정 ID 사이의 질문 조회 (between)
        # SELECT * FROM Question WHERE id BETWEEN 1 AND 5;
        query = Question.objects.filter(id__range=(1, 5))  # id < 5
        # print(query)

        # 2025년 1월 1일과 2025년 3월 14일 사이에 생성된 질문
        query = Question.objects.filter(create_date__range=("2025-01-01", "2025-03-14"))
        # print(query)

        # 제목이 'Django란?'이고, 내용에 'MTV'가 포함된 질문
        # SELECT * FROM Question WHERE subject = 'Django란?' AND content LIKE '%Django%';
        query = Question.objects.filter(
            subject="Django란?", content__icontains="Django"
        )  # dev_2
        # print(query)

        # 제목이 'Django란?'이거나 'Python이란?'인 질문 (OR 조건)
        from django.db.models import Q

        # SELECT * FROM Question WHERE subject = 'Django란?' and subject = 'Python이란?';
        query = Question.objects.filter(
            Q(subject="Django란?") & Q(subject="Python이란?") | Q(subject="홍길동")
        )  # dev_2
        # print(query)

        # 정렬
        # SELECT * FROM Question ORDER BY create_date DESC LIMIT 2;
        query = Question.objects.order_by("-id").values()[:2]
        # print(query)

        # null 처리
        # query = Question.objects.filter(answer__isnull=True)
        # print(query)

        # if Question.objects.filter(subject="Django란?").exists():
        #    print("해당 질문이 존재합니다.")

        # annotate , aggregate
        # aggregate = 전체 통계 함수

    def test_aggregate(self):

        # 1. 전체 대답 갯수
        # select count(id) as total_answers from answer
        answer = Answer.objects.aggregate(total_answers=Count("id"))
        # print(answer) #{'total_answers': 5}

        # 2. 전체 질문 개수 구하기
        question = Question.objects.aggregate(total_questions=Count("id"))
        # print(question) #{'total_questions': 5}

        # 3. 전체 답변의 평균 길이 구하기
        # SELECT AVG(LENGTH(content)) AS avg_content_length FROM Answer;
        result = Answer.objects.aggregate(avg_content_length=Avg(Length("content")))
        # print(result)

        # 4.가장 오래된 질문 날짜 구하기(MIN)
        question = Question.objects.aggregate(oldest_questions=Min("create_date"))
        print(question)  # {'total_questions': 5}

        # 5. 전체 답변 글자 수 합계 구하기
        # 6. 가장 긴 질문 길이 구하기

    def test_raw(self):
        # raw 함수 다이렉트로 sql 구문을 적을수 있도록 만든함수
        questions = Question.objects.raw("SELECT * FROM pybo_question")
        for question in questions:
            print(question.id, question.subject)

        # 2. 특정 질문 가져오기 (id=1)
        # SELECT * FROM pybo_question WHERE id = 1;
        questions = Question.objects.raw(
            "SELECT * FROM pybo_question where id = %s", [1]
        )
        for q in questions:
            print(q.subject, q.content)

        # 3. 특정 키워드가 포함된 질문 검색
        keyword = "%Django%"
        questions = Question.objects.raw(
            "SELECT * FROM pybo_question WHERE content LIKE %s", [keyword]
        )
        for q in questions:
            print(q.subject)

        # 4. 답변이 가장 많은 질문 가져오기
        questions = Question.objects.raw(
            """
            SELECT q.id, q.subject, COUNT(a.id) AS answer_count
            FROM pybo_question q
            LEFT JOIN pybo_answer a ON q.id = a.question_id
            GROUP BY q.id
            ORDER BY answer_count DESC
            LIMIT 1
            """
        )
        for q in questions:
            print(q.subject, q.answer_count)
