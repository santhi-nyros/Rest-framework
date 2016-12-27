from django.contrib.auth.models import User, Group
from rest_framework import serializers
from consumers.models import Consumer,Consumer_profile,Registered_devices
from providers.serializers import UserSerializer

from rest_framework.serializers import ModelSerializer
from push_notifications.models import GCMDevice

class GetConsumerSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Consumer
        fields = ('user','email')


class RegDevicesSerializer(ModelSerializer):
    class Meta:
        model = Registered_devices
        fields = ('device_id','registration_id')


class ConsumerSerializer(ModelSerializer):
    user = UserSerializer()
    device = RegDevicesSerializer()
    class Meta:
        model = Consumer
        fields = ('user','email','device')


    def create(self, validated_data):
        email = validated_data.pop('email')
        # create user
        user_data = validated_data.pop('user')
        password = user_data['password']
        user = User.objects.create(
            username = user_data['username'],
            email = email,
            password = user_data['password']
        )
        if password is not None:
            user.set_password(password)
        user.groups.add(2)
        user.save()

        # Create consumer
        consumer = Consumer.objects.create(
            user = user,
            email = email
        )
        consumer.save()

        # Device details storing
        device_data = validated_data.pop('device')
        device = Registered_devices.objects.create(
            consumer = consumer,
            device_id = device_data['device_id'],
            registration_id = device_data['registration_id']
        )
        device.save()


        gcm_device = GCMDevice.objects.create(
            user=user,
            device_id=device_data['device_id'],
            registration_id= device_data['registration_id']
        )
        gcm_device.save()

        return consumer


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class ProfileSerializer(ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Consumer_profile
        fields = ('consumer','first_name','avatar','last_name','category','location')

    def create(self, validated_data):
        # create profile
        consumer = validated_data.pop('consumer')
        profile = Consumer_profile.objects.create(
            consumer=consumer,
            first_name = validated_data.pop('first_name'),
            last_name = validated_data.pop('last_name'),
            avatar = validated_data.pop('avatar'),
            category = validated_data.pop('category'),
            location = validated_data.pop('location')
        )
        profile.save()
        return profile

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

