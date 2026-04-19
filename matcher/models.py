from django.db import models


class CandidateProfile(models.Model):
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    uploaded_resume = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    best_role = models.CharField(max_length=120, blank=True)
    best_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or f'Candidate {self.pk}'


class PredictionResult(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='predictions')
    role_name = models.CharField(max_length=120)
    score = models.FloatField(default=0)
    rank = models.PositiveIntegerField(default=1)
    recommendation = models.CharField(max_length=40, default='Moderate Fit')

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f'{self.candidate} - {self.role_name} ({self.score:.1f}%)'
