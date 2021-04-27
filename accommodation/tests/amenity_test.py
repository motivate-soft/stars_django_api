from django_seed import Seed
from accommodation.models.amenity import Amenity

seeder = Seed.seeder()
seeder.add_entity(Amenity, 10)
seeder.execute()
