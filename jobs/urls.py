from django.urls import path
from . import views

urlpatterns = [
    path("",views.job_list, name="job_list"),
    path("create/", views.create_job, name="create_job"),
    path("jobs/<int:job_id>/", views.apply_for_job, name="apply_for_job"),
    path(
    "employer/applications/",
    views.employer_applications,
    name="employer_applications",
    ),
    path("my-applications/", views.my_applications, name="my_applications"),
    path(
    "employer/applications/<int:application_id>/status/",
    views.update_application_status,
    name="update_application_status",
    ),
    path("jobs/<int:job_id>/detail/", views.job_detail, name="job_detail"),
]