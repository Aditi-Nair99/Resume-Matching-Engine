from django.contrib import admin
from .models import CandidateProfile, PredictionResult


class PredictionInline(admin.TabularInline):
    model = PredictionResult
    extra = 0


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'best_role', 'best_score', 'created_at')
    search_fields = ('full_name', 'email', 'best_role')
    inlines = [PredictionInline]


@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'role_name', 'score', 'rank', 'recommendation')
    list_filter = ('role_name', 'recommendation')
