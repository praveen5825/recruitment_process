from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "is_candidate",
            "is_recruiter",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])

        user = User.objects.create(**validated_data)

        return user


class JobDetailSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.ReadOnlyField(source="posted_by.first_name")

    class Meta:
        model = JobDetail
        fields = [
            "id",
            "title",
            "description",
            "posted_by",
            "recruiter_name",
            "created_at",
        ]
        read_only_fields = ["posted_by"]

    def create(self, validated_data):

        if not self.context["request"].user.is_recruiter:
            raise serializers.ValidationError(
                {"Validation Error": "A Candidate can't post a Job."}
            )

        validated_data["posted_by"] = self.context["request"].user
        return super().create(validated_data)


class AppliedJobSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source="job.title")
    candidate_name = serializers.ReadOnlyField(source="attached_candidate.first_name")

    class Meta:
        model = AppliedJob
        fields = [
            "id",
            "job",
            "job_title",
            "attached_candidate",
            "candidate_name",
            "applied_at",
        ]
        read_only_fields = ["attached_candidate"]

    def create(self, validated_data):
        if not self.context["request"].user.is_candidate:
            raise serializers.ValidationError(
                {"Validation Error": "A Recruiter can't apply a Job."}
            )

        validated_data["attached_candidate"] = self.context["request"].user
        return super().create(validated_data)
