from django.db import models

# Create your models here.
# dev_2


# 하나의 질문에는 무수히 많은 답변이 등록
class Question(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()  # 글자 수에 제한이 없는 텍스트는 TextField를 사용한다.
    create_date = models.DateTimeField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 1:n
    content = models.TextField()
    create_date = models.DateTimeField()
