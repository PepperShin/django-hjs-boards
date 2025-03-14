from django.test import TestCase
from django.db.models import Count, Sum, Avg, Min, Max
from django.db.models.functions import Length  # Length를 여기에서 임포트

from django.utils import timezone
from pybo.models import Answer, Question

# 테이블에 임시적으로 올라가서 반영되진 않는다.
# python manage.py test


class AggregateTestCase(TestCase):  # 테스트용 클래스. 데이터베이스에 올라가지 않는다

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

    def test_value(self):
        ## SQL 쿼리:
        ## SELECT subject, content  FROM Answer;
        ## 딕셔너리 형태로 반환
        result = Question.objects.values("subject", "content")
        result = Question.objects.all().values()  # 딕셔너리
        result = Question.objects.all().values_list()  # 튜플

        # 관련 테입즐 필드 조회(포오린키 조회)
        # SELECT Answer.id, Question.subject, Answer.content
        # FROM Answer
        # JOIN Question ON Answer.question_id = Question.id;

        query_set = Answer.objects.values("id", "question__subject", "content")
        # print(query_set.query)

    def test_filter(self):

        # SELECT * FROM question WHERE id = 1;;
        # 1. 특정 ID의 질문 조회
        query = Question.objects.filter(id=1)
        # print(query.query)

        # 2. 특정 제목을 가진 질문 조회
        # SELECT * FROM Question WHERE subject = 'Django란?';
        query = Question.objects.filter(subject="Django란?")
        # print(query)

        # 3. 특정 내용이 포함된 질문 조회 (icontains)
        # SELECT * FROM question WHERE content LIKE '%Python%';
        query = Question.objects.filter(content__icontains="Python").values()
        # print(query)

        # 4. 날짜 형 조회
        # query = Question.objects.filter(create_date__gt=datetime(2024, 1, 1)).values()

        # 5. 숫자 필터링
        # lt -> less then -> lt < 5, lte <= 5
        # gt -> greater then -> gt > 5, gte >= 5
        query = Question.objects.filter(id__lt=5)
        # print(query)

        # 특정 ID 사이의 질문 조회 (between)
        # SELECT * FROM Question WHERE id BETWEEN 1 AND 5;
        query = Question.objects.filter(id__range=(1, 5))
        # print(query)

        # 2025년 1월 1일과 2025년 3월 14일 사이에 생성된 질문
        query = Question.objects.filter(create_date__range=("2025-01-01", "2025-03-14"))
        # print(query)

        # 제목이 'Django란?'이고, 내용에 'Django'가 포함된 질문
        # SELECT * FROM Question WHERE subject = 'Django란?' AND content LIKE '%Django%';
        query = Question.objects.filter(
            subject="Django란?", content__icontains="Django"
        )
        # print(query)

        # 제목이 'Django란?'이거나, 내용에 'Django'가 포함된 질문
        # SELECT * FROM Question WHERE subject = 'Django란?' OR content LIKE '%Django%';
        from django.db.models import Q

        query = Question.objects.filter(
            Q(subject="Django란?") | Q(content__icontains="Django")
        )
        # print(query)

        # 정렬
        # SELECT * FROM Question ORDER BY create_date DESC LIMIT 2;
        query = Question.objects.order_by("-id").values()[:2]
        # print(query)

        # null 처리
        # query = Question.objects.filter(answer__isnull=False)
        # print(query)
        if Question.objects.filter(subject="Django란?").exists():
            print("해당 질문이 존재합니다.")

    # annotate @, aggregate
    def test_annotate(self):
        # 부서별 사람수 = SELECT count(*), depton FROM emp GROUP BY deptno
        # 부서별 월급 총합 = SELECT avg(sal), deptno FROM emp GROUP BY deptno

        # 각 질문별 최신 답변의 날짜 가져오기 (GROUP BY)
        questions = Question.objects.annotate(
            latest_answer_date=Max(
                "answers__create_date"
            )  # related_name으로 해야함. sql에서 group by의 필드명. 딕셔너리 패킹.
        )
        # for q in questions:
        #     print(q.subject, q.latest_answer_date)

        # 각 질문별, 대답들 갯수

        # SELECT q.id, COUNT(a.id) AS answer_count
        # FROM Question q
        # LEFT JOIN Answer a ON q.id = a.question_id
        # GROUP BY q.id

        questions = Question.objects.annotate(answer_count=Count("answers"))

        # for q in questions:
        #     print(f"질문: {q.subject}, 답변 개수: {q.answer_count}")

    def test_aggregate(self):
        # 전체 통계 함수

        # 1. 전체 대답 갯수
        # SELECT count(id) as total_answers FROM answer
        answer = Answer.objects.aggregate(total_answers=Count("id"))
        print(answer)  # {'total_answer': 5}

        # 2. 전체 질문 갯수
        question = Question.objects.aggregate(total_questions=Count("id"))
        print(question)  # {'total_questions': 3}

        # 3. 전체 답변의 평균 길이
        # SELECT AVG(LENGTH(content)) AS avg_content_length FROM answer
        result = Answer.objects.aggregate(avg_content_length=Avg(Length("content")))
        print(result)  # {'avg_content_length': 20.8}

        # 4. 가장 오래된 질문 날짜 구하기
        question = Question.objects.aggregate(oldest_questions=Min("create_date"))
        print(
            question
        )  #  {'oldest_questions': datetime.datetime(2025, 3, 14, 2, 15, 31, 413570, tzinfo=datetime.timezone.utc)}

        # 5. 전체 답변 글자 수 합계 구하기
        # 6. 가장 긴 질문 길이 구하기

    def test_raw(self):
        # SQL문 다이렉트로 사용
        questions = Question.objects.raw("SELECT * FROM pybo_question")
        for question in questions:
            print(question.id, question.subject)

        # 2. 특정 질문 가져오기 (id=1)
        # SELECT * FROM pybo_question where id = 1;
        questions = Question.objects.raw(
            "SELECT * FROM pybo_question where id = %s", [1]
        )
        for question in questions:
            print(question.id, question.subject)

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

    def test_f(self):
        from django.db.models import F

        # 각 질문에 대해 최신 답변 날짜를 question 테이블의 필드 업데이트
        # UPDATE question
        # SET latest_answer_date = (SELECT MAX(a.create_date)
        #                           FROM answer a
        #                           WHERE a.question_id = question.id);
        # F()를 사용하면 Python 메모리를 사용하지 않고, DB에서 직접 연산 수행
        # JOIN과 GROUP BY 없이도 데이터를 효율적으로 업데이트 가능
        Question.objects.update(latest_answer_date=F("answers__create_date"))

    # def test_sum_answer_ids(self):
    #     """
    #     Test for Sum aggregation on answer ids
    #     """
    #     result = Answer.objects.aggregate(Sum("id"))
    #     # SQL 쿼리:
    #     # SELECT SUM(id) FROM Answer;
    #     print(result)
    #     self.assertEqual(result["id__sum"], 15)
