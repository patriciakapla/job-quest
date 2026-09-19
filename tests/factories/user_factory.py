from factory.base import Factory
from factory.faker import Faker

from job_quest.models.user import User


class UserFactory(Factory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('ascii_email')
    google_id = Faker('numerify', text='#####################')
    birth_date = Faker('date_object')
