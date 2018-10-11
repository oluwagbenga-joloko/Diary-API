from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name', 
            'created_at', 'updated_at','is_staff', 'password'
        )
        read_only_fields = ('created_at', 'updated_at', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = User.objects.normalize_email(validated_data.pop('email'))
        password = validated_data.pop('password')
        user = User(
            email=email,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
    
    def update(self, user, validated_data):
        if 'email' in validated_data:
            validated_data['email'] = User.objects.normalize_email(validated_data['email'])
        if 'password' in validated_data:
            password = validated_data.pop('password')
            user.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()
        return user




