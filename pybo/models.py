from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# dev_2


# 하나의 질문에는 무수히 많은 답변이 등록
class Question(models.Model):
    # 필드가 null로 저장되는 것을 허용
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # 사용자 이름을 외래키로 받아오기 # dev_16
    subject = models.CharField(max_length=100)
    content = models.TextField()  # 글자 수에 제한이 없는 텍스트는 TextField를 사용한다
    create_date = models.DateTimeField()
    # dev_17
    # modify_date 칼럼에 null을 허용함
    # blank=True는 form.is_valid()를 통한 입력 데이터 검증 시 값이 없어도 된다는 의미
    modify_date = models.DateTimeField(null=True, blank=True)  # 수정 일시

    def __str__(self):
        return self.subject


class Answer(models.Model):

    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # null=True는 null값 가능 # dev_16

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)  # 수정 일시


# q=Question.objects.get(id=4)
# q.answer_set.all()
# <QuerySet [<Answer: Answer object (3)>, <Answer: Answer object (4)>, <Answer: Answer object (8)>]>

# .answer_set.all()    # 4.answer_set.all() # 역방향 참조
# Question .answers.all()    # 4.answers.all() # 역방향 참조
