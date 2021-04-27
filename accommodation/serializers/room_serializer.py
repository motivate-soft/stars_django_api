from rest_framework import serializers
from accommodation.models.room import Room

TWIN = 'T'
SOFA = 'S'
QUEEN = 'Q'
KING = 'K'
CHAIR = 'C'
MURPHY = 'M'
Full = 'F'
SINGLE = 'P'

BED_CHOICES = (
    (TWIN, 'Twin Bed'),
    (SOFA, 'Sofa Bed'),
    (QUEEN, 'Queen Bed'),
    (KING, 'King Bed'),
    (CHAIR, 'Chair Bed'),
    (MURPHY, 'Murphy Bed'),
    (Full, 'Full Bed'),
    (SINGLE, 'Single Chair Sleeper Bed'),
)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id', 'name', 'bed_type'
        )
        # In Django REST Framework AutoField fields (those that are automatically generated) are defaulted to read-only.
        # You can override this by settings read_only=False against the id field in the extra_kwargs:
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'name': instance.name,
            'bed_type': instance.bed_type
        }
        return representation


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id', 'name', 'bed_type'
        )
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def to_representation(self, instance):
        bed_dic = dict(BED_CHOICES)
        representation = {
            'id': instance.id,
            'name': instance.name,
            'bed_type': bed_dic[instance.bed_type]
        }
        return representation


# def to_internal_value(self, data):
#     """
#     Dict of native values <- Dict of primitive datatypes.
#     Add instance key to values if `id` present in primitive dict
#     :param data:
#     """
#     obj = super(RoomSerializer, self).to_internal_value(data)
#     instance_id = data.get('id', None)
#     if instance_id:
#         obj['instance'] = Room.objects.get(id=instance_id)
#     return obj


"""
 You can also use custom field
"""

# class RoomSerializer(serializers.ModelSerializer):
#     # room_id = serializers.IntegerField(source='id')
#     # id = serializers.IntegerField(required=False)
#     id = serializers.ModelField(model_field=Room()._meta.get_field('id'))
#
#     class Meta:
#         model = Room
#         fields = (
#             'id', 'name', 'bed_type'
#         )
