from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, JobSeekerProfile, Company, Job, Application


class RegisterSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = [
            'id',
            'user',
            'profile_image',
            'full_name',
            'address',
            'education',
            'cv_file',
        ]
        read_only_fields = ['user']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'user',
            'profile_image',
            'company_name',
            'company_info',
            'business_license',
        ]
        read_only_fields = ['user']


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'profile_image',
            'company_name',
            'company_info',
        ]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'company',
            'position',
            'education_level',
            'required_language',
            'job_description',
        ]
        read_only_fields = ['company']


class ApplicantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = [
            'id',
            'profile_image',
            'full_name',
            'address',
            'education',
            'cv_file',
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    job_seeker_profile = ApplicantProfileSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'job_seeker_profile',
            'applied_at',
        ]


class AppliedJobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source='company.company_name',
        read_only=True,
    )

    class Meta:
        model = Job
        fields = [
            'id',
            'position',
            'education_level',
            'required_language',
            'job_description',
            'company_name',
        ]


class MyApplicationSerializer(serializers.ModelSerializer):
    job = AppliedJobSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'applied_at',
        ]


class AdminUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'role',
            'is_staff',
            'is_superuser',
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['role'] = self.user.role

        return data
class AdminCompanySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Company
        fields = [
            'id',
            'user_id',
            'username',
            'profile_image',
            'company_name',
            'company_info',
            'business_license',
        ]


class AdminJobSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(source='company.id', read_only=True)
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    company_username = serializers.CharField(source='company.user.username', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'company_id',
            'company_name',
            'company_username',
            'position',
            'education_level',
            'required_language',
            'job_description',
        ]