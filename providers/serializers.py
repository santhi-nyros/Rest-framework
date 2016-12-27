from django.contrib.auth.models import User, Group
from rest_framework import serializers

from providers.models import Provider,Category


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url','name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('url','user','name','created','updated')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


