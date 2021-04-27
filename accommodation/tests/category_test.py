from django_seed import Seed
from accommodation.models.category import Category

seeder = Seed.seeder()
seeder.add_entity(Category, 10)
inserted_pks = seeder.execute()
print(inserted_pks)
