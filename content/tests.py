from django_seed import Seed

from content.models import Content

seeder = Seed.seeder()
seeder.add_entity(Content, 10)
seeder.execute()
inserted_pks = seeder.execute()
print(inserted_pks)
