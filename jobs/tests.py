from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import Job, Application


class JobPortalTests(TestCase):
    def setUp(self):
        self.employer = User.objects.create_user(
            username="employer_test",
            password="testpass123",
            role="employer",
        )

        self.candidate = User.objects.create_user(
            username="candidate_test",
            password="testpass123",
            role="candidate",
        )

        self.job = Job.objects.create(
            title="Backend Developer",
            company="Test Company",
            description="Build backend applications.",
            location="Bhubaneswar",
            job_type=Job.JobType.FULL_TIME,
            employer=self.employer,
        )

    def test_job_list_page_loads(self):
        response = self.client.get(reverse("job_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Backend Developer")

    def test_candidate_can_apply_for_job(self):
        self.client.force_login(self.candidate)

        response = self.client.post(
            reverse("apply_for_job", args=[self.job.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Application.objects.filter(
                candidate=self.candidate,
                job=self.job,
            ).exists()
        )

    def test_candidate_cannot_apply_twice(self):
        Application.objects.create(
            candidate=self.candidate,
            job=self.job,
        )
        self.client.force_login(self.candidate)

        self.client.post(
            reverse("apply_for_job", args=[self.job.id])
        )

        self.assertEqual(
            Application.objects.filter(
                candidate=self.candidate,
                job=self.job,
            ).count(),
            1,
        )

    def test_employer_cannot_edit_another_employers_job(self):
        other_employer = User.objects.create_user(
            username="other_employer",
            password="testpass123",
            role="employer",
        )
        self.client.force_login(other_employer)

        response = self.client.get(
            reverse("edit_job", args=[self.job.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_employer_cannot_delete_another_employers_job(self):
        other_employer = User.objects.create_user(
            username="other_employer",
            password="testpass123",
            role="employer",
        )
        self.client.force_login(other_employer)

        response = self.client.post(
            reverse("delete_job", args=[self.job.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Job.objects.filter(id=self.job.id).exists())

    def test_employer_can_create_job(self):
        self.client.force_login(self.employer)

        response = self.client.post(
            reverse("create_job"),
            {
                "title": "Python Developer",
                "company": "New Company",
                "description": "Develop Python applications.",
                "location": "Bhubaneswar",
                "job_type": Job.JobType.FULL_TIME,
                "salary": "600000",
            },
        )

        self.assertEqual(response.status_code, 302)

        job = Job.objects.get(title="Python Developer")
        self.assertEqual(job.employer, self.employer)

    def test_candidate_cannot_create_job(self):
        self.client.force_login(self.candidate)

        response = self.client.post(
            reverse("create_job"),
            {
                "title": "Python Developer",
                "company": "New Company",
                "description": "Develop Python applications.",
                "location": "Bhubaneswar",
                "job_type": Job.JobType.FULL_TIME,
                "salary": "600000",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Job.objects.filter(title="Python Developer").exists()
        )

    def test_employer_can_update_application_status(self):
        application = Application.objects.create(
            candidate=self.candidate,
            job=self.job,
        )

        self.client.force_login(self.employer)

        response = self.client.post(
            reverse(
                "update_application_status",
                args=[application.id],
            ),
            {"status": Application.Status.SHORTLISTED},
        )

        self.assertEqual(response.status_code, 302)

        application.refresh_from_db()
        self.assertEqual(
            application.status,
            Application.Status.SHORTLISTED,
        )
