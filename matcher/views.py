from pathlib import Path

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import ResumeUploadForm
from .ml_engine import ROLE_SKILLS, normalize_text, predictor
from .models import CandidateProfile, PredictionResult
from .resume_parser import extract_basic_fields, extract_text_from_resume


@require_http_methods(["GET"])
def home(request):
    form = ResumeUploadForm()
    latest_candidates = CandidateProfile.objects.prefetch_related('predictions').order_by('-created_at')[:5]
    stats = build_dashboard_summary()
    demo_roles = [
        {'role': 'Data Analyst', 'score': 85},
        {'role': 'Web Developer', 'score': 72},
        {'role': 'HR Intern', 'score': 60},
        {'role': 'Graphic Designer', 'score': 45},
    ]
    return render(request, 'matcher/home.html', {
        'form': form,
        'latest_candidates': latest_candidates,
        'stats': stats,
        'demo_roles': demo_roles,
    })


@require_http_methods(["POST"])
def analyze_resume(request):
    form = ResumeUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, 'Please fill all required fields and upload a valid resume file.')
        return redirect('home')

    resume_file = form.cleaned_data['resume']
    storage = FileSystemStorage()
    filename = storage.save(f'resumes/{resume_file.name}', resume_file)
    full_path = Path(storage.path(filename))

    text = extract_text_from_resume(full_path)
    parsed = extract_basic_fields(text, fallback_name=form.cleaned_data['full_name'])
    if form.cleaned_data['email']:
        parsed['email'] = form.cleaned_data['email']
    if form.cleaned_data['phone']:
        parsed['phone'] = form.cleaned_data['phone']

    predictions = predictor.predict_top_roles(text, top_n=len(ROLE_SKILLS))
    best = predictions[0]

    candidate = CandidateProfile.objects.create(
        full_name=parsed['full_name'],
        email=parsed['email'],
        phone=parsed['phone'],
        uploaded_resume=filename,
        extracted_text=text[:15000],
        best_role=best['role'],
        best_score=best['score'],
    )

    for row in predictions:
        PredictionResult.objects.create(
            candidate=candidate,
            role_name=row['role'],
            score=row['score'],
            rank=row['rank'],
            recommendation=row['recommendation'],
        )

    messages.success(request, 'Resume analyzed successfully. Scroll down to see the result.')
    return redirect('candidate_detail', pk=candidate.pk)


@require_http_methods(["GET"])
def candidate_detail(request, pk: int):
    candidate = get_object_or_404(CandidateProfile.objects.prefetch_related('predictions'), pk=pk)
    stats = build_dashboard_summary()
    top_roles = list(candidate.predictions.all())
    role_keywords = {role: ', '.join(skills[:6]) for role, skills in ROLE_SKILLS.items()}
    extracted_skills = extract_candidate_skills(candidate.extracted_text)
    best_match = top_roles[0] if top_roles else None
    other_roles = top_roles[1:]
    return render(request, 'matcher/result.html', {
        'candidate': candidate,
        'top_roles': top_roles,
        'best_match': best_match,
        'other_roles': other_roles,
        'stats': stats,
        'role_keywords': role_keywords,
        'extracted_skills': extracted_skills,
    })


@require_http_methods(["GET"])
def history_view(request):
    candidates = CandidateProfile.objects.prefetch_related('predictions').order_by('-created_at')
    return render(request, 'matcher/history.html', {'candidates': candidates})


@require_GET
def dashboard_data(request):
    return JsonResponse(build_dashboard_summary())



def extract_candidate_skills(text: str):
    clean = normalize_text(text)
    found = []
    for skills in ROLE_SKILLS.values():
        for skill in skills:
            if skill in clean and skill not in found:
                found.append(skill)
    return found[:14]



def build_dashboard_summary():
    total = CandidateProfile.objects.count()
    recent = CandidateProfile.objects.order_by('-created_at')[:10]
    role_counts = {role: 0 for role in ROLE_SKILLS.keys()}
    for candidate in CandidateProfile.objects.all():
        if candidate.best_role in role_counts:
            role_counts[candidate.best_role] += 1

    chart_growth = []
    running = 0
    for idx, candidate in enumerate(reversed(list(recent)), start=1):
        running += 1
        chart_growth.append({'label': f'Run {idx}', 'value': running})

    if not chart_growth:
        chart_growth = [{'label': 'Run 1', 'value': 0}, {'label': 'Run 2', 'value': 1}, {'label': 'Run 3', 'value': 2}]

    score_distribution = []
    buckets = ['0-30', '31-50', '51-70', '71-85', '86-100']
    values = {bucket: 0 for bucket in buckets}
    for candidate in CandidateProfile.objects.all():
        score = candidate.best_score
        if score <= 30:
            values['0-30'] += 1
        elif score <= 50:
            values['31-50'] += 1
        elif score <= 70:
            values['51-70'] += 1
        elif score <= 85:
            values['71-85'] += 1
        else:
            values['86-100'] += 1
    for bucket in buckets:
        score_distribution.append({'label': bucket, 'value': values[bucket]})

    return {
        'total_candidates': total,
        'role_counts': role_counts,
        'growth_points': chart_growth,
        'score_distribution': score_distribution,
    }
