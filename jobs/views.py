from django.shortcuts import render
from .models import Job 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import JobForm

# Create your views here.

def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, "jobs/job_list.html", {"jobs": jobs})


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
