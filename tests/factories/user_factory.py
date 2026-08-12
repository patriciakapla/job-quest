from factory.base import Factory
from factory.faker import Faker

from job_quest.models.user import User


class UserFactory(Factory):
    class Meta:
        model = User

    username = Faker('user_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('ascii_email')
    password_hash = Faker('password')
    birth_date = Faker('date_object')
