from rest_framework import serializers
from .models import City, DataCenter, Host, HostPassword, HostStatistic


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DataCenterSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        source='city',
        write_only=True
    )

    class Meta:
        model = DataCenter
        fields = '__all__'


class HostSerializer(serializers.ModelSerializer):
    data_center = DataCenterSerializer(read_only=True)
    data_center_id = serializers.PrimaryKeyRelatedField(
        queryset=DataCenter.objects.all(),
        source='data_center',
        write_only=True
    )
    status = serializers.ChoiceField(choices=Host.STATUS_CHOICES)

    class Meta:
        model = Host
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class HostPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostPassword
        fields = ['root_password', 'last_changed']
        read_only_fields = ['last_changed']


class HostStatisticSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    data_center = DataCenterSerializer(read_only=True)

    class Meta:
        model = HostStatistic
        fields = '__all__'