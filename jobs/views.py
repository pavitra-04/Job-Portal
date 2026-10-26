from django.shortcuts import render
from .models import Job 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import JobForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Application
from django.db import models
# Create your views here.
    


def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    location_query = request.GET.get("location", "").strip()
    job_type = request.GET.get("job_type", "").strip()

    if search_query:
        jobs = jobs.filter(
            models.Q(title__icontains=search_query)
            | models.Q(company__icontains=search_query)
        )

    if location_query:
        jobs = jobs.filter(location__icontains=location_query)

    valid_job_types = Job.JobType.values
    if job_type in valid_job_types:
        jobs = jobs.filter(job_type=job_type)
    else:
        job_type = ""

    applied_job_ids = set()

    if request.user.is_authenticated and request.user.role == "candidate":
        applied_job_ids = set(
            Application.objects.filter(candidate=request.user)
            .values_list("job_id", flat=True)
        )

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "applied_job_ids": applied_job_ids,
            "search_query": search_query,
            "location_query": location_query,
            "selected_job_type": job_type,
            "job_types": Job.JobType.choices,
        },
    )

    jobs = Job.objects.filter(is_active=True).order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    location_query = request.GET.get("location", "").strip()
    job_type = request.GET.get("job_type", "").strip()
    if search_query:
        jobs = jobs.filter(
            models.Q(title__icontains=search_query)
            | models.Q(company__icontains=search_query)
        )

    if location_query:
        jobs = jobs.filter(location__icontains=location_query)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    applied_job_ids = set()

    if request.user.is_authenticated and request.user.role == "candidate":
        applied_job_ids = set(
            Application.objects.filter(candidate=request.user)
            .values_list("job_id", flat=True)
        )

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "applied_job_ids": applied_job_ids,
            "search_query": search_query,
        },
    )

    jobs = Job.objects.filter(is_active=True).order_by("-created_at")

    applied_job_ids = set()

    if request.user.is_authenticated and request.user.role == "candidate":
        applied_job_ids = set(
            Application.objects.filter(
                candidate=request.user
            ).values_list("job_id", flat=True)
        )

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "applied_job_ids": applied_job_ids,
        },
    )



@login_required
def create_job(request):
    if request.user.role != "employer":
        messages.error(request, "Only employers can post jobs.")
        return redirect("job_list")

    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect("job_list")
    else:
        form = JobForm()

    return render(request, "jobs/job_form.html", {"form": form})


@login_required
@require_POST
def apply_for_job(request, job_id):
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can apply for jobs.")
        return redirect("job_list")

    job = get_object_or_404(Job, id=job_id, is_active=True)

    application, created = Application.objects.get_or_create(
        candidate=request.user,
        job=job,
    )

    if created:
        messages.success(request, "Application submitted successfully.")
    else:
        messages.info(request, "You have already applied for this job.")

    return redirect("job_list")


@login_required
def employer_applications(request):
    if request.user.role != "employer":
        messages.error(request, "Only employers can view applicants.")
        return redirect("job_list")

    applications = Application.objects.filter(
        job__employer=request.user
    ).select_related("candidate", "job").order_by("-applied_at")

    return render(
        request,
        "jobs/employer_applications.html",
        {"applications": applications},
    )

@login_required
def my_applications(request):
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can view their applications.")
        return redirect("job_list")

    applications = (
        Application.objects
        .filter(candidate=request.user)
        .select_related("job")
        .order_by("-applied_at")
    )

    return render(
        request,
        "jobs/my_applications.html",
        {"applications": applications},
    )


@login_required
@require_POST
def update_application_status(request, application_id):
    if request.user.role != "employer":
        messages.error(request, "Only employers can update application statuses.")
        return redirect("job_list")

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user,
    )

    status = request.POST.get("status")
    valid_statuses = Application.Status.values

    if status in valid_statuses:
        application.status = status
        application.save(update_fields=["status"])
        messages.success(request, "Application status updated.")
    else:
        messages.error(request, "Invalid application status.")

    return redirect("employer_applications")


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    has_applied = False

    if request.user.is_authenticated and request.user.role == "candidate":
        has_applied = Application.objects.filter(
            candidate=request.user,
            job=job,
        ).exists()

    return render(
        request,
        "jobs/job_detail.html",
        {
            "job": job,
            "has_applied": has_applied,
        },
    )


@login_required
def edit_job(request, job_id):
    if request.user.role != "employer":
        messages.error(request, "Only employers can edit jobs.")
        return redirect("job_list")

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user,
    )

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect("job_list")
    else:
        form = JobForm(instance=job)

    return render(
        request,
        "jobs/job_form.html",
        {"form": form, "job": job},
    )

@login_required
@require_POST
def delete_job(request, job_id):
    if request.user.role != "employer":
        messages.error(request, "Only employers can delete jobs.")
        return redirect("job_list")

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user,
    )

    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect("job_list")
