from django.shortcuts import render

from rest_framework import viewsets
from .models import *
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            {"message": "User created", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."}, status=400
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid Username or password."}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login successful!",
            },
            status=200,
        )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully!"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid refresh token!"}, status=400)


class JobDetailViewSet(viewsets.ModelViewSet):
    queryset = JobDetail.objects.all().order_by("-created_at")
    serializer_class = JobDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_recruiter:

            self.queryset = JobDetail.objects.filter(posted_by=self.request.user)

        return super().get_queryset()


class AppliedJobViewSet(viewsets.ModelViewSet):
    queryset = AppliedJob.objects.all().order_by("-applied_at")
    serializer_class = AppliedJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_candidate:
            self.queryset = AppliedJob.objects.filter(
                attached_candidate=self.request.user
            )

        return super().get_queryset()


#
# {"title": "PL-SQL Developer", "description": "abcd"}

# {
#     "username":"recruiter",
#     "password":"1234"
# }
