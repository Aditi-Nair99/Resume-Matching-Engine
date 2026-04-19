from django.core.management.base import BaseCommand

from matcher.ml_engine import predictor
from matcher.models import CandidateProfile, PredictionResult

SAMPLES = [
    ('Aditi Nair', 'aditi@example.com', '9876543210', 'python sql power bi excel pandas analytics dashboard machine learning'),
    ('Rahul Verma', 'rahul@example.com', '9876500011', 'html css javascript react django bootstrap api frontend backend'),
    ('Sneha Patel', 'sneha@example.com', '9876500022', 'figma canva photoshop illustrator ui ux branding design system'),
    ('Nikita Shah', 'nikita@example.com', '9876500033', 'seo social media marketing google ads campaign content marketing growth'),
    ('Arjun Singh', 'arjun@example.com', '9876500044', 'recruitment hr operations coordination documentation communication management'),
]


class Command(BaseCommand):
    help = 'Seed demo candidates and force model training.'

    def handle(self, *args, **options):
        predictor.load_or_train()
        if CandidateProfile.objects.exists():
            self.stdout.write(self.style.WARNING('Demo data already exists. Skipping seed.'))
            return
        for name, email, phone, text in SAMPLES:
            preds = predictor.predict_top_roles(text)
            candidate = CandidateProfile.objects.create(
                full_name=name,
                email=email,
                phone=phone,
                uploaded_resume='resumes/demo.txt',
                extracted_text=text,
                best_role=preds[0]['role'],
                best_score=preds[0]['score'],
            )
            for row in preds:
                PredictionResult.objects.create(
                    candidate=candidate,
                    role_name=row['role'],
                    score=row['score'],
                    rank=row['rank'],
                    recommendation=row['recommendation'],
                )
        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
