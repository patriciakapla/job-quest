from random import choice

from factory.base import Factory
from factory.declarations import LazyAttribute, LazyFunction
from factory.faker import Faker

from job_quest.models.application import Application
from job_quest.models.status import Status

get_faker = Faker._get_faker()


def generate_technologies():
    numbers = get_faker.pyint(min_value=1, max_value=10)
    return ','.join(get_faker.words(nb=numbers, unique=True))


class ApplicationFactory(Factory):
    class Meta:
        model = Application

    title = Faker('sentence', nb_words=4)
    company = Faker('company')
    location = Faker('city')
    description = Faker('text')
    notes = Faker('text')
    technologies = LazyFunction(generate_technologies)
    currency_code = Faker('currency_code')
    offered_salary_min = Faker('pyint', min_value=1, max_value=1_000_000)
    offered_salary_max = LazyAttribute(
        lambda application: (
            application.offered_salary_min
            + get_faker.pyint(min_value=1, max_value=100_000)
        )
    )
    expected_salary_min = Faker('pyint', min_value=1, max_value=1_000_000)
    expected_salary_max = LazyAttribute(
        lambda application: (
            application.expected_salary_min
            + get_faker.pyint(min_value=1, max_value=100_000)
        )
    )
    job_posting_url = Faker('url')
    source_platform = Faker('url')
    applied_at = Faker('date_between', start_date='today', end_date='+10d')
    status = choice(list(Status))
