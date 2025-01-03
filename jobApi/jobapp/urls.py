from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"jobs", JobDetailViewSet)
router.register(r"apply_jobs", AppliedJobViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
