from django_seed import Seed
from accommodation.models.room import Room

seeder = Seed.seeder()
seeder.add_entity(Room, 10)
inserted_pks = seeder.execute()
print(inserted_pks)
