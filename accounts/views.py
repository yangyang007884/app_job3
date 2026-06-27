from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, JobSeekerProfile, Company, Job, Application
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    JobSeekerProfileSerializer,
    CompanySerializer,
    CompanyListSerializer,
    JobSerializer,
    ApplicationSerializer,
    MyApplicationSerializer,
    AdminUserSerializer,
    AdminCompanySerializer,
    AdminJobSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class JobSeekerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        try:
            profile = request.user.job_seeker_profile
        except JobSeekerProfile.DoesNotExist:
            return Response(
                {'detail': 'Job seeker profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSeekerProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if hasattr(request.user, 'job_seeker_profile'):
            return Response(
                {'detail': 'Profile already exists.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = JobSeekerProfileSerializer(
            data=request.data,
            context={'request': request},
        )

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            profile = request.user.job_seeker_profile
        except JobSeekerProfile.DoesNotExist:
            return Response(
                {'detail': 'Job seeker profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSeekerProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={'request': request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        try:
            company = request.user.company_profile
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CompanySerializer(company, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if hasattr(request.user, 'company_profile'):
            return Response(
                {'detail': 'Company profile already exists.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CompanySerializer(
            data=request.data,
            context={'request': request},
        )

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            company = request.user.company_profile
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CompanySerializer(
            company,
            data=request.data,
            partial=True,
            context={'request': request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        companies = Company.objects.all().order_by('id')
        serializer = CompanyListSerializer(
            companies,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)


class CompanyJobListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            company = request.user.company_profile
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        jobs = Job.objects.filter(company=company).order_by('-id')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            company = request.user.company_profile
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyJobDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, job_id):
        try:
            company = request.user.company_profile
            job = Job.objects.get(id=job_id, company=company)
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Job.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSerializer(job, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_id):
        try:
            company = request.user.company_profile
            job = Job.objects.get(id=job_id, company=company)
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Job.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicCompanyJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        jobs = Job.objects.filter(company_id=company_id).order_by('-id')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]

    def get_job_seeker_profile(self, request):
        try:
            return request.user.job_seeker_profile
        except JobSeekerProfile.DoesNotExist:
            return None

    def profile_required_response(self):
        return Response(
            {'detail': 'ກະລຸນາປ້ອນຂໍ້ມູນໂປຣໄຟລ໌ກ່ອນ'},
            status=status.HTTP_403_FORBIDDEN,
        )

    def get(self, request, job_id):
        profile = self.get_job_seeker_profile(request)

        if profile is None:
            return self.profile_required_response()

        is_applied = Application.objects.filter(
            job_id=job_id,
            job_seeker_profile=profile,
        ).exists()

        return Response({'is_applied': is_applied})

    def post(self, request, job_id):
        profile = self.get_job_seeker_profile(request)

        if profile is None:
            return self.profile_required_response()

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        application, created = Application.objects.get_or_create(
            job=job,
            job_seeker_profile=profile,
        )

        if not created:
            return Response(
                {'detail': 'ທ່ານໄດ້ສະໝັກວຽກນີ້ແລ້ວ'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ApplicationSerializer(
            application,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, job_id):
        profile = self.get_job_seeker_profile(request)

        if profile is None:
            return self.profile_required_response()

        try:
            application = Application.objects.get(
                job_id=job_id,
                job_seeker_profile=profile,
            )
        except Application.DoesNotExist:
            return Response(
                {'detail': 'ບໍ່ພົບຂໍ້ມູນການສະໝັກ'},
                status=status.HTTP_404_NOT_FOUND,
            )

        application.delete()

        return Response(
            {'detail': 'ຍົກເລີກສະໝັກແລ້ວ'},
            status=status.HTTP_200_OK,
        )


class JobApplicantsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        try:
            company = request.user.company_profile
            job = Job.objects.get(id=job_id, company=company)
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Job.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        applications = Application.objects.filter(
            job=job,
        ).select_related('job_seeker_profile').order_by('-applied_at')

        serializer = ApplicationSerializer(
            applications,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)


class JobSeekerApplicationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.job_seeker_profile
        except JobSeekerProfile.DoesNotExist:
            return Response(
                {'detail': 'ກະລຸນາປ້ອນຂໍ້ມູນໂປຣໄຟລ໌ກ່ອນ'},
                status=status.HTTP_403_FORBIDDEN,
            )

        applications = Application.objects.filter(
            job_seeker_profile=profile,
        ).select_related('job', 'job__company').order_by('-applied_at')

        serializer = MyApplicationSerializer(
            applications,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)


class AdminUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin' and not request.user.is_superuser:
            return Response(
                {'detail': 'Admin only.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        users = User.objects.all().order_by('id')
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)
class AdminUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        if request.user.role != 'admin' and not request.user.is_superuser:
            return Response(
                {'detail': 'Admin only.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.user.id == user_id:
            return Response(
                {'detail': 'ບໍ່ສາມາດລຶບບັນຊີ admin ທີ່ກຳລັງໃຊ້ຢູ່'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.delete()

        return Response(
            {'detail': 'ລຶບຜູ້ໃຊ້ແລ້ວ'},
            status=status.HTTP_200_OK,
        )
class AdminCompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin' and not request.user.is_superuser:
            return Response(
                {'detail': 'Admin only.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        companies = Company.objects.select_related('user').all().order_by('id')
        serializer = AdminCompanySerializer(
            companies,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)


class AdminCompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, company_id):
        if request.user.role != 'admin' and not request.user.is_superuser:
            return Response(
                {'detail': 'Admin only.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            company = Company.objects.select_related('user').get(id=company_id)
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Company not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        company_user = company.user
        company_user.delete()

        return Response(
            {'detail': 'ລຶບບໍລິສັດແລະຜູ້ໃຊ້ແລ້ວ'},
            status=status.HTTP_200_OK,
        )
class AdminJobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin' and not request.user.is_superuser:
            return Response(
                {'detail': 'Admin only.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        jobs = Job.objects.select_related('company', 'company__user').all().order_by('-id')

        serializer = AdminJobSerializer(
            jobs,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)


class AdminJobDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, job_id):
        if request.user.role != 'admin' and not request.user.is_superuser:
            return Response(
                {'detail': 'Admin only.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        job.delete()

        return Response(
            {'detail': 'ລຶບວຽກແລ້ວ'},
            status=status.HTTP_200_OK,
        )
class CompanyPublicDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

        serializer = CompanyListSerializer(company)
        return Response(serializer.data)
class JobSeekerPublicProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            profile = JobSeekerProfile.objects.get(user_id=user_id)
        except JobSeekerProfile.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

        serializer = JobSeekerProfileSerializer(profile)
        return Response(serializer.data)