from rest_framework import serializers
from core.models import News,Notification, Plate
from django.conf import settings

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude = ['slug',]
        read_only_fields = ('published',)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields='__all__'
        read_only_fields = ('created_at',)
        
class PlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plate
        fields = '__all__'      

class UserRegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('email', 'first_name', 'last_name','phone_number')
        extra_kwargs = {'password': {'write_only': True}}