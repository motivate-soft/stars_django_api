from unittest import TestCase

from rest_framework.test import APIClient

from accommodation.models import Property


class TestPropertys(TestCase):
    def test_movies(self):
        property = Property.objects.create(name='tet', category='1', bookerville_id=1234)

        client = APIClient()
        response = client.put('/api/accommodation/property/'.format(property.id), {
            'name': 'TEST title',
            'room': [
                {'name': 'Test item', 'bed_type': 'M'},
                {'name': 'Test item', 'bed_type': 'M'},
            ]
        }, format='json')
        print(response)

        self.assertEqual(response.status_code, 200, response.content)
