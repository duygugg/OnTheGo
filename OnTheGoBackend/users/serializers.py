from rest_framework import serializers
from users.models import NewUser
from phonenumber_field.serializerfields import PhoneNumberField

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = PhoneNumberField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
   

    class Meta:
        model = NewUser
        fields = ('id','email', 'first_name','last_name','phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance