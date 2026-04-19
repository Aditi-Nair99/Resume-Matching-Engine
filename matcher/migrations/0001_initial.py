from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('uploaded_resume', models.FileField(upload_to='resumes/')),
                ('extracted_text', models.TextField(blank=True)),
                ('best_role', models.CharField(blank=True, max_length=120)),
                ('best_score', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PredictionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=120)),
                ('score', models.FloatField(default=0)),
                ('rank', models.PositiveIntegerField(default=1)),
                ('recommendation', models.CharField(default='Moderate Fit', max_length=40)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='matcher.candidateprofile')),
            ],
            options={'ordering': ['rank']},
        ),
    ]
