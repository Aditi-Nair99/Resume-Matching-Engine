from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / 'trained_models'
MODEL_PATH = MODEL_DIR / 'resume_role_model.joblib'
META_PATH = MODEL_DIR / 'resume_role_meta.json'

ROLE_SKILLS = {
    'Data Analytics Intern': [
        'python', 'sql', 'excel', 'power bi', 'tableau', 'pandas', 'numpy', 'matplotlib', 'statistics', 'dashboard', 'analysis'
    ],
    'Web Development Intern': [
        'html', 'css', 'javascript', 'react', 'django', 'flask', 'node', 'api', 'bootstrap', 'frontend', 'backend'
    ],
    'Graphic Design Intern': [
        'photoshop', 'illustrator', 'figma', 'canva', 'ui', 'ux', 'branding', 'prototype', 'poster', 'design'
    ],
    'Digital Marketing Intern': [
        'seo', 'sem', 'marketing', 'social media', 'campaign', 'google ads', 'content marketing', 'lead generation', 'analytics'
    ],
    'HR/Operations Intern': [
        'recruitment', 'screening', 'communication', 'operations', 'scheduling', 'hr', 'coordination', 'management', 'documentation'
    ],
}

SAMPLE_RESUMES = {
    'Data Analytics Intern': [
        'python sql excel power bi pandas numpy dashboard statistics data cleaning machine learning reporting',
        'sql tableau excel pandas matplotlib data visualization business analysis kpi reports',
        'python power bi excel analytics dashboard predictive model statistics jupyter',
    ],
    'Web Development Intern': [
        'html css javascript react bootstrap responsive design frontend api integration web app',
        'django python sqlite backend rest api authentication html css javascript',
        'full stack web development react node express mongodb ui components',
    ],
    'Graphic Design Intern': [
        'photoshop illustrator figma canva poster branding social media creatives ui ux',
        'figma wireframe prototype design system visual identity banner brochure',
        'graphic design canva adobe illustrator branding logo layout typography',
    ],
    'Digital Marketing Intern': [
        'seo social media marketing content marketing google ads campaign analytics keyword research',
        'digital marketing lead generation email marketing brand promotion instagram facebook seo',
        'content creation seo sem social media strategy campaign optimization growth',
    ],
    'HR/Operations Intern': [
        'recruitment screening operations coordination documentation communication scheduling hr management',
        'employee engagement hiring process sourcing interviews documentation operations excel communication',
        'human resources recruitment onboarding coordination administration operations management',
    ],
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9+.# ]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


class ResumeRolePredictor:
    def __init__(self) -> None:
        MODEL_DIR.mkdir(exist_ok=True)
        self.pipeline = None
        self.roles = list(ROLE_SKILLS.keys())
        self.load_or_train()

    def build_training_rows(self):
        texts, labels = [], []
        for role, samples in SAMPLE_RESUMES.items():
            for sample in samples:
                texts.append(sample)
                labels.append(role)
            joined = ' '.join(ROLE_SKILLS[role])
            texts.append(joined)
            labels.append(role)
            texts.append(joined + ' internship project certification tools experience')
            labels.append(role)
        return texts, labels

    def train(self):
        texts, labels = self.build_training_rows()
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
            ('clf', LogisticRegression(max_iter=2000, multi_class='auto')),
        ])
        pipeline.fit(texts, labels)
        joblib.dump(pipeline, MODEL_PATH)
        with open(META_PATH, 'w', encoding='utf-8') as f:
            json.dump({'roles': self.roles}, f)
        self.pipeline = pipeline

    def load_or_train(self):
        if MODEL_PATH.exists():
            self.pipeline = joblib.load(MODEL_PATH)
        else:
            self.train()

    def keyword_boosts(self, text: str) -> Dict[str, float]:
        boosts = {}
        for role, skills in ROLE_SKILLS.items():
            matches = sum(1 for skill in skills if skill in text)
            boosts[role] = matches / max(len(skills), 1)
        return boosts

    def predict_top_roles(self, resume_text: str, top_n: int = 3) -> List[Dict]:
        clean = normalize_text(resume_text)
        if not clean:
            clean = 'communication internship fresher'
        probs = self.pipeline.predict_proba([clean])[0]
        classes = list(self.pipeline.classes_)
        boosts = self.keyword_boosts(clean)
        scored = []
        for role, prob in zip(classes, probs):
            final_score = (prob * 0.75 + boosts.get(role, 0) * 0.25) * 100
            scored.append((role, round(final_score, 2)))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:top_n]
        normalized_total = sum(score for _, score in top) or 1
        output = []
        for idx, (role, score) in enumerate(top, start=1):
            normalized_score = round((score / normalized_total) * 100, 2)
            recommendation = 'Strong Fit' if normalized_score >= 55 else 'Moderate Fit' if normalized_score >= 30 else 'Low Fit'
            output.append({
                'role': role,
                'score': normalized_score,
                'rank': idx,
                'recommendation': recommendation,
            })
        return output


predictor = ResumeRolePredictor()
