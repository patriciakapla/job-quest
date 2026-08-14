from factory.base import Factory
from factory.faker import Faker

from job_quest.models.answer import Answer


class AnswerFactory(Factory):
    class Meta:
        model = Answer

    description = Faker('sentence', nb_words=12)
    answer = Faker('text', max_nb_chars=500)
