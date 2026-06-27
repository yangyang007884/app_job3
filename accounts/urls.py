from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    JobSeekerProfileView,
    JobSeekerApplicationListView,
    CompanyProfileView,
    CompanyListView,
    CompanyJobListCreateView,
    CompanyJobDetailView,
    PublicCompanyJobsView,
    ApplyJobView,
    JobApplicantsView,
    AdminUserListView,
    AdminUserDetailView,
    AdminCompanyListView,
    AdminCompanyDetailView,
    AdminJobListView,
    AdminJobDetailView,
    CompanyPublicDetailView,
    JobSeekerPublicProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('job-seeker/profile/', JobSeekerProfileView.as_view(), name='job_seeker_profile'),
    path('job-seeker/applications/', JobSeekerApplicationListView.as_view(), name='job_seeker_applications'),

    path('company/profile/', CompanyProfileView.as_view(), name='company_profile'),
    path('companies/', CompanyListView.as_view(), name='company_list'),

    path('company/jobs/', CompanyJobListCreateView.as_view(), name='company_jobs'),
    path('company/jobs/<int:job_id>/', CompanyJobDetailView.as_view(), name='company_job_detail'),
    path('company/jobs/<int:job_id>/applicants/', JobApplicantsView.as_view(), name='job_applicants'),

    path('companies/<int:company_id>/jobs/', PublicCompanyJobsView.as_view(), name='public_company_jobs'),

    path('jobs/<int:job_id>/apply/', ApplyJobView.as_view(), name='apply_job'),

    path('admin/users/', AdminUserListView.as_view(), name='admin_users'),
    path('admin/users/<int:user_id>/', AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin/companies/', AdminCompanyListView.as_view(), name='admin_companies'),
    path('admin/companies/<int:company_id>/', AdminCompanyDetailView.as_view(), name='admin_company_detail'),
    path('admin/jobs/', AdminJobListView.as_view(), name='admin_jobs'),
    path('admin/jobs/<int:job_id>/', AdminJobDetailView.as_view(), name='admin_job_detail'),
    path('company/<int:company_id>/', CompanyPublicDetailView.as_view(), name='company_public_detail'),
    path('job-seeker/profile/<int:user_id>/', JobSeekerPublicProfileView.as_view(),name='jobseeker_public_detail'),

]