from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterViewSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny


# Create your views here.
class RegisterView(APIView):
    permission_classes=(AllowAny,)

    def post(self,request):
        register_serializer = RegisterViewSerializer(data=request.data)

        if register_serializer.is_valid():
            user_instance = register_serializer.save()
            if user_instance:
                return Response(status=status.HTTP_201_CREATED)

        return Response({"errors":register_serializer.errors},status=status.HTTP_400_BAD_REQUEST)