from rest_framework import serializers
from .models import Entry
from django.utils import timezone
from datetime import timedelta


class EntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Entry
        exclude = ['user']  
    
    def validate(self, data):
        if self.instance:
            if self.instance.created_at + timedelta(hours=24) < timezone.now():
                raise serializers.ValidationError("cannot edit entry after 24 hours")
        return data
        