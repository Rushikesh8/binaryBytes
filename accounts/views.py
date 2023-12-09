from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterViewSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import ( TokenObtainPairView )
from django.http import HttpRequest
import json

class RegisterView(APIView):
    permission_classes=(AllowAny,)

    def post(self,request):
        register_serializer = RegisterViewSerializer(data=request.data)

        if register_serializer.is_valid():
            user_instance = register_serializer.save()
            if user_instance:
                # token_data = {
                #     'contact': user_instance.contact,
                #     'password': request.data.get('password'),
                # }
                # django_request = HttpRequest()
                # django_request.method = 'POST'
                # django_request._body = json.dumps(token_data).encode('utf-8')
                # django_request.content_type = 'application/json'
                # try:
                #     token_view = TokenObtainPairView.as_view()
                #     token_response = token_view(request=django_request)
                #     if token_response.status_code == 200:
                #         return Response(token_response.data, status=status.HTTP_201_CREATED)
                # except Exception as e: 
                #     print(str(e))

                return Response(status=status.HTTP_201_CREATED)

        return Response({"errors":register_serializer.errors},status=status.HTTP_400_BAD_REQUEST)