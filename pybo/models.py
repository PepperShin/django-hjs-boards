from django.db import models

# Create your models here.
# dev_2


# 하나의 질문에는 무수히 많은 답변이 등록
class Question(models.Model):
    # 필드가 null로 저장되는 것을 허용
    subject = models.CharField(max_length=100)
    content = models.TextField()  # 글자 수에 제한이 없는 텍스트는 TextField를 사용한다
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    create_date = models.DateTimeField()


# q=Question.objects.get(id=4)
# q.answer_set.all()
# <QuerySet [<Answer: Answer object (3)>, <Answer: Answer object (4)>, <Answer: Answer object (8)>]>

# .answer_set.all()    # 4.answer_set.all() # 역방향 참조
# Question .answers.all()    # 4.answers.all() # 역방향 참조
