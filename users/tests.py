import random
from django.utils import timezone
from django_seed import Seed

from authentication.models import CustomUser

seeder = Seed.seeder()
seeder.add_entity(CustomUser, 10, {
    # 'score': lambda x: random.randint(0,1000),
    'username': lambda x: seeder.faker.user_name(),
    'email': lambda x: seeder.faker.email(),
    'first_name': lambda x: seeder.faker.user_name(),
    'last_name': lambda x: seeder.faker.user_name(),
    'password': lambda x: "$UA9Lc6cv/6b3GJd9WY6Dv0hvxHNmD96jjdCJua68dmk=",
    'last_login': lambda x: timezone.now(),
    'is_active': lambda x: bool(random.getrandbits(1)),
    'is_superuser': lambda x: False,
})

# seeder_admin = Seed.seeder()
# seeder.add_entity(CustomUser, 1, {
#     'username': 'superadmin',
#     'email': 'admin@admin.com',
#     'first_name': 'Robert',
#     'last_name': 'Octavian',
#     'password': "password",
#     'last_login': timezone.now(),
#     'is_staff': True,
#     'is_active': True,
#     'is_superuser': True,
# })
# seeder_admin.execute()
seeder.execute()

