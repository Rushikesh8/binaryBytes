from rest_framework.serializers import ModelSerializer
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterViewSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ["email","username","password","first_name","last_name","oraganization","role"]
        extra_kwargs = {"password":{"write_only":True}}

    def create(self,validated_data):
        password = validated_data.pop("password",None)
        validated_data["is_active"] = True
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = f"{user.first_name.capitalize()} {user.last_name.capitalize()}"

        return token