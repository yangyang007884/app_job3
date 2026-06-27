from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='job_seeker'
    )

    def __str__(self):
        return self.username


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='job_seeker_profile'
    )
    profile_image = models.ImageField(
        upload_to='job_seekers/profile_images/',
        blank=True,
        null=True
    )
    full_name = models.CharField(max_length=150)
    address = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    cv_file = models.FileField(
        upload_to='job_seekers/cvs/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name


class Company(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company_profile'
    )
    profile_image = models.ImageField(
        upload_to='companies/profile_images/',
        blank=True,
        null=True
    )
    company_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    company_info = models.TextField(
        blank=True,
        null=True
    )
    business_license = models.FileField(
        upload_to='companies/business_licenses/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.company_name or self.user.username


class Job(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    position = models.CharField(max_length=150)
    education_level = models.CharField(max_length=150)
    required_language = models.CharField(max_length=150)
    job_description = models.TextField()

    def __str__(self):
        return self.position


class Application(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    job_seeker_profile = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'job_seeker_profile')

    def __str__(self):
        return f'{self.job_seeker_profile.full_name} - {self.job.position}'