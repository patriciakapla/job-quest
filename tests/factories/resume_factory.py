from factory.base import Factory
from factory.faker import Faker

from job_quest.models.resume import Resume


class ResumeFactory(Factory):
    class Meta:
        model = Resume

    name = Faker('uri_path', deep=4)
    object_key = Faker('uri_path', deep=4)
    size_bytes = Faker('pyint', min_value=1, max_value=2 * 1024 * 1024)
