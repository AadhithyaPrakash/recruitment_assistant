from django.db import models


class Resume(models.Model):
    """Stores uploaded resume and extracted data"""
    candidate_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} - {self.candidate_name or 'Unknown'}"


class Job(models.Model):
    """Stores job description"""
    job_title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} - {self.id}"


class MatchResult(models.Model):
    """Stores resume-job matching outcome"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    score = models.FloatField()  # Match percentage 0-100
    matched_skills = models.TextField()  # Comma-separated or JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match {self.id} - Score: {self.score}%"